Command to run SWE Bench harness: 
```
python -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_Lite \
    --predictions_path /home/ec2-user/dkang_starter_task/experiments/evaluation/lite/20250214_agentless_lite_o3_mini/all_preds.jsonl \
    --max_workers 8 \
    --cache_level env \
    --run_id test_basic_eval_lite
```

Will run on 100 randomly sampled tasks from the SWE-bench verified set.

Sources
- https://anonymous.4open.science/r/UTBoost-7224/readme.md 
- UTBoost paper
- https://github.com/SWE-bench/experiments?tab=readme-ov-file
- https://github.com/SWE-bench/SWE-bench
- PerplexityAI, understanding UTBoost system and SWEBench
- Github Copilot + Clause 3.7 Sonnet: Code generation primarily for scripts; setting up EC2 instance