import logging
import polars as pl
from pathlib import Path

logger = logging.getLogger(__name__)

def _process_metrics( metric_dir: Path) -> list[pl.DataFrame]:
    metric_dfs = []
    for metric_file in metric_dir.glob("*.csv"):
        if "metric" in metric_file.name:
            try:
                df = pl.read_csv(
                    metric_file, schema_overrides={"SyscallRead": pl.Float64, "SyscallWrite": pl.Float64}
                )

                exclude_columns = ["Time", "TimeStamp", "PodName"]
                metric_columns = [col for col in df.columns if col not in exclude_columns]

                df_long = df.unpivot(
                    index=["Time", "PodName"], on=metric_columns, variable_name="metric", value_name="value"
                )

                df_long = df_long.rename({"Time": "time", "PodName": "service_name"})
                df_long = df_long.with_columns(pl.col("value").cast(pl.Float64, strict=False))

                df_long = df_long.with_columns(
                    pl.col("time")
                    .str.extract(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6})")
                    .str.strptime(pl.Datetime(time_zone="UTC"), "%Y-%m-%d %H:%M:%S%.f")
                    .alias("time")
                )

                filtered_df = df_long

                metric_dfs.append(filtered_df)
            except Exception as e:
                logger.warning("Failed to load metric data {} \nError: {}", metric_file, e)
    return metric_dfs

if __name__ == "__main__":


    metric_dir = Path("/mnt/jfs/Nezha/construct_data/2022-08-23/metric")
    result = _process_metrics(metric_dir)
    Path("normal_metric/2022-08-23").mkdir(parents=True, exist_ok=True)
    pl.concat(result).write_parquet("normal_metric/2022-08-23/metric.parquet")