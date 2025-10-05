---
description: this is a list of commands and prompt aliases that can be used to interact with the agent.
globs: 
alwaysApply: true
---



# Command Aliases
--------------------------------

The following are **command aliases**:

.c -> continue
. -> see attached logs/content
.m -> read ALL the core memory files; my question will come on the next turn. do not return control to the user until you have read ALL the core memory files
.mc -> .m, then .c (this is for transitioning from a too-long chat to a fresh one)
.mr <arg> -> use `npx repomix --quiet --include _memory/ --ignore _memory/knowledgeBase --style markdown --stdout`, then ARG. Your first response MUST be a tool call to the repomix tool.
.m <arg> -> .m THEN <arg>
.um -> update memory
.ts -> update _memory/currentState/currentTaskState.md with the current state and progress, and (if applicable) all previous attempts and outcomes. Also update currentEpic.md and/or theBacklog.md if applicable. Make sure that these files contain enough detail for a new agent to pick up the task where you left off.
.r -> run it yourself
.cn -> please give me a standalone prompt to use for the next agent to continue this process. it will not have access to this conversation, only the memory and codebase.
.rj -> repeat ("reinject") the user's goals, plan, and instructions into the conversation
.rrr <optional-arg> -> re-read the rules files (or <arg> if specified)
.? -> list commands and prompt aliases

The following are **prompt aliases**. They refer to prompts found elsewhere in the context, and can take arguments (space-delimited, treating quoted items as one argument).

.ip -> Interactive Planning
.bp -> Blueprint
.bpp -> Blueprint w Prompts

## Interactive Planning 

(if you haven't already, read the core memory files)

Ask me one question at a time so we can develop a both a high-level plan, fleshing out all the requirements and constraints, and then a thorough, step-by-step spec for the below idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail.  Remember, only one question at a time.

 IDEA: {arg1}

**Remember, only one question at a time!**

## Blueprint

Draft a detailed, step-by-step blueprint for building {arg1}. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.  
  
From here you should have the foundation to provide a series of tasks for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each task builds on the previous prompts, There should be no hanging or orphaned code that isn't integrated into a previous step.  Make sure that the tasks provide working functionality incrementally, without a big bang integration at the end. 

## Blueprint w Prompts

Same as Blueprint, but once you have reached the lowest level of detail, generate a complete LLM prompt for each task.
  
Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.


 
