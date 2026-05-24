import argparse
import warnings

import networkx as nx
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from rcabench_platform.v2.algorithms.spec import (
    Algorithm,
    AlgorithmAnswer,
    AlgorithmArgs,
)
from rcabench_platform.v2.logging import timeit
from sklearn.preprocessing import StandardScaler
from torch.autograd import Variable
from torch.utils.data import DataLoader, Dataset
from tqdm import trange

from ._common import SimpleMetricsAdapter

# NOTE: set_detect_anomaly 会让 autograd 逐 op 检查 NaN/Inf，训练速度慢 20-30%
# torch.autograd.set_detect_anomaly(True)


class moving_avg(nn.Module):
    """
    Moving average block to highlight the trend of time series
    """

    def __init__(self, kernel_size, stride):
        super(moving_avg, self).__init__()
        self.kernel_size = kernel_size
        self.avg = nn.AvgPool1d(kernel_size=kernel_size, stride=stride, padding=0)

    def forward(self, x):
        # padding on the both ends of time series
        front = x[:, 0:1, :].repeat(1, (self.kernel_size - 1) // 2, 1)
        end = x[:, -1:, :].repeat(1, (self.kernel_size - 1) // 2, 1)
        x = torch.cat([front, x, end], dim=1)
        x = self.avg(x.permute(0, 2, 1))
        x = x.permute(0, 2, 1)
        return x


class series_decomp(nn.Module):
    """
    Series decomposition block
    """

    def __init__(self, kernel_size):
        super(series_decomp, self).__init__()
        self.moving_avg = moving_avg(kernel_size, stride=1)

    def forward(self, x):
        moving_mean = self.moving_avg(x)
        res = x - moving_mean
        return res, moving_mean


class DLinear(nn.Module):
    """
    Decomposition-Linear (batched version)

    所有逐通道 ModuleList 循环已替换为 grouped Conv1d batched 操作，
    消除 Python 级 for 循环，让 GPU 充分并行。
    """

    def __init__(self, seq_len, pred_len, enc_in):
        super(DLinear, self).__init__()
        self.seq_len = seq_len
        self.pred_len = pred_len
        self.channels = enc_in

        kernel_size = 25
        self.decompsition = series_decomp(kernel_size)

        # attention score
        self._attention = torch.ones(self.channels, 1)
        self._attention = Variable(self._attention, requires_grad=False)
        self.fs_attention = torch.nn.Parameter(self._attention.data)

        self.IsTest = False
        self.pretrain = False
        self.project = False

        C, S, P = enc_in, seq_len, pred_len

        # encoder: per-channel Linear(S, P) → grouped Conv1d
        self.Linear_Seasonal = nn.Conv1d(C, C * P, kernel_size=S, groups=C, bias=True)
        self.Linear_Trend = nn.Conv1d(C, C * P, kernel_size=S, groups=C, bias=True)

        # decoder: per-channel Linear(P, S) → grouped Conv1d
        self.Decoder_Seasonal = nn.Conv1d(C, C * S, kernel_size=P, groups=C, bias=True)
        self.Decoder_Trend = nn.Conv1d(C, C * S, kernel_size=P, groups=C, bias=True)

        self.Decoder_Seasonal_pointwise = nn.Linear(S * C, 1)
        self.Decoder_Trend_pointwise = nn.Linear(S * C, 1)

        # projector: per-channel Linear(P, P*2) and Linear(P*2, P)
        self.Proj_Seasonal = nn.Conv1d(C, C * P * 2, kernel_size=P, groups=C, bias=True)
        self.Proj_Trend = nn.Conv1d(C, C * P * 2, kernel_size=P, groups=C, bias=True)
        self.Proj_Seasonal_2 = nn.Conv1d(C, C * P, kernel_size=P * 2, groups=C, bias=True)
        self.Proj_Trend_2 = nn.Conv1d(C, C * P, kernel_size=P * 2, groups=C, bias=True)
        self.activation = nn.PReLU()

    def _apply_enc(self, layer, x):
        # [B, C, S] → [B, C, P]
        B = x.size(0)
        return layer(x).squeeze(-1).view(B, self.channels, self.pred_len)

    def _apply_dec(self, layer, x):
        # [B, C, P] → [B, C, S]
        B = x.size(0)
        return layer(x).squeeze(-1).view(B, self.channels, self.seq_len)

    def _apply_proj(self, proj1, proj2, x):
        # [B, C, P] → PReLU → [B, C, P]
        B = x.size(0)
        h = proj1(x).squeeze(-1).view(B, self.channels, self.pred_len * 2)
        h = self.activation(h)
        return proj2(h).squeeze(-1).view(B, self.channels, self.pred_len)

    def forward(self, x):
        B = x.size(0)
        device = x.device

        if self.pretrain:
            x = x.transpose(1, 2)

            seasonal_init, trend_init = self.decompsition(x)

            if self.project:
                enc_s = self._apply_enc(self.Linear_Seasonal, seasonal_init)
                seasonal_output = self._apply_proj(self.Proj_Seasonal, self.Proj_Seasonal_2, enc_s)
                enc_t = self._apply_enc(self.Linear_Trend, trend_init)
                trend_output = self._apply_proj(self.Proj_Trend, self.Proj_Trend_2, enc_t)
                x = seasonal_output + trend_output
            else:
                with torch.no_grad():
                    enc_s = self._apply_enc(self.Linear_Seasonal, seasonal_init)
                    enc_t = self._apply_enc(self.Linear_Trend, trend_init)
                    x = enc_s + enc_t

            return x.transpose(1, 2)

        # x: [Batch, Input length, Channel]
        x = x.transpose(1, 2)

        seasonal_init, trend_init = self.decompsition(x)

        seasonal_output = self._apply_enc(self.Linear_Seasonal, seasonal_init)
        trend_output = self._apply_enc(self.Linear_Trend, trend_init)

        fs_attention = self.fs_attention.to(device)
        seasonal_output = seasonal_output * F.softmax(fs_attention, dim=0)
        trend_output = trend_output * F.softmax(fs_attention, dim=0)

        seasonal_output_1 = self._apply_dec(self.Decoder_Seasonal, seasonal_output)
        trend_output_1 = self._apply_dec(self.Decoder_Trend, trend_output)

        # 使用实际 batch size，不硬编码 128
        reshape_seasonal = seasonal_output_1.reshape(B, 1, self.seq_len * self.channels)
        reshape_trend = trend_output_1.reshape(B, 1, self.seq_len * self.channels)

        y1 = self.Decoder_Seasonal_pointwise(reshape_seasonal)
        y2 = self.Decoder_Trend_pointwise(reshape_trend)

        x = y1 + y2
        x = x.transpose(1, 2)

        return x

    def setPretrain(self, x):
        self.pretrain = x

    def setProj(self, x):
        self.project = x

    def setTest(self, x):
        self.IsTest = x


warnings.filterwarnings("ignore")

drop_num = 10


class Dataset_RCA(Dataset):
    def __init__(
        self,
        data,
        flag,
        target,
        features="MS",
        size=None,
        scale=True,
        timeenc=0,
        freq="s",
        train_only=False,
    ):
        if size == None:
            self.seq_len = 24 * 4 * 4
            self.label_len = 24 * 4
            self.pred_len = 24 * 4
        else:
            self.seq_len = size[0]
            self.label_len = size[1]
            self.pred_len = size[2]
        # init
        assert flag in ["train", "test"]
        type_map = {"train": 0, "test": 1}
        self.set_type = type_map[flag]

        self.features = features
        self.target = target
        self.scale = scale
        self.timeenc = timeenc
        self.freq = freq

        self.data = data
        self.__read_data__()

    def __read_data__(self):
        self.scaler = StandardScaler()
        df_raw = self.data

        data_len = len(df_raw)

        border1s = [0, int(data_len * (3 / 4)) - self.seq_len]
        border2s = [int(data_len * (3 / 4)), data_len]
        border1 = border1s[self.set_type]
        border2 = border2s[self.set_type]

        df_data = df_raw

        train_data = df_data[border1:border2]
        self.scaler.fit(train_data.values)
        data = self.scaler.transform(df_data.values)

        self.data_x = data[border1:border2]
        self.data_y = data[border1:border2]

    def __getitem__(self, index):
        s_begin = index
        s_end = s_begin + self.seq_len
        r_begin = s_end - self.label_len
        r_end = r_begin + self.label_len + self.pred_len

        seq_x = self.data_x[s_begin:s_end]
        seq_y = self.data_y[r_begin:r_end]
        return seq_x, seq_y

    def __len__(self):
        return len(self.data_x) - self.seq_len - self.pred_len + 1

    def inverse_transform(self, data):
        return self.scaler.inverse_transform(data)


def data_provider(args, flag):
    Data = Dataset_RCA
    timeenc = 0
    train_only = False

    if flag == "test":
        shuffle_flag = False
        drop_last = False
        batch_size = 1
        freq = "s"

    else:
        shuffle_flag = True
        drop_last = True
        batch_size = 128
        freq = "s"

    data_set = Data(
        flag=flag,
        size=[32, 0, 1],
        features="MS",
        target="",
        timeenc=timeenc,
        freq=freq,
        train_only=train_only,
        data=args.data,
        scale=True,
    )

    data_loader = DataLoader(
        data_set,
        batch_size=batch_size,
        shuffle=shuffle_flag,
        num_workers=args.num_workers,
        drop_last=drop_last,
    )
    return data_set, data_loader


def hierarchical_contrastive_loss(z1, z2, temporal_unit=0):
    loss = torch.tensor(0.0, device=z1.device)
    d = 0
    while z1.size(1) > 1:
        if d >= temporal_unit:
            loss += temporal_contrastive_loss(z1, z2)
        d += 1
        z1 = F.max_pool1d(z1.transpose(1, 2), kernel_size=2).transpose(1, 2)
        z2 = F.max_pool1d(z2.transpose(1, 2), kernel_size=2).transpose(1, 2)
    return loss / d


def temporal_contrastive_loss(z1, z2):
    B, T = z1.size(0), z1.size(1)
    if T == 1:
        return z1.new_tensor(0.0)

    positive_pairs = torch.cat([z1, z2], dim=1)  # B x 2T x C
    sim = torch.matmul(positive_pairs, positive_pairs.transpose(1, 2))  # B x 2T x 2T

    positive_logits = sim[:, :T, T:]
    positive_logits = -F.log_softmax(positive_logits, dim=-1)

    loss = positive_logits.mean()
    return loss


@timeit()
def pre_train(train_data, train_loader, model, optimizer, args, target_idx, cuda):
    train_steps = len(train_loader)
    model.train()
    total_batches = len(train_loader)
    for i, (batch_x, batch_y) in enumerate(train_loader):
        optimizer.zero_grad()

        batch_x = batch_x.float()
        if cuda == "cuda:0":
            batch_x = batch_x.to("cuda:0")

        ts_l = batch_x.size(1)
        crop_l = 32
        crop_left = np.random.randint(ts_l - crop_l + 1)
        crop_right = crop_left + crop_l
        crop_eleft = np.random.randint(crop_left + 1)
        crop_eright = np.random.randint(low=crop_right, high=ts_l + 1)
        crop_offset = np.random.randint(
            low=-crop_eleft, high=ts_l - crop_eright + 1, size=batch_x.size(0)
        )

        model.setProj(True)
        out = model(take_per_row(batch_x, crop_offset + crop_eleft, 32))
        p1 = out[:, -crop_l:]
        out = model(take_per_row(batch_x, crop_offset + crop_left, 32))
        p2 = out[:, :crop_l]

        model.setProj(False)
        out = model(take_per_row(batch_x, crop_offset + crop_left, 32))
        z1 = out[:, :crop_l]
        out = model(take_per_row(batch_x, crop_offset + crop_eleft, 32))
        z2 = out[:, -crop_l:]

        loss = (
            hierarchical_contrastive_loss(p1, z2, temporal_unit=0)
            + hierarchical_contrastive_loss(p2, z1, temporal_unit=0)
        ) * 0.5
        loss.backward()
        optimizer.step()

    return loss


@timeit()
def train(train_data, train_loader, model, optimizer, args, target_idx, cuda):
    train_steps = len(train_loader)

    if cuda == "cuda:0":
        model.to("cuda:0")
    model.train()
    for i, (batch_x, batch_y) in enumerate(train_loader):
        optimizer.zero_grad()
        if cuda == "cuda:0":
            batch_x = batch_x.float().to("cuda:0")
            batch_y = batch_y.float().to("cuda:0")
        else:
            batch_x = batch_x.float()
            batch_y = batch_y.float()

        outputs = model(batch_x)

        f_dim = -1
        outputs = outputs[:, -1:, f_dim:]
        if cuda == "cuda:0":
            batch_y = batch_y[:, -1:, target_idx].to("cuda:0")
        else:
            batch_y = batch_y[:, -1:, target_idx]
        loss = F.mse_loss(outputs, batch_y)

        loss.backward()
        optimizer.step()

    attention = model.fs_attention
    return attention.data, loss


def test(test_data, test_loader, model, optimizer, args, target_idx, cuda):
    test_steps = len(test_loader)
    model.eval()
    with torch.no_grad():
        for i, (batch_x, batch_y) in enumerate(test_loader):
            optimizer.zero_grad()
            if cuda == "cuda:0":
                batch_x = batch_x.float().to("cuda:0")
                batch_y = batch_y.float().to("cuda:0")
            else:
                batch_x = batch_x.float()
                batch_y = batch_y.float()
            outputs = model(batch_x)
            f_dim = -1
            outputs = outputs[:, -1:, f_dim:]
            if cuda == "cuda:0":
                batch_y = batch_y[:, -1:, target_idx].to("cuda:0")
            else:
                batch_y = batch_y[:, -1:, target_idx]
            loss = F.mse_loss(outputs, batch_y)
    return loss


def take_per_row(A, indx, num_elem):
    all_indx = indx[:, None] + np.arange(num_elem)
    return A[torch.arange(all_indx.shape[0])[:, None], all_indx]


def GraphConstruct(target, cuda, epochs, lr, optimizername, data, args,
                   train_loader, test_loader):
    print(f"graph construct for {target}")

    df_tmp = data

    targetidx = df_tmp.columns.get_loc(target)

    window_size = 32
    layers = 128
    model = DLinear(window_size, layers, len(df_tmp.columns))

    if cuda == "cuda:0":
        model.to("cuda:0")
    optimizer = getattr(optim, optimizername)(model.parameters(), lr=lr)

    model.setPretrain(True)
    pbar = trange(1, epochs + 1, desc="pre train")
    for ep in pbar:
        pretrain_loss = pre_train(
            None, train_loader, model, optimizer, args, targetidx, cuda
        )
        pbar.set_postfix(pretrain_loss=pretrain_loss)

    model.setPretrain(False)
    pbar = trange(1, epochs + 1, desc="train and test")
    for ep in pbar:
        scores, train_loss = train(
            None, train_loader, model, optimizer, args, targetidx, cuda
        )
        model.setTest(True)
        test_loss = test(
            None, test_loader, model, optimizer, args, targetidx, cuda=cuda
        )
        model.setTest(False)
        pbar.set_postfix(train_loss=train_loss, test_loss=test_loss)

    s = sorted(scores.view(-1).cpu().detach().numpy(), reverse=True)
    indices = np.argsort(-1 * scores.view(-1).cpu().detach().numpy())

    if len(s) <= 5:
        potentials = []
        for i in indices:
            if scores[i] > 1:
                potentials.append(i)
    else:
        potentials = []
        gaps = []
        for i in range(len(s) - 1):
            if s[i] < 1:
                break
            gap = s[i] - s[i + 1]
            gaps.append(gap)
        sortgaps = sorted(gaps, reverse=True)

        for i in range(0, len(gaps)):
            largestgap = sortgaps[i]
            index = gaps.index(largestgap)
            ind = -1
            if index < ((len(s) - 1) / 2):
                if index > 0:
                    ind = index
                    break
        if ind < 0:
            ind = 0
        potentials = indices[: ind + 1].tolist()
    edge_to_target = dict()
    for v in potentials:
        edge_to_target[(targetidx, v)] = 0

    return edge_to_target


def pearson_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("The lengths of the input variables must be the same.")
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x_sq = sum(x[i] ** 2 for i in range(n))
    sum_y_sq = sum(y[i] ** 2 for i in range(n))
    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2)) ** 0.5
    if denominator == 0:
        return 0
    correlation = numerator / denominator
    return correlation


def breaktie(pagerank, G, trigger_point):
    if trigger_point == "None":
        return pagerank

    rank = []
    tmp_rank = []
    last_score = 0
    for cnt, (node, score) in enumerate(pagerank.items()):
        if last_score != score:
            if len(tmp_rank) == 0:
                last_score = score
                rank.append(node)
            else:
                ad = []
                for i in range(len(tmp_rank)):
                    try:
                        distance = nx.shortest_path_length(
                            G, source=trigger_point, target=node
                        )
                    except nx.NetworkXNoPath:
                        distance = 0
                    ad.append(distance)
                ad = np.array(ad)
                dis_rank = np.argsort(-ad)  # Negative sign to sort in descending order
                for i in range(len(dis_rank)):
                    rank.append(tmp_rank[dis_rank[i]])
                tmp_rank = [node]
        else:
            tmp_rank.append(node)
            if cnt == len(pagerank) - 1:
                ad = []
                for i in range(len(tmp_rank)):
                    try:
                        distance = nx.shortest_path_length(
                            G, source=trigger_point, target=node
                        )
                    except nx.NetworkXNoPath:
                        distance = 0
                    ad.append(distance)
                ad = np.array(ad)
                dis_rank = np.argsort(-ad)
                for i in range(len(dis_rank)):
                    rank.append(tmp_rank[dis_rank[i]])
    return rank


def Run(args):
    df_data = args.data
    edges = dict()

    columns = list(df_data)

    # DataLoader 只创建一次，所有列共享 Scaler 和数据
    _, train_loader = data_provider(args, flag="train")
    _, test_loader = data_provider(args, flag="test")

    for c in columns:
        idx = df_data.columns.get_loc(c)
        edge = GraphConstruct(
            c,
            cuda=args.cuda,
            epochs=args.epochs,
            lr=args.learning_rate,
            optimizername=args.optimizer,
            data=df_data,
            args=args,
            train_loader=train_loader,
            test_loader=test_loader,
        )

        print(c, idx, edge)
        edges.update(edge)
        torch.cuda.empty_cache()

    return edges, columns


@timeit()
def CreateGraph(edge, columns):
    G = nx.DiGraph()
    for c in columns:
        G.add_node(c)
    for pair in edge:
        p1, p2 = pair
        G.add_edge(columns[p2], columns[p1])
    return G


def run(data, inject_time=None, dataset=None, with_bg=False, args=None, **kwargs):
    args = argparse.Namespace(
        cuda="cuda:0" if torch.cuda.is_available() else -1,
        epochs=1,
        learning_rate=0.001,
        optimizer="Adam",
        num_workers=0,
        root_cause="unknown",
        data=data,
    )

    nrepochs = args.epochs
    learningrate = args.learning_rate
    optimizername = args.optimizer
    cuda = args.cuda
    root_cause = args.root_cause

    edge_pair, columns = Run(args)
    pruning = args.data

    G = CreateGraph(edge_pair, columns)

    while not nx.is_directed_acyclic_graph(G):
        edge_cor = []
        edges = G.edges()
        for edge in edges:
            source, target = edge
            edge_cor.append(pearson_correlation(pruning[source], pruning[target]))
        tmp = np.array(edge_cor)
        tmp_idx = np.argsort(tmp)
        edges = list(edges)
        source, target = edges[tmp_idx[0]][0], edges[tmp_idx[0]][1]

        G.remove_edge(source, target)

    dangling_nodes = [node for node, out_degree in G.out_degree() if out_degree == 0]
    personalization = {}
    for node in G.nodes():
        if node in dangling_nodes:
            personalization[node] = 1.0
        else:
            personalization[node] = 0.5
    pagerank = nx.pagerank(G, personalization=personalization)
    ranks = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)

    ranks = [r[0] for r in ranks]
    return {"ranks": ranks}


class RUN(Algorithm):
    def needs_cpu_count(self) -> int | None:
        return 2

    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        adapter = SimpleMetricsAdapter(run)
        return adapter(args)
