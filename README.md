# Coding Agent Rules

A repository of rules for use with a coding agent. An evolving work in progress, as coding agents themselves evolve.

This set of rules helps ameliorate some of the main issues with coding agents, and helps you get the most out of them.

They cover the following topics:
- High-level software development principles
- Curbing bad agent behavior
- Memory management
- Agent interaction workflow

I've attempted to keep these small, in order to make it easier for the agent to understand and follow, to limit the token usage, and to make it flexible enough to be used with different agents, technologies, and project types, and to be supplemented with your own rules and workflows. 

# Components

## Structured Memory
Credit where credit is due: this memory bank prompt is an adaptation of the [Cline Memory Bank](https://docs.cline.bot/improving-your-prompting-skills/cline-memory-bank). 

Its purpose is to provide ongoing documentation of the project's purpose, scope, architecture, roadmap, and status, all of which is critical context for the coding agent to inform all its responses. 

If you're an engineer, think of this as:
1. The project documentation and onboarding that you'd give a new engineer joining the project
2. The project backlog and roadmap maintained by the product manager.
3. The status updates you'd give your PM and stakeholders.
4. Your working notes as you [yak](https://projects.csail.mit.edu/gsb/old-archive/gsb-archive/gsb2000-02-11.html)-[shave](https://youtu.be/AbSehcT19u0) your way through a new feature or bug.

Memory is stored in the `_memory` directory, in a particular structure/schema that I've found effective. I believe that having a structured memory makes the the agent more reliably understand the project and its context, track its internal state, and make better decisions more aligned with your goals, in comparison to techniques used by other coding agents, such as an unstructured set of atomic memories as used by Windsurf, or a single freetext file such as the one used by Claude.

## Principles

A set of core coding principles that your agent should follow. Most of it is common sense, but there are a few in there that are specific to coding agents, which currently have a habit of getting over-ambitious and doing massive refactors, or going off the rails entirely, disregarding the original scope, deleting files, etc. 

I recommend giving it a read.

NB I prefer to have tests written for all new features, so that the agent can test its own code as it writes it, handle edge cases, and catch regressions. Not everyone will agree with this, so you may wish to remove that section.

## Global Rules

A set of common commands and aliases for the most important prompts. These aliases make it quick and easy to interact with the agent without a lot of typing.

e.g.

- `.ip` -> Interactive Planning
- `.ts` -> Update Task State
- `.c` -> Continue



# Installation

The `symlink-rules.sh` script is the primary method for installing and managing the agent rules. It is a wrapper for the `rules_manager.py` Python script, which contains the core logic for handling the rules.

## Basic Installation

To set up the rules for your project, run the `symlink-rules.sh` script from your project's root directory. You will need to provide the path to your clone of the `coding-agent-rules` repository.

```bash
bash /path/to/your/coding-agent-rules/symlink-rules.sh
```

By default, this command symlinks the rules for the `cursor` agent into the current directory.

## Target Directory

You can also specify a different target directory for the rules:

```bash
bash /path/to/your/coding-agent-rules/symlink-rules.sh /path/to/your/project
```

## Options

The script accepts several command-line options to customize its behavior:

-   `--agent <agent_name>`: Specifies the agent you are using.
    -   **Choices**: `cursor` (default), `windsurf`, `claude`
    -   **Example**: `bash symlink-rules.sh --agent claude`

-   `--copy`: Copies the rule files to the target directory instead of creating symbolic links.
    -   **Example**: `bash symlink-rules.sh --copy`

-   `--init-memory`: Initializes an empty `_memory` directory structure in the target directory, which is essential for agents that rely on structured memory.
    -   **Example**: `bash symlink-rules.sh --init-memory`

-   `--output <filename>`: For agents that use a single concatenated rule file (like `claude` or `windsurf`), this option allows you to specify a custom name for the output file. Note that this cannot be used in conjunction with the `--agent` option.
    -   **Example**: `bash symlink-rules.sh --output CUSTOM_AGENT_RULES.md`

These options can be combined. For instance, to initialize the memory structure and copy the rules for the `claude` agent into a specific project directory, you would run:

```bash
bash /path/to/your/coding-agent-rules/symlink-rules.sh --agent claude --init-memory --copy /path/to/your/project
```

I also highly recommend using the specstory extension for Cursor, which will save your interaction history and allow you to reference it later.

## Other coding agents

Install the rules according to the instructions of the coding agent. 

## Usage

The Global Rules file defines common commands and aliases for the most important prompts. In Cursor, I put this in the Cursor Settings > Rules > User Rules.

If your agent doesn't do it automatically, include all the rules in the context at the beginning of every chat with the coding agent.

The memory rules *should* make the agent read the memory automatically, but if not, you can use the `.m` command to ask it explicitly, or use Repomix (see below) to turn your memory into a single file that you can include in your context.


# Workflow

## Modes

Some people like to define specific modes for the coding agent to be in, with strict rules on what it can and can't do. I have not found this to be necessary with this set of rules and prompts, since it's implicitly defined by the two main prompts.

## Interactive Planning

alias: `.ip`

This is a way to interactively plan the project or feature with the coding agent. This is where you will make a plan, along with the agent, for what you want to build and how you want to build it. The agent will ask you a series of clarifying questions to help you flesh out the requirements and constraints, and then you will all agree on a plan.

Use the best thinking model you can afford for this stage.

## Blueprinting

alias: `.bp`

**After** you have completed the interactive planning phase, create a blueprint for the project with this command. This forces the agent to make a very detailed plan for the project or feature, including generating a list of very specific prompts that will be used to build the project.

When you're done with this, you can use the `.umb` command to update the memory bank with the latest information about the project.


## Initial memory bank setup

To start, I'd do `.ip <the goal of the project>` to create the memory bank. If you're working on an existing codebase, have it read as much of the codebase as possible before beginning, and use the model that can handle a lot of context. For this stage, use the best thinking model you can afford. It's worth it.

## Build your backlog (optional)

If you have a lot of ideas on what you plan to build, put it `backlog.md`.

## Development lifecycle

1. `.mb THEN .ip <your current goal>`
2. `.bp in activeContext.md`
3. `Begin implementing step <x> of the plan in activeContext.md`
4. 


# Related tools

## Repomix

[Repomix](https://repomix.com/) is a tool that bundles your codebase (or some subset of it) into a single file that you can include in your coding agent's context. If getting the agent to read your memory bank is unreliable, you can repomix to turn it into a single file that you can explicitly include in your context.

```
npx repomix --include _memory/ --ignore _memory/knowledgeBase/ --style markdown
```

This produces a file called repomix-output.md that you can @ in your context. (Be sure to include it in your gitignore.)







