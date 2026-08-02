#!/usr/bin/env python3

import argparse
import os
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Output targets. Both concatenate the rule files into a single document; they
# differ only in filename.
AGENT_CONFIGS = {
    "claude": {"output_filename": "CLAUDE.md"},
    "agentsmd": {"output_filename": "AGENTS.md"},
}

# The rule files that ship, in the order they are concatenated. This is an
# explicit list rather than a glob of the repo root so that a scratch file left
# lying around cannot silently end up in every project's CLAUDE.md.
RULE_FILES = [
    "core.md",
    "commands.md",
]

SKILLS_DIRNAME = "skills"

# The content for currentTaskState.md, read from the template
with open(os.path.join(SCRIPT_DIR, "_templates/currentTaskState.md"), "r", encoding="utf-8") as f:
    CURRENT_TASK_STATE_CONTENT = f.read()

# Placeholder content for the basicTruths files created by --init-memory.
PLACEHOLDER_CONTENT = {
    "productContext.md": """# Product Context

- Why this project exists
- Problems it solves
- How it should work
- User experience goals
""",
    "projectScope.md": """# Project Scope

- Foundation document that shapes all other files
- Created at project start if it doesn't exist
- Defines core requirements and goals
- Source of truth for project scope
""",
    "repoStructure.md": """# Repo Structure

- Top-level directory layout
- Where each kind of code lives
- Anything about the layout that would surprise someone new
""",
    "systemArchitecture.md": """# System Architecture

- High-level system architecture
- Key technical decisions
- Design patterns in use
- Component relationships
""",
    "theBacklog.md": """# The Backlog

- Prioritized list of features and tasks
- Recent changes
""",
    "theTechContext.md": """# The Tech Context

- Technologies used
- Technical constraints
- Dependencies
- Development setup
- Build and deployment instructions
- Standards and conventions
""",
}


def create_memory_structure(target_dir):
    """Creates the _memory directory structure and populates it with initial files."""
    base_dir = os.path.join(target_dir, "_memory")
    if os.path.exists(base_dir):
        print(f"Directory '{base_dir}' already exists. Aborting.", file=sys.stderr)
        sys.exit(1)

    print(f"Creating directory: {base_dir}")
    os.makedirs(base_dir)

    dirs_to_create = {
        "basicTruths": list(PLACEHOLDER_CONTENT.keys()),
        "currentState": ["currentEpic.md", "currentTaskState.md"],
        "knowledgeBase": [],
    }

    knowledge_base_subdirs = ["designs", "domainKnowledge", "reference", "requirements"]

    for dir_name, files in dirs_to_create.items():
        dir_path = os.path.join(base_dir, dir_name)
        print(f"Creating directory: {dir_path}")
        os.makedirs(dir_path)

        for filename in files:
            file_path = os.path.join(dir_path, filename)
            print(f"Creating file: {file_path}")
            with open(file_path, "w", encoding="utf-8") as f:
                if filename == "currentTaskState.md":
                    f.write(CURRENT_TASK_STATE_CONTENT)
                else:
                    f.write(PLACEHOLDER_CONTENT.get(filename, f"# {filename}\n"))

    for subdir in knowledge_base_subdirs:
        subdir_path = os.path.join(base_dir, "knowledgeBase", subdir)
        print(f"Creating directory: {subdir_path}")
        os.makedirs(subdir_path)
        # Create a .gitkeep file to ensure the directory is tracked by git
        with open(os.path.join(subdir_path, ".gitkeep"), "w") as f:
            pass

    # Copy templates into _memory/_templates
    print("\nProcessing templates...")
    source_templates_dir = os.path.join(SCRIPT_DIR, "_templates")
    memory_templates_dir = os.path.join(base_dir, "_templates")
    templates_processed_count = 0

    if os.path.isdir(source_templates_dir):
        os.makedirs(memory_templates_dir, exist_ok=True)
        for item in sorted(os.listdir(source_templates_dir)):
            if item.startswith((".", "@")):  # Skip dotfiles and @-files
                continue
            if item.endswith(".md"):
                templates_processed_count += 1
                source_template_path = os.path.join(source_templates_dir, item)
                dest_template_path = os.path.join(memory_templates_dir, item)

                print(f"Copying template {source_template_path} to {dest_template_path}")
                shutil.copy2(source_template_path, dest_template_path)

        if templates_processed_count == 0:
            print("No template files found in _templates directory (excluding dotfiles, @-files).")
        else:
            print(f"Processed {templates_processed_count} template file(s).")
    else:
        print(f"Templates source directory not found: {source_templates_dir}")

    print("\nMemory structure created successfully.")


def install_skills(target_dir):
    """Copies each skill directory into the target project's .claude/skills/."""
    source_skills_dir = os.path.join(SCRIPT_DIR, SKILLS_DIRNAME)
    if not os.path.isdir(source_skills_dir):
        print(f"Skills source directory not found: {source_skills_dir}", file=sys.stderr)
        return 0

    dest_skills_dir = os.path.join(target_dir, ".claude", "skills")
    os.makedirs(dest_skills_dir, exist_ok=True)

    installed = 0
    for item in sorted(os.listdir(source_skills_dir)):
        if item.startswith((".", "@")):
            continue
        source_skill_path = os.path.join(source_skills_dir, item)
        if not os.path.isdir(source_skill_path):
            continue
        dest_skill_path = os.path.join(dest_skills_dir, item)
        print(f"Installing skill {item} -> {dest_skill_path}")
        if os.path.exists(dest_skill_path):
            shutil.rmtree(dest_skill_path)
        shutil.copytree(source_skill_path, dest_skill_path)
        installed += 1

    if installed == 0:
        print("No skills found to install.")
    else:
        print(f"Installed {installed} skill(s).")
    return installed


def resolve_rule_files(excluded):
    """Returns the absolute paths of the rule files to ship, in order."""
    resolved = []
    for name in RULE_FILES:
        if name in excluded:
            continue
        path = os.path.join(SCRIPT_DIR, name)
        if not os.path.isfile(path):
            print(f"Error: rule file listed in RULE_FILES not found: {path}", file=sys.stderr)
            sys.exit(1)
        resolved.append(path)
    return resolved


def main():
    parser = argparse.ArgumentParser(
        description="Generates a CLAUDE.md / AGENTS.md ruleset for a target project.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--init-memory",
        action="store_true",
        help="Initialize an empty _memory directory structure in the target directory.",
    )
    parser.add_argument(
        "--install-skills",
        action="store_true",
        help="Install the skills/ directories into the target project's .claude/skills/.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Exclude a rule file from the generated output. Repeatable. Example: --exclude commands.md",
    )
    parser.add_argument(
        "--list-files",
        action="store_true",
        help="List the rule files, skills, and templates that would be used, then exit.",
    )

    # --agent and --output are mutually exclusive
    agent_group = parser.add_mutually_exclusive_group(required=False)
    agent_group.add_argument(
        "--agent",
        default="claude",
        choices=AGENT_CONFIGS.keys(),
        help="Specify the output target.",
    )
    agent_group.add_argument(
        "--output",
        help="Write the concatenated rules to a custom filename. Cannot be used with --agent.",
    )

    parser.add_argument(
        "base_target_directory",
        nargs="?",
        default=os.getcwd(),
        help="The directory to write into. Defaults to the current working directory.",
    )

    args = parser.parse_args()

    if args.list_files:
        print("Rule files (in output order):")
        for name in RULE_FILES:
            missing = "" if os.path.isfile(os.path.join(SCRIPT_DIR, name)) else "  (MISSING)"
            print(f"  - {name}{missing}")

        print("\nSkills:")
        source_skills_dir = os.path.join(SCRIPT_DIR, SKILLS_DIRNAME)
        skills = []
        if os.path.isdir(source_skills_dir):
            skills = [
                item
                for item in sorted(os.listdir(source_skills_dir))
                if not item.startswith((".", "@"))
                and os.path.isdir(os.path.join(source_skills_dir, item))
            ]
        for item in skills:
            print(f"  - {item}")
        if not skills:
            print("  (none found)")

        print("\nTemplates:")
        source_templates_dir = os.path.join(SCRIPT_DIR, "_templates")
        template_files = []
        if os.path.isdir(source_templates_dir):
            template_files = [
                item
                for item in sorted(os.listdir(source_templates_dir))
                if item.endswith(".md") and not item.startswith((".", "@"))
            ]
        for item in template_files:
            print(f"  - {item}")
        if not template_files:
            print("  (none found)")

        print(
            f"\nTotal: {len(RULE_FILES)} rule file(s), "
            f"{len(skills)} skill(s), {len(template_files)} template file(s)"
        )
        sys.exit(0)

    excluded_files = set(args.exclude)
    if excluded_files:
        print(f"User-specified exclusions: {', '.join(sorted(excluded_files))}")

    base_target_dir_abs = os.path.abspath(args.base_target_directory)

    if args.init_memory:
        print(f"Initializing memory structure in: {base_target_dir_abs}")
        create_memory_structure(base_target_dir_abs)
        sys.exit(0)

    if args.install_skills:
        print(f"Installing skills into: {base_target_dir_abs}")
        install_skills(base_target_dir_abs)
        sys.exit(0)

    output_filename = args.output if args.output else AGENT_CONFIGS[args.agent]["output_filename"]
    target_label = "custom" if args.output else args.agent

    print(f"Target: {target_label}")
    print(f"Source directory: {SCRIPT_DIR}")
    print(f"Target directory: {base_target_dir_abs}")

    os.makedirs(base_target_dir_abs, exist_ok=True)

    rule_paths = resolve_rule_files(excluded_files)
    if not rule_paths:
        print("No rule files left to write after exclusions.", file=sys.stderr)
        sys.exit(1)

    output_path = os.path.join(base_target_dir_abs, output_filename)
    print(f"\nWriting rules into: {output_path}")

    with open(output_path, "w", encoding="utf-8") as outfile:
        for index, rule_path in enumerate(rule_paths):
            if index > 0:
                outfile.write("\n\n")
            with open(rule_path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read().rstrip("\n") + "\n")
            print(f"  + {os.path.basename(rule_path)}")

    print(f"\nWrote {output_path} from {len(rule_paths)} rule file(s).")


if __name__ == "__main__":
    main()
