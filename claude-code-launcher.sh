#!/bin/bash
# Memory MCP Server launcher for Claude Code
# This script ensures the virtual environment is activated before starting the server

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Start the MCP server
exec python src/server.py
