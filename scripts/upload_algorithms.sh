#!/bin/bash

# Script to upload algorithms to RCABench

set -e

export RCABENCH_BASE_URL=http://10.10.10.220:32080
export RCABENCH_USERNAME=admin
export RCABENCH_PASSWORD=admin123

# Check if algorithms directory exists
if [ ! -d "algorithms" ]; then
    echo "Error: algorithms directory does not exist"
    exit 1
fi

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "Error: uv command not found, please ensure uv is installed"
    exit 1
fi

# Get all subdirectories in algorithms directory
algorithm_dirs=$(find algorithms -maxdepth 1 -type d -not -name "algorithms" | sort)

if [ -z "$algorithm_dirs" ]; then
    echo "Warning: No subdirectories found in algorithms directory"
    exit 0
fi

echo "Starting algorithm upload..."

# Iterate and upload each algorithm
for algorithm_dir in $algorithm_dirs; do
    algorithm_name=$(basename "$algorithm_dir")
    echo "Uploading algorithm: $algorithm_name"
    
    if RCABENCH_BASE_URL="$RCABENCH_BASE_URL" \
       RCABENCH_USERNAME="$RCABENCH_USERNAME" \
       RCABENCH_PASSWORD="$RCABENCH_PASSWORD" \
       uv run rca upload-algorithm-harbor "$algorithm_dir"; then
        echo "Algorithm $algorithm_name uploaded successfully"
    else
        echo "Algorithm $algorithm_name upload failed"
        exit 1
    fi
done

echo "All algorithms uploaded successfully!" 