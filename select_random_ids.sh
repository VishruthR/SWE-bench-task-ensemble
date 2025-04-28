#!/bin/bash

# Selects 30 random instance IDs from pool of instance_ids
# AI Gen using GitHub Copilot + Clause Sonnet 3.7

# Path to the instance ID pool file
POOL_FILE="/home/ec2-user/dkang_starter_task/instance_id_pool.txt"

# Output file for the randomly selected IDs
OUTPUT_FILE="/home/ec2-user/dkang_starter_task/selected_ids.txt"

# Check if the pool file exists
if [ ! -f "$POOL_FILE" ]; then
    echo "Error: Instance ID pool file not found at $POOL_FILE"
    exit 1
fi

# Count the total number of IDs in the pool
TOTAL_IDS=$(wc -l < "$POOL_FILE")
echo "Total instance IDs in pool: $TOTAL_IDS"

# Check if we have at least 100 IDs
if [ "$TOTAL_IDS" -lt 30 ]; then
    echo "Error: The pool contains fewer than 100 IDs"
    exit 1
fi

# Randomly select 100 instance IDs without replacement
echo "Selecting 30 random instance IDs..."
shuf -n 30 "$POOL_FILE" > "$OUTPUT_FILE"

echo "Successfully selected 30 random instance IDs"
echo "Selected IDs saved to $OUTPUT_FILE"
echo "Use run_evaluation.sh to execute the evaluation command"

# Make the output file readable
chmod +r "$OUTPUT_FILE"