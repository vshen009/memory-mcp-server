#!/bin/bash
# Memory MCP Server launcher for Codex
# This script ensures the virtual environment is activated before starting the server

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Start the MCP server using the venv interpreter directly.
# This avoids depending on a global `python` binary being present.
exec "$SCRIPT_DIR/venv/bin/python" src/server.py
