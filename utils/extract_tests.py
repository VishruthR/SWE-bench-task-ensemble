#!/usr/bin/env python3
import re
import sys
import os
import json
import argparse
from pathlib import Path

"""
Extracts test cases that were added in a git diff

AI Gen using GitHub Copilot + Clause Sonnet 3.7
"""

def extract_test_names(diff_content):
    """
    Extract test method names from a git diff content.
    
    Args:
        diff_content (str): Content of the git diff
        
    Returns:
        list: List of extracted test names
    """
    # Pattern to match added lines (starting with '+') that define test methods
    # The pattern looks for lines that start with + followed by whitespace, then 'def test_'
    test_pattern = re.compile(r'^\+\s*def\s+(test_\w+)\(', re.MULTILINE)
    
    matches = test_pattern.findall(diff_content)
    
    return matches

def process_json_file(input_file):
    """
    Process a JSON file containing git diffs and extract test names.
    
    Args:
        input_file (str): Path to the JSON file containing git diffs
        
    Returns:
        dict: Dictionary with instance IDs as keys and lists of test names as values
    """
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    results = {}
    
    for instance_id, diff_content in data.items():
        # Skip empty diffs
        if not diff_content:
            results[instance_id] = []
            continue
        
        test_names = extract_test_names(diff_content)
        results[instance_id] = test_names
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Extract test names from git diff files or JSON')
    parser.add_argument('input', help='Path to input file (git diff file or JSON)')
    parser.add_argument('-o', '--output', help='Path to output JSON file (for JSON input only)', default='added_test_cases.json')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output')
    
    args = parser.parse_args()
    
    input_file = args.input
    
    if args.verbose:
        print(f"Processing JSON file: {input_file}")
    
    results = process_json_file(input_file)
    
    output_file = args.output
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    if args.verbose:
        total_test_count = sum(len(tests) for tests in results.values())
        instance_count = len(results)
        instances_with_tests = sum(1 for tests in results.values() if tests)
        
        print(f"\nResults saved to {output_file}")
        print(f"Processed {instance_count} instance IDs")
        print(f"Found {instances_with_tests} instances with test additions")
        print(f"Total unique test names found: {total_test_count}")

if __name__ == '__main__':
    main()