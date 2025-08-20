#!/bin/zsh
# setup_and_launch.sh
# Sets up the Blender MPC environment and launches Blender

# 1. Activate or create virtual environment (prefers blender-mcp-venv)
if [ -d "blender-mcp-venv" ]; then
    source blender-mcp-venv/bin/activate
elif [ -d "blender-mpc-venv" ]; then
    # Back-compat with existing env name
    source blender-mpc-venv/bin/activate
else
    python3 -m venv blender-mcp-venv
    source blender-mcp-venv/bin/activate
fi

# 2. Use vendored Blender MCP (no clone needed)

# 3. Install dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
pip install -e blender-mcp

# 4. Launch Blender
# Make sure to activate the virtual environment before launching Blender.
# If 'blender' is in your PATH, this will launch the local/project version.
blender &

# 5. Start the Blender MCP server (MCP tool layer)
# This will connect to Blender's addon socket at localhost:9876 when available
blender-mcp &

echo "Blender launched and Blender MCP server started. In Cascade, add the MCP server command 'blender-mcp' or run this script to begin."
