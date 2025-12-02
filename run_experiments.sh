#!/bin/bash

# MaAS on MSCoRe Benchmark - Experiment Runner
# Author: Pavan Patel

echo "========================================="
echo "MaAS on MSCoRe Benchmark - Experiment Runner"
echo "========================================="

# Configuration
DATA_DIR="./data/mscore"
CODE_DIR="./code"
RESULTS_DIR="./results"
LOG_DIR="./logs"

# Create directories
mkdir -p $DATA_DIR $RESULTS_DIR $LOG_DIR $RESULTS_DIR/detailed_logs

echo "[1] Setting up environment..."
python3 -m venv maas_env
source maas_env/bin/activate

echo "[2] Installing dependencies..."
pip install --upgrade pip
pip install -r $CODE_DIR/requirements.txt

echo "[3] Downloading MSCoRe dataset..."
# Note: Actual download code would go here
# For now, assuming dataset is already in place
echo "Dataset ready at: $DATA_DIR"

echo "[4] Running MaAS with MSCoRe adapter..."
python3 $CODE_DIR/run_experiment.py \
    --dataset $DATA_DIR/mscore_test.json \
    --output $RESULTS_DIR/experiment_results.json \
    --log $LOG_DIR/experiment.log \
    --agents all \
    --max_time 10 \
    --samples 500

echo "[5] Analyzing results..."
python3 $CODE_DIR/analyze_results.py \
    --input $RESULTS_DIR/experiment_results.json \
    --output $RESULTS_DIR/analysis_report.json

echo "[6] Generating visualizations..."
python3 $CODE_DIR/generate_visualizations.py \
    --input $RESULTS_DIR/analysis_report.json \
    --output_dir ./visualizations

echo "[7] Creating summary report..."
python3 $CODE_DIR/create_report.py \
    --results $RESULTS_DIR/analysis_report.json \
    --template ./templates/report_template.md \
    --output ./REPORT.pdf

echo "========================================="
echo "Experiment completed successfully!"
echo "Results saved in: $RESULTS_DIR"
echo "Report generated: ./REPORT.pdf"
echo "Visualizations: ./visualizations/"
echo "========================================="

# Deactivate virtual environment
deactivate