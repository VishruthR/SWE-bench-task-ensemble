"""
Identifies the best model trial for each task based on pass rates.

This script compares multiple model trials and determines which model performs best
on each individual task based on the highest pass rate.

Generated using GitHub Copilot + Claude Sonnet 3.7
"""

import os
import sys
import json
import glob
from pathlib import Path
from calculate_passed_test_cases import get_pass_rates

def get_model_child_from_dir(model_dir):
    # Find the single child directory (assuming there's only one)
    child_dirs = [d for d in os.listdir(model_dir) if os.path.isdir(os.path.join(model_dir, d))]
    if not child_dirs:
        print(f"Warning: No child directory found in {model_dir}")
        return ""
    if len(child_dirs) > 1:
        print(f"Warning: Multiple child directories found in {model_dir}, using first one: {child_dirs[0]}")
    
    # Use the child directory for processing
    model_dir = os.path.join(model_dir, child_dirs[0])
    model_name = os.path.basename(os.path.normpath(model_dir))

    return model_dir

def find_best_model_per_task(model_trial_directories):
    """
    Find the best model trial for each task based on pass rates.
    
    Args:
        model_trial_directories (list): List of directories containing model trials
        
    Returns:
        dict: Dictionary mapping task IDs to their best model trial info
    """
    # Dictionary to store all results: {task_id: {model_name: pass_rate}}
    all_results = {}
    
    # Dictionary to store best model per task: {task_id: {'model': model_name, 'pass_rate': pass_rate}}
    best_models = {}
    
    for model_dir in model_trial_directories:
        # print(model_dir)
        if not os.path.exists(model_dir):
            print(f"Warning: Directory not found: {model_dir}")
            continue
        
        model_dir_child = get_model_child_from_dir(model_dir)
        if not model_dir_child:
            continue

        # Extract model name from the model directory path
        model_name = os.path.basename(model_dir).replace("new_tests_", "")
        print(f"Processing model trial: {model_name}")
        
        # Get pass rates for all tasks in this model trial
        model_results = get_pass_rates(model_dir_child)
        
        # Add results to all_results dictionary
        for task_id, stats in model_results.items():
            if task_id not in all_results:
                all_results[task_id] = {}
            
            # Store the pass rate for this model on this task
            all_results[task_id][model_name] = stats["pass_rate"]
            
            # Update best model if this one has a higher pass rate
            if task_id not in best_models or stats["pass_rate"] >= best_models[task_id]["pass_rate"]:
                best_models[task_id] = {
                    "model": model_name,
                    "pass_rate": stats["pass_rate"],
                    "pass_count": stats["pass_count"],
                    "missing_count": stats["total_count"] - stats["pass_count"],
                    "total_count": stats["total_count"]
                }
    
    return best_models

def get_evaluation_directories(base_path="/home/ec2-user/dkang_starter_task/logs/run_evaluation"):
    """
    Find all directories under run_evaluation that start with "new_tests_"
    
    Args:
        base_path (str): Base directory to search in
        
    Returns:
        list: List of full paths to matching directories
    """
    if not os.path.exists(base_path):
        print(f"Warning: Base directory not found: {base_path}")
        return []
    
    matching_dirs = []
    for item in os.listdir(base_path):
        full_path = os.path.join(base_path, item)
        if os.path.isdir(full_path) and item.startswith("new_tests_"):
            matching_dirs.append(full_path)
    
    if not matching_dirs:
        print(f"Warning: No directories starting with 'new_tests_' found in {base_path}")
    else:
        print(f"Found {len(matching_dirs)} evaluation directories")
    
    return matching_dirs

def generate_model_to_predictions(model_directories):
    """
    Generates a dictionary mapping model names to their prediction files.
    
    Args:
        model_directories (list): List of directories containing model trials
        
    Returns:
        dict: Dictionary mapping model names to their prediction file paths
    """
    model_to_predictions = {}
    
    for model_dir in model_directories:
        # Extract the base model name by removing "new_tests_" prefix
        model_name = os.path.basename(model_dir).replace("new_tests_", "")
        
        # Create the path to the prediction file
        prediction_path = f"/home/ec2-user/dkang_starter_task/top_models/{model_name}/all_preds.jsonl"
        
        # Add to the dictionary
        model_to_predictions[model_name] = prediction_path
    
    return model_to_predictions

def create_preds_file(best_models, output_dir="/home/ec2-user/dkang_starter_task/ensemble_model"):
    """
    Creates an all_preds.jsonl file for each task using the best models' patches.
    
    Args:
        best_models (dict): Dictionary mapping task IDs to their best model info
        output_dir (str): Directory where the output files will be saved
    
    Returns:
        dict: Dictionary mapping task IDs to their output file paths
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    output_file = output_dir + "/" + "all_preds.jsonl"

    # Clear the output file if it exists
    if os.path.exists(output_file):
        open(output_file, 'w').close()
    
    for task_id, info in best_models.items():
        model_name = info["model"]
        task_json = {}

        # Locate the all_preds.jsonl file for this model
        pred_file_path = f"/home/ec2-user/dkang_starter_task/top_models/{model_name}/all_preds.jsonl"
        
        if not os.path.exists(pred_file_path):
            print(f"Warning: Prediction file not found: {pred_file_path}")
            continue
        
        # Process the prediction file
        with open(pred_file_path, 'r') as f:
            for line in f:
                try:
                    # Parse the JSON line
                    pred = json.loads(line)
                    instance_id = pred.get("instance_id")
                    
                    if instance_id == task_id:
                        task_json = {
                            "instance_id": task_id,
                            "model_name_or_path": model_name,
                            "model_patch": pred["model_patch"]
                        }
                except json.JSONDecodeError:
                    print(f"Warning: Invalid JSON in {pred_file_path}")
                except Exception as e:
                    print(f"Error processing {pred_file_path}: {str(e)}")

        # Write the task_json to the output file if it has data
        if task_json:
            with open(output_file, 'a') as out_f:
                out_f.write(json.dumps(task_json) + '\n')
            print(f"Added prediction for task {task_id} from model {model_name}")

def main():
    model_directories = get_evaluation_directories()
    model_to_predictions = generate_model_to_predictions(model_directories)
    best_models = find_best_model_per_task(model_directories)
    
    # Print summary of best models
    print("\nBest Models Per Task:")
    for task_id, info in best_models.items():
        print(f"{task_id}: {info['model']} ({info['pass_rate']:.2%} - {info['pass_count']}/{info['total_count']} tests)")
    
    # Save results to a JSON file
    output_file = "top_models.json"
    with open(output_file, 'w') as f:
        json.dump(best_models, f, indent=2)
    print(f"\nResults saved to {output_file}")
    
    # Create prediction files for each task using the best models
    create_preds_file(best_models)

if __name__ == "__main__":
    main()