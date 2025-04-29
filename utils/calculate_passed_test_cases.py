"""
Calculates pass rate for a given model

AI Gen by GitHub Copilot + Clause Sonnet 3.7
"""
import os
import sys
import json
from pathlib import Path
from log_parsers import MAP_REPO_TO_PARSER

def get_repo_from_dir_name(dir_name):
    """
    Convert directory name format (e.g., 'django__django-15104') to repository format (e.g., 'django/django')
    
    Args:
        dir_name (str): Directory name in the format 'repo__repo-issue'
        
    Returns:
        str: Repository name in the format 'repo/repo'
    """
    # Split by '-' to separate the issue number, then split by '__' to get repo parts
    parts = dir_name.rsplit('-', 1)[0].split('__')
    if len(parts) >= 2:
        # Format as owner/repo (e.g., django/django)
        return f"{parts[0]}/{parts[1]}"
    return None

def extract_instance_id(directory_path):
    """
    Extract the instance_id from a directory path
    
    Args:
        directory_path (str): Directory path which may include parent directories
        
    Returns:
        str: The instance_id (e.g., 'django__django-15104')
    """
    # Get the last directory name from the path
    return os.path.basename(os.path.normpath(directory_path))

def parse_test_logs(directory):
    """
    Parse test logs from the specified directory
    
    Args:
        directory (str): Directory name containing test logs (e.g., 'django__django-15104')
        
    Returns:
        dict: Test case to test status mapping
    """
    # Extract instance_id from directory path if it contains parent directories
    instance_id = extract_instance_id(directory)
    
    # Get repository name from directory
    repo_name = get_repo_from_dir_name(instance_id)
    if not repo_name or repo_name not in MAP_REPO_TO_PARSER:
        print(f"Error: Could not find parser for repository: {repo_name}")
        return None
    
    # Get the parser function for this repository
    parser_func = MAP_REPO_TO_PARSER[repo_name]
    
    # Path to test output file
    log_file_path = os.path.join(directory, "test_output.txt")
    if not os.path.exists(log_file_path):
        print(f"Error: Test output file not found at {log_file_path}")
        return None
    
    # Read test log file
    with open(log_file_path, 'r', errors='replace') as f:
        log_content = f.read()
    
    # Parse test logs
    return parser_func(log_content)

def calculate_pass_rate(test_results):
    """
    Calculate pass rate from test results
    
    Args:
        test_results (dict): Test case to test status mapping
        
    Returns:
        tuple: (pass_count, total_count, pass_rate)
    """
    if not test_results:
        return 0, 0, 0.0
    
    total_count = len(test_results)
    pass_count = sum(1 for status in test_results.values() if status == "PASSED")
    
    if total_count == 0:
        return 0, 0, 0.0
    
    return pass_count, total_count, pass_count / total_count

def process_directory(base_dir):
    """
    Process all tasks in the given directory and calculate pass rates
    
    Args:
        base_dir (str): Base directory containing task directories
        
    Returns:
        dict: Dictionary mapping task IDs to their pass rates
    """
    results = {}
    
    # Check if base_dir exists
    if not os.path.exists(base_dir):
        print(f"Error: Directory not found: {base_dir}")
        return results
    
    # Iterate through all subdirectories
    # print(os.listdir(base_dir))
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        
        # Check if it's a directory
        if os.path.isdir(item_path):
            instance_id = extract_instance_id(item_path)
            test_results = parse_test_logs(item_path)
            
            if test_results:
                pass_count, total_count, pass_rate = calculate_pass_rate(test_results)
                results[instance_id] = {
                    "pass_count": pass_count,
                    "total_count": total_count,
                    "pass_rate": pass_rate
                }
                # print(f"{instance_id}: {pass_count}/{total_count} tests passed ({pass_rate:.2%})")
    
    return results

def get_pass_rates(directory):
    results = process_directory(directory)
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python calculate_passed_test_cases.py <directory>")
        return
    
    directory = sys.argv[1]
    results = process_directory(directory)
    
    # Print overall summary
    if results:
        total_tasks = len(results)
        avg_pass_rate = sum(task["pass_rate"] for task in results.values()) / total_tasks if total_tasks > 0 else 0
        print(f"\nOverall Summary:")
        print(f"Total tasks: {total_tasks}")
        print(f"Average pass rate: {avg_pass_rate:.2%}")
        
        # Save results to a JSON file
        output_file = "task_pass_rates.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {output_file}")
    else:
        print("No test results found.")

if __name__ == "__main__":
    main()