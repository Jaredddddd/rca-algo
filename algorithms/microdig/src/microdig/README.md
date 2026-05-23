# MicroDig - Microservice Failure Root Cause Analysis

MicroDig is a Python package for analyzing microservice failure patterns and identifying root causes using graph-based anomaly detection algorithms.

## Project Structure

```
src/microdig/
├── __init__.py              # Package initialization and exports
├── data_structures.py       # Core data structures (CaseModel, AlgorithmInput, etc.)
├── preprocessor.py          # Data preprocessing and loading
├── utils.py                # Utility functions
├── anomaly.py              # Anomaly detection algorithms
├── graph.py                # Graph generation and manipulation  
├── ranker.py               # Ranking algorithms
├── evaluator.py            # Evaluation metrics and functions
└── algorithm.py            # Main MicroDig algorithm
```

## Key Components

### Data Structures
- `CaseModel`: Represents a failure case with metrics and metadata
- `AlgorithmInput`: Input structure containing case data and parameters
- `AlgorithmOutput`: Output structure with rankings and evaluation results
- `TraceData`: Represents processed trace data

### Core Components
- `DataPreprocessor`: Handles trace data preprocessing and loading
- `AnomalyDetector`: Detects anomalies using k-sigma method
- `GraphGenerator`: Creates various graph structures for analysis
- `Ranker`: Implements different ranking algorithms
- `Evaluator`: Calculates evaluation metrics (MAR, MRR, AC@k)
- `MicroDigAlgorithm`: Main algorithm orchestrating all components

## Usage

### Basic Usage

```python
from microdig import MicroDigAlgorithm, CaseModel, AlgorithmInput

# Initialize algorithm
algorithm = MicroDigAlgorithm({
    'test_length_before': 10,
    'test_length_after': 10,
    'train_length': 60,
    'search_method': 'all',
    'rank_method': 'random walk',
    'level': 'method'
})

# Create a case model
case = CaseModel(
    alarm_start_time="2022-02-23 07:00:00",
    alarm_end_time="2022-02-23 07:05:00", 
    alarm_start_minute=420,
    alarm_end_minute=425,
    monitor_id=1,
    alarm_item="ts-preserve-other-service",
    sli_type="error_rate",
    where_info={"service": "ts-preserve-other-service"},
    rc=["ts-basic-service"]  # Ground truth
)

# Create algorithm input
algorithm_input = AlgorithmInput(case=case)

# Analyze the case
output = algorithm.analyze_case(algorithm_input)

if output.success:
    print(f"Analysis completed in {output.processing_time:.2f}s")
    print(f"Server rankings: {output.alg1_server_ranking}")
else:
    print(f"Analysis failed: {output.error_message}")
```

### Full Pipeline

```python
# Run complete pipeline with case files
results = algorithm.run_full_pipeline(
    case_info_file='./cases_testbed.csv',
    case_data_dir='./cases/',
    output_dir='./results/'
)

print(f"Processed {results['total_cases']} cases")
print(f"Success rate: {results['success_rate']:.2%}")
```

### Data Preprocessing

```python
# Preprocess trace files
algorithm.preprocess_traces(
    input_dir='./raw_traces',
    output_dir='./processed_traces'
)

# Generate calling statistics
algorithm.process_trace_statistics(
    input_pattern='./processed_traces/*.csv',
    output_file='./output.csv'
)
```

## Algorithms

The package implements several ranking algorithms:

1. **Algorithm 1**: Basic method and server ranking
2. **Algorithm 4**: Mixed node ranking without method-level detection  
3. **Algorithm 5**: Server node ranking

Each algorithm produces rankings that are evaluated using standard metrics like MAR (Mean Average Rank), MRR (Mean Reciprocal Rank), and AC@k (Accuracy at k).

## Evaluation Metrics

- **MAR (Mean Average Rank)**: Average rank of correct root causes
- **MRR (Mean Reciprocal Rank)**: Average reciprocal rank
- **AC@k**: Accuracy at top-k (percentage of cases with correct root cause in top-k)
- **Avg@k**: Average of AC@1 through AC@k

## Configuration

Key hyperparameters:

- `test_length_before/after`: Time window around alarm for testing
- `train_length`: Historical data window for training
- `search_method`: Strategy for finding candidates ('all', 'deepest2', 'last2')
- `rank_method`: Ranking algorithm ('pagerank', 'random walk')
- `level`: Analysis level ('method', 'service')
- `rev_weight`: Weight for reverse edges in graph
- `beta`: Weight factor for mixed node ranking

## Dependencies

The package assumes the following dependencies are installed:
- `rcabench_platform.v2.logging` for logging
- Standard scientific Python packages (numpy, pandas, scipy, networkx, matplotlib)
- Additional packages (snappy, tqdm, graphviz)

## Example

See `examples/run_microdig.py` for a complete example of using the MicroDig algorithm.
