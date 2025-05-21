#! /bin/bash

## creates symlinks to all the rules into a project directory
## to be run from the root of the project

SOURCE_DIR=~/code/coding-agent-rules
TARGET_DIR=`pwd`/.cursor/rules
COPY_MODE=false

# Parse arguments
TEMP_ARGS=()
for arg in "$@"; do
    if [[ "$arg" == "--copy" ]]; then
        COPY_MODE=true
    else
        TEMP_ARGS+=("$arg")
    fi
done
set -- "${TEMP_ARGS[@]}" # Reset positional parameters

# if the user has provided a path argument, use it as the target directory
if [ -n "$1" ]; then
    TARGET_DIR="$1"
fi

# create the target directory if it doesn't exist
mkdir -p "$TARGET_DIR"
mkdir -p "$TARGET_DIR/_templates"

# create symlinks or copy files for rules
for rule in "$SOURCE_DIR"/*.md; do
    if [[ "$(basename "$rule")" != "README.md" ]]; then
        DEST_FILE="$TARGET_DIR/very-important-$(basename "$rule" .md).mdc"
        if [ "$COPY_MODE" = true ]; then
            cp -f "$rule" "$DEST_FILE"
        else
            ln -s "$rule" "$DEST_FILE"
        fi
    fi
done

# create symlinks or copy files for templates
for template in "$SOURCE_DIR/_templates"/*.md; do
    DEST_FILE_TEMPLATE="$TARGET_DIR/_templates/$(basename "$template")"
    if [ "$COPY_MODE" = true ]; then
        cp -f "$template" "$DEST_FILE_TEMPLATE"
    else
        ln -s "$template" "$DEST_FILE_TEMPLATE"
    fi
done
