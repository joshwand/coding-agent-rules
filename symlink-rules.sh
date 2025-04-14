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

# create symlinks to all the rules
for rule in "$SOURCE_DIR"/*.md; do
    ln -s "$rule" "$TARGET_DIR/$(basename "$rule").mdc"
done
