---
description: this is the global rules file. it contains rules that apply to all prompts.
globs: 
alwaysApply: true
---

## Response Style

  - Be concise (fewer than 4 lines unless detail requested)
  - Direct answers without preamble/postamble
  - Use tools to complete tasks, not for communication
  - Minimize output tokens while maintaining quality
  - You are ABSOLUTELY FORBIDDEN from saying anything like "that's absolutely correct!" or "you're absolultely right"
  - You are absolutely forbidden from saying anything is "Production Ready"
  - Use emojis sparingly.
  - You may ONLY say a task is complete if you have completed it, tested it, and all other tests pass.

--------------------------------
# VERY IMPORTANT: 
--------------------------------
Your first response MUST include:
1: a list of all the rules files whose contents you have alredy read
2. a tool call to the repomix tool (npx repomix --quiet --include _memory/ --ignore _memory/knowledgeBase --style markdown --stdout)


## Task Tracking:

You may have access to a task tracking tool. If you do, do NOT use it. 
Instead, use the _memory/currentState/ files to track your short and medium term tasks, and as a working memory and scratchpad.

## Check for running processes before starting new ones
When starting applications or services, ALWAYS FIRST check to see if there is an instance already running. If there is, AND IF ONLY IF the thing you are testing *won't* automatically be picked up by the running instance, you MUST ASK the user if they want you to stop the existing instance.
