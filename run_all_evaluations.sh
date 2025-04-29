#!/bin/bash

# Script to automatically run evaluations for all prediction files in the top_models directory
# Each evaluation uses the directory name as the RUN_ID

TOP_MODELS_DIR="/home/ec2-user/dkang_starter_task/top_models"
SELECTED_IDS_FILE="/home/ec2-user/dkang_starter_task/selected_ids.txt"
REPORT_DIR="/home/ec2-user/dkang_starter_task/new_test_case_runs"
COMPLETED_EVALS_FILE="/home/ec2-user/dkang_starter_task/completed_evaluations.txt"

# Check if the selected IDs file exists
if [ ! -f "$SELECTED_IDS_FILE" ]; then
    echo "Error: Selected instance IDs file not found at $SELECTED_IDS_FILE"
    echo "Please run select_random_ids.sh first"
    exit 1
fi

# Create completed evaluations file if it doesn't exist
if [ ! -f "$COMPLETED_EVALS_FILE" ]; then
    echo "Creating empty completed evaluations file at $COMPLETED_EVALS_FILE"
    touch "$COMPLETED_EVALS_FILE"
fi

# Read the selected instance IDs and join them with spaces
INSTANCE_IDS=$(tr '\n' ' ' < "$SELECTED_IDS_FILE")

echo "Starting evaluations for all prediction files in $TOP_MODELS_DIR"
echo "========================================================================"

# Initialize counters
TOTAL_DIRS=0
PROCESSED_DIRS=0
SKIPPED_DIRS=0

# Count total number of directories
for dir in "$TOP_MODELS_DIR"/*/ ; do
    if [ -d "$dir" ]; then
        TOTAL_DIRS=$((TOTAL_DIRS+1))
    fi
done

# Process each directory in the top_models directory
for dir in "$TOP_MODELS_DIR"/*/ ; do
    if [ -d "$dir" ]; then
        # Get directory name (RUN_ID)
        DIR_NAME=$(basename "$dir")
        
        # Check if this evaluation has already been completed
        if grep -q "^$DIR_NAME$" "$COMPLETED_EVALS_FILE"; then
            echo "Skipping $DIR_NAME: Already completed according to $COMPLETED_EVALS_FILE"
            SKIPPED_DIRS=$((SKIPPED_DIRS+1))
            continue
        fi
        
        # Path to the predictions file
        PREDICTIONS_PATH="$dir/all_preds.jsonl"
        
        # Check if the predictions file exists
        if [ -f "$PREDICTIONS_PATH" ]; then
            PROCESSED_DIRS=$((PROCESSED_DIRS+1))
            echo "[$PROCESSED_DIRS/$((TOTAL_DIRS-SKIPPED_DIRS))] Processing: $DIR_NAME"
            echo "Using predictions from: $PREDICTIONS_PATH"
            
            # MAKE SURE TO UPDATE RUN_ID WHEN RUNNING MODIFIED TESTS!!!!
            # Build and run the swebench evaluation command
            echo "Running evaluation with RUN_ID: $DIR_NAME"
            CMD="python -m swebench.harness.run_evaluation \
                --dataset_name princeton-nlp/SWE-bench_Verified \
                --predictions_path $PREDICTIONS_PATH \
                --max_workers 6 \
                --cache_level env \
                --run_id new_tests_${DIR_NAME} \
                --instance_ids $INSTANCE_IDS \
                --report_dir $REPORT_DIR \
                --timeout 600 \
                --clean True"
            
            echo "Executing command: $CMD"
            eval "$CMD"
            
            # Mark this evaluation as completed
            # echo "$DIR_NAME" >> "$COMPLETED_EVALS_FILE"
            
            echo "Evaluation complete for $DIR_NAME"
            echo "---------------------------------------------------------------"
        else
            echo "Skipping $DIR_NAME: No predictions file found at $PREDICTIONS_PATH"
        fi
    fi
done

echo "========================================================================"
echo "All evaluations complete! Processed $PROCESSED_DIRS directories."
echo "Skipped $SKIPPED_DIRS already completed directories."