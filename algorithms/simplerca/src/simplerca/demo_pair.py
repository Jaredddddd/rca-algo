import marimo

__generated_with = "0.13.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import re
    from collections import Counter

    import marimo as mo
    import pandas as pd

    mo.md("# Log根因分析工具")

    # 定义关键字
    ERROR_KWS = ["error", "fail", "exception", "timeout", "refused"]

    # 编译正则模式，忽略大小写
    error_pattern = re.compile(r"|".join(ERROR_KWS), re.IGNORECASE)

    def parse_log_line(log_json_str, ns="hipster"):
        try:
            try:
                # 优先：标准双层 JSON 格式
                inner = json.loads(json.loads(log_json_str)["log"])
                msg = inner.get("message", "")
            except:
                # 降级处理：直接从 log_json_str 中提取 log 字段
                msg = json.loads(log_json_str).get("log", "")

            if ns == "hipster":
                # 提取 SpanID 后的 log_event
                pattern = r"SpanID:\s*([a-zA-Z0-9]+)\s+(.*)$"
                match = re.search(pattern, msg)
                if match:
                    return match.group(2).strip()
                return ""

            return msg.strip()

        except:
            return ""

    # 处理日志文件，返回 dataframe
    def process_log_csv(file_path, ns="hipster"):
        df = pd.read_csv(file_path, engine="c", on_bad_lines="skip")
        df[["log_event"]] = (
            df["Log"].apply(lambda x: parse_log_line(x, ns=ns)).apply(pd.Series)
        )
        return df[["Timestamp", "PodName", "TraceID", "SpanID", "log_event"]]

    def detect_root_pod(ab_df, ns):
        def has_kw(msg):
            return bool(error_pattern.search(msg))  # 匹配任意一个关键词

        ab_df["has_kw"] = ab_df["log_event"].apply(has_kw)
        pod_count = (
            ab_df[ab_df["has_kw"]]
            .groupby("PodName")
            .size()
            .sort_values(ascending=False)
        )

        if not pod_count.empty:
            # Remove frontend pod if there are multiple pods with errors
            if len(pod_count) >= 2 and ns == "hipster":
                pod_count = pod_count[pod_count.index != "frontend-579b9bff58-t2dbm"]
            return pod_count.index[0]
        return None

    # 找出根因事件（最常见的 fail msg）对应的根因event
    def get_top_fail_event(df, root_pod, ns):
        pod_df = df[(df["PodName"] == root_pod)]
        fail_msgs = [
            msg
            for msg in pod_df["log_event"]
            if any(kw in msg.lower() for kw in ERROR_KWS)
        ]
        counter = Counter(fail_msgs)
        if len(counter) >= 2 and ns == "hipster":
            del counter["Request error"]

        return counter.most_common(1)[0][0] if counter else "unknown"

    # 主函数：输入正常日志文件、异常日志文件
    def rca_on_logs(
        abnormal_csv, ns="hipster", normal_csv=None, trace_data=None, cause=None
    ):
        ab_df = process_log_csv(abnormal_csv, ns)

        # If normal log is provided, check for log changes (only for 2023-01-29)
        if normal_csv and ns == "ts":
            try:
                normal_df = process_log_csv(normal_csv, ns)

                # Add OperationName filtering based on trace data
                def filter_logs_by_operation_intersection(normal_df, ab_df):
                    """Filter logs to keep only SpanIDs with OperationName that exist in both normal and abnormal traces"""
                    try:
                        if trace_data is None:
                            return normal_df, ab_df

                        normal_trace_df, abnormal_trace_df = trace_data

                        # Get OperationName mappings
                        normal_spanid_to_operation = dict(
                            zip(
                                normal_trace_df["SpanID"],
                                normal_trace_df["OperationName"],
                            )
                        )
                        abnormal_spanid_to_operation = dict(
                            zip(
                                abnormal_trace_df["SpanID"],
                                abnormal_trace_df["OperationName"],
                            )
                        )

                        # Add OperationName to log dataframes
                        normal_df["OperationName"] = normal_df["SpanID"].map(
                            normal_spanid_to_operation
                        )
                        ab_df["OperationName"] = ab_df["SpanID"].map(
                            abnormal_spanid_to_operation
                        )

                        # Get intersection of OperationNames from trace data
                        normal_operations = set(
                            normal_trace_df["OperationName"].dropna()
                        )
                        abnormal_operations = set(
                            abnormal_trace_df["OperationName"].dropna()
                        )
                        common_operations = normal_operations & abnormal_operations

                        if common_operations:
                            # Filter to keep only common OperationNames
                            normal_df = normal_df[
                                normal_df["OperationName"].isin(common_operations)
                            ]
                            ab_df = ab_df[
                                ab_df["OperationName"].isin(common_operations)
                            ]
                            print(
                                f"Filtered to {len(common_operations)} common OperationNames"
                            )
                        else:
                            print(
                                "No common OperationNames found, keeping original data"
                            )

                        return normal_df, ab_df
                    except Exception as e:
                        print(f"Error in OperationName filtering: {e}")
                        return normal_df, ab_df

                # Apply OperationName filtering
                normal_df, ab_df = filter_logs_by_operation_intersection(
                    normal_df, ab_df
                )

                # Module 1: Error log ratio increase detection
                def detect_error_ratio_increase():
                    # Count error logs per pod
                    def count_error_logs(df):
                        df["has_error"] = df["log_event"].apply(
                            lambda msg: bool(error_pattern.search(msg))
                        )
                        error_counts = df[df["has_error"]].groupby("PodName").size()
                        total_counts = df.groupby("PodName").size()
                        return error_counts, total_counts

                    normal_error_counts, normal_total_counts = count_error_logs(
                        normal_df
                    )
                    abnormal_error_counts, abnormal_total_counts = count_error_logs(
                        ab_df
                    )

                    error_ratio_changes = []
                    for pod in set(normal_total_counts.index) | set(
                        abnormal_total_counts.index
                    ):
                        normal_errors = normal_error_counts.get(pod, 0)
                        normal_total = normal_total_counts.get(pod, 1)
                        abnormal_errors = abnormal_error_counts.get(pod, 0)
                        abnormal_total = abnormal_total_counts.get(pod, 1)

                        normal_ratio = (
                            normal_errors / normal_total if normal_total > 0 else 0
                        )
                        abnormal_ratio = (
                            abnormal_errors / abnormal_total
                            if abnormal_total > 0
                            else 0
                        )

                        # Detect significant error ratio increase
                        if (
                            abnormal_ratio > normal_ratio * 1.5
                            and abnormal_errors > 0
                            and abnormal_total > 10
                        ):
                            error_ratio_changes.append(
                                (pod, abnormal_ratio - normal_ratio)
                            )

                    # Return top pods with highest error ratio increase
                    if error_ratio_changes:
                        error_ratio_changes.sort(key=lambda x: x[1], reverse=True)
                        return [pod for pod, _ in error_ratio_changes[:5]]
                    return []

                # Module 2: Log count reduction detection (now includes error filtering)
                def detect_count_reduction():
                    # First filter out error spans from both normal and abnormal data
                    def filter_error_spans(df):
                        """Remove spans that contain error keywords"""
                        df_filtered = df[
                            ~df["log_event"].apply(
                                lambda msg: bool(error_pattern.search(msg))
                            )
                        ].copy()
                        return df_filtered

                    # Filter both datasets to remove error spans for fair comparison
                    normal_df_clean = filter_error_spans(normal_df)
                    ab_df_clean = filter_error_spans(ab_df)

                    normal_counts = normal_df_clean.groupby("PodName").size()
                    abnormal_counts = ab_df_clean.groupby("PodName").size()

                    count_reductions = []

                    # Pod-level count reduction detection (comparing clean normal vs clean abnormal)
                    for pod in normal_counts.index:
                        normal_count = normal_counts.get(pod, 0)
                        abnormal_count = abnormal_counts.get(pod, 0)

                        # If log count drops significantly (>40% reduction)
                        if (
                            normal_count > 0
                            and abnormal_count < normal_count * 0.6
                            and normal_count > 40
                        ):
                            reduction_ratio = (
                                normal_count - abnormal_count
                            ) / normal_count
                            count_reductions.append((pod, reduction_ratio))

                    if count_reductions:
                        count_reductions.sort(key=lambda x: x[1], reverse=True)
                        return [pod for pod, _ in count_reductions[:5]]

                    # SpanID-based anomaly detection (using clean data for both)
                    def detect_operation_anomalies_emd_asymmetric():
                        import numpy as np
                        from scipy.stats import wasserstein_distance

                        anomalies = []
                        # Use filtered normal data for comparison
                        if "OperationName" not in normal_df_clean.columns:
                            print(
                                "Warning: 'OperationName' not found in normal_df_clean. Skipping analysis."
                            )
                            return []

                        normal_op_groups = normal_df_clean.groupby(
                            ["PodName", "OperationName"]
                        )

                        for (pod_name, op_name), normal_group_df in normal_op_groups:
                            normal_span_counts_for_op = normal_group_df.groupby(
                                "SpanID"
                            ).size()

                            if "OperationName" not in ab_df_clean.columns:
                                ab_span_counts_for_op = pd.Series(dtype="int")
                            else:
                                abnormal_group_df = ab_df_clean[
                                    (ab_df_clean["PodName"] == pod_name)
                                    & (ab_df_clean["OperationName"] == op_name)
                                ]
                                if abnormal_group_df.empty:
                                    ab_span_counts_for_op = pd.Series(dtype="int")
                                else:
                                    ab_span_counts_for_op = abnormal_group_df.groupby(
                                        "SpanID"
                                    ).size()

                            if normal_span_counts_for_op.empty:
                                continue

                            aligned_normal, aligned_abnormal = (
                                normal_span_counts_for_op.align(
                                    ab_span_counts_for_op, fill_value=0
                                )
                            )

                            penalized_abnormal = pd.Series(
                                np.minimum(aligned_normal, aligned_abnormal),
                                index=aligned_normal.index,
                            )

                            emd_value = wasserstein_distance(
                                aligned_normal.values, penalized_abnormal.values
                            )

                            normal_mean = aligned_normal.mean()
                            if normal_mean == 0:
                                continue

                            normalized_emd = emd_value / normal_mean

                            if normalized_emd > 0.2:
                                anomalies.append((pod_name, normalized_emd))

                        anomalies.sort(key=lambda x: x[1], reverse=True)
                        return anomalies

                    spanid_anomalies = detect_operation_anomalies_emd_asymmetric()

                    if spanid_anomalies:
                        spanid_anomalies.sort(key=lambda x: x[1], reverse=True)
                        spanid_pods = [pod for pod, _ in spanid_anomalies[:5]]

                        # Add pod-level reductions that aren't already detected
                        count_reductions.sort(key=lambda x: x[1], reverse=True)
                        for pod, _ in count_reductions:
                            if pod not in spanid_pods and len(spanid_pods) < 5:
                                spanid_pods.append(pod)

                        return spanid_pods

                    return []

                # Choose detection method based on cause parameter
                if cause == "return":
                    # For return type faults, use error-based detection
                    error_pods = detect_error_ratio_increase()
                    if error_pods:
                        return error_pods
                else:
                    # For other fault types, use count reduction detection
                    count_pods = detect_count_reduction()
                    if count_pods:
                        return count_pods

            except Exception as e:
                print(f"Error processing normal logs: {e}")

        # Fallback to original error detection
        ab_df["has_kw"] = ab_df["log_event"].apply(
            lambda msg: bool(error_pattern.search(msg))
        )
        pod_count = (
            ab_df[ab_df["has_kw"]]
            .groupby("PodName")
            .size()
            .sort_values(ascending=False)
        )

        if not pod_count.empty:
            # Remove frontend pod if there are multiple pods with errors
            if len(pod_count) >= 2 and ns == "hipster":
                pod_count = pod_count[pod_count.index != "frontend-579b9bff58-t2dbm"]
            return pod_count.index.tolist()[:5]
        return None

    return json, mo, pd, rca_on_logs, re


@app.cell
def _(mo, pd):
    import statistics

    import numpy as np

    mo.md("# Trace根因分析工具")

    def get_latency_metric(trace_file, pod_name):
        latency_list = []
        if "front" in pod_name:
            return 10, 10

        try:
            pod_reader = pd.read_csv(
                trace_file,
                index_col="PodName",
                usecols=["TraceID", "SpanID", "ParentID", "PodName", "EndTimeUnixNano"],
            )
            parent_span_reader = pd.read_csv(
                trace_file,
                index_col="SpanID",
                usecols=["TraceID", "SpanID", "ParentID", "PodName", "EndTimeUnixNano"],
            )
        except Exception as e:
            print(f"Error reading file {trace_file}: {e}")
            return 10, 10

        try:
            pod_spans = pod_reader.loc[
                [pod_name], ["SpanID", "ParentID", "EndTimeUnixNano"]
            ]
        except:
            print(f"Pod {pod_name} not found in {trace_file}")
            return 10, 10

        for span_index in range(len(pod_spans["SpanID"])):
            parent_id = pod_spans["ParentID"].iloc[span_index]
            pod_start_time = int(pod_spans["EndTimeUnixNano"].iloc[span_index])

            try:
                parent_pod_span = parent_span_reader.loc[
                    [parent_id], ["PodName", "EndTimeUnixNano"]
                ]
                for parent_span_index in range(len(parent_pod_span["PodName"])):
                    parent_pod_name = parent_pod_span["PodName"].iloc[parent_span_index]
                    parent_end_time = int(
                        parent_pod_span["EndTimeUnixNano"].iloc[parent_span_index]
                    )

                    if str(parent_pod_name) != str(pod_name):
                        latency = (
                            parent_end_time - pod_start_time
                        ) / 1000000  # Convert to microseconds
                        latency_list.append(latency)
            except:
                continue

        if len(latency_list) > 2:
            return np.percentile(latency_list, 90), statistics.stdev(latency_list)
        else:
            return 1, 1

    def rca_on_trace(trace_file, date=None):
        latency_results = {}
        df = pd.read_csv(trace_file)
        unique_values = df["PodName"].unique()
        for pod_name in unique_values:
            p90_latency, _ = get_latency_metric(trace_file, pod_name)
            latency_results[pod_name] = p90_latency
        result_df = pd.DataFrame(
            list(latency_results.items()), columns=["PodName", "P90_Latency"]
        )
        result_df = result_df[
            result_df["P90_Latency"] > (200 if date == "2023-01-29" else 100)
        ].sort_values("P90_Latency", ascending=False)
        if len(result_df) == 0:
            return []
        return result_df["PodName"].tolist()[:5]

    return (rca_on_trace,)


@app.cell
def _(mo, pd, re):
    import os

    mo.md("# Metric根因分析工具")

    # 正则匹配时间数据
    def parse_time(time_str):
        pattern = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}")
        match = pattern.search(time_str)
        if match:
            return pd.to_datetime(match.group())
        return None

    ##读取每一个pod中所需的metric数据
    def load_pod_metrics(base_dir, date, selected_columns=None):
        """
        Load pod metrics from csv files under Nezha/rca_data/{date}/metric/

        :param base_dir: Base directory, e.g., 'Nezha/rca_data'
        :param date: e.g., '2022-08-22'
        :param selected_columns: List of columns to keep (default = common RCA columns)
        :return: Dict mapping pod_name -> DataFrame
        """
        if selected_columns is None:
            selected_columns = [
                "Time",
                "TimeStamp",
                "PodName",
                "CpuUsageRate(%)",
                "PodClientLatencyP90(s)",
                "PodServerLatencyP90(s)",
                "PodClientLatencyP99(s)",
                "PodServerLatencyP99(s)",
            ]

        metric_dir = os.path.join(base_dir, date, "metric")
        pod_metric_dict = {}

        for fname in os.listdir(metric_dir):
            if fname.endswith(".csv") and "metric" in fname:
                fpath = os.path.join(metric_dir, fname)
                try:
                    df = pd.read_csv(fpath, usecols=lambda x: x in selected_columns)
                    df["parsed_time"] = df["Time"].apply(parse_time)
                    df["Network_Latency"] = (
                        df["PodClientLatencyP99(s)"] - df["PodServerLatencyP99(s)"]
                    ).abs()
                    if df["parsed_time"].isnull().all():
                        print(f"No valid timestamps for {fname}")
                        continue
                    pod_name = df["PodName"].iloc[0]

                    # pod_name = pod_name.split('-')[0]  # Extract the pod name
                    pod_metric_dict[pod_name] = df
                except Exception as e:
                    print(f"Failed to load {fname}: {e}")

        return pod_metric_dict

    def detect_anomalies_p95(
        pod_metrics: dict, target_timestamp, metrics=["CpuUsageRate(%)"]
    ):
        anomalies = []
        # target_minute = parse_time(target_timestamp)

        for pod_name, df in pod_metrics.items():
            row = df[df["parsed_time"] == target_timestamp]
            if row.empty:
                continue

            matched_metrics = []
            metric_values = {}
            thresholds = {}

            for metric in metrics:
                threshold = df[metric].quantile(0.95)
                value = row[metric].values[0]
                if value > 1.19 * threshold and value > 80:
                    matched_metrics.append(metric)
                    metric_values[metric] = value
                    thresholds[metric] = threshold

            if matched_metrics:
                anomalies.append(
                    {
                        "pod": pod_name,
                        "metrics": matched_metrics,
                        "values": metric_values,
                        "thresholds": thresholds,
                        "matched_time": row["parsed_time"].values[0],
                    }
                )

        # Sort by highest anomaly score and return top pods
        if anomalies:
            cpu_metric = "CpuUsageRate(%)"

            def get_anomaly_score(anomaly):
                if cpu_metric in anomaly["metrics"]:
                    v = anomaly["values"].get(cpu_metric, 0)
                    t = anomaly["thresholds"].get(cpu_metric, 1e-8)
                    return v / t if t != 0 else 0
                elif anomaly["metrics"]:
                    metric = anomaly["metrics"][0]
                    v = anomaly["values"].get(metric, 0)
                    t = anomaly["thresholds"].get(metric, 1e-8)
                    return v / t if t != 0 else 0
                return 0

            anomalies.sort(key=get_anomaly_score, reverse=True)
            return [anomaly["pod"] for anomaly in anomalies[:5]]

        return []

    ## 对于输出为多个rc，比较metric value的峰值和threshold的比值
    def filter_top_root_cause_by_priority(root_causes):
        if len(root_causes) < 2:
            return root_causes

        cpu_metric = "CpuUsageRate(%)"

        # Step 1: 筛选含有 CPU 的 root cause
        cpu_causes = [cause for cause in root_causes if cpu_metric in cause["metrics"]]

        # Step 2: 如果存在 CPU，则只比较这些；否则比较 latency
        if cpu_causes:
            key_metric = cpu_metric
            candidates = cpu_causes
        else:
            # 尝试比较 latency（任选第一个 latency 指标）
            if not root_causes[0]["metrics"]:
                return []
            key_metric = root_causes[0]["metrics"][0]  # 假设至少有一个 latency 指标
            candidates = root_causes

        # Step 3: 比较 value / threshold
        def ratio(cause):
            v = cause["values"].get(key_metric, 0)
            t = cause["thresholds"].get(key_metric, 1e-8)
            return v / t if t != 0 else 0

        best_cause = max(candidates, key=ratio)
        return [best_cause]

    return (
        detect_anomalies_p95,
        filter_top_root_cause_by_priority,
        load_pod_metrics,
        os,
        parse_time,
    )


@app.cell
def _(
    detect_anomalies_p95,
    filter_top_root_cause_by_priority,
    json,
    load_pod_metrics,
    mo,
    os,
    parse_time,
    pd,
    rca_on_logs,
    rca_on_trace,
):
    mo.md("# RCA main")

    # 读取groundtruth数据
    def load_groundtruth(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        groundtruth = []
        for key, cases in data.items():
            for case in cases:
                if (
                    case["inject_type"] != "return"
                    or case["inject_type"] != "exception"
                ):
                    groundtruth.append(
                        {
                            "time": case["inject_time"],
                            "pod": case["inject_pod"],
                            "type": case["inject_type"],
                        }
                    )
        return groundtruth

    # 评估异常检测的准确率
    def evaluate(base_dir=r"data/Nezha/rca_data", date="2022-08-22", ns="hipster"):
        ac1, ac3, ac5 = 0, 0, 0
        total_cases = 0

        # 读取groundtruth数据
        gt_dir = rf"data/Nezha/rca_data/{date}/{date}-fault_list.json"
        groundtruth = load_groundtruth(gt_dir)
        total_cases = len(groundtruth)
        print(f"Total cases: {total_cases}")

        # 读取metric数据
        pod_metric_dict = load_pod_metrics(base_dir, date)

        for idx, case in enumerate(groundtruth):
            target_time = parse_time(case["time"]) + pd.Timedelta(minutes=2)
            if target_time is None:
                continue

            predicted_pods = []
            method_used = "none"

            # Load trace data for OperationName filtering (for ts namespace)
            trace_data = None
            if date == "2023-01-29" and ns == "ts":
                try:
                    # Load normal trace data
                    normal_trace_folder = os.path.join(
                        base_dir.replace("rca_data", "construct_data"), date, "trace"
                    )
                    normal_trace_file = os.path.join(
                        normal_trace_folder, "08_50_trace.csv"
                    )

                    # Load abnormal trace data
                    abnormal_trace_folder = os.path.join(base_dir, date, "trace")
                    abnormal_trace_file = os.path.join(
                        abnormal_trace_folder,
                        f"{target_time.hour:02d}_{target_time.minute:02d}_trace.csv",
                    )

                    if os.path.exists(normal_trace_file) and os.path.exists(
                        abnormal_trace_file
                    ):
                        normal_trace_df = pd.read_csv(
                            normal_trace_file, usecols=["SpanID", "OperationName"]
                        )
                        abnormal_trace_df = pd.read_csv(
                            abnormal_trace_file, usecols=["SpanID", "OperationName"]
                        )
                        trace_data = (normal_trace_df, abnormal_trace_df)
                except Exception as e:
                    print(f"Error loading trace data: {e}")

            # metric RCA (highest priority)
            metric_pods = detect_anomalies_p95(pod_metric_dict, target_time)
            if metric_pods:
                predicted_pods = metric_pods
                method_used = "metric"
            else:
                # TraceRCA (medium priority)
                trace_folder = os.path.join(base_dir, date, "trace")
                file_name = f"{target_time.hour:02d}_{target_time.minute:02d}_trace.csv"
                file_path = os.path.join(trace_folder, file_name)
                try:
                    trace_pods = rca_on_trace(file_path, date)
                    if trace_pods:
                        predicted_pods = trace_pods
                        method_used = "trace"
                except:
                    print(f"Error reading trace file {file_path}")

                # logRCA (lowest priority)
                if not predicted_pods:
                    log_folder = os.path.join(base_dir, date, "log")
                    file_name = (
                        f"{target_time.hour:02d}_{target_time.minute:02d}_log.csv"
                    )
                    file_path = os.path.join(log_folder, file_name)

                    normal_log_path = None
                    if date == "2023-01-29":
                        normal_log_folder = os.path.join(
                            base_dir.replace("rca_data", "construct_data"), date, "log"
                        )
                        normal_log_file = "08_50_log.csv"
                        normal_log_path = os.path.join(
                            normal_log_folder, normal_log_file
                        )

                    try:
                        log_pods = rca_on_logs(
                            file_path, ns, normal_log_path, trace_data, case["type"]
                        )
                        if log_pods:
                            predicted_pods = log_pods
                            method_used = "log"
                    except Exception as e:
                        print(f"Error reading log file {file_path} {e}")

            # Calculate AC@k and debug info
            gt_pod = case["pod"]
            rank = -1

            if predicted_pods:
                try:
                    rank = predicted_pods.index(gt_pod) + 1  # 1-based rank
                except ValueError:
                    rank = -1  # Not found

            # Debug output
            print(
                f"Case {idx}: target_time={target_time}, gt_pod={gt_pod}, method={method_used}, rank={rank}"
            )
            print(
                f"  Predicted pods: {predicted_pods[:5] if predicted_pods else 'None'}"
            )

            if predicted_pods and rank != -1:
                if rank <= 1:
                    ac1 += 1
                if rank <= 3:
                    ac3 += 1
                if rank <= 5:
                    ac5 += 1

        # Calculate accuracies
        ac1_rate = ac1 / total_cases if total_cases > 0 else 0
        ac3_rate = ac3 / total_cases if total_cases > 0 else 0
        ac5_rate = ac5 / total_cases if total_cases > 0 else 0

        print("\nFinal Results:")
        print(f"AC@1: {ac1_rate * 100:.2f}% ({ac1}/{total_cases})")
        print(f"AC@3: {ac3_rate * 100:.2f}% ({ac3}/{total_cases})")
        print(f"AC@5: {ac5_rate * 100:.2f}% ({ac5}/{total_cases})")

    # 主函数
    def main():
        date = [ "2023-01-29"]
        ns = ["ts"]
        for i, d in enumerate(date):
            print(f"Evaluating date: {d}")
            evaluate(base_dir=r"data/Nezha/rca_data", date=d, ns=ns[i])


@app.cell
def _(main):
    main()
    return


if __name__ == "__main__":
    app.run()
