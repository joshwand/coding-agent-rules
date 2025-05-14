#! /bin/bash

## creates symlinks to all the rules into a project directory
## to be run from the root of the project

SOURCE_DIR=~/code/coding-agent-rules

TARGET_DIR=`pwd`/.cursor/rules

# if the user has provided a path argument, use it as the target directory
if [ -n "$1" ]; then
    TARGET_DIR="$1"
fi

# create the target directory if it doesn't exist
mkdir -p "$TARGET_DIR"
mkdir -p "$TARGET_DIR/_templates"

# create symlinks to all the rules
for rule in "$SOURCE_DIR"/*.md; do
    if [[ "$(basename "$rule")" != "README.md" ]]; then
        ln -s "$rule" "$TARGET_DIR/very-important-$(basename "$rule" .md).mdc"
    fi
done

for template in "$SOURCE_DIR/_templates"/*.md; do
    ln -s "$template" "$TARGET_DIR/_templates/$(basename "$template")"
done
