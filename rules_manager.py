#!/usr/bin/env python3

import argparse
import os
import shutil
import sys

SOURCE_DIR_NAME = "code/coding-agent-rules" # Relative to user's home directory

AGENT_CONFIGS = {
    "cursor": {
        "concatenate_rules": False,
        "agent_subdir": ".cursor/rules",
        "individual_file_prefix": "very-important-",
        "individual_file_suffix": ".mdc",
        "output_filename": None,
    },
    "windsurf": {
        "concatenate_rules": True,
        "agent_subdir": "",
        "output_filename": ".windsurfrules",
        "individual_file_prefix": None,
        "individual_file_suffix": None,
    },
    "claude": {
        "concatenate_rules": True,
        "agent_subdir": "",
        "output_filename": "AGENT.md",
        "individual_file_prefix": None,
        "individual_file_suffix": None,
    }
}

# The content for currentTaskState.md, read from the template
CURRENT_TASK_STATE_CONTENT = """### currentTaskState.md
# Task State
  
**INSTRUCTIONS:** This is the working document for the current task. Update it after EVERY turn with the user, with enough information for another agent to take over. Do not remove the instructions from each section.
  
## Current goal
[insert current goal here]
  
## Current mode:
INSTRUCTIONS: *(choose from: ANALYZE, PLAN, ACT, VERIFY, REFLECT, DOCUMENT)*
  
**ANALYZE**
  
## Current Status
INSTRUCTIONS: *(describe the current state of the task, including any recent changes or progress)
  
[insert current status here]
  
### Yak-Shaving Stack:
INSTRUCTIONS: *(from high-level to low-level; treat as an inverted stack. the bottom-most level is the current working level, and you can only add or remove the bottom-most level)*
  
[example content]
- Level 1: The main goal
- Level 2: The task we currently need to do to accomplish the main goal
- Level 3: Solve the issue we encountered while trying to do the task in level 2
- Level 4: Try one specific approach to solving the problem in level 3
- Level 5: resolve any issues that came up while trying to take the approach in level 4
[end example content]
  
## Scratchpad
INSTRUCTIONS: *(add notes here to record progress and reflections)*
  
[insert scratchpad here]
  
**Next Steps:**
1. [insert next step here]
2. [insert next step here]
  
## Action Log
INSTRUCTIONS: *(add notes here to record major actions taken while working on the task and their results, newest actions at the top)*

[example content]
turn 3: did a third thing
turn 2: did a second thing
turn 1: did the first thing
[end example content]
"""

# Placeholder content for other files
PLACEHOLDER_CONTENT = {
    "productContext.md": "# Product Context\\n\\n- Why this project exists\\n- Problems it solves\\n- How it should work\\n- User experience goals",
    "projectScope.md": "# Project Scope\\n\\n- Foundation document that shapes all other files\\n- Created at project start if it doesn't exist\\n- Defines core requirements and goals\\n- Source of truth for project scope",
    "systemArchitecture.md": "# System Architecture\\n\\n- High-level system architecture\\n- Key technical decisions\\n- Design patterns in use\\n- Component relationships",
    "theBacklog.md": "# The Backlog\\n\\n- Prioritized list of features and tasks\\n- Recent changes",
    "theTechContext.md": "# The Tech Context\\n\\n- Technologies used\\n- Technical constraints\\n- Dependencies\\n- Development setup\\n- Build and deployment instructions\\n- Standards and conventions",
}

def create_memory_structure(target_dir):
    """Creates the _memory directory structure and populates it with initial files."""
    base_dir = os.path.join(target_dir, "_memory")
    if os.path.exists(base_dir):
        print(f"Directory '{base_dir}' already exists. Aborting.", file=sys.stderr)
        return

    print(f"Creating directory: {base_dir}")
    os.makedirs(base_dir)

    # Directories to create
    dirs_to_create = {
        "basicTruths": list(PLACEHOLDER_CONTENT.keys()),
        "currentState": ["currentEpic.md", "currentTaskState.md"],
        "knowledgeBase": []
    }

    knowledge_base_subdirs = ["designs", "domainKnowledge", "reference", "requirements"]

    for dir_name, files in dirs_to_create.items():
        dir_path = os.path.join(base_dir, dir_name)
        print(f"Creating directory: {dir_path}")
        os.makedirs(dir_path)

        for filename in files:
            file_path = os.path.join(dir_path, filename)
            print(f"Creating file: {file_path}")
            with open(file_path, "w") as f:
                if filename == "currentTaskState.md":
                    f.write(CURRENT_TASK_STATE_CONTENT)
                else:
                    f.write(PLACEHOLDER_CONTENT.get(filename, f"# {filename}\\n"))

    for subdir in knowledge_base_subdirs:
        subdir_path = os.path.join(base_dir, "knowledgeBase", subdir)
        print(f"Creating directory: {subdir_path}")
        os.makedirs(subdir_path)
        # Create a .gitkeep file to ensure the directory is tracked by git
        with open(os.path.join(subdir_path, ".gitkeep"), "w") as f:
            pass

    print("\nMemory structure created successfully.")

def main():
    parser = argparse.ArgumentParser(
        description="Manages rule files for different agents.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy files instead of symlinking. Concatenated rule files are always copied."
    )
    
    parser.add_argument(
        "--init-memory",
        action="store_true",
        help="Initialize an empty _memory directory structure in the target directory."
    )
    
    # Create mutually exclusive group for --agent and --output
    agent_group = parser.add_mutually_exclusive_group(required=False)
    agent_group.add_argument(
        "--agent",
        default="cursor",
        choices=AGENT_CONFIGS.keys(),
        help="Specify the agent type."
    )
    agent_group.add_argument(
        "--output",
        help="Specify a custom output file for concatenated rules. Cannot be used with --agent."
    )
    
    parser.add_argument(
        "base_target_directory",
        nargs="?",
        default=os.getcwd(),
        help="The base directory where rules/templates will be placed. Defaults to current working directory."
    )

    args = parser.parse_args()

    if args.init_memory:
        target_dir = os.path.abspath(args.base_target_directory)
        print(f"Initializing memory structure in: {target_dir}")
        create_memory_structure(target_dir)
        

    source_dir_abs = os.path.expanduser(f"~/{SOURCE_DIR_NAME}")
    if not os.path.isdir(source_dir_abs):
        print(f"Error: Source directory not found: {source_dir_abs}", file=sys.stderr)
        sys.exit(1)

    # Determine if we're using custom output or agent-based configuration
    if args.output:
        # Custom output mode - always concatenate
        concatenate_rules = True
        agent_subdir = ""
        output_filename = args.output
        agent_type = "custom"
        individual_file_prefix = None
        individual_file_suffix = None
    else:
        # Agent-based mode
        agent_config = AGENT_CONFIGS[args.agent]
        concatenate_rules = agent_config["concatenate_rules"]
        agent_subdir = agent_config["agent_subdir"]
        output_filename = agent_config["output_filename"]
        agent_type = args.agent
        individual_file_prefix = agent_config["individual_file_prefix"]
        individual_file_suffix = agent_config["individual_file_suffix"]
    
    base_target_dir_abs = os.path.abspath(args.base_target_directory)

    effective_target_dir = base_target_dir_abs
    if agent_subdir:
        effective_target_dir = os.path.join(base_target_dir_abs, agent_subdir)

    effective_templates_dir = os.path.join(effective_target_dir, "_templates")

    print(f"Selected agent type: {agent_type}")
    print(f"Copy mode: {args.copy}")
    print(f"Source directory: {source_dir_abs}")
    print(f"Base target directory: {base_target_dir_abs}")
    print(f"Effective rules target directory: {effective_target_dir}")
    print(f"Effective templates target directory: {effective_templates_dir}")

    os.makedirs(effective_target_dir, exist_ok=True)
    os.makedirs(effective_templates_dir, exist_ok=True)

    # Process Rules
    print("\nProcessing rules...")
    rules_processed_count = 0
    if concatenate_rules:
        output_path = os.path.join(effective_target_dir, output_filename)
        print(f"Concatenating rules into: {output_path}")
        with open(output_path, "w", encoding="utf-8") as outfile:
            first_rule_file = True
            for item in sorted(os.listdir(source_dir_abs)): # Sort for consistent order
                if item.startswith((".", "@")): # Skip dotfiles and @-files
                    continue
                if item.endswith(".md") and item.lower() != "readme.md":
                    rules_processed_count += 1
                    rule_file_path = os.path.join(source_dir_abs, item)
                    if not first_rule_file:
                        outfile.write("\n\n") # Separator between files
                    
                    outfile.write(f"# {item}\n\n") # Add filename as H1 header
                    
                    with open(rule_file_path, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                    first_rule_file = False
        if rules_processed_count > 0:
            print(f"Successfully created {output_path} with {rules_processed_count} rule(s).")
        else:
            print("No rule files found to concatenate (excluding README.md, dotfiles, @-files).")
            # Remove the empty file if it was created
            if os.path.exists(output_path) and os.path.getsize(output_path) == 0:
                os.remove(output_path)

    else: # Individual file processing
        for item in sorted(os.listdir(source_dir_abs)):
            if item.startswith((".", "@")): # Skip dotfiles and @-files
                continue
            if item.endswith(".md") and item.lower() != "readme.md":
                rules_processed_count +=1
                source_file_path = os.path.join(source_dir_abs, item)
                base_filename, _ = os.path.splitext(item)
                dest_filename = f"{individual_file_prefix}{base_filename}{individual_file_suffix}"
                dest_file_path = os.path.join(effective_target_dir, dest_filename)

                # Remove existing destination if it's a symlink or file to avoid errors/issues
                if os.path.islink(dest_file_path) or os.path.exists(dest_file_path):
                    os.remove(dest_file_path)

                if args.copy:
                    print(f"Copying rule {source_file_path} to {dest_file_path}")
                    shutil.copy2(source_file_path, dest_file_path)
                else:
                    print(f"Symlinking rule {source_file_path} to {dest_file_path}")
                    # For symlink, source path should be absolute for robustness
                    os.symlink(os.path.abspath(source_file_path), dest_file_path)
        if rules_processed_count == 0:
            print("No rule files found to process (excluding README.md, dotfiles, @-files).")
        else:
            print(f"Processed {rules_processed_count} individual rule file(s).")


    # Process _templates
    print("\nProcessing templates...")
    source_templates_dir = os.path.join(source_dir_abs, "_templates")
    templates_processed_count = 0
    if os.path.isdir(source_templates_dir):
        for item in sorted(os.listdir(source_templates_dir)):
            if item.startswith((".", "@")): # Skip dotfiles and @-files
                continue
            if item.endswith(".md"):
                templates_processed_count +=1
                source_template_path = os.path.join(source_templates_dir, item)
                dest_template_path = os.path.join(effective_templates_dir, item)

                if os.path.islink(dest_template_path) or os.path.exists(dest_template_path):
                    os.remove(dest_template_path)

                if args.copy:
                    print(f"Copying template {source_template_path} to {dest_template_path}")
                    shutil.copy2(source_template_path, dest_template_path)
                else:
                    print(f"Symlinking template {source_template_path} to {dest_template_path}")
                    os.symlink(os.path.abspath(source_template_path), dest_template_path)
        if templates_processed_count == 0:
            print("No template files found in _templates directory (excluding dotfiles, @-files).")
        else:
            print(f"Processed {templates_processed_count} template file(s).")
    else:
        print(f"Templates source directory not found: {source_templates_dir}")

    print("\nScript finished.")

if __name__ == "__main__":
    main() 