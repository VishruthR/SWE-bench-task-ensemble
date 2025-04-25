#!/usr/bin/env python3
import json
import os
import shutil
import sys
from pathlib import Path

def copy_top_models():
    # Load the data.json file
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: data.json file not found")
        return
    except json.JSONDecodeError:
        print("Error: data.json is not valid JSON")
        return

    # Get the "Verified" leaderboard
    verified_leaderboard = None
    for leaderboard in data.get('leaderboards', []):
        if leaderboard.get('name') == 'Verified':
            verified_leaderboard = leaderboard
            break
    
    if not verified_leaderboard:
        print("Error: 'Verified' leaderboard not found in data.json")
        return

    # Sort models by resolved score (highest first)
    models = verified_leaderboard.get('results', [])
    models.sort(key=lambda x: x.get('resolved', 0), reverse=True)

    # Take top 20 models
    top_models = models[:20]
    
    # Create top_models directory if it doesn't exist
    top_models_dir = Path('top_models')
    top_models_dir.mkdir(exist_ok=True)

    # Source directory for model folders
    source_dir = Path('experiments/evaluation/verified')
    
    # Copy each model folder
    for i, model in enumerate(top_models, 1):
        folder_name = model.get('folder')
        if not folder_name:
            print(f"Warning: Model {model.get('name')} doesn't have a folder name")
            continue
        
        src_path = source_dir / folder_name
        dst_path = top_models_dir / folder_name
        
        if not src_path.exists():
            print(f"Warning: Source folder not found: {src_path}")
            continue
        
        # Remove destination if it already exists
        if dst_path.exists():
            if dst_path.is_dir():
                shutil.rmtree(dst_path)
            else:
                dst_path.unlink()
        
        # Copy the directory
        try:
            shutil.copytree(src_path, dst_path)
            print(f"#{i}: Copied {model.get('name')} ({folder_name}) - Score: {model.get('resolved')}")
        except Exception as e:
            print(f"Error copying {folder_name}: {e}")

if __name__ == "__main__":
    print("Starting to copy top 20 verified models...")
    copy_top_models()
    print("Done!")