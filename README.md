# Coding Agent Rules

A small set of rules for use with a coding agent, installed into a project as `CLAUDE.md` or `AGENTS.md`. An evolving work in progress, as coding agents themselves evolve.

## What changed, and why

This repo used to carry about 720 lines of rules: software engineering principles, guardrails against bad agent behavior, a mode machine, and a step-by-step interaction loop. Most of that was written to patch behaviors that models of the time actually had. They overclaimed completion, left placeholders behind, picked a strategy without asking, wandered off scope, and forgot to run the tests.

In July 2026 Anthropic published two pieces arguing that corpus has become a liability on frontier models:

- [The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) — the Claude Code team cut over 80% of their system prompt with no measurable loss on coding evaluations. The reversals: give judgment rather than rules, design better tool interfaces rather than supplying examples, disclose progressively rather than front-loading, and point at rich references (code, test suites) rather than verbose markdown.
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) — in particular: explicit verification instructions now cause *over*-verification and cost tokens without improving results, and positive examples of the style you want beat lists of things not to do.

So the ruleset was cut to roughly 110 always-on lines. What survives is the part a model cannot infer from the codebase: personal command shorthand, tone preferences, and the agreements about when to ask rather than decide. What went is everything that was compensating for a weaker model.

Specifically removed: the textbook principles (DRY, KISS, YAGNI, and friends, decorated with metrics nothing measured); four overlapping verification principles collapsed into one line about reporting honestly; a rule to `cd` to an absolute path before every command, which now fights the harness rather than helping it; a mandated first-response tool call; an instruction not to use native task tracking; the mermaid state machines; and the long lists of phrasings not to use.

Non-Anthropic frontier models have made comparable gains, so there is no legacy profile here. If you are driving an older or smaller model, `git log` has the fuller version.

## Components

### `core.md`

The always-on rules. Communication and tone, honest reporting of results, when to ask rather than decide, a short list of code preferences, and a pointer at the memory bank.

### `commands.md`

Command and prompt aliases. Short tokens so you can steer without a lot of typing: `.c` to continue, `.v` to verify, `.ts` to update task state, `.ip` to plan interactively. This is the highest-value file in the repo, because it is pure personal vocabulary that no model can guess at.

### `skills/`

The two blocks that are large but only situationally needed, kept out of the always-on context and loaded on demand:

- `memory-bank` — the full `_memory/` schema. Loads when reading project memory or writing to it.
- `interactive-planning` — the one-question-at-a-time elicitation prompt behind `.ip`.

### Structured memory

Credit where due: the memory bank is an adaptation of the [Cline Memory Bank](https://docs.cline.bot/improving-your-prompting-skills/cline-memory-bank).

Its purpose is ongoing documentation of the project's purpose, scope, architecture, roadmap, and status. If you're an engineer, think of it as:

1. The documentation and onboarding you'd give a new engineer joining the project.
2. The backlog and roadmap a product manager would maintain.
3. The status updates you'd give your PM and stakeholders.
4. Your working notes as you [yak](https://projects.csail.mit.edu/gsb/old-archive/gsb-archive/gsb2000-02-11.html)-[shave](https://youtu.be/AbSehcT19u0) your way through a feature or bug.

Memory lives in `_memory/`, in a structure documented by the `memory-bank` skill. A structured memory makes the agent understand the project more reliably than an unstructured pile of atomic memories or a single freetext file.

Now that agents ship their own automatic memory, this is less load-bearing than it was. It still earns its place for handing work across sessions and for context you want to curate deliberately rather than accumulate incidentally.

## Installation

`install-rules.sh` wraps `rules_manager.py`, which does the actual work. Run it from your project root, pointing at your clone of this repo:

```bash
bash /path/to/coding-agent-rules/install-rules.sh
```

That writes `CLAUDE.md` into the current directory. To target a different directory, pass it as an argument:

```bash
bash /path/to/coding-agent-rules/install-rules.sh /path/to/your/project
```

### Options

- `--agent <name>` — output target. `claude` (default) writes `CLAUDE.md`; `agentsmd` writes `AGENTS.md`. The contents are identical.
- `--output <filename>` — write to a custom filename instead. Cannot be combined with `--agent`.
- `--install-skills` — copy `skills/*` into the target project's `.claude/skills/`.
- `--init-memory` — scaffold an empty `_memory/` structure in the target directory.
- `--exclude <file.md>` — leave a rule file out of the generated output. Repeatable.
- `--list-files` — show which rule files, skills, and templates would be used, then exit.

A typical first-time setup for a project:

```bash
bash /path/to/coding-agent-rules/install-rules.sh --install-skills /path/to/your/project
bash /path/to/coding-agent-rules/install-rules.sh --init-memory /path/to/your/project
bash /path/to/coding-agent-rules/install-rules.sh /path/to/your/project
```

Only the files named in `RULE_FILES` in `rules_manager.py` ship. Adding a markdown file to the repo root does not put it in every project's `CLAUDE.md`; add it to that list deliberately.

## Workflow

### Interactive planning

alias: `.ip`

Plan a project or feature with the agent before building it. It asks a series of clarifying questions, one at a time, until the requirements and constraints are pinned down and you have a spec you could hand to a developer. Use the strongest thinking model you can afford for this stage.

### Starting a project

Run `.ip <the goal of the project>`, then `.um` to write the result into memory. On an existing codebase, let the agent read widely first.

### Day to day

1. `.m <your current goal>` to load memory and start work.
2. Build.
3. `.ts` to record task state before the context gets long, or `.cn` to generate a handoff prompt for a fresh session.
4. `.um` when something worth keeping has changed.

### Modes

Some people define explicit agent modes with strict rules about what's allowed in each. The previous version of this repo had one. It's been removed: on current models it produced ceremony rather than better work.

## Related tools

### Repomix

[Repomix](https://repomix.com/) bundles a codebase, or a subset of one, into a single file you can drop into context. Useful for pulling the whole memory bank in with one call:

```
npx repomix --quiet --include _memory/ --ignore _memory/knowledgeBase --style markdown --stdout
```

## References and inspiration

- [The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Cline Memory Bank](https://docs.cline.bot/improving-your-prompting-skills/cline-memory-bank)
- [Harper Reed: My LLM Codegen Workflow at ATM](https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/)
