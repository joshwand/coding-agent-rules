# Command aliases

Shorthand I use in prompts. When a message is one of these tokens, expand it as follows.

```
.c                  continue
.                   see attached logs/content

.r                  run it yourself
.v                  verify that the work you have done is correct and works as expected
.pi                 prove it: show the passing tests, the screenshot, the actual output
.nd, .ndy, .ynd     not done until the functionality completely works; no partial victories
.cn                 give me a standalone prompt for the next agent to continue this process.
                    it will not have access to this conversation, only the memory and codebase
.rj                 repeat ("reinject") my goals, plan, and instructions into the conversation
.rrr <optional-arg> re-read the rules files (or <arg> if specified)
.dr, .ds            don't start new instances of running processes; anything already running
                    will pick up the changes automatically
.nyr, .inar, .ynar  drop the affirming openers ("you're absolutely right", "great catch")

.?                  list commands and prompt aliases
```

# Prompt aliases

These expand into a prompt rather than a one-line instruction. They take space-delimited arguments, treating quoted items as a single argument.

```
.ip <idea>          Interactive Planning — use the `interactive-planning` skill
.m <arg>            load memory, then do <arg>:
                    npx repomix --quiet --include _memory/ --ignore _memory/knowledgeBase --style markdown --stdout
.mc                 .m, then .c — for moving a too-long chat into a fresh one
.um                 update memory — use the `memory-bank` skill
.ts                 update _memory/currentState/currentTaskState.md with the current state and
                    progress, including previous attempts and their outcomes. Update
                    currentEpic.md and theBacklog.md if applicable. Leave enough detail that a
                    new agent can pick the task up where you left off.
```
