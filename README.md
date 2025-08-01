# RCA Algorithm Contribution Repository

This repository is designed to centralize existing Root Cause Analysis (RCA) algorithms and provide command-line tools for uploading and running algorithms, making it convenient for users to test their contributions.

## Environment Setup

### Installing Dependencies

#### Using uv (Recommended)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate
```

#### Using pip

```bash
pip install rcabench-platform
```

## Command Line Tool Usage

### Basic Commands

All commands support server connection configuration through environment variables:

```bash
export RCABENCH_BASE_URL=http://10.10.10.220:32080
export RCABENCH_USERNAME=admin
export RCABENCH_PASSWORD=admin123
```

### View Help

```bash
# Using uv
uv run rca --help

# After pip installation
rca --help
```

### List Available Algorithms

```bash
# Using uv
uv run rca list-algorithms

# After pip installation
rca list-algorithms
```

**Output Example:**
```
shape: (9, 13)
┌──────────────┬──────────────┬──────────────┬─────┬──────────────┬───────────┬────────────┬─────────┬──────────┬────────┬─────────┬───────────┬─────────────┐
│ command      ┆ created_at   ┆ env_vars     ┆  id ┆ image        ┆ is_public ┆ name       ┆ project ┆ project_id ┆ status ┆ tag     ┆ type      ┆ updated_at  │
│ ---          ┆ ---          ┆ ---          ┆ --- ┆ ---          ┆ ---       ┆ ---        ┆ ---     ┆ ---        ┆ ---    ┆ ---     ┆ ---       ┆ ---         │
│ str          ┆ str          ┆ str          ┆ i64 ┆ str          ┆ bool      ┆ str        ┆ null    ┆ i64        ┆ bool   ┆ str     ┆ str       ┆ str         │
╞══════════════╪══════════════╪══════════════╪═════╪══════════════╪═══════════╪════════════╪═════════╪════════════╪════════╪═════════╪═══════════╪═════════════╡
│ bash /entryp ┆ 2025-07-30T0 ┆              ┆  22 ┆ 10.10.10.240 ┆ false     ┆ baro       ┆ null    ┆ 0          ┆ true   ┆ latest  ┆ algorithm ┆ 2025-07-30T │
│ oint.sh      ┆ 2:41:13.8423 ┆              ┆     ┆ /library/rca ┆           ┆            ┆         ┆            ┆        ┆         ┆           ┆ 02:55:09.81 │
│              ┆ 58Z          ┆              ┆     ┆ -algo-baro   ┆           ┆            ┆         ┆            ┆        ┆         ┆           ┆ 1785Z       │
└──────────────┴──────────────┴──────────────┴─────┴──────────────┴───────────┴────────────┴─────────┴──────────┴────────┴─────────┴───────────┴─────────────┘
```

### List Available Datasets

```bash
# Using uv
uv run rca list-datasets

# After pip installation
rca list-datasets
```

**Output Example:**
```
shape: (4, 4)
┌─────┬───────────┬───────────────┬────────┐
│  ID ┆ Name      ┆ Version       ┆ Status │
│ --- ┆ ---       ┆ ---           ┆    --- │
│ i64 ┆ str       ┆ str           ┆    i64 │
╞═════╪═══════════╪═══════════════╪════════╡
│  38 ┆ pair-diag ┆ test-stage-1  ┆      1 │
│  37 ┆ pair-diag ┆ train-stage-1 ┆      1 │
│  36 ┆ pair-diag ┆ test-stage-0  ┆      1 │
│  35 ┆ pair-diag ┆ train-stage-0 ┆      1 │
└─────┴───────────┴───────────────┴────────┘
```

### List Injections

```bash
# Using uv
uv run rca list-injections

# After pip installation
rca list-injections
```

### Upload Algorithm

Upload algorithm using Harbor mode (requires pre-built image pushed to Harbor registry):

```bash
# Using uv
uv run rca upload-algorithm-harbor algorithms/simplerca

# After pip installation
rca upload-algorithm-harbor algorithms/simplerca
```

**Output Example:**
```
2025-08-01 20:28:36.444 | INFO     | rcabench_platform.v2.cli.online:upload_algorithm_harbor:247 - 🐳 Using HARBOR MODE for algorithm: algorithms/simplerca
2025-08-01 20:28:36.444 | INFO     | rcabench_platform.v2.cli.online:upload_algorithm_harbor:264 - Uploading algorithm: simplerca
2025-08-01 20:28:36.476 | INFO     | rcabench_platform.v2.cli.online:upload_algorithm_harbor:284 - Response: code=200 data=DtoSubmitResp(group_id='', traces=[DtoTrace(head_task_id='harbor-1754051323971343470', index=0, trace_id='trace-1754051323971347806')]) message='Container information updated successfully from Harbor (existing record was overwritten)' timestamp=1754051323
2025-08-01 20:28:36.477 | INFO     | rcabench_platform.v2.cli.online:upload_algorithm_harbor:287 - ✅ Successfully uploaded algorithm: simplerca
```

### Submit Algorithm Execution

```bash
# Using uv
uv run rca submit-execution -a simplerca -ds pair-diag -dsv test-stage-1 -p pair_diagnosis

# After pip installation
rca submit-execution -a simplerca -ds pair-diag -dsv test-stage-1 -p pair_diagnosis
```

**Parameter Description:**
- `-a, --algorithm`: Algorithm name (required)
- `-p, --project`: Project name (required)
- `-ds, --dataset`: Dataset name
- `-dsv, --dataset-version`: Dataset version
- `-d, --datapack`: Datapack name
- `--env`: Environment variables (optional)

**Output Example:**
```
shape: (60, 7)
┌───────┬──────────┬─────────┬───────────┬───────────┬──────────────────────────────────────┬─────────────────────────────────────────────────────┐
│ Index ┆ Datapack ┆ Dataset ┆ Algorithm ┆ Status    ┆ Task ID                              ┆ Trace ID                                            │
│   --- ┆      --- ┆     --- ┆       --- ┆ ---       ┆ ---                                  ┆ ---                                                 │
│   i64 ┆      i64 ┆     i64 ┆       i64 ┆ str       ┆ str                                  ┆ str                                                 │
╞═══════╪══════════╪═════════╪═══════════╪═══════════╪══════════════════════════════════════╪═════════════════════════════════════════════════════╡
│     1 ┆      175 ┆      38 ┆        21 ┆ submitted ┆ 2d5e12b7-7329-43ce-ade2-8ef1f49e7933 ┆ 0bd46865-e122-4aa6-a38f-f89564899684               │
│     2 ┆     1094 ┆      38 ┆        21 ┆ submitted ┆ e068f058-1078-4686-87f5-adedc2d5eb1e ┆ d2edae39-f5ae-491d-9132-02edc84ab8db               │
└───────┴──────────┴─────────┴───────────┴───────────┴──────────────────────────────────────┴─────────────────────────────────────────────────────┘
```

### Monitor Execution Status

Use the trace command to monitor algorithm execution status in real-time:

```bash
# Using uv
uv run rca trace <trace_id> --timeout 600

# After pip installation
rca trace <trace_id> --timeout 600
```

**Parameter Description:**
- `trace_id`: Trace ID obtained from submit-execution command output
- `--timeout`: Timeout in seconds (default 600 seconds)

## Algorithm Development

### Algorithm Folder Structure Requirements

Each algorithm folder must contain the following files:

```
algorithms/your-algorithm/
├── Dockerfile          # Container build file
├── entrypoint.sh       # Container startup script
├── info.toml          # Algorithm information configuration
├── main.py            # Main algorithm implementation
├── requirements.txt    # Python dependencies (optional)
├── README.md          # Algorithm documentation
└── src/               # Source code directory (optional)
```

#### Required Files Description:

1. **Dockerfile**: Defines how to build the algorithm container
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   RUN chmod +x entrypoint.sh
   
   ENTRYPOINT ["./entrypoint.sh"]
   ```

2. **entrypoint.sh**: Container startup script that runs the algorithm
   ```bash
   #!/bin/bash
   python main.py "$@"
   ```

3. **info.toml**: Algorithm configuration file

   If you need some parameters to configure your algorithm, you can use `env_vars` to describe the ENV VARs, it will resigter the env var to the RCABench. When you submit the algorithm execution, it will check you whether pass the ENV VAR.

   ```toml
   name = "your-algorithm-name"
   
   [env_vars]
   DEBUG = "true"
   LOG_LEVEL = "INFO"
   MAX_ITERATIONS = "1000"
   ```

4. **main.py**: Main algorithm implementation, the requirement is you should follow the `rcabench_platform` usage, so that your algo can pass the correct result to the RCABench.
   ```python
   from rcabench_platform.v2.cli.main import main
   from rcabench_platform.v2.algorithms.spec import (
      global_algorithm_registry,
      Algorithm,
      AlgorithmArgs,
      AlgorithmAnswer,
   )
   import os
   from main import run_inference

   class PadiRCA(Algorithm):
      def needs_cpu_count(self) -> int | None:
         return 4

      def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
         model_path = os.environ["MODEL_PATH"]
         results = run_inference(
               datapack_path=args.input_folder,
               model_path=model_path,
               output_dir="data/RCABENCH", 
               service_map_path="data/RCABENCH/service_to_idx.pkl",
               batch_size=32
         )
         answers = [
               AlgorithmAnswer(level="service", name=name, rank=i + 1)
               for i, name in enumerate(results)
         ]
         return answers



   if __name__ == "__main__":
      registry = global_algorithm_registry()
      registry["padi-rca"] = PadiRCA               # register the algo to the registry
      main(enable_builtin_algorithms=False)
   ```

### Adding New Algorithms

#### Step 1: Fork and Clone the Repository

```bash
# Fork the repository on GitHub first, then clone your fork
git clone https://github.com/your-username/rca-algo-contrib.git
cd rca-algo-contrib

# Add the original repository as upstream
git remote add upstream https://github.com/original-owner/rca-algo-contrib.git
```

#### Step 2: Create a New Branch

```bash
# Create and switch to a new branch
git checkout -b feature/add-new-algorithm

# Make sure you're on the new branch
git branch
```

#### Step 3: Add Your Algorithm

```bash
# Create your algorithm directory
mkdir algorithms/your-algorithm-name

# Add your algorithm files
# - Dockerfile
# - entrypoint.sh
# - info.toml
# - main.py
# - README.md
# - requirements.txt (if needed, you can use `pyproject.toml` also)
```

#### Step 4: Test Your Algorithm Locally

```bash
# Build the algorithm container
cd algorithms/your-algorithm-name
docker build -t your-algorithm-name .

# Test the container locally, you may modify the command depends on your algo.
echo '{"test": "data"}' | docker run -i your-algorithm-name
```

#### Step 5: Build and Push to Harbor

```bash
# Tag your image for Harbor
docker tag your-algorithm-name 10.10.10.240/library/rca-algo-your-algorithm-name:latest

# Push to Harbor
docker push 10.10.10.240/library/rca-algo-your-algorithm-name:latest
```

#### Step 6: Test with RCABench

```bash
# Upload your algorithm
RCABENCH_BASE_URL=http://10.10.10.220:32080 RCABENCH_USERNAME=admin RCABENCH_PASSWORD=admin123 uv run rca upload-algorithm-harbor algorithms/your-algorithm-name

# Submit execution
RCABENCH_BASE_URL=http://10.10.10.220:32080 RCABENCH_USERNAME=admin RCABENCH_PASSWORD=admin123 uv run rca submit-execution -a your-algorithm-name -ds pair-diag -dsv test-stage-1 -p pair_diagnosis
```

#### Step 7: Commit and Push Your Changes

```bash
# Add your changes
git add algorithms/your-algorithm-name/

# Commit with a descriptive message
git commit -m "feat: add new algorithm 'your-algorithm-name'

- Add Dockerfile for containerization
- Add entrypoint.sh for container startup
- Add info.toml for algorithm configuration
- Add main.py with algorithm implementation
- Add README.md with algorithm documentation"

# Push to your fork
git push origin feature/add-new-algorithm
```

### Submitting a Pull Request

**Important**: Direct commits to the main branch are not allowed. All changes must go through Pull Requests.

#### Step 1: Create Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request" for your branch
3. Fill in the PR template:

```markdown
## Description
Brief description of your algorithm and what it does.

## Algorithm Details
- **Name**: your-algorithm-name
- **Type**: [e.g., Causal Inference, Machine Learning, Statistical]
- **Input Format**: [describe expected input format]
- **Output Format**: [describe expected output format]

## Testing
- [ ] Algorithm builds successfully
- [ ] Algorithm runs without errors
- [ ] Algorithm produces expected output format
- [ ] Algorithm has been tested with RCABench
- [ ] Documentation is complete

## Checklist
- [ ] All required files are present (Dockerfile, entrypoint.sh, info.toml, main.py, README.md)
- [ ] Algorithm follows the repository's coding standards
- [ ] Algorithm is properly documented
- [ ] Algorithm has been tested with sample data
- [ ] No sensitive information is included in the code

## Related Issues
Closes #[issue-number] (if applicable)
```

#### Step 2: Code Review Process

1. **Automated Checks**: Ensure all CI/CD checks pass
2. **Code Review**: Wait for maintainers to review your code
3. **Address Feedback**: Make any requested changes
4. **Final Approval**: Once approved, your PR will be merged

#### Step 3: After Merge

```bash
# Update your local repository
git checkout main
git pull upstream main

# Delete your feature branch
git branch -d feature/add-new-algorithm
git push origin --delete feature/add-new-algorithm
```

## Testing Algorithms

### Remote Testing

Submit algorithm execution to the remote server and run it. Environment variables are used to control runtime behavior during algorithm execution.

**Complete Testing Workflow:**

1. **Upload Algorithm:**
```bash
RCABENCH_BASE_URL=http://10.10.10.220:32080 RCABENCH_USERNAME=admin RCABENCH_PASSWORD=admin123 uv run rca upload-algorithm-harbor algorithms/simplerca
```

2. **Submit Execution:**
```bash
RCABENCH_BASE_URL=http://10.10.10.220:32080 RCABENCH_USERNAME=admin RCABENCH_PASSWORD=admin123 uv run rca submit-execution -a simplerca -ds pair-diag -dsv test-stage-1 -p pair_diagnosis
```

3. **Monitor Execution:**
```bash
RCABENCH_BASE_URL=http://10.10.10.220:32080 RCABENCH_USERNAME=admin RCABENCH_PASSWORD=admin123 uv run rca trace <trace_id>
```

### Environment Variable Configuration

You can configure server connection through environment variables:

```bash
export RCABENCH_BASE_URL=http://10.10.10.220:32080
export RCABENCH_USERNAME=admin
export RCABENCH_PASSWORD=admin123
```

Then run commands directly:

```bash
uv run rca list-algorithms
uv run rca submit-execution -a simplerca -ds pair-diag -dsv test-stage-1 -p pair_diagnosis
```

## Available Algorithms

The current repository contains the following algorithms:

- `baro`: Bayesian network-based root cause analysis algorithm
- `causalrca`: Causal inference root cause analysis algorithm
- `diagfusion`: Diagnostic fusion algorithm
- `random`: Random baseline algorithm
- `rcd`: Root cause diagnosis algorithm
- `run`: Runtime algorithm
- `simplerca`: Simple root cause analysis algorithm
- `traceback`: Backtrace algorithm

## Building Algorithms

```bash
# Build all algorithms
make build
```

## Troubleshooting

### Common Issues

1. **Project Not Found Error:**
   - Ensure you're using the correct project name, such as `pair_diagnosis`

2. **Algorithm Upload Failure:**
   - Ensure the algorithm image is built and pushed to Harbor registry
   - Check that `info.toml` configuration is correct

3. **Execution Submission Failure:**
   - Check that the algorithm name is correct
   - Ensure the dataset and version exist
   - Verify the project name is correct

4. **Trace Monitoring Failure:**
   - Check that the trace ID is correct
   - Ensure network connection is normal
   - Try increasing the timeout

### Debug Commands

```bash
# View detailed logs
uv run rca --help

# Check algorithm status
uv run rca list-algorithms

# Check dataset status
uv run rca list-datasets
```

## Contributing Guidelines

### Code Standards

1. **File Naming**: Use lowercase with hyphens for algorithm names
2. **Documentation**: Each algorithm must have a comprehensive README.md
3. **Error Handling**: Implement proper error handling in your algorithm
4. **Logging**: Use appropriate logging levels for debugging

### Best Practices

1. **Containerization**: Ensure your algorithm runs in a containerized environment
2. **Input/Output**: Follow the standard JSON input/output format
3. **Performance**: Optimize your algorithm for reasonable execution times
4. **Testing**: Test your algorithm with various input scenarios

### Review Process

1. **Automated Testing**: All PRs must pass automated tests
2. **Code Review**: At least one maintainer must approve your PR
3. **Documentation**: Ensure all documentation is complete and accurate
4. **Testing**: Verify that your algorithm works correctly in the RCABench environment

## Support

If you encounter issues or have questions:

1. Check the existing issues on GitHub
2. Create a new issue with detailed information about your problem
3. Join our community discussions
4. Review the algorithm examples in the `algorithms/` directory

