#!/bin/bash

# Runs evaluation on selected instance IDs, basically a command formatter
# AI Gen using GitHub Copilot + Clause Sonnet 3.7

# Path to the file with selected instance IDs
SELECTED_IDS_FILE="/home/ec2-user/dkang_starter_task/selected_ids.txt"

# Path to the predictions file
PREDICTIONS_PATH="/home/ec2-user/dkang_starter_task/ensemble_model/all_preds.jsonl"

# Run ID for the evaluation
RUN_ID="ensemble_model"

# Check if the selected IDs file exists
if [ ! -f "$SELECTED_IDS_FILE" ]; then
    echo "Error: Selected instance IDs file not found at $SELECTED_IDS_FILE"
    echo "Please run select_random_ids.sh first"
    exit 1
fi

# Read the selected instance IDs and join them with spaces
INSTANCE_IDS=$(tr '\n' ' ' < "$SELECTED_IDS_FILE")

echo "Running evaluation on 100 selected instance IDs..."
echo "Using predictions from: $PREDICTIONS_PATH"
echo "Run ID: $RUN_ID"

# Build and run the swebench evaluation command
CMD="python -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_Verified \
    --predictions_path $PREDICTIONS_PATH \
    --max_workers 6 \
    --cache_level env \
    --run_id $RUN_ID \
    --instance_ids $INSTANCE_IDS \
    --timeout 600 \
    --clean True"

echo "Executing command:"
echo "$CMD"

# Execute the command
eval "$CMD"

echo "Evaluation complete!"