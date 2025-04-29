Command to run SWE Bench harness: 
```
python -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_Lite \
    --predictions_path /home/ec2-user/dkang_starter_task/experiments/evaluation/lite/20250214_agentless_lite_o3_mini/all_preds.jsonl \
    --max_workers 8 \
    --cache_level instance \
    --run_id test_basic_eval_lite
```

Concatenate diffs:
```
python concatenate_diffs.py \
    --test-cases /home/ec2-user/dkang_starter_task/generated_test_cases.json \
    --predictions /home/ec2-user/dkang_starter_task/top_models/20241208_gru/all_preds.jsonl \
    --output /home/ec2-user/dkang_starter_task/gru_updated_patch.jsonl
```

Will run on 100 randomly sampled tasks from the SWE-bench verified set.

File with test cases: `/home/ec2-user/dkang_starter_task/UTBoost/generated_test_cases/dir_generated_test_cases/verified_new_gen_testCase_t099_lm01_extracted/output_320_processed.json`

Sources
- https://anonymous.4open.science/r/UTBoost-7224/readme.md 
- UTBoost paper
- https://github.com/SWE-bench/experiments?tab=readme-ov-file
- https://github.com/SWE-bench/SWE-bench
- PerplexityAI, understanding UTBoost system and SWEBench
- Github Copilot + Clause 3.7 Sonnet: Code generation primarily for scripts; setting up EC2 instance

Challenges:
- How to apply the new test cases to the repository

python -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_Verified \
    --predictions_path /home/ec2-user/dkang_starter_task/top_models/20250316_augment_agent_v0/all_preds.jsonl \
    --max_workers 8 \
    --cache_level instance \
    --run_id test_single_instance_patch \
    --instance_ids django__django-15104 \
    --clean True

Running each model takes about 6-10 minutes

Running 20 takes 2-3 hours O_O