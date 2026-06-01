"""
修复 rcabench_platform MRR 计算缺陷。

问题：原 calc_mrr 在计算前用 filter(hit) 过滤了所有未命中的查询，
导致这些查询不参与分母，MRR 被人为抬高。

修复：未命中查询的 RR 记为 0，纳入分母，得到严格 MRR。

用法：
    import patches.rcabench_mrr_fix  # 在调用 calc_all_perf 之前导入即可
"""

import polars as pl

import rcabench_platform.v2.evaluation.ranking as _mod
from rcabench_platform.v2.evaluation.ranking import (
    INDEX_COLUMNS,
    SAMPLER_COLUMNS,
    agg_index,
)


def _calc_mrr_fixed(df: pl.DataFrame, agg_level: str) -> pl.DataFrame:
    is_sampler_level = agg_level in ["sampler", "sampler_dataset"]
    if is_sampler_level:
        group_by_columns = INDEX_COLUMNS + SAMPLER_COLUMNS
    else:
        group_by_columns = INDEX_COLUMNS

    lf = df.lazy()
    lf = lf.select(*group_by_columns, pl.col("hit"), pl.col("rank"))

    # 每个 query 取命中记录中的最小 rank；无命中则为 null
    lf = lf.group_by(group_by_columns).agg(
        pl.col("rank").filter(pl.col("hit")).min().alias("rank"),
    )

    # 有命中 → 1/rank，无命中 → 0
    lf = lf.with_columns(
        pl.when(pl.col("rank").is_not_null())
        .then(1 / pl.col("rank"))
        .otherwise(0.0)
        .alias("MRR")
    )

    agg_cols = [pl.col("MRR").mean().round(6)]
    if agg_level == "datapack":
        agg_cols = [pl.col("rank").first(), *agg_cols]

    lf = lf.group_by(agg_index(agg_level)).agg(*agg_cols)
    return lf.collect()


# 应用 monkey-patch
_mod.calc_mrr = _calc_mrr_fixed
