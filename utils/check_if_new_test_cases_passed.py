"""
Checks if newly generated test cases passed

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
    parts = dir_name.split('-')[0].split('__')
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

def check_new_test_cases(instance_id, test_results, new_test_cases):
    """
    Check which new test cases passed or failed
    
    Args:
        instance_id (str): Instance ID (e.g., 'django__django-15104')
        test_results (dict): Mapping of test case names to their status
        new_test_cases (dict): Dictionary of instance IDs to lists of new test cases
        
    Returns:
        tuple: Lists of passed and failed test cases
    """
    if instance_id not in new_test_cases or not new_test_cases[instance_id]:
        return [], []
        
    simplified_test_cases = {
        test_name.split(" ")[0]: test_name for test_name in test_results.keys()
    }
    
    passed_tests = []
    failed_tests = []
    
    for test_case in new_test_cases[instance_id]:
        # Check if the test case exists in test_results
        full_test_case_name = simplified_test_cases[test_case]
        if full_test_case_name in test_results:
            if test_case == "test_custom_fk_with_hardcoded_to":
                print("here")
                print(test_results[full_test_case_name])
            status = test_results[full_test_case_name]
            if status == "PASSED":
                passed_tests.append(full_test_case_name)
            else:
                failed_tests.append((full_test_case_name, status))
        else:
            failed_tests.append((full_test_case_name, "NOT_RUN"))
    
    return passed_tests, failed_tests

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_if_new_test_cases_passed.py <directory>")
        return
    
    directory = sys.argv[1]
    instance_id = extract_instance_id(directory)
    test_results = parse_test_logs(directory)
    
    if not test_results:
        print(f"No test results found for {instance_id}")
        return
    
    # Load the new test cases
    try:
        with open("./added_test_cases.json", 'r') as json_file:
            new_test_cases = json.load(json_file)
    except FileNotFoundError:
        print("Error: added_test_cases.json file not found")
        return
    except json.JSONDecodeError:
        print("Error: added_test_cases.json is not valid JSON")
        return
    
    # Check which new test cases passed or failed
    passed_tests, failed_tests = check_new_test_cases(instance_id, test_results, new_test_cases)
    
    # Display results
    print(f"\nResults for new test cases in {instance_id}:")
    print("-" * 60)
    
    if instance_id in new_test_cases:
        if not new_test_cases[instance_id]:
            print(f"No new test cases defined for {instance_id}")
        else:
            print(f"Total new test cases: {len(new_test_cases[instance_id])}")
            
            if passed_tests:
                print(f"\nPassed test cases ({len(passed_tests)}):")
                for test in passed_tests:
                    print(f"  ✅ {test}")
            else:
                print("\nNo test cases passed.")
            
            if failed_tests:
                print(f"\nFailed test cases ({len(failed_tests)}):")
                for test, status in failed_tests:
                    print(f"  ❌ {test} ({status})")
            else:
                print("\nNo test cases failed.")
    else:
        print(f"No new test cases defined for {instance_id}")

if __name__ == "__main__":
    main()