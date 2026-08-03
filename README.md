# Coding Agent Rules

A small set of rules for use with a coding agent. Copy `AGENTS.md` (or `CLAUDE.md`, which is a symlink to it) into your project and you're done.

## What changed, and why

This repo used to carry about 720 lines of rules plus a Python installer that generated per-agent output: Cursor `.mdc` files, `.windsurfrules`, `CLAUDE.md`, `AGENTS.md`. Both the rules and the installer have been cut.

**The rules shrank from ~720 lines to 89.** Most of that corpus was written to patch behaviors that models of the time actually had. They overclaimed completion, left placeholders behind, picked a strategy without asking, wandered off scope, and forgot to run the tests. In July 2026 Anthropic published two pieces arguing that corpus has become a liability on frontier models:

- [The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) — the Claude Code team cut over 80% of their system prompt with no measurable loss on coding evaluations. The reversals: give judgment rather than rules, design better tool interfaces rather than supplying examples, disclose progressively rather than front-loading, and point at rich references (code, test suites) rather than verbose markdown.
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) — in particular: explicit verification instructions now cause *over*-verification and cost tokens without improving results, and positive examples of the style you want beat lists of things not to do.

What survives is the part a model cannot infer from the codebase: personal command shorthand, tone preferences, and the agreements about when to ask rather than decide. What went is everything that was compensating for a weaker model.

Specifically removed: the textbook principles (DRY, KISS, YAGNI, and friends, decorated with metrics nothing measured); four overlapping verification principles collapsed into one line about reporting honestly; a rule to `cd` to an absolute path before every command, which now fights the harness rather than helping it; a mandated first-response tool call; an instruction not to use native task tracking; the mermaid state machines; and the long lists of phrasings not to use.

**The installer is gone too.** `AGENTS.md` and `CLAUDE.md` are now well-established enough across agents that generating them per-target solved a problem that no longer exists. A build step that concatenates two markdown files into a third is worse than just having the file. Memory scaffolding moved into the `memory-bank` skill, where the agent creates the structure itself — and does it better than the old `--init-memory` flag did, because it reads the repo first and writes real content instead of six placeholder stubs.

Non-Anthropic frontier models have made comparable gains, so there is no legacy profile here. If you are driving an older or smaller model, `git log` has the fuller version.

## Installation

Copy or symlink the file into your project root:

```bash
cp /path/to/coding-agent-rules/AGENTS.md ./AGENTS.md
```

Symlinking instead means you pick up changes as this repo evolves:

```bash
ln -s /path/to/coding-agent-rules/AGENTS.md ./AGENTS.md
```

`CLAUDE.md` is a symlink to `AGENTS.md`, so either name works and the contents are identical. Use whichever your agent reads. If you want both, make the second a symlink to the first rather than keeping two copies in sync.

For the skills, copy them into your project (or into `~/.claude/skills/` to have them everywhere):

```bash
cp -r /path/to/coding-agent-rules/skills/* ./.claude/skills/
```

To supplement these rules with project-specific ones, append to your copy, or keep the symlink and add a second rules file alongside it.

## Contents

### `AGENTS.md`

The rules themselves. Communication and tone, honest reporting of results, when to ask rather than decide, a short list of code preferences, a pointer at the memory bank, and the command aliases.

The aliases are short tokens so you can steer without a lot of typing: `.c` to continue, `.v` to verify, `.ts` to update task state, `.ip` to plan interactively. This is the highest-value part of the repo, because it is pure personal vocabulary that no model can guess at.

### `skills/`

The blocks that are large but only situationally needed, kept out of the always-on rules and loaded on demand:

- **`memory-bank`** — the `_memory/` schema, how to set one up for a project, and how to keep it current. Bundles the `currentTaskState.md` template.
- **`interactive-planning`** — the one-question-at-a-time elicitation prompt behind `.ip`.
- **`handoff`** — the briefing behind `.cn`, for moving work into a fresh chat. Its output is written to the agent picking the work up rather than as a recap for you, so the sections are operative: what to read and in what order, the state inherited, the scope and where to stop, the standing constraints, and the definition of done.

## Structured memory

Credit where due: the memory bank is an adaptation of the [Cline Memory Bank](https://docs.cline.bot/improving-your-prompting-skills/cline-memory-bank).

Its purpose is ongoing documentation of the project's purpose, scope, architecture, roadmap, and status. If you're an engineer, think of it as:

1. The documentation and onboarding you'd give a new engineer joining the project.
2. The backlog and roadmap a product manager would maintain.
3. The status updates you'd give your PM and stakeholders.
4. Your working notes as you [yak](https://projects.csail.mit.edu/gsb/old-archive/gsb-archive/gsb2000-02-11.html)-[shave](https://youtu.be/AbSehcT19u0) your way through a feature or bug.

Memory lives in `_memory/`, in the structure documented by the `memory-bank` skill. A structured memory makes the agent understand the project more reliably than an unstructured pile of atomic memories or a single freetext file.

To set one up, ask the agent to create a memory bank for the project. On an existing codebase it will read the repo and write the basic truths from what's actually there, asking about the parts the code can't tell it.

Now that agents ship their own automatic memory, this is less load-bearing than it was. It still earns its place for handing work across sessions and for context you want to curate deliberately rather than accumulate incidentally.

## Workflow

### Starting a project

Run `.ip <the goal of the project>` to plan it interactively, then ask for a memory bank to be set up from the result. On an existing codebase, let the agent read widely first.

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
