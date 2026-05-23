import torch
import typer
import os
from typing import Optional
from torch.utils.data import DataLoader
import pickle
import warnings
from pathlib import Path
import yaml
import pandas as pd
from src.models.diagnosis_tasks.diag_workflow import diag_workflow
from src.models.unified_representation.train import train_model
from src.utils.public_functions import load_samples, hash_init, save_json, save_pkl, load_pkl
from src.preprocess import run_preprocess, DataPreprocessor, DatasetPack, process_case, minmax_tensor, build_groundtruth
import numpy as np


# 过滤特定的 PyTorch 警告
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

app = typer.Typer(help="ART")

@app.command()
def preprocess(
    data_root: str = typer.Option(
        "/mnt/jfs/rcabench-platform-v2/data",
        help="Root directory containing case data",
    ),
    output_dir: str = typer.Option(
        "data/RCABENCH", help="Output directory for processed data"
    ),
    dataset_type: str = typer.Option(
        "RCABENCH_r1", help="Dataset type: RCABENCH_r1, RCABENCH_filtered, or other"
    ),
):
    """Run data preprocessing"""
    typer.echo("Starting data preprocessing...")
    typer.echo(f"Data root: {data_root}")
    typer.echo(f"Output directory: {output_dir}")

    try:
        result = run_preprocess(
            data_root=data_root,
            output_dir=output_dir,
            ds=dataset_type,
        )

        typer.echo("\nPreprocessing completed successfully!")
        typer.echo(
            f"Found {result['num_services']} services and {result['num_metrics']} metrics"
        )

    except Exception as e:
        typer.echo(f"Error during preprocessing: {e}", err=True)
        raise typer.Exit(1)

def load_config(dataset: str, config_dir: str = "config"):
    """加载配置文件"""
    config_path = os.path.join(config_dir, f"{dataset}.yaml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件 {config_path} 不存在")
    return yaml.load(open(config_path, 'r'), Loader=yaml.FullLoader)


@app.command()
def train(
    dataset: str = typer.Option(
        "RCABENCH",
        help="数据集名称: D1, D2 或 RCABENCH",
    ),
    config_dir: str = typer.Option(
        "config", help="配置文件所在目录"
    ),
    output_dir: str = typer.Option(
        None, help="模型输出目录，默认使用 res/[dataset]"
    ),
):
    """训练模型"""
    typer.echo(f"开始训练模型，数据集: {dataset}")
    typer.echo(f"配置文件目录: {config_dir}")
    
    try:
        # 加载配置
        config = load_config(dataset, config_dir)
        # 如果未指定输出目录，使用默认路径
        res_dir = output_dir if output_dir else f'res/{dataset}'
        os.makedirs(res_dir,exist_ok=True)
        model_path = f'{res_dir}/model.pkl'
        
        typer.echo(f"模型将保存至: {model_path}")
        
        # 加载样本
        train_samples, test_samples = load_samples(config['path']['sample_dir'])
        typer.echo(f"加载样本完成，训练样本数: {len(train_samples)}, 测试样本数: {len(test_samples)}")
        
        # 选择训练样本数量
        input_samples = train_samples if config['train_samples_num'] == 'whole' else train_samples[:int(config['train_samples_num'])]
        typer.echo(f"使用 {len(input_samples)} 个样本进行训练")
        
        # 训练或加载模型
        typer.echo("开始训练模型...")
        model = train_model(input_samples, config['model_param'])
        save_pkl(model_path, model)
        typer.echo("模型训练完成并保存")
        
    except Exception as e:
        typer.echo(f"训练过程中发生错误: {e}", err=True)
        raise typer.Exit(1)



@app.command()
def test(
    dataset: str = typer.Option(
        "RCABENCH",
        help="数据集名称: D1, D2 或 RCABENCH",
    ),
    config_dir: str = typer.Option(
        "config", help="配置文件所在目录"
    ),
    model_dir: str = typer.Option(
        None, help="模型所在目录，默认使用 res/[dataset]"
    ),
    workflow: str = typer.Option(
        "RCL", help="工作流程: AD, FT, RCL 或它们的组合，用逗号分隔"
    ),
):
    """测试模型"""
    typer.echo(f"开始测试模型，数据集: {dataset}")
    typer.echo(f"配置文件目录: {config_dir}")
    typer.echo(f"工作流程: {workflow}")
    
    try:
        # 解析工作流程为列表
        workflow_list = workflow.split(',')
        
        # 加载配置
        config = load_config(dataset, config_dir)
        # 如果未指定模型目录，使用默认路径
        res_dir = model_dir if model_dir else f'res/{dataset}'
        tmp_dir = f'{res_dir}/tmp'
        os.makedirs(res_dir, exist_ok=True)
        os.makedirs(tmp_dir, exist_ok=True)
        model_path = f'{res_dir}/model.pkl'
        res_path = f'{res_dir}/res.json'
        
        # 检查模型是否存在
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件 {model_path} 不存在，请先训练模型")
        
        # 加载模型
        model = load_pkl(model_path)
        typer.echo(f"模型加载完成: {model_path}")
        
        # 加载样本和病例数据
        train_samples, test_samples = load_samples(config['path']['sample_dir'])
        cases = pd.read_csv(config['path']['case_path'])
        typer.echo(f"数据加载完成，故障数: {len(cases)}")
        
        # 加载节点字典并反转
        node_dict = load_pkl(f"{config['path']['node_dict']}")
        node_dict = {v: k for k, v in node_dict.items()}
        
        # 初始化一些变量
        ad_cases_label, type_hash, type_dict = "{}", "{}", "{}"
        
        # 执行诊断工作流程
        typer.echo("开始执行诊断工作流程...")
        tmp_res, eval_res = diag_workflow(
            config['downstream_param'], 
            model, 
            train_samples, 
            test_samples,
            cases, 
            ad_cases_label, 
            node_dict, 
            type_hash, 
            type_dict, 
            channel_dict=None,
            workflow=workflow_list
        )
        
        # 保存结果
        if 'AD' in tmp_res:
            save_json(f'{tmp_dir}/pre_interval.json', tmp_res['AD']['pre_interval'])
        if 'FT' in tmp_res:
            save_json(f'{tmp_dir}/pre_types.json', tmp_res['FT']['pre_types'])
        if 'RCL' in tmp_res:
            tmp_res['RCL']['rank_df'].to_csv(f'{tmp_dir}/rank_df.csv', index=False)
        
        save_json(res_path, eval_res)
        typer.echo(f"测试结果已保存至: {res_path}")
        typer.echo("测试命令执行完成")
        
    except Exception as e:
        typer.echo(f"测试过程中发生错误: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def preprocess_single(
    datapack_path: str = typer.Option(
        "/mnt/jfs/rcabench-platform-v2/data/__dev__rcabench_test_r1/ts2-mysql-loss-qwhd9z", 
        help="Single datapack directory path"
    ),
    dataset: str = typer.Option(
        "RCABENCH", help="Dataset name to get global services and metrics"
    ),
):
    """Preprocess a single datapack"""
    # typer.echo(f"开始预处理单个 datapack: {datapack_path}")
    
    try:
        datapack_dir = Path(datapack_path)
        if not datapack_dir.exists():
            raise FileNotFoundError(f"Datapack 路径不存在: {datapack_path}")
        
        # 加载配置获取全局 services 和 metrics
        config_name=dataset+"_online"
        config = load_config(config_name, "config")
        
        # 加载全局 services 和 metrics（从训练时保存的文件）
        all_services = load_pkl(config['path']['node_dict'])
        all_metrics = load_pkl(config['path']['metric_dict'])

        # typer.echo(f"全局 services 数量: {len(all_services)}")
        # typer.echo(f"全局 metrics 数量: {len(all_metrics)}")
        
        # 处理单个 datapack
        samples = process_case(
            case_dir=datapack_dir,
            metric_file='abnormal_metrics.parquet',
            trace_file='abnormal_traces.parquet', 
            log_file='abnormal_logs.parquet',
            all_services=all_services,
            all_metrics=all_metrics
        )
        
        if not samples:
            typer.echo("警告: 没有生成任何样本")
            return
        
        all_features = [s[2] for s in samples]
        normed_features = minmax_tensor(all_features)

        # 替换原始feature
        for i, s in enumerate(samples):
            samples[i] = (s[0], s[1], normed_features[i])

        pack = DatasetPack(samples)
        samples=pack.create_sliding_windows(window_size=10, max_gap=30)


        #build case.csv
        gt = build_groundtruth([datapack_dir])
        df_time_set = {item[0].item() for item in samples}  # 使用集合提高查找效率
        filtered_gt = gt[gt.iloc[:, 0].isin(df_time_set)]


        return samples, filtered_gt

    except Exception as e:
        typer.echo(f"预处理过程中发生错误: {e}", err=True)
        raise typer.Exit(1)


@app.command() 
def inference_single(
    datapack_path: Path,
    model_path: str = typer.Option(
        "model.pkl", help="Model directory, default: res/[dataset]"
    ),
):
    """Run inference on a single datapack"""
    # typer.echo(f"开始对单个 datapack 进行推理: {datapack_path}")

    dataset="RCABENCH"
    try:

        if not datapack_path.exists():
            raise FileNotFoundError(f"Datapack 路径不存在: {datapack_path}")
        
        # 加载配置
        config_name=dataset+"_online"
        config = load_config(config_name, "config")

        # 加载模型
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件不存在: {model_path}")
        
        model = load_pkl(model_path)
        
        # 加载处理后的样本
        result = preprocess_single(
            datapack_path=datapack_path,
            dataset=dataset,
        )

        if result is None:
            raise FileNotFoundError(f"处理后的样本文件不存在: {datapack_path}")

        samples, cases = result
        
        # 加载节点字典
        node_dict = load_pkl(config['path']['node_dict'])
        node_dict = {v: k for k, v in node_dict.items()}
        
        # 初始化一些变量
        ad_cases_label, type_hash, type_dict = "{}", "{}", "{}"
        
        # 执行诊断工作流程（只进行 RCL）
        tmp_res, eval_res = diag_workflow(
            config['downstream_param'], 
            model, 
            samples, 
            samples,
            cases, 
            ad_cases_label, 
            node_dict, 
            type_hash, 
            type_dict, 
            channel_dict=None,
            workflow=['RCL']
        )
        result=tmp_res['RCL']['rank_df']
        columns_to_keep = ['timestamp', 'injection_name']  # 保留原始的标识列
        # 添加Top1到Top5的列
        columns_to_keep.extend([f'Top{i}' for i in range(1, 6)])

        # 筛选需要保留的列
        result = result[columns_to_keep]
        result=result.iloc[0,2:].tolist()
        topk_name=[result[i].split(':')[0] for i in range(len(result))]

        topk_name = ["none-service" if topk_name[i]=="" else topk_name[i] for i in range(len(topk_name))]
        
        return topk_name
        
    except Exception as e:
        typer.echo(f"推理过程中发生错误: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
