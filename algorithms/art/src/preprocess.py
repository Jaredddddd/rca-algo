import pandas as pd
import numpy as np
import torch
import dgl
import pickle
import json
from tqdm import tqdm
from pathlib import Path
from collections import defaultdict
from typing import Optional, Dict, Any, List, Tuple, Union
from loguru import logger
import os
from rcabench.openapi import InjectionApi, ApiClient, Configuration

from enum import Enum, auto  # 导入Enum基类和auto值生成器
import typer

class Dataset(Enum):  # 定义名为Dataset的枚举类，继承自Enum
    RCABENCH_r1 = auto()
    RCABENCH_r2 = auto()


# 1. 修改窗口大小为10秒
SAMPLING_SIZE = 10 #处理数据平滑时用samling_size
WINDOW_SIZE = 10  # 滑动窗口大小为6个采样点，即60秒
SLIDING_STEP = 5  # Sliding step size

def create_dataset(
    data_root: str,
    output_dir: str,
    ds: str = "RCABENCH_r1",
) -> Union[List[Path], Tuple[List[Path], List[Path]]]:
    if ds == "RCABENCH_r1":
        dataset = Dataset.RCABENCH_r1
    elif ds == "RCABENCH_r2":
        dataset = Dataset.RCABENCH_r2

    logger.info("Starting dataset creation...")
    output_path = Path(output_dir) / ds

    logger.info(f"Using {ds} dataset from {data_root}")
    # Use RCABENCH_r1 or RCABENCH_r2 dataset
    if dataset == Dataset.RCABENCH_r1:
        train_dir = Path(data_root) / "__dev__rcabench_train_r1"
        test_dir = Path(data_root) / "__dev__rcabench_test_r1"
    else:
        train_dir = Path(data_root) / "__dev__rcabench_train_r2"
        test_dir = Path(data_root) / "__dev__rcabench_test_r2"

    if not train_dir.exists() or not test_dir.exists():
        raise FileNotFoundError("Train or test directory does not exist")

    train_cases = os.listdir(train_dir)
    test_cases = os.listdir(test_dir)

    train_data_packs = [train_dir / case for case in train_cases]
    test_data_packs = [test_dir / case for case in test_cases]
    
    return train_data_packs, test_data_packs


class DataPreprocessor:
    def __init__(self, metrics_path: str, traces_path: str, logs_path: str, all_services: List[str], all_metrics: List[str], sampling_size: int = SAMPLING_SIZE):
        self.metrics_path = metrics_path
        self.traces_path = traces_path
        self.logs_path = logs_path
        self.sampling_size = sampling_size
        self.metrics_df: Optional[pd.DataFrame] = None
        self.traces_df: Optional[pd.DataFrame] = None
        self.logs_df: Optional[pd.DataFrame] = None
        self.features_by_window: Optional[Dict[Any, Any]] = None
        self.services: Optional[list] = None
        self.graphs_by_window: Optional[Dict[Any, Any]] = None
        self.samples: Optional[list] = None
        self.services = all_services
        self.metrics = all_metrics

    @staticmethod
    def extract_service_name(row: pd.Series) -> Optional[str]:
        if row['service_name'] != "":
            return row['service_name']
        elif 'attr.k8s.container.name' in row and row['attr.k8s.container.name'] != "":
            return row['attr.k8s.container.name']
        elif 'attr.k8s.service.name' in row and row['attr.k8s.service.name'] != "":
            return row['attr.k8s.service.name']
        return None

    def load_data(self) -> None:
        self.metrics_df = pd.read_parquet(self.metrics_path)
        self.metrics_df['value'] = self.metrics_df['value'].fillna(0)
        self.traces_df = pd.read_parquet(self.traces_path)
        self.logs_df = pd.read_parquet(self.logs_path)

    def preprocess_metrics(self) -> None:
        if self.metrics_df is None:
            raise ValueError("metrics_df is None. Please call load_data() before preprocessing metrics.")
        df = self.metrics_df.copy()
        df['extracted_service'] = df.apply(DataPreprocessor.extract_service_name, axis=1) ## type: ignore
        df = df.dropna(subset=['extracted_service']).copy()
        df.loc[:, 'timestamp'] = df['time'].astype('int64') // 1_000_000_000
        df.loc[:, 'time_window'] = df['timestamp'] // self.sampling_size
        grouped = df.groupby(['time_window', 'extracted_service', 'metric'])['value'].mean().reset_index()

        # --- trace统计量 ---
        if self.traces_df is None:
            raise ValueError("traces_df is None. Please call load_data() before preprocessing traces.")
        trace_df = self.traces_df.copy()
        trace_df['extracted_service'] = trace_df.apply(DataPreprocessor.extract_service_name, axis=1) ## type: ignore
        trace_df = trace_df.dropna(subset=['extracted_service']).copy()
        trace_df.loc[:, 'timestamp'] = trace_df['time'].astype('int64') // 1_000_000_000
        trace_df.loc[:, 'time_window'] = trace_df['timestamp'] // self.sampling_size
        trace_duration = trace_df.groupby(['time_window', 'extracted_service'])['duration'].mean().reset_index()
        trace_duration = trace_duration.rename(columns={'duration': 'trace_duration_mean'})
        trace_count = trace_df.groupby(['time_window', 'extracted_service'])['trace_id'].count().reset_index()
        trace_count = trace_count.rename(columns={'trace_id': 'trace_request_count'})
        trace_feat = pd.merge(trace_duration, trace_count, on=['time_window', 'extracted_service'], how='outer')

        # --- log统计量 ---
        if self.logs_df is None:
            raise ValueError("logs_df is None. Please call load_data() before preprocessing logs.")
        log_df = self.logs_df.copy()
        log_df['extracted_service'] = log_df.apply(DataPreprocessor.extract_service_name, axis=1) ## type: ignore
        log_df = log_df.dropna(subset=['extracted_service']).copy()
        log_df.loc[:, 'timestamp'] = log_df['time'].astype('int64') // 1_000_000_000
        log_df.loc[:, 'time_window'] = log_df['timestamp'] // self.sampling_size
        log_levels = ['INFO', 'ERROR', 'WARN', 'DEBUG']
        log_counts = (
            log_df.groupby(['time_window', 'extracted_service', 'level'])
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )
        for level in log_levels:
            if level not in log_counts.columns:
                log_counts[level] = 0
        log_counts = log_counts.rename(columns={lvl: f'log_{lvl.lower()}' for lvl in log_levels})

        # --- 合并所有特征 ---
        assert self.services is not None, "services must be provided"
        service_to_idx = {service: i for i, service in enumerate(self.services)}
        metric_to_idx = {metric: i for i, metric in enumerate(self.metrics)}
        time_windows = sorted(grouped['time_window'].unique())
        features_by_window = {}
        for window in time_windows:
            window_data = grouped[grouped['time_window'] == window]
            feature_matrix = np.zeros((len(self.services), len(self.metrics) + 6))  # 6=4(log)+2(trace)
            # metric
            for _, row in window_data.iterrows():
                service_idx = service_to_idx[row['extracted_service']]
                metric_idx = metric_to_idx[row['metric']]
                feature_matrix[service_idx, metric_idx] = row['value']
            # trace
            trace_row = trace_feat[trace_feat['time_window'] == window]
            for _, row in trace_row.iterrows():
                service_idx = service_to_idx.get(row['extracted_service'])
                if service_idx is not None:
                    feature_matrix[service_idx, len(self.metrics)] = row.get('trace_duration_mean', 0)
                    feature_matrix[service_idx, len(self.metrics)+1] = row.get('trace_request_count', 0)
            # log
            log_row = log_counts[log_counts['time_window'] == window]
            for _, row in log_row.iterrows():
                service_idx = service_to_idx.get(row['extracted_service'])
                if service_idx is not None:
                    feature_matrix[service_idx, len(self.metrics)+2] = row.get('log_info', 0)
                    feature_matrix[service_idx, len(self.metrics)+3] = row.get('log_error', 0)
                    feature_matrix[service_idx, len(self.metrics)+4] = row.get('log_warn', 0)
                    feature_matrix[service_idx, len(self.metrics)+5] = row.get('log_debug', 0)
            features_by_window[window] = (pd.to_datetime(window * self.sampling_size, unit='s'), torch.FloatTensor(feature_matrix))
        self.features_by_window = features_by_window

    def preprocess_traces(self) -> None:
        if self.traces_df is None:
            raise ValueError("traces_df is None. Please call load_data() before preprocessing traces.")
        df = self.traces_df.copy()
        df['source_service'] = df.apply(DataPreprocessor.extract_service_name, axis=1)  # type: ignore
        df['destination_service'] = None
        span_service_map = df.set_index('span_id')['source_service'].to_dict()
        def find_destination(row) -> Optional[str]:
            parent_span_id = row['parent_span_id']
            if parent_span_id in span_service_map:
                return span_service_map[parent_span_id]
            return None
        df['destination_service'] = df.apply(lambda row: find_destination(row), axis=1)  # type: ignore
        

        df = df.dropna(subset=['source_service', 'destination_service']).copy()
        df.loc[:, 'timestamp'] = df['time'].astype('int64') // 1_000_000_000
        df.loc[:, 'time_window'] = df['timestamp'] // self.sampling_size

        assert self.services is not None
        service_to_idx = {service: i for i, service in enumerate(self.services)}
        time_windows = sorted(df['time_window'].unique())
        graphs_by_window = {}
        for window in time_windows:
            window_data = df[df['time_window'] == window]
            edge_set = set()
            for _, row in window_data.iterrows():
                src = service_to_idx.get(row['source_service'])
                dst = service_to_idx.get(row['destination_service'])
                if src is not None and dst is not None and src != dst:
                    edge_set.add((src, dst))
            if edge_set:
                src_nodes, dst_nodes = zip(*edge_set)
                g = dgl.graph((list(src_nodes), list(dst_nodes)), num_nodes=len(self.services))
                graphs_by_window[window] = g
        self.graphs_by_window = graphs_by_window

    def combine_data(self) -> None:
        samples = []
        if self.features_by_window is None or self.graphs_by_window is None:
            raise ValueError("features_by_window or graphs_by_window is None.")
        common_windows = set(self.features_by_window.keys()) & set(self.graphs_by_window.keys())
        for window in sorted(common_windows):
            timestamp, feature_tensor = self.features_by_window[window]
            graph = self.graphs_by_window[window]
            samples.append((timestamp, graph, feature_tensor))
        self.samples = samples

class DatasetPack:
    """每个case的数据包，包含滑动窗口样本提取功能"""
    def __init__(self, samples: List[Any]):
        self.samples = samples  # [(timestamp, graph, feature_tensor), ...]

    def create_sliding_windows(self, window_size: int = 10, max_gap: int = 12) -> List[Any]:
        # 滑动窗口提取，max_gap为12s，window_size为滑窗长度
        series_samples = [self.samples[i:i+window_size] for i in range(0, len(self.samples) - window_size + 1, SLIDING_STEP)]
        series_samples = [
            series_sample for series_sample in series_samples
            if all(abs(int((series_sample[i][0] - series_sample[i+1][0]).total_seconds())) <= max_gap for i in range(len(series_sample) - 1))
        ]
        dataset = [
            [
                torch.tensor(int(series_sample[-2][0].timestamp())),  # 倒数第二个个时间戳
                series_sample[-1][1],
                torch.stack([step[2] for step in series_sample[:-1]]),
                torch.tensor(series_sample[-1][2])
            ] for series_sample in series_samples
        ]
        return dataset

def extract_injection_name(injection_name: str) -> str:
    parts = injection_name.split('-')
    for i, p in enumerate(parts):
        if p == 'service' and i > 0:
            return '-'.join(parts[:i+1])
    return injection_name

def minmax_tensor(tensor_list: List[torch.Tensor]) -> List[torch.Tensor]:
    all_tensor = torch.cat([t.unsqueeze(0) for t in tensor_list], dim=0)
    min_val = all_tensor.min(dim=0, keepdim=True)[0]
    max_val = all_tensor.max(dim=0, keepdim=True)[0]
    # 防止分母为0
    range_val = max_val - min_val
    range_val[range_val < 1e-8] = 1.0
    normed = (all_tensor - min_val) / range_val
    return [normed[i] for i in range(normed.shape[0])]

def collect_all_metrics_services(case_dirs: List[Path], metric_file_name: str) -> Tuple[List[str], List[str]]:
    all_metrics = set()
    all_services = set()
    for case_dir in case_dirs:
        metric_path = case_dir / metric_file_name
        if not metric_path.exists():
            continue
        df = pd.read_parquet(metric_path)
        all_metrics.update(df['metric'].unique())
        all_services.update(df['service_name'].unique())
    return sorted(all_services), sorted(all_metrics)


def process_case(case_dir: Path, metric_file: str, trace_file: str, log_file: str, all_services: List[str], all_metrics: List[str], sampling_size: int = SAMPLING_SIZE) -> List[Any]:
    processor = DataPreprocessor(
        metrics_path=os.path.join(case_dir, metric_file),
        traces_path=os.path.join(case_dir, trace_file),
        logs_path=os.path.join(case_dir, log_file),
        all_services=all_services,
        all_metrics=all_metrics,
        sampling_size=sampling_size
    )
    processor.load_data()
    processor.preprocess_metrics()
    processor.preprocess_traces()
    processor.combine_data()
    return processor.samples if processor.samples is not None else []


def build_groundtruth(case_dirs: List[Path]):
    records = []
    for case_dir in case_dirs:
        env_path = case_dir / 'env.json'
        inj_path = case_dir / 'injection.json'
        if not env_path.exists() or not inj_path.exists():
            continue
        with open(env_path) as f:
            env = json.load(f)
        with open(inj_path) as f:
            inj = json.load(f)
        inj_name = extract_injection_name(inj['injection_name'])
        failure_type = inj['fault_type']
        ab_start=pd.to_datetime(int(env['ABNORMAL_START']), unit='s', utc=True)
        ab_end=pd.to_datetime(int(env['ABNORMAL_END']), unit='s', utc=True)
        ab_start=int(ab_start.timestamp())
        ab_end=int(ab_end.timestamp())

        aligned_start = ab_start - (ab_start % SAMPLING_SIZE)
        for t in range(aligned_start, ab_end, SAMPLING_SIZE):
            # 直接存储为int秒
            records.append({
                'timestamp': t,
                'injection_name': inj_name,
                'failure_type': failure_type
            })
    
    return pd.DataFrame(records)

def create_dataset_for_training(case_samples_list: List[List[Any]], window_size: int = 10, max_gap: int = 10) -> List[Any]:
    """对所有case的样本做滑动窗口，合并为训练集"""
    all_dataset = []
    for samples in case_samples_list:
        pack = DatasetPack(samples)
        all_dataset.extend(pack.create_sliding_windows(window_size=window_size, max_gap=max_gap))
    return all_dataset

def run_preprocess(
        data_root="/mnt/jfs/rcabench-platform-v2/data",
        output_dir="data/RCABENCH",
        ds="RCABENCH_r1",

):
    os.makedirs(output_dir, exist_ok=True)
    dataset_result = create_dataset(
        data_root=data_root,
        output_dir=output_dir,
        ds=ds
    )

    if isinstance(dataset_result, tuple):
        train_data_packs, test_data_packs = dataset_result
        typer.echo(f"Found {len(train_data_packs)} train data packs")
        typer.echo(f"Found {len(test_data_packs)} test data packs")
        all_data_packs = train_data_packs + test_data_packs

    all_services, all_metrics = collect_all_metrics_services(all_data_packs, 'abnormal_metrics.parquet')
    typer.echo(f"Found {len(all_services)} services: {all_services}")
    typer.echo(f"Found {len(all_metrics)} metrics: {all_metrics}")


    # 保存全局service_to_idx
    service_to_idx = {service: i for i, service in enumerate(all_services)}
    with open(os.path.join(output_dir, 'node_dict.pkl'), 'wb') as f:
        pickle.dump(service_to_idx, f)

    metric_to_idx = {metric: i for i, metric in enumerate(all_metrics)}
    with open(os.path.join(output_dir, 'metric_dict.pkl'), 'wb') as f:
        pickle.dump(metric_to_idx, f)

    ## 构建groundtruth
    gt= build_groundtruth(test_data_packs)
    

    test_case_samples = []
    for case_dir in tqdm(test_data_packs, desc='Processing abnormal cases'):
        samples = process_case(case_dir, 'abnormal_metrics.parquet', 'abnormal_traces.parquet', 'abnormal_logs.parquet', all_services, all_metrics)
        test_case_samples.append(samples)
    train_case_samples = []
    for case_dir in tqdm(train_data_packs, desc='Processing normal cases'):
        samples = process_case(case_dir, 'normal_metrics.parquet', 'normal_traces.parquet', 'normal_logs.parquet', all_services, all_metrics)
        train_case_samples.append(samples)
    # min-max归一化所有feature
    all_features = [s[2] for samples in (test_case_samples + train_case_samples) for s in samples]
    normed_features = minmax_tensor(all_features)
    # 替换原始feature
    idx = 0
    for samples in test_case_samples:
        for i, s in enumerate(samples):
            samples[i] = (s[0], s[1], normed_features[idx])
            idx += 1
    for samples in train_case_samples:
        for i, s in enumerate(samples):
            samples[i] = (s[0], s[1], normed_features[idx])
            idx += 1

    # 滑动窗口提取
    test_samples = create_dataset_for_training(test_case_samples, window_size=WINDOW_SIZE, max_gap=12)
    train_samples = create_dataset_for_training(train_case_samples, window_size=WINDOW_SIZE, max_gap=12)
    # 保存
    os.makedirs(os.path.join(output_dir, 'samples'), exist_ok=True)
    with open(os.path.join(output_dir,r'samples/test_samples.pkl'), 'wb') as f:
        pickle.dump(test_samples, f)
    with open(os.path.join(output_dir,r'samples/train_samples.pkl'), 'wb') as f:
        pickle.dump(train_samples, f)

    # 提取df中的所有时间索引（从列表中取第一个元素）
    df_time_set = {item[0].item() for item in test_samples}  # 使用集合提高查找效率
    filtered_gt = gt[gt.iloc[:, 0].isin(df_time_set)]
    gt_timestamp = [filtered_gt[i]["timestamp"] for i in range(len(filtered_gt))]

    # 重新保存筛选后的结果
    filtered_gt.to_csv(os.path.join(output_dir,'cases.csv'), index=False)

    
    time_abnormal = [s[0] for s in test_samples]
    for i in range(len(time_abnormal)):
        time=time_abnormal[i]
        if time not in gt_timestamp:
            print(f"Warning: Timestamp {time} not found in ground truth.")

    return {
    "num_train_samples": len(train_samples),
    "num_test_samples": len(test_samples),
    "num_services": len(all_services),
    "num_metrics": len(all_metrics),
    "train_samples_path": os.path.join(output_dir, "samples", "train_samples.pkl") if train_data_packs else None,
    "train_labels_path": os.path.join(output_dir, "samples", "train_labels.pkl") if train_data_packs else None,
    "test_samples_path": os.path.join(output_dir, "samples", "test_samples.pkl") if test_data_packs else None,
    "test_labels_path": os.path.join(output_dir, "samples", "test_labels.pkl") if test_data_packs else None,
    }
    


if __name__ == '__main__':
    # main()
    # node_dict_path = r'data/D1/hash_info/node_hash.pkl'
    # with open(node_dict_path, 'rb') as f:
    #     node_dict = pickle.load(f)
    # print(node_dict)  # 打印节点字典


    # 指定文件路径
    file_path = r'data/RCABENCH/samples/abnormal_samples.pkl'  # 替换为实际文件路径
    label_path = r'data/RCABENCH/cases.csv'

    # 打开文件并读取数据
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    label=pd.read_csv(label_path)
    print(label["timestamp"])
    print(type(label["timestamp"]))
    print(len(data))
    print(len(data[0]))
    print(data[0][0])  # 打印第一个样本的时间戳
    print(data[0][1])  # 打印第一个样本的图
    print(data[0][2].shape)  # 打印第一个样本的特征张量
    print(data[0][3].shape)  # 打印第一个样本的标签张量




