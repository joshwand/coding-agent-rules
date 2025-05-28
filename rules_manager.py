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