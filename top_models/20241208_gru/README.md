# Gru.ai

Gru.ai is an advanced AI developer designed to assist you in solving technical issues such as coding/testing/debugging, building algorithms, solutions. Gru is built to be professional, reliable and deliver high quality results.

Learn more about Gru here:

-   [Gru.ai](https://gru.ai)
-   [Gru.ai/blog](https://gru.ai/blog)
-   [Discord](https://discord.gg/jGNWxZbCXs)
-   [Youtube](https://www.youtube.com/channel/UCAIIFJR9CItz7SM-Kjx_YhQ)
-   [Twitter](https://twitter.com/BabelCloudAI)

# SWE-bench

The SWE-bench cases are handled by Gru, which is designed to solve issues of a given repo.

## Results

| Total Instances | Patch Generated | Unresolved | Partially Resolved | Resolved | Resolved Rate |
| --------------- | --------------- | ---------- | ------------------ | -------- | ------------- |
| 500             | 500             | 197        | 17                 | 286      | 57.20%        |

## Approach

The Gru has the following setup:

**Task Init:** The init task sets the docker env for Gru. System sends information including repo, commit and issue description to Gru. Because this task is procedural, it is not shown in the agent plan.

**Task 1:** Find files related to the issue. Gru should decide by itself which files to read, which directories to list or search code. Basically Gru explores the codebase, read what it’s interested and saves findings to file `interested-files.yml`.

**Task 2:** Make decisions of what files to change and how to change. Gru will reference the result of task 1 `interested-files.yml`, read more details of the code and make a decision of which files to change and how to change and saves change plan to `file-change-plan.yml`.

**Task 3 (Optional):** This task serves as a mechanism to validate and isolate the issue. It is intended to create a script that can reproduce the issue in the current environment. (a) If the reproduce script is successfully created and saved in the file `gru_reproduce.py`, Gru must execute it during Task 4 (Ground Changes) to ensure the issue no longer reproduces. If Task 4 fails after using the reproduce script, Gru will enter Task 5 (Revise Changes) with the reproduce mechanism disabled. The repository will be reset to its initial state, and Gru will retry the process. (b) If the reproduce script is not created, Gru will proceed to Task 4 and ignore the reproduce script.

**Task 4:** Ground the changes according to the change plan from task 2. We have meticulously curated a tool `editFile` that allows Gru to make micro changes to a file. Gru can also use bare bash commands to make changes. As there are different approaches to solve an issue and there may not be a perfect solution, Gru will decide by itself if modification of files is sufficient and finish this task.

**Task 5:** Generate diff patch and review changes. In very few cases, Gru will make additional edits in this task.

**Task Summary:** Gru will summarize what has been done during the task and upload deliverables(including the patch file and intermediate files) to S3 and return a summary with links to the user(which is evaluation harness in SWE-bench cases). Because this task is procedural, it is not shown in the agent plan.

For each of the task 1-4, we have a hard limitation of 30 steps. If exceeds, the task will be ended by system and gru will be forced to move on to the next task. As gru can almost do anything during a task, it is not rare see gru making compensations for previous tasks. In very rare cases, gru failed the whole job that means failed to generate a patch.

More details can be found in [The Road to Ultimate Pull Request Machine](https://gru.ai/blog/road-to-ultimate-pull-request-machine/).

## Checklist

-   [x] Is a pass@1 submission (does not attempt the same task instance more than once)
-   [x] Does not use SWE-bench test knowledge (`PASS_TO_PASS`, `FAIL_TO_PASS`)
-   [x] Does not use the `hints` field in SWE-bench
-   [x] Does not have web-browsing OR has taken steps to prevent lookup of SWE-bench solutions via web-browsing
