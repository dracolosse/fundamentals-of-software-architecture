#!/usr/bin/env bash
# sa-learn launcher — run from anywhere via shell alias
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/.venv/bin/python3" "$SCRIPT_DIR/sa-learn-cli.py" "$@"
