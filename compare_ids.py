import json
import os
import glob

# finds common instance ids between UTGenerator output and patch prediction format

def find_common_instance_ids():
    test_case_file = "/home/ec2-user/dkang_starter_task/generated_test_cases.json"
    
    model_dir = "/home/ec2-user/dkang_starter_task/top_models/"
    
    with open(test_case_file, 'r') as f:
        json_data = json.load(f)
    
    test_gen_instance_ids = set(json_data.keys())
    
    jsonl_files = glob.glob(os.path.join(model_dir, "**", "all_preds.jsonl"), recursive=True)
    
    results = {}
    
    for jsonl_file in jsonl_files:
        model_name = os.path.basename(os.path.dirname(jsonl_file))
        model_patch_instance_ids = set()
        
        with open(jsonl_file, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if "instance_id" in data:
                        model_patch_instance_ids.add(data["instance_id"])
                except json.JSONDecodeError:
                    continue
        
        common_ids = test_gen_instance_ids.intersection(model_patch_instance_ids)
        
        if common_ids:
            results[model_name] = list(common_ids)
    
    if results:
        print("\nCommon instance_ids found in:")
        for model_name, common_ids in results.items():
            print(f"- {model_name}: {len(common_ids)} common IDs")
            # if len(common_ids) <= 10:  # Print all if not too many
            #     print(f"  IDs: {', '.join(common_ids)}")
            # else:
            #     print(f"  Sample IDs: {', '.join(common_ids[:5])}...")
        
        # Print all common instance_ids across all JSONL files
        all_common = set(list(results.values())[0])
        for common_ids in results.values():
            all_common = all_common.intersection(common_ids)
        print(f"\nTotal unique common instance_ids across all models: {len(all_common)}")
        if len(all_common) <= 20:
            print(f"IDs: {', '.join(sorted(all_common))}")
    else:
        print("\nNo common instance_ids across all found.")

    # Save common instance IDs to a file
    if all_common:
        with open("instance_id_pool.txt", "w") as f:
            for instance_id in sorted(all_common):
                f.write(f"{instance_id}\n")
        print(f"Common instance IDs saved to instance_id_pool.txt")

    return results

if __name__ == "__main__":
    find_common_instance_ids()