#! /bin/bash

## Wrapper script to call the Python-based rules manager.

# Determine the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

PYTHON_SCRIPT_PATH="$SCRIPT_DIR/rules_manager.py"

if [ ! -f "$PYTHON_SCRIPT_PATH" ]; then
    echo "Error: Python script not found at $PYTHON_SCRIPT_PATH" >&2
    exit 1
fi

# Execute the Python script, passing all arguments through
# Use python3, assuming it's available in the PATH
python3 "$PYTHON_SCRIPT_PATH" "$@"

exit $?
