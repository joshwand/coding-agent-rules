---
description: this is the global rules file. it contains rules that apply to all prompts.
globs: 
alwaysApply: true
---


  Response Style

  - Be concise (fewer than 4 lines unless detail requested)
  - Direct answers without preamble/postamble
  - Use tools to complete tasks, not for communication
  - Minimize output tokens while maintaining quality
--------------------------------
# VERY IMPORTANT: 
--------------------------------
Your first response MUST include:
1: a list of all the rules files whose contents you have alredy read
2. a tool call to the repomix tool (npx repomix --quiet --include _memory/ --ignore _memory/knowledgeBase --style markdown --stdout)


You may have access to a task tracking system. If you do, do NOT use it. 
Instead, use the _memory/currentState/ files to track your short and medium term tasks, and as a working memory and scratchpad.

