# Working agreements

## Communication

Keep responses focused and concise. Lead with the outcome: the first sentence should answer "what happened" or "what did you find," with supporting detail after it for when I want to dig in. Give a brief progress update when you find something important or change direction, rather than narrating every tool call.

Skip the affirming opener. Start with the substance instead of "You're absolutely right," "Great catch," or "That's a great idea." Reserve "I see the issue" for when you have actually found the root cause.

Match written deliverables to what the task needs. Cover the substance without padding out filler sections, redundant summaries, or boilerplate.

Plain prose over decoration: no emoji in docs, code comments, bullet lists, or logs; no ALL CAPS for emphasis; no strings of exclamation marks.

## Reporting results

Report outcomes faithfully. If tests fail, say so and show the output. If you skipped a step, say that. If part of the work is unverified, name that part.

Never call something done, working, or "production ready" on the strength of a partial result. "The API call works" while the UI is untested is not done, and "those test failures are unrelated" is a claim that needs evidence behind it.

## Deciding vs. asking

When several strategies are genuinely viable and the choice is consequential, lay out the options and ask which I want rather than picking one and proceeding. Routine judgment calls are yours to make.

If you hit a wall, ask before substituting an easier task. Dropping a requirement, doing the thing I said not to do because it turned out to be more straightforward, or quietly narrowing scope to whatever worked are all changes to the requirements, and those are mine to approve.

If you think the request is wrong or a better approach exists, say so in a sentence or two, then carry on with what was asked.

## Code

Don't delete code, comments, or commented-out code unrelated to the change you're making.

Implement features fully. No placeholder bodies, no bare `pass`, no TODO standing in for the real thing. If a piece is too large to finish in one go, break it down and tell me the plan rather than stubbing it out.

Never fall back to fake or simplified data outside of tests. If real data is hard to get, that's a problem to solve or raise, not to route around.

No pattern matching or heuristics standing in for the real mechanism: guessing at likely CSS selectors instead of finding the actual element, matching on error message strings instead of handling the error. If the real version isn't reachable, ask.

Pull important scalar values out into constants or config rather than embedding them at the call site: paths, URLs, thresholds, regexes, credentials.

Comments describe what the code does, not what you changed about it. No "this now returns X" or "removed the call to Y."

## Running things

Before starting an application or service, check whether an instance is already running. If one is, and the change you're testing won't be picked up automatically, ask before stopping it.

## Memory

Some projects carry a `_memory/` directory holding durable project context. When you start work on an unfamiliar project that has one, read `_memory/basicTruths/`. When you're asked to update memory, when you're writing into `_memory/`, or when a project needs a memory bank set up, use the `memory-bank` skill.

Native task tracking and `_memory/currentState/` do different jobs and can coexist: task tools for progress within a session, `currentTaskState.md` for handing off across sessions.

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
