---
name: memory-bank
description: The _memory/ directory schema for durable project context. Use when reading project memory at the start of unfamiliar work, when asked to update memory (.um), when updating task state (.ts), or when creating any file under _memory/.
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
    designs/*
    domainKnowledge/*
    reference/*
    requirements/*
```

Templates live in `_memory/_templates/`. Read the relevant template before creating a new memory file or making large changes to an existing one. If no template exists, follow the purpose described below.

## basicTruths/

Slow-changing facts about the project. Read these when starting work on an unfamiliar project.

- **productContext.md** — why this project exists, the problems it solves, how it should work, user experience goals.
- **projectScope.md** — the foundation document that shapes the others. Core requirements and goals; the source of truth for what is and isn't in scope. Create at project start if absent.
- **repoStructure.md** — how the repository is laid out: top-level directories, where each kind of code lives, and any layout that would surprise someone new.
- **systemArchitecture.md** — high-level architecture, key technical decisions, design patterns in use, component relationships.
- **theBacklog.md** — prioritized list of features and tasks, plus recent changes.
- **theTechContext.md** — technologies, technical constraints, dependencies, development setup, build and deployment instructions, standards and conventions.

## currentState/

Fast-changing working context.

- **currentEpic.md** — current work focus, next steps within that focus, active decisions and considerations, recent changes.
- **currentTaskState.md** — working memory for the concrete task in flight. Holds the current goal, the yak-shaving stack (the chain of dependency tasks blocking the real one), a scratchpad, and a log of what each turn did. Update it as the task moves, and keep the template's own instructions in the file rather than stripping them out.

## knowledgeBase/

Optional reference material, read only when relevant to the task at hand. List the directory to see what exists rather than reading the whole tree.

- **designs/** — one file per major component or cross-cutting concern, written when you design or redesign it. `designs/AuthAndSecurity.md`, `designs/Billing.md`, `designs/Payments.md`.
- **domainKnowledge/** — domain facts worth keeping. `domainKnowledge/CustomerPersonas.md`, `domainKnowledge/LoanProcess.md`.
- **reference/** — technical or business reference data. `reference/stripe_api_reference.md`, `reference/deploymentRunbook.md`.
- **requirements/** — one file per epic or feature, in user story format; a single file may hold several stories. `requirements/01-login-reqs.md`, `requirements/02-signup-reqs.md`.

## Loading memory

To pull the whole memory bank into context in one call, excluding the knowledge base:

```
npx repomix --quiet --include _memory/ --ignore _memory/knowledgeBase --style markdown --stdout
```

## Updating memory

Update when you discover a project pattern worth keeping, after implementing something significant, or when context turns out to be wrong or missing.

On an explicit "update memory" (`.um`), review every core file even if some need no change, paying particular attention to `currentTaskState.md` and `currentEpic.md`. The bar for the update: could an agent with no access to this conversation continue the work from the files alone?

Renamed over time, in case you meet an older tree: `systemPatterns.md` → `systemArchitecture.md`, `activeContext.md` → `currentEpic.md`, `taskState.md` → `currentTaskState.md`.
