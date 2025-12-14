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

.r -> run it yourself
.v -> verify that the work you have done is correct and works as expected.
.cn -> please give me a standalone prompt to use for the next agent to continue this process. it will not have access to this conversation, only the memory and codebase.
.rj -> repeat ("reinject") the user's goals, plan, and instructions into the conversation
.rrr <optional-arg> -> re-read the rules files (or <arg> if specified)
.dr, .ds -> don't start new instances of running processes. if processes are alread running, they'll pick up the changes automatically.
.nyr, .inar, .ynar -> remember you are forbidden from saying anything like "that's absolutely correct!" or "you're absolultely right"

.? -> list commands and prompt aliases

The following are **prompt aliases**. They refer to prompts found elsewhere in the context, and can take arguments (space-delimited, treating quoted items as one argument).

.ip -> Interactive Planning
.bp -> Blueprint
.bpp -> Blueprint w Prompts

## Interactive Planning 

Ask me one question at a time so we can develop a both a high-level plan, fleshing out all the requirements and constraints, and then a thorough, step-by-step spec for the below idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. 

If you include more than one sub-question (less than ideal but sometimes necessary), you MUST number each one (1, 2, 3, etc.). If a sub-question is multiple choice, you MUST include a letter for each option. (A, B, C, etc.) This is so that the user can easily reference the sub-question they are answering with minimal typing.

 Remember, only one question at a time.

 IDEA: {arg1}

**Remember, only one question at a time!**
