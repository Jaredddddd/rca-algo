可以，已经实现了：现在可以先保存融合前的 raw feature matrix，后面改 `FEATURE_PRIORITY_WEIGHTS` 不用反复跑 batch eval。

新增工具在 [evidrank_feature_cache.py](/home/ljw/paper/aegis/rca-algo-contrib/VibeResearchTools/evidrank_feature_cache.py:1)：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py dump --version FW_FEATURE_CACHE_BASE --dataset rcabench --workers 48
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py reweight --cache FW_FEATURE_CACHE_BASE --version FW_REWEIGHT_CURRENT --preset current --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py scan --cache FW_FEATURE_CACHE_BASE --version FW_SCAN_CURRENT_LOW_STRONG_RANGE --dataset rcabench ...
```

feature cache 已生成：`1422` cases，`69684` service-feature rows，`0` errors。离线 reweight 复现 full eval 完全一致：

| ladder | weights | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: |
| current | `0,.75,1,1.25,1.5,6,10,16` | 0.800985 | 0.874517 | 0.942335 | 0.975387 |
| linear 0-7 | `0,1,2,3,4,5,6,7` | 0.671589 | 0.789295 | 0.886076 | 0.945148 |
| power2 | `0,1,1,1,2,4,8,16` | 0.756681 | 0.851812 | 0.941632 | 0.973980 |
| decimal | `0,1,1,1,2,5,10,15` | 0.768636 | 0.858448 | 0.942335 | 0.975387 |

**为什么影响这么大：**  
这些权重不是普通编号，而是在控制 root-specific evidence 和 propagation/background evidence 的分离倍率。`0-7` 把 `CRITICAL/BASELINE` 从 `16` 压到 `3.5`，`ROOT/BASELINE` 从 `10` 压到 `3`，同时把 support/background 相对抬高，所以 victim/入口/高流量症状会抢掉 top1。

**区间扫描结果：**

固定低层为 current：`.75,1,1.25,1.5`

| level | tested values | best/no-loss AC@1 |
| --- | --- | ---: |
| HIGH | 4,5,6,7,8 | only `6` reaches 0.800985 |
| ROOT | 8,9,10,11,12 | `8..11` reach 0.800985 |
| CRITICAL | 12,14,15,16,18,20 | only `16` reaches 0.800985; `18` is 0.799578 |

固定强层为 current：`6,10,16`

| level | tested values | best AC@1 |
| --- | --- | ---: |
| BACKGROUND | .5,.75,1 | `.75` gives 0.800985 |
| SUPPORT | 1,1.25,1.5 | `1.25` gives 0.800985 |
| LOCAL | 1,1.5,2 | `1.5` gives 0.800985 |

结论：当前数值确实敏感，尤其 `HIGH=6`、`CRITICAL=16`、`BACKGROUND=.75`、`LOCAL=1.5`。可以表述成 **“SRE feature-priority prior with a calibrated severity ladder”**，但不能说 priority value 随便取都行。

我已把记录写到 [FW_PRIORITY_LADDER_ABLATION_iteration.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/FW_PRIORITY_LADDER_ABLATION_iteration.md:1)，并刷新了 VibeResearch index。当前 `algorithm.py` 已恢复，无实验 ladder 残留；guard 无 high-risk，full eval 恢复为 AC@1 `0.800985`。