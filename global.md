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

YOUR FIRST TWO TURNS: 

Your first response must always be a tool call to read the memory (`.mr` command). Your second response must always be a tool call to read the output ("repomix-output.md"). 

Task Tracking:

You may have access to a task tracking system. If you do, do NOT use it. 
Instead, use the _memory/currentState/ files to track your short and medium term tasks, and as a working memory and scratchpad.

