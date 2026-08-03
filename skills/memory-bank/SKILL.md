---
name: memory-bank
description: The _memory/ directory schema for durable project context. Use when setting up a memory bank for a project, reading project memory at the start of unfamiliar work, when asked to update memory (.um), when updating task state (.ts), or when creating any file under _memory/.
---

# Memory bank

`_memory/` holds durable project context that outlives a single session. Read it to pick up work; write to it so the next session can.

## Structure

```
_memory/
  basicTruths/
    productContext.md
    projectScope.md
    repoStructure.md
    systemArchitecture.md
    theBacklog.md
    theTechContext.md
  currentState/
    currentEpic.md
    currentTaskState.md
  knowledgeBase/
    designs/
    domainKnowledge/
    reference/
    requirements/
```

## basicTruths/

Slow-changing facts about the project. Read these when starting work on an unfamiliar project.

- **productContext.md** — why this project exists, the problems it solves, how it should work, user experience goals.
- **projectScope.md** — the foundation document that shapes the others. Core requirements and goals; the source of truth for what is and isn't in scope.
- **repoStructure.md** — how the repository is laid out: top-level directories, where each kind of code lives, and any layout that would surprise someone new.
- **systemArchitecture.md** — high-level architecture, key technical decisions, design patterns in use, component relationships.
- **theBacklog.md** — prioritized list of features and tasks, plus recent changes.
- **theTechContext.md** — technologies, technical constraints, dependencies, development setup, build and deployment instructions, standards and conventions.

## currentState/

Fast-changing working context.

- **currentEpic.md** — current work focus, next steps within that focus, active decisions and considerations, recent changes.
- **currentTaskState.md** — working memory for the concrete task in flight. Holds the current goal, the yak-shaving stack (the chain of dependency tasks blocking the real one), a scratchpad, and a log of what each turn did. Follow `templates/currentTaskState.md` in this skill directory, and keep the template's own instructions in the file rather than stripping them out.

## knowledgeBase/

Optional reference material, read only when relevant to the task at hand. List the directory to see what exists rather than reading the whole tree.

- **designs/** — one file per major component or cross-cutting concern, written when you design or redesign it. `designs/AuthAndSecurity.md`, `designs/Billing.md`, `designs/Payments.md`.
- **domainKnowledge/** — domain facts worth keeping. `domainKnowledge/CustomerPersonas.md`, `domainKnowledge/LoanProcess.md`.
- **reference/** — technical or business reference data. `reference/stripe_api_reference.md`, `reference/deploymentRunbook.md`.
- **requirements/** — one file per epic or feature, in user story format; a single file may hold several stories. `requirements/01-login-reqs.md`, `requirements/02-signup-reqs.md`.

## Setting up a memory bank

When a project has no `_memory/` yet, create the tree above. Two ways to fill it, and the choice matters:

**If the project already has code**, don't write placeholder files. Read the repo first — README, package manifests, directory layout, entry points, CI config, existing docs — and write `basicTruths/` from what you actually find. A `repoStructure.md` derived from the real tree is worth more than six stub files. Say plainly which files you had to guess at, and ask about anything the code can't tell you: why the project exists, who it's for, what's deliberately out of scope.

**If the project is new or you're starting from an idea**, run the `interactive-planning` skill first and write the resulting spec into `projectScope.md` and `productContext.md`. The rest can stay thin until there's something to describe.

Either way: create `currentState/currentTaskState.md` from `templates/currentTaskState.md`, leave `currentEpic.md` as a short stub until there's an actual epic, and create the four `knowledgeBase/` subdirectories empty (add `.gitkeep` files if the project tracks empty directories).

Never invent architecture, scope, or backlog content to fill a section out. An empty heading with a note saying what's missing is honest; a plausible-sounding fabrication becomes a false basic truth that every later session inherits.

## Loading memory

To pull the whole memory bank into context in one call, excluding the knowledge base:

```
npx repomix --quiet --include _memory/ --ignore _memory/knowledgeBase --style markdown --stdout
```

## Updating memory

Update when you discover a project pattern worth keeping, after implementing something significant, or when context turns out to be wrong or missing.

On an explicit "update memory" (`.um`), review every core file even if some need no change, paying particular attention to `currentTaskState.md` and `currentEpic.md`. The bar for the update: could an agent with no access to this conversation continue the work from the files alone?

Renamed over time, in case you meet an older tree: `systemPatterns.md` → `systemArchitecture.md`, `activeContext.md` → `currentEpic.md`, `taskState.md` → `currentTaskState.md`.
