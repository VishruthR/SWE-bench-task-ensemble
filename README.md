# SWE-Bench w/ Ensemble Agents

## Overview

SWE-bench is a benchmark that measures an AI agents ability to solve real-world software engineering tasks by submitting patches for issues on open-source repositories. Many agents have attempted the various SWE-bench tasks and the best models complete about 64% of issues on the SWE-bench verified dataset. We want to test if using an ensemble method using multiple agents can improve performance on SWE-bench. Specifically, if we take the best output for each AI agent on each task, how much does our performance on SWE-bench improve?

## Methodology

SWE-bench works by giving an AI agent a repository and an issue text description. The AI agent writes a patch that is then applied to the codebase. Finally, the test cases within the codebase are run to ensure the patch passes all unit tests. We propose that selecting the best patch out of a group of patch generations from various AI agents will outperform the performance of a single AI agent.

We must find a way to identify the best patch for each task. To do this, we will use the test case generation method proposed by UTBoost. For each task, we will genarate test cases to verify if the issue was resolved appropriately. It is important to note that within SWE-bench, each task has one or more unit tests added to it to verify that the issue has been fixed correctly (these are unit tests usually written by a human developer when the issue was solved in the real repository). To ensure we are not selecting the best patch based on the unit tests added after the issue has been resolved, we replace those unit tests with the ones we generate using UTBoost. This means we only select models based on the existing test cases in the repository before the issue was resolved and the new test cases we generated.