# EvidenceRank Evolution Log

本目录记录 EvidenceRank 的自进化研究过程。每一轮优化都应保留：

- 版本号，例如 `V1`、`V2`；
- 修改前 snapshot；
- false case summary；
- 假设和通用算法动机；
- 代码改动摘要；
- full eval 指标；
- 新 snapshot；
- 与上一版本的 compare report；
- 接受或拒绝结论。

Vibe Research 主页面为 `VibeResearchTools/VibeResearch.md`。本目录中的文档应通过主页面 index 可见；生成或修改研究文档后运行：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

推荐命令：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V1 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V1 --source V1 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py new-note --version V2 --hypothesis "一句话描述下一轮通用算法假设"
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
```

评估命令：

```bash
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

比较命令：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V2 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V2 --source V2 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V1 --new V2 --algorithm evidencerank --dataset rcabench
```

注意：`labels.csv` 和 `injection.json` 只能用于离线分析和文档，不能进入算法运行路径。
