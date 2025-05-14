# Coding Agent Rules

A repository of rules for use with a coding agent. An evolving work in progress as coding agents evolve.

For now these are oriented towards Cursor, but they can easily be adapted to other coding agents with minor tweaks.

## Components

### Memory Bank
Credit where credit is due: this memory bank prompt is an adaptation of the [Cline Memory Bank](https://docs.cline.bot/improving-your-prompting-skills/cline-memory-bank). 

Its purpose is to provide ongoing documentation of the project's purpose, scope, architecture, roadmap, and status, all of which is critical context for the coding agent to inform all its responses. 

If you're an engineer, think of this as:
1. The project documentation and onboarding that you'd give a new engineer joining the project
2. The project backlog and roadmap maintained by the product manager.
3. The status updates you'd give your PM and stakeholders.
4. Your working notes as you [yak](https://projects.csail.mit.edu/gsb/old-archive/gsb-archive/gsb2000-02-11.html)-[shave](https://youtu.be/AbSehcT19u0) your way through a new feature or bug.

### Principles

A set of core coding principles that your agent should follow. Most of it is common sense, but there are a few in there that are specific to coding agents, which currently have a habit of getting over-ambitious and doing massive refactors, or going off the rails entirely, disregarding the original scope, deleting files, etc. 

I recommend giving it a read.

NB I prefer to have tests written for all new features, so that the agent can test its own code as it writes it, handle edge cases, and catch regressions. Not everyone will agree with this, so you may wish to remove that section.

### Global Rules

A set of common commands and aliases for the most important prompts.

### Workflow
## Installation 

### Cursor

1. clone this repo
2. run the symlink script from the root of your project

```bash
bash ~/code/coding-agent-rules/symlink-rules.sh
```

I also highly recommend using the specstory extension for Cursor, which will save your interaction history and allow you to reference it later.

### Other coding agents

Install the rules according to the instructions of the coding agent. 

## Usage

The Global Rules file defines common commands and aliases for the most important prompts. In Cursor, I put this in the Cursor Settings > Rules > User Rules.

If your agent doesn't do it automatically, include all the rules in the context at the beginning of every chat with the coding agent.




### Workflow

#### Modes

Some people like to define specific modes for the coding agent to be in, with strict rules on what it can and can't do. I have not found this to be necessary with this set of rules and prompts, since it's implicitly defined by the two main prompts.

##### Interactive Planning

alias: `.ip`

This is a way to interactively plan the project or feature with the coding agent. This is where you will make a plan, along with the agent, for what you want to build and how you want to build it. The agent will ask you a series of clarifying questions to help you flesh out the requirements and constraints, and then you will all agree on a plan.

Use the best thinking model you can afford for this stage.

##### Blueprinting

alias: `.bp`

**After** you have completed the interactive planning phase, create a blueprint for the project with this command. This forces the agent to make a very detailed plan for the project or feature, including generating a list of very specific prompts that will be used to build the project.

When you're done with this, you can use the `.umb` command to update the memory bank with the latest information about the project.


#### Initial memory bank setup

To start, I'd do `.ip <the goal of the project>` to create the memory bank. If you're working on an existing codebase, have it read as much of the codebase as possible before beginning, and use the model that can handle a lot of context. For this stage, use the best thinking model you can afford. It's worth it.

#### Build your backlog (optional)

If you have a lot of ideas on what you plan to build, put it `backlog.md`.

#### Development lifecycle

1. `.mb THEN .ip <your current goal>`
2. `.bp in activeContext.md`
3. `Begin implementing step <x> of the plan in activeContext.md`
4. 









