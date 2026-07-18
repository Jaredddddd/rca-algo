# RCABench 结果清理记录

日期：2026-07-16

## 范围与保留规则

清理 `output/rcabench-platform-v2/data` 中所有目录名匹配
`cera*`、`evidencerank*` 和 `pv_*` 的结果。CREST 仅保留当前注册的
modality、`local`/`nocf` 和 active feature-profile 比较套件：

- `crest_metric`、`crest_log`、`crest_trace`、`crest_metric_log`、
  `crest_metric_trace`、`crest_log_trace`
- `crest_local`、`crest_nocf`
- `crest_feature_min8`、`crest_feature_min8_local`、
  `crest_feature_min8_nocf`
- `crest_aiops25_generic`、`crest_aiops25_generic_local`、
  `crest_aiops25_generic_nocf`

其余 `crest*` 结果（包括 `crest`、`crest_meo*` 及探索性变体）已删除。

## 统计与验证

- 删除前：3.7 GiB；31,158 个指定模式目录和 50,146 个非白名单 CREST
  目录。
- 删除后：1.7 GiB，约释放 2.0 GiB；保留 18,172 个 CREST 白名单结果目录。
- 验证：指定模式目录数量为 0，非白名单 `crest*` 目录数量为 0；其余算法
  结果目录未被清理命令匹配。
