
NoSideEffects: When applying changes, do not delete existing code, comments, commented-out code, etc. unless it is directly related to the code being changed.

CDAbsPathBeforeRun: Before running any command, cd into the *absolute path* to the required working directory first, e.g. `cd ~/code/projectdir/subdir && run_command_from_here`

The following are **command aliases**:

.c -> continue
. -> see attached logs/content
.r -> run it yourself
.mb -> read the memory bank; my question will come on the next turn
.umb -> update the memory bank
.ts -> update taskStatus.md with the current state and progress
.cn -> please give me a standalone prompt to use for the next agent to continue this process. it will not have access to this conversation, only the memory-bank and codebase.
.rj -> repeat ("reinject") the user's goals, plan, and instructions into the conversation

The following are **prompt aliases**. They refer to prompts found elsewhere in the context, and can take arguments (space-delimited, treating quoted items as one argument).

.ip -> Interactive Planning
.bp -> Blueprint


## Interactive Planning 

(if you haven't already, read the memory-bank)

Ask me one question at a time so we can develop a thorough, step-by-step spec for the below idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail.  Remember, only one question at a time.

 IDEA: {arg1}

Remember, only one question at a time.

---

## Blueprint

Draft a detailed, step-by-step blueprint for building {arg1}. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.  
  
From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.  
  
Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.
