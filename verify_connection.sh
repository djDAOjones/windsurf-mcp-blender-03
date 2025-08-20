#!/bin/zsh
# verify_connection.sh
# Verifies MCP connectivity and saves a proof screenshot

set -e

# 1) Activate venv
if [ -d "blender-mcp-venv" ]; then
  source blender-mcp-venv/bin/activate
elif [ -d "blender-mpc-venv" ]; then
  source blender-mpc-venv/bin/activate
else
  echo "No venv found. Run ./setup_and_launch.sh first."
  exit 1
fi

# 2) Check connection
python project-internal-scripts/test_blender_connection.py

# 3) Probe scene + screenshot proof -> runs/connection_proof_*.png
python project-internal-scripts/_probe_connection.py
