# MicroDig Project Refactoring

这个项目已经被重构为标准的Python包结构。原有的MicroDig代码已经被组织成模块化、可重用的组件。

## 重构概览

### 原始结构
```
MicroDig/
├── locator/
│   ├── preprocess1-extract.py    # 数据提取
│   ├── preprocess2-statistic.py  # 统计处理
│   ├── utils.py                  # 工具函数
│   └── code/
│       ├── main.py              # 主程序
│       ├── anomaly.py           # 异常检测
│       ├── dataloader.py        # 数据加载
│       ├── evaluator.py         # 评估
│       ├── graph.py             # 图结构
│       ├── ranker.py            # 排名算法
│       └── utils.py             # 工具函数
└── dataset/
    └── cases_testbed.csv        # 测试数据
```

### 重构后结构
```
src/microdig/
├── __init__.py              # 包初始化
├── data_structures.py       # 数据结构定义
├── preprocessor.py          # 数据预处理模块
├── utils.py                # 通用工具函数
├── anomaly.py              # 异常检测模块
├── graph.py                # 图生成模块
├── ranker.py               # 排名算法模块
├── evaluator.py            # 评估模块
├── algorithm.py            # 主算法模块
└── README.md               # 包文档
```

## 主要改进

### 1. 标准化项目结构
- 将所有代码迁移到`src/microdig/`标准包结构
- 分离数据处理和算法逻辑
- 定义清晰的模块边界

### 2. 规范化导入和日志
- 统一使用`from rcabench_platform.v2.logging import logger`
- 修复不规范的导入语句
- 添加适当的错误处理

### 3. 数据结构标准化
- 定义`AlgorithmInput`作为算法输入接口
- 创建`AlgorithmOutput`存储结果
- 标准化`CaseModel`和`TraceData`结构

### 4. 模块化设计
- **DataPreprocessor**: 处理原始trace数据和统计
- **AnomalyDetector**: k-sigma异常检测
- **GraphGenerator**: 各种图结构生成
- **Ranker**: 多种排名算法实现
- **Evaluator**: 评估指标计算
- **MicroDigAlgorithm**: 主算法协调器

### 5. 两阶段处理架构

#### 预处理阶段
```python
preprocessor = DataPreprocessor()

# 1. 提取trace数据
preprocessor.extract_traces_from_pickle(input_dir, output_dir)

# 2. 生成调用统计
preprocessor.process_trace_statistics(input_pattern, output_file)

# 3. 加载案例数据  
cases = preprocessor.load_case_data(info_file, data_dir)
```

#### 算法运行阶段
```python
algorithm = MicroDigAlgorithm(hyperparameters)

# 分析单个案例
output = algorithm.analyze_case(algorithm_input)

# 批量分析
results = algorithm.analyze_multiple_cases(cases)
```

## 使用方法

### 快速开始
```python
from microdig import MicroDigAlgorithm, CaseModel, AlgorithmInput

# 创建算法实例
algorithm = MicroDigAlgorithm()

# 运行完整流水线
results = algorithm.run_full_pipeline(
    case_info_file='./MicroDig/dataset/cases_testbed.csv',
    case_data_dir='./MicroDig/cases',
    output_dir='./results'
)
```

### 分步处理
```python
# 1. 数据预处理
algorithm.preprocess_traces('./raw_data', './processed_data')
algorithm.process_trace_statistics('./processed_data/*.csv', './stats.csv')

# 2. 加载案例
cases = algorithm.load_cases_from_files('./cases_info.csv', './cases_data/')

# 3. 分析
results = algorithm.analyze_multiple_cases(cases, './output')
```

## 核心算法

重构后保持了原有的三个主要算法：

1. **Algorithm 1**: 基础方法和服务器排名
2. **Algorithm 4**: 混合节点排名（无方法级检测）
3. **Algorithm 5**: 服务器节点排名

每个算法都会产生排名结果，并使用MAR、MRR、AC@k等指标进行评估。

## 配置参数

主要超参数：
- `test_length_before/after`: 告警时间窗口
- `train_length`: 历史数据训练窗口
- `search_method`: 候选搜索策略
- `rank_method`: 排名方法
- `level`: 分析级别（方法/服务）
- `rev_weight`: 反向边权重
- `beta`: 混合排名权重因子

## 兼容性

重构后的代码保持了与原始算法的兼容性：
- 相同的输入数据格式
- 相同的算法逻辑
- 相同的评估指标
- 更好的错误处理和日志记录

## 示例

查看`examples/run_microdig.py`获得完整的使用示例。
