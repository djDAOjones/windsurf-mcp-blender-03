#!/bin/zsh
# start_blender_mcp.sh
# Fast start: activate venv and start Blender + MCP server (no installs)

set -e

# 1) Activate preferred venv
if [ -d "blender-mcp-venv" ]; then
  source blender-mcp-venv/bin/activate
elif [ -d "blender-mpc-venv" ]; then
  source blender-mpc-venv/bin/activate
else
  echo "No venv found. Run ./setup_and_launch.sh first."
  exit 1
fi

# 2) Launch Blender (handle PATH, /Applications, or macOS 'open -a')
AUTOPY_SCRIPT="$PWD/project-internal-scripts/_blender_autostart_mcp.py"
if command -v blender >/dev/null 2>&1; then
  echo "Launching Blender via PATH 'blender'..."
  blender --python "${AUTOPY_SCRIPT}" &
  BLENDER_PID=$!
elif [ -x "/Applications/Blender.app/Contents/MacOS/Blender" ]; then
  echo "Launching Blender via /Applications/Blender.app..."
  "/Applications/Blender.app/Contents/MacOS/Blender" --python "${AUTOPY_SCRIPT}" &
  BLENDER_PID=$!
else
  echo "Launching Blender via macOS 'open -a Blender'..."
  open -a "Blender" --args --python "${AUTOPY_SCRIPT}" || { echo "ERROR: Could not launch Blender. Install Blender or add it to PATH."; exit 1; }
fi

# 3) Wait for Blender MCP addon to listen on port 9876 (up to 60s)
echo "Waiting for Blender MCP addon to listen on 9876 (up to 60s)..."
python3 - <<'PY'
import socket, time, sys
host='127.0.0.1'; port=9876
for _ in range(60):
    s=socket.socket(); s.settimeout(0.5)
    try:
        s.connect((host,port))
    except Exception:
        time.sleep(1)
    else:
        print("READY")
        sys.exit(0)
print("TIMEOUT")
sys.exit(1)
PY

if [ $? -ne 0 ]; then
  echo "WARNING: Port 9876 not detected. Ensure the Blender MCP addon is enabled in Blender (Preferences > Add-ons)."
  echo "After enabling, run 'blender-mcp &' or re-run this script."
  exit 1
fi

# 4) Start the Blender MCP server
echo "Starting blender-mcp..."
blender-mcp &

echo "Blender running and Blender MCP server started. Run ./verify_connection.sh to confirm."
