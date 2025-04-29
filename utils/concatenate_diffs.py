#!/usr/bin/env python3
import json
import os
import argparse

"""
Concatenates diffs of model output and generated_test_cases.json

AI Gen using GitHub Copilot + Clause Sonnet 3.7
"""

def concatenate_diffs(test_cases_file, predictions_file, output_file):
    """
    Concatenate git diffs from test cases and model predictions for matching instance_ids.
    
    Args:
        test_cases_file: Path to the JSON file with instance_ids as keys and git diffs as values
        predictions_file: Path to the JSONL file with predictions
        output_file: Path to write the output JSONL file
    """
    # Load test cases
    print(f"Loading test cases from {test_cases_file}")
    with open(test_cases_file, 'r') as f:
        test_cases = json.load(f)
    
    # Read predictions line by line
    print(f"Reading predictions from {predictions_file}")
    predictions = []
    with open(predictions_file, 'r') as f:
        for line in f:
            try:
                prediction = json.loads(line)
                predictions.append(prediction)
            except json.JSONDecodeError:
                continue
    
    # Create updated predictions with concatenated diffs
    updated_predictions = []
    concatenated_count = 0
    
    for prediction in predictions:
        instance_id = prediction.get("instance_id")
        
        # Check if this instance_id exists in the test cases
        if instance_id in test_cases:
            test_case_diff = test_cases[instance_id]
            model_patch = prediction.get("model_patch", "")
            
            # If both have content, concatenate the diffs
            if test_case_diff and model_patch:
                # Concatenate the diffs
                concatenated_diff = model_patch + "\n" + test_case_diff
                
                # Create updated prediction with concatenated diff
                updated_prediction = prediction.copy()
                updated_prediction["model_patch"] = concatenated_diff
                updated_predictions.append(updated_prediction)
                concatenated_count += 1
            else:
                # If one is empty, just use the other one
                updated_prediction = prediction.copy()
                if not model_patch and test_case_diff:
                    updated_prediction["model_patch"] = test_case_diff
                    concatenated_count += 1
                elif model_patch and not test_case_diff:
                    updated_prediction["model_patch"] = model_patch
                    concatenated_count += 1
                updated_predictions.append(updated_prediction)
        else:
            # If instance_id is not in test cases, keep the prediction as is
            updated_predictions.append(prediction)
    
    # Write updated predictions to output file as JSONL
    print(f"Writing updated predictions to {output_file}")
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    with open(output_file, 'w') as f:
        for prediction in updated_predictions:
            f.write(json.dumps(prediction) + "\n")
    
    print(f"Updated predictions written to {output_file}")
    print(f"Total predictions processed: {len(predictions)}")
    print(f"Total instance IDs with concatenated diffs: {concatenated_count}")

def main():
    parser = argparse.ArgumentParser(description='Concatenate git diffs from test cases and model predictions.')
    parser.add_argument('--test-cases', type=str, default='/home/ec2-user/dkang_starter_task/generated_test_cases.json',
                        help='Path to the test cases JSON file')
    parser.add_argument('--predictions', type=str, default='/home/ec2-user/dkang_starter_task/top_models/20241208_gru/all_preds.jsonl',
                        help='Path to the predictions JSONL file')
    parser.add_argument('--output', type=str, default='/home/ec2-user/dkang_starter_task/updated_all_preds.json',
                        help='Path to write the output JSONL file')
    
    args = parser.parse_args()
    
    concatenate_diffs(args.test_cases, args.predictions, args.output)

if __name__ == "__main__":
    main()