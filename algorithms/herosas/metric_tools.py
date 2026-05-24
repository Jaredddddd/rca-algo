'''
PYTHONPATH=. python tools/OpenRCA/bank/metric_tools.py
'''
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz
from typing import Annotated, List, Dict, Any
from langchain.tools import tool

from utils.settings import DATASET_DIR


@tool
def find_metric_anomalies_bank(
    start_time_str: Annotated[
        str,
        "Start time of the diagnosis window in 'YYYY-MM-DD HH:MM:SS' format, e.g., '2021-03-04 18:00:00'",
    ],
    end_time_str: Annotated[
        str,
        "End time of the diagnosis window in 'YYYY-MM-DD HH:MM:SS' format, e.g., '2021-03-04 18:30:00'",
    ],
    date_str: Annotated[
        str,
        "Date string for locating data files, in 'YYYY_MM_DD' format, e.g., '2021_03_04'",
    ],
    stable_window_size: Annotated[
        int, "Number of data points to define a stable phase."
    ] = 5,
    min_stable_window_size: Annotated[
        int,
        "Minimum number of data points required for the stable phase in boundary scenarios.",
    ] = 3,
    recovery_window_size: Annotated[
        int, "Number of data points to define a recovery phase."
    ] = 5,
    anomaly_window_min: Annotated[
        int, "Minimum number of data points for an anomaly phase."
    ] = 1,
    anomaly_window_max: Annotated[
        int, "Maximum number of data points for an anomaly phase."
    ] = 8,
    stable_std_threshold: Annotated[
        float,
        "Standard deviation threshold for a phase to be considered stable (on a 0-100 normalized scale).",
    ] = 10.0,
    recovery_std_threshold: Annotated[
        float,
        "Standard deviation threshold for the recovery phase (on a 0-100 normalized scale).",
    ] = 25.0,
    jump_threshold_factor: Annotated[
        float,
        "A factor to determine a significant jump. The jump value must be greater than this factor times the stable phase's standard deviation.",
    ] = 3.0,
    noise_reduction_w: Annotated[
        float,
        "Weight for noise reduction within a metric. Anomalies with a delta less than w * max_delta for that metric are removed.",
    ] = 0.4,
    cluster_minutes_k: Annotated[
        int, "Time window in minutes to group anomalies into a single cluster."
    ] = 3,
    max_clusters_nc: Annotated[
        int,
        "If a metric has more than this number of anomaly clusters, it's considered noisy and its anomalies are discarded.",
    ] = 3,
    final_filter_x: Annotated[
        float,
        "Final noise reduction factor. Anomalies with a delta less than x * overall_max_delta are removed.",
    ] = 0.2,
) -> List[Dict[str, Any]]:
    """
    Detect metric anomalies from Bank container telemetry within a diagnosis window.

    Notes:
        This tool runs a multi-stage anomaly search over the selected KPI set.
        It loads telemetry for the specified date, normalizes KPI values across components,
        searches for a Stable -> Anomaly -> Recovery pattern, removes noisy results by
        delta and temporal clustering, and returns the remaining anomalies sorted by severity.
        The Bank KPI set mixes CPU, memory, network, disk, filesystem, and JVM indicators.

    Args:
        start_time_str: Start time of the diagnosis window.
        end_time_str: End time of the diagnosis window.
        date_str: Date string used to locate telemetry files.
        stable_window_size: Number of data points used to define a stable phase.
        min_stable_window_size: Minimum stable phase size allowed near window boundaries.
        recovery_window_size: Number of data points used to define a recovery phase.
        anomaly_window_min: Minimum anomaly phase length.
        anomaly_window_max: Maximum anomaly phase length.
        stable_std_threshold: Maximum normalized standard deviation for the stable phase.
        recovery_std_threshold: Maximum normalized standard deviation for the recovery phase.
        jump_threshold_factor: Minimum jump factor relative to stable-phase deviation.
        noise_reduction_w: Per-metric noise filter threshold.
        cluster_minutes_k: Time window used to merge nearby anomalies into one cluster.
        max_clusters_nc: Maximum allowed cluster count before a metric is treated as noisy.
        final_filter_x: Final global noise filter threshold.

    Returns:
        A severity-sorted list of anomaly dictionaries. Returns an empty list when no significant anomalies are found.
    """
    debug = False
    # data_source_path = 'dataset/Bank/telemetry'
    data_source_path = DATASET_DIR

    # if "Bank" in data_source_path:
    #     TARGET_KPIS = [metric for metrics in kpi_Bank.values() for metric in metrics]
    # elif "Telecom" in data_source_path:
    #     TARGET_KPIS = [metric for metrics in kpi_Telecom.values() for metric in metrics]
    # elif "Market" in data_source_path:
    #     TARGET_KPIS = [metric for metrics in kpi_Market.values() for metric in metrics]
    # else:
    #     raise ValueError("Unknown data source path, cannot determine KPI set.")
    TARGET_KPIS = [
        "OSLinux-CPU_CPU_CPUCpuUtil",
        "OSLinux-CPU_CPU_CPUUserTime",
        "OSLinux-OSLinux_MEMORY_MEMORY_NoCacheMemPerc",
        "OSLinux-OSLinux_MEMORY_MEMORY_MEMUsedMemPerc",
        "OSLinux-OSLinux_MEMORY_MEMORY_MEMFreeMem",
        "OSLinux-OSLinux_NETWORK_NETWORK_TCP-FIN-WAIT",
        "OSLinux-OSLinux_NETWORK_NETWORK_TotalTcpConnNum",
        "OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKReadWrite",
        "OSLinux-OSLinux_FILESYSTEM_-tomcat_FSCapacity",
        "OSLinux-OSLinux_FILESYSTEM_-apache_FSCapacity",
        "JVM-Operating System_7779_JVM_JVM_CPULoad",
        "JVM-Operating System_7778_JVM_JVM_CPULoad",
        "JVM-Memory_7778_JVM_Memory_NoHeapMemoryUsed",
        "JVM-Memory_7779_JVM_Memory_NoHeapMemoryUsed",
    ]
    
    # 
    NORMALIZED_KPIS = [
        'OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKReadWrite',
        'OSLinux-OSLinux_FILESYSTEM_-tomcat_FSCapacity',
        'OSLinux-OSLinux_FILESYSTEM_-apache_FSCapacity'
    ]
        

    if debug:
        print("=" * 80)
        print("🔍 DEBUG: ")
        print("=" * 80)
        print(f"📅 : {start_time_str} ~ {end_time_str}")
        print(f"📂 : {date_str}")
        print(f"📊 KPI: {len(TARGET_KPIS)}")
        print("⚙️  :")
        print(f"   - : {stable_window_size}")
        print(f"   - : {min_stable_window_size}")
        print(f"   - : {recovery_window_size}")
        print(f"   - : {anomaly_window_min}-{anomaly_window_max}")
        print(f"   - : {stable_std_threshold}")
        print(f"   - : {recovery_std_threshold}")
        print(f"   - : {jump_threshold_factor}")
        print(f"   - : {noise_reduction_w}")
        print(f"   - : {cluster_minutes_k}")
        print(f"   - : {max_clusters_nc}")
        print(f"   - : {final_filter_x}")

    tz = pytz.timezone("Asia/Shanghai")
    diag_start_time = tz.localize(
        datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    )
    diag_end_time = tz.localize(datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S"))

    extended_start_time = diag_start_time - timedelta(minutes=5)
    extended_end_time = diag_end_time + timedelta(minutes=5)

    if debug:
        print("\n⏰ :")
        print(f"   - : {diag_start_time} ~ {diag_end_time}")
        print(f"   - : {extended_start_time} ~ {extended_end_time}")
        print("   - : 15")

    metric_path = os.path.join(
        data_source_path, "telemetry", date_str, "metric", "metric_container.csv"
    )
    if debug:
        print(f"\n📁 : {metric_path}")

    if not os.path.exists(metric_path):
        if debug:
            print("❌ !")
        raise FileNotFoundError(f"Data file not found: {metric_path}")

    if debug:
        print("📖 ...")

    df = pd.read_csv(metric_path)
    original_rows = len(df)

    if debug:
        print(f"   - : {original_rows}")
        print(f"   - KPI: {df['kpi_name'].nunique()}")
        print(f"   - : {df['cmdb_id'].nunique()}")

    df = df[df["kpi_name"].isin(TARGET_KPIS)]
    filtered_rows = len(df)

    if debug:
        print(
            f"   - KPI: {filtered_rows} ( {original_rows - filtered_rows} )"
        )

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.tz_convert(
        tz
    )

    df = df[
        (df["timestamp"] >= extended_start_time)
        & (df["timestamp"] <= extended_end_time)
    ]
    time_filtered_rows = len(df)

    if debug:
        print(
            f"   - : {time_filtered_rows} ( {filtered_rows - time_filtered_rows} )"
        )
        if time_filtered_rows > 0:
            print(f"   - : {df['timestamp'].min()} ~ {df['timestamp'].max()}")
            print(f"   - KPI: {df['kpi_name'].nunique()}")
            print(f"   - : {df['cmdb_id'].nunique()}")

    if df.empty:
        if debug:
            print("⚠️  ,")
        return []

    all_anomalies = []

    if debug:
        print(f"\n🔄  {len(TARGET_KPIS)} KPI...")

    for kpi_idx, kpi in enumerate(TARGET_KPIS, 1):
        if debug:
            print(f"\n📊 KPI [{kpi_idx}/{len(TARGET_KPIS)}]: {kpi}")

        kpi_df = df[df["kpi_name"] == kpi]
        if kpi_df.empty:
            if debug:
                print("   ⚠️  KPI,")
            continue

        if debug:
            print(f"   - : {len(kpi_df)}")
            print(f"   - : {kpi_df['cmdb_id'].nunique()}")
            print(
                f"   - : {kpi_df['timestamp'].min()} ~ {kpi_df['timestamp'].max()}"
            )

        # FutureWarning: DataFrame.fillna with 'method' is deprecated and will raise in a future version. Use obj.ffill() or obj.bfill() instead.
        pivot_df = (
            kpi_df.pivot_table(index="timestamp", columns="cmdb_id", values="value")
            .resample("1min")
            .mean()
        )
        # pivot_df = pivot_df.interpolate(method='time').fillna(method='ffill').fillna(method='bfill')
        pivot_df = pivot_df.interpolate(method="time").ffill().bfill()

        # datetime
        if not isinstance(pivot_df.index, pd.DatetimeIndex):
            pivot_df.index = pd.to_datetime(pivot_df.index)

        if debug:
            print(f"   - : {pivot_df.shape}")
            print(f"   - : {len(pivot_df)}")
            print(f"   - : {len(pivot_df.columns)}")
            print(f"   - : {type(pivot_df.index)}")

        if pivot_df.empty:
            if debug:
                print("   ⚠️  ,")
            continue

        # Normalization
        min_val, max_val = pivot_df.min().min(), pivot_df.max().max()
        if debug:
            print(f"   - : {min_val:.2f} ~ {max_val:.2f}")

        if max_val == min_val:
            norm_df = pivot_df * 0  # DataFrame,0
            if debug:
                print("   - : ,0")
        else:
            norm_df = (pivot_df - min_val) / (max_val - min_val) * 100
            if debug:
                print("   - : 0-100")
                print(
                    f"   - : {norm_df.min().min():.2f} ~ {norm_df.max().max():.2f}"
                )

        # DataFramedatetime
        if not isinstance(norm_df.index, pd.DatetimeIndex):
            norm_df.index = pivot_df.index

        kpi_anomalies = []

        # 
        try:
            diag_norm_df = norm_df[
                (norm_df.index >= diag_start_time) & (norm_df.index <= diag_end_time)
            ]
        except TypeError as e:
            if debug:
                print(f"   ⚠️  : {e}")
                print(f"   - : {type(norm_df.index)}")
                print(f"   - : {type(diag_start_time)}")
            # datetime
            norm_df.index = pd.to_datetime(norm_df.index)
            diag_norm_df = norm_df[
                (norm_df.index >= diag_start_time) & (norm_df.index <= diag_end_time)
            ]
        if diag_norm_df.empty:
            if debug:
                print("   ⚠️  ,")
            continue

        sorted_components = diag_norm_df.max().sort_values(ascending=False).index

        if debug:
            print(f"   - : {diag_norm_df.shape}")
            print(f"   - : {len(sorted_components)}")
            print(
                f"   - 5: {diag_norm_df.max().sort_values(ascending=False).head().to_dict()}"
            )

        for comp_idx, cmdb_id in enumerate(sorted_components, 1):
            if debug and comp_idx <= 3:  # 3
                print(
                    f"     🔍  [{comp_idx}/{len(sorted_components)}]: {cmdb_id}"
                )

            series = norm_df[cmdb_id].dropna()
            effective_min_stable_window_size = max(
                1, min(min_stable_window_size, stable_window_size)
            )
            min_required_length = (
                effective_min_stable_window_size
                + anomaly_window_min
                + recovery_window_size
            )

            if debug and comp_idx <= 3:
                print(f"       - : {len(series)}")
                print(f"       - : {min_required_length}")

            if len(series) < min_required_length:
                if debug and comp_idx <= 3:
                    print(
                        f"       ⚠️  , ( {min_required_length} )"
                    )
                continue

            component_events = []
            processed_indices = set()

            diag_series = series[
                (series.index >= diag_start_time) & (series.index <= diag_end_time)
            ]
            sorted_points = diag_series.sort_values(ascending=False)

            if debug and comp_idx <= 3:
                print(f"       - : {len(diag_series)}")
                print(f"       - 5: {sorted_points.head().to_dict()}")

            for peak_idx_in_loop, (peak_time, peak_value) in enumerate(
                sorted_points.items()
            ):
                if peak_time in processed_indices or len(component_events) >= 2:
                    break

                if (
                    debug and comp_idx <= 3 and peak_idx_in_loop == 0
                ):  # 
                    print(f"       🎯 : ={peak_time}, ={peak_value:.2f}")

                peak_idx = series.index.get_loc(peak_time)

                for anom_len in range(anomaly_window_min, anomaly_window_max + 1):
                    for offset in range(anom_len):
                        start_idx = peak_idx - offset
                        end_idx = start_idx + anom_len - 1

                        if start_idx < 0 or end_idx >= len(series):
                            continue

                        anomaly_start_time = series.index[start_idx]
                        anomaly_end_time = series.index[end_idx]

                        if not (
                            diag_start_time <= anomaly_start_time <= diag_end_time
                            and diag_start_time <= anomaly_end_time <= diag_end_time
                        ):
                            continue

                        # Stable phase
                        stable_end_idx = start_idx - 1
                        available_stable_points = stable_end_idx + 1
                        current_stable_window_size = min(
                            stable_window_size, available_stable_points
                        )
                        if current_stable_window_size < effective_min_stable_window_size:
                            continue
                        stable_start_idx = stable_end_idx - current_stable_window_size + 1

                        stable_series = series.iloc[
                            stable_start_idx : stable_end_idx + 1
                        ]
                        if len(stable_series) != current_stable_window_size:
                            continue

                        stable_std = stable_series.std()
                        if stable_std > stable_std_threshold:
                            continue

                        # Recovery phase
                        recovery_start_idx = end_idx + 1
                        recovery_end_idx = recovery_start_idx + recovery_window_size - 1
                        if recovery_end_idx >= len(series):
                            continue

                        recovery_series = series.iloc[
                            recovery_start_idx : recovery_end_idx + 1
                        ]
                        if len(recovery_series) != recovery_window_size:
                            continue
                        if recovery_series.std() > recovery_std_threshold:
                            continue

                        # Sudden jump
                        jump = series.iloc[start_idx] - stable_series.iloc[-1]
                        if jump <= jump_threshold_factor * (
                            stable_std if stable_std > 0 else 1
                        ):
                            continue

                        # Event found
                        stable_mean = stable_series.mean()
                        anomaly_series = series.iloc[start_idx : end_idx + 1]
                        actual_peak_val = anomaly_series.max()
                        delta = actual_peak_val - stable_mean

                        # ()
                        # pivot_df
                        original_stable_series = pivot_df[cmdb_id].iloc[
                            stable_start_idx : stable_end_idx + 1
                        ]
                        original_anomaly_series = pivot_df[cmdb_id].iloc[
                            start_idx : end_idx + 1
                        ]
                        original_stable_mean = original_stable_series.mean()
                        original_actual_peak_val = original_anomaly_series.max()

                        if delta > 0:
                            event = {
                                'data_source': 'Metric',
                                'timestamp': anomaly_start_time,
                                'cmdb_id': cmdb_id,
                                'kpi_name': kpi,
                                'delta': delta,  # delta
                                'peak_value': original_actual_peak_val,  # 
                                'baseline_value': original_stable_mean,  # 
                                'normalized_peak_value': actual_peak_val,  # 
                                'normalized_baseline_value': stable_mean,  # 
                            }
                            component_events.append(event)
                            for i in range(stable_start_idx, recovery_end_idx + 1):
                                processed_indices.add(series.index[i])
                            break  # Move to next peak
                    if peak_time in processed_indices:
                        break

            kpi_anomalies.extend(component_events)

        # Noise reduction per metric
        if not kpi_anomalies:
            if debug:
                print("   ❌ KPI")
            continue

        if debug:
            print(f"   ✅  {len(kpi_anomalies)} ")
            print(
                f"   📈 delta: {min(e['delta'] for e in kpi_anomalies):.2f} ~ {max(e['delta'] for e in kpi_anomalies):.2f}"
            )

        max_delta = max(event["delta"] for event in kpi_anomalies)
        noise_threshold = noise_reduction_w * max_delta
        denoised_anomalies = [
            event for event in kpi_anomalies if event["delta"] >= noise_threshold
        ]

        if debug:
            print(
                f"   🔧 : ={noise_threshold:.2f},  {len(denoised_anomalies)}/{len(kpi_anomalies)} "
            )

        # Clustering
        if not denoised_anomalies:
            if debug:
                print("   ⚠️  ")
            continue

        denoised_anomalies.sort(key=lambda x: x["timestamp"])
        clusters = []
        if denoised_anomalies:
            current_cluster = [denoised_anomalies[0]]
            for i in range(1, len(denoised_anomalies)):
                time_diff = (
                    denoised_anomalies[i]["timestamp"]
                    - current_cluster[-1]["timestamp"]
                )
                if time_diff <= timedelta(minutes=cluster_minutes_k):
                    current_cluster.append(denoised_anomalies[i])
                else:
                    clusters.append(current_cluster)
                    current_cluster = [denoised_anomalies[i]]
            clusters.append(current_cluster)

        if debug:
            print(f"   🔗 : {len(clusters)} ")
            for cluster_idx, cluster in enumerate(clusters, 1):
                print(
                    f"     {cluster_idx}: {len(cluster)}, : {cluster[0]['timestamp']} ~ {cluster[-1]['timestamp']}"
                )

        if 1 <= len(clusters) <= max_clusters_nc:
            all_anomalies.extend(denoised_anomalies)
            if debug:
                print(
                    f"   ✅ , {len(denoised_anomalies)} "
                )
        else:
            if debug:
                print(
                    f"   ❌  {len(clusters)}  (1-{max_clusters_nc}),KPI"
                )

    # Final filtering
    if debug:
        print("\n🎯 ")
        print(f"   - KPI: {len(all_anomalies)}")

    if not all_anomalies:
        if debug:
            print("   ❌ ,")
        return []

    overall_max_delta = max(event["delta"] for event in all_anomalies)
    final_threshold = final_filter_x * overall_max_delta
    final_anomalies = [
        event for event in all_anomalies if event["delta"] >= final_threshold
    ]

    if debug:
        print(f"   - delta: {overall_max_delta:.2f}")
        print(f"   - : {final_threshold:.2f}")
        print(f"   - : {len(final_anomalies)}")

    # Sort and format
    final_anomalies.sort(key=lambda x: x["delta"], reverse=True)

    if debug:
        print("\n📋  (10):")
        for i, event in enumerate(final_anomalies[:10], 1):
            print(f"   {i}. {event['cmdb_id']} - {event['kpi_name']}")
            print(f"      : {event['timestamp']}, Delta: {event['delta']:.2f}")

    output_events = []
    for event in final_anomalies[:10]:
        # NORMALIZED_KPIS
        if event['kpi_name'] in NORMALIZED_KPIS:
            peak_val = event['normalized_peak_value']
            baseline_val = event['normalized_baseline_value']
        else:
            peak_val = event['peak_value']
            baseline_val = event['baseline_value']
        
        output_events.append({
            'data_source': event['data_source'],
            'timestamp': event['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            'cmdb_id': event['cmdb_id'],
            'description': f"Spike alert: {event['kpi_name']} rose from baseline {baseline_val:.2f} to {peak_val:.2f} (delta={event['delta']:.2f})"

        })

    if debug:
        print(f"\n✅ , {len(output_events)} ")
        print("=" * 80)

    return output_events


if __name__ == "__main__":
    # start_time = "2021-03-23 00:00:00"
    # end_time = "2021-03-23 00:30:00"
    # date_str = "2021_03_23"
    start_time = "2021-03-10 16:30:00"
    end_time = "2021-03-10 17:00:00"
    date_str = "2021_03_10"

    # Use the invoke method instead of direct call to avoid LangChain tool wrapper issues
    anomaly_events = find_metric_anomalies_bank.invoke(
        {
            "start_time_str": start_time,
            "end_time_str": end_time,
            "date_str": date_str,
            "stable_std_threshold": 10.0,
            "recovery_std_threshold": 25.0,
            "jump_threshold_factor": 3.0,
            "noise_reduction_w": 0.4,
            "cluster_minutes_k": 3,
            "max_clusters_nc": 3,
            "final_filter_x": 0.2,
        }
    )
    for e in anomaly_events:
        print(e)
    # print(anomaly_events)
