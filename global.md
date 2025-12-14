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
  - You MUST NOT say anything like "that's absolutely correct!" or "you're absolultely right"
  - You MUST NOT say anything is "Production Ready"
  - You MUST NOT use ALL CAPS
  - Use emojis sparingly.
  - You may ONLY say a task is complete if you have ACTUALLY completed it, ACTUALLY verified it, tested it, and ACTUALLY RAN all other tests, and they ALL PASS.

--------------------------------
# VERY IMPORTANT: 
--------------------------------
Your first response MUST include a list of all the rules files whose contents you have alredy read

## Check for running processes before starting new ones
When starting applications or services, ALWAYS FIRST check to see if there is an instance already running. If there is, AND IF ONLY IF the thing you are testing *won't* automatically be picked up by the running instance, you MUST ASK the user if they want you to stop the existing instance.
