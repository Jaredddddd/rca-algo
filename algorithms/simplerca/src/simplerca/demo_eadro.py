import os
import json
import pandas as pd
import re
import numpy as np
from collections import Counter
from typing import Dict, Tuple, List

# 读取groundtruth数据
def load_groundtruth(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    groundtruth = []
    for case in data["faults"]:
        if "SN" in file_path:
            groundtruth.append({
                "pod": "-".join(case["name"].split('-')[1:-1]),
                "type": case["fault"],
                "start_time": case["start"],
                "duration": int(case["duration"])
            })
        elif "TT" in file_path:
            groundtruth.append({
                "pod": case["name"].split('_')[1],
                "type": case["fault"],
                "start_time": case["start"],
                "duration": int(case["duration"])
            })
    return groundtruth


##读取每一个pod中所需的metric数据
def load_pod_metrics(base_dir, date):
    """
    Load pod metrics from csv files under Eadro/SN Dataset/SN Dataset/data/{date}/metrics/

    :param base_dir: Base directory, e.g., 'Eadro/SN Dataset/SN Dataset/data'
    :param date: e.g., 'SN.2022-04-17T181245D2022-04-17T183616'
    :return: Dict mapping pod_name -> DataFrame
    """

    metric_dir = os.path.join(base_dir, date, "metrics")
    pod_metric_dict = {}

    for fname in os.listdir(metric_dir):
        if fname.endswith('.csv'):
            fpath = os.path.join(metric_dir, fname)
            try:
                df = pd.read_csv(fpath)
                df['parsed_time'] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
                df['rx/tx'] = np.where(df['tx_bytes'] == 0, 0, df['rx_bytes'] / df['tx_bytes'])
                if df['parsed_time'].isnull().all():
                    print(f"No valid timestamps for {fname}")
                    continue
                pod_name = fname.split('.')[0]  # Extract the pod name
                pod_metric_dict[pod_name] = df
            except Exception as e:
                print(f"Failed to load {fname}: {e}")
    
    return pod_metric_dict


def detect_anomalies_rules(pod_metrics: dict, target_timestamp, duration,ns='SN'):
    anomalies = []
    
    # 定义检测指标及其判定规则
    if ns == 'SN':
        METRIC_RULES = {
            "cpu_usage_total": lambda x: x > 8,             # CPU总使用率超过8
            "rx/tx": lambda x: 5 < x < 30                   # 网络收发量在(5, 30)区间外
        }
    elif ns == 'TT':
        METRIC_RULES = {
            "cpu_usage_total": lambda x: x > 8,             # CPU总使用率超过8
            "rx/tx": lambda x: 8 < x < 30                   # 网络收发量在(5, 30)区间外
        }
    
    for pod_name, df in pod_metrics.items():
        # 计算时间窗口：[target_timestamp, target_timestamp + duration]
        if ns == 'SN':
            start_time = pd.to_datetime(target_timestamp, unit="s", utc=True)-pd.Timedelta(seconds=6)
        elif ns == 'TT':
            start_time = pd.to_datetime(target_timestamp, unit="s", utc=True)-pd.Timedelta(seconds=1)   
        end_time = start_time + pd.Timedelta(seconds=duration)
        
        # 筛选时间窗口内的数据
        time_window_data = df[(df["parsed_time"] >= start_time) & 
                             (df["parsed_time"] <= end_time)]
        
        if time_window_data.empty:
            print(f"No data for pod {pod_name} in the time window {start_time} to {end_time}")
            continue
            
        # 初始化每个指标的异常计数
        event_counts = {metric: 0 for metric in METRIC_RULES}
        
        # 遍历时间窗口内的每个时间点
        for _, row in time_window_data.iterrows():
            # 检查每个指标是否满足异常条件
            for metric, rule in METRIC_RULES.items():
                if metric not in row:
                    continue
                    
                if rule(row[metric]):
                    event_counts[metric] += 1
                
        # 汇总所有指标的异常次数
        total_events = sum(event_counts.values())
        
        # 如果有异常事件，记录该Pod的异常统计信息
        if total_events > 0:
            anomalies.append({
                "pod": pod_name,
                "event_counts": event_counts,
                "total_events": total_events,
            })
    rc = anomalies
    if len(anomalies) > 1:
        rc = [max(anomalies, key=lambda x: x["total_events"])]

    return rc,anomalies



def SLI_filter(pod_metric_dict, case):
    """
    过滤无效的故障注入：检查指定时间段内rx_bytes和tx_bytes是否有80%以上的值为0
    
    参数:
    - pod_metric_dict: 包含所有Pod监控数据的字典，格式为 {pod_name: dataframe}
    - case: 包含故障信息的字典，需包含 'pod', 'start_time', 'duration' 字段
    
    返回:
    - 如果rx_bytes或tx_bytes有80%以上的值为0，返回 {"valid": False, "reason": "无效注入原因"}
    - 否则返回 {"valid": True}
    """
    filter=False
    try:
        # 解析时间参数
        target_time = case['start_time']
        duration = int(case['duration'])
        start_time = pd.to_datetime(target_time, unit="s", utc=True)
        end_time = start_time + pd.Timedelta(seconds=duration)
        
        # 获取目标Pod的数据
        pod_name = case['pod']
        if pod_name not in pod_metric_dict:
            return {"valid": False, "reason": f"Pod '{pod_name}' 不存在于监控数据中"}
        
        target_pod_df = pod_metric_dict[pod_name]
            
        time_window_df = target_pod_df[
            (target_pod_df['parsed_time'] >= start_time) &
            (target_pod_df['parsed_time'] <= end_time)
        ]
        
        # 检查时间窗口是否有数据
        if time_window_df.empty:
            return {"valid": False, "reason": f"Pod '{pod_name}' 在指定时间段内没有数据"}
        
        # 计算rx_bytes和tx_bytes中0值的比例
        rx_zero_ratio = (time_window_df['rx_bytes'] == 0).mean()
        tx_zero_ratio = (time_window_df['tx_bytes'] == 0).mean()
        
        # 判断是否为无效注入（90%以上为0）
        if rx_zero_ratio >= 0.9 and tx_zero_ratio >= 0.9:
            filter = True
        return filter    
    except Exception as e:
        return {"valid": False, "reason": f"处理Pod '{pod_name}' 时发生错误: {str(e)}"}
    
    


# 评估rca的准确率
def evaluate(base_dir=r'Eadro/SN Dataset/SN Dataset/data', date='SN.2022-04-17T181245D2022-04-17T183616', ns='SN'):
    true_positives = 0
    filter_cases=0
    success = []

    # 读取groundtruth数据
    gt_name=date[0:3]+'fault-'+date[3:]+'.json'
    gt_dir= os.path.join(base_dir, gt_name)
    groundtruth = load_groundtruth(gt_dir)
    total_cases = len(groundtruth)
    print(f"Total cases: {total_cases}")

    #读取metric数据
    pod_metric_dict=load_pod_metrics(base_dir, date)

    for idx,case in enumerate(groundtruth):

        # 检查是否需要过滤
        if 'network' in case['type']:
            filter_result = SLI_filter(pod_metric_dict, case)
            if filter_result:
                filter_cases += 1
                print(f"Filtered case {idx+1}: {case} | Reason: 无效注入")
                continue

        target_time = case['start_time']
        if target_time is None:
            continue
        duration = int(case['duration'])
        # metric RCA
        metric_rc, anomalies = detect_anomalies_rules(pod_metric_dict, target_time, duration,ns=ns)
        if not metric_rc:
            print(f"No anomalies detected for case {idx+1}: {case}")
            continue
        if metric_rc[0]['pod']==case['pod']:
            true_positives += 1
            success.append(idx)
        if case['pod']=='nginx-thrift':
            if 'nginx' in metric_rc[0]['pod']:
                true_positives += 1
                success.append(idx)
        if idx not in success:
            print(f"Failed to detect case {idx+1}: {case} | Detected: {anomalies}")
    
    accuracy = true_positives / (total_cases-filter_cases) if total_cases > 0 else 0
    print(f"Detection Accuracy: {accuracy * 100:.2f}%")
    print(f"True Positives: {true_positives}, Cases: {total_cases}, Filtered Cases: {filter_cases}")
    return true_positives, total_cases, filter_cases

# 主函数
def main(ns='SN'):
    base_dir= rf'/mnt/jfs/Eadro/{ns}_Dataset/{ns}_Dataset/data'
    total_cases = 0
    true_positives = 0
    filter_cases = 0
    date = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    for i,d in enumerate(date):
        print(f"Evaluating folder: {d}")
        tp, tc, fc = evaluate(base_dir= base_dir,date=d,ns=ns)
        total_cases += tc
        true_positives += tp
        filter_cases += fc
    accuracy = true_positives / (total_cases-filter_cases) if total_cases > 0 else 0
    print(f"Overall Detection Accuracy: {accuracy * 100:.2f}%")
    print(f"Total True Positives: {true_positives}, Total Cases: {total_cases}, Filtered Cases: {filter_cases}")


if __name__ == '__main__':
    ns= 'TT'  # Change to 'TT' for TT Dataset
    main(ns=ns)







    