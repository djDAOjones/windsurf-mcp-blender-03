import os
import sys
import json
from datetime import datetime
from blender_mcp.server import BlenderConnection

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "blender-scripts", "generated")
COUNT_FILE = ".script_count"
RUNS_DIR = os.path.join(os.path.dirname(__file__), "runs")

# Persistent connection holder
_conn = None

def get_connection(host: str = "localhost", port: int = 9876) -> BlenderConnection:
    global _conn
    if _conn is None:
        _conn = BlenderConnection(host, port)
        if not _conn.connect():
            raise RuntimeError(f"Could not connect to Blender MCP at {host}:{port}. Ensure addon is enabled and server running.")
    return _conn

# -- Script Management --
def get_next_script_number():
    count_path = os.path.join(SCRIPTS_DIR, COUNT_FILE)
    if not os.path.exists(count_path):
        with open(count_path, "w") as f:
            f.write("1")
        return 1
    try:
        with open(count_path, "r") as f:
            raw = f.read().strip()
        count = int(raw) if raw else 0
    except Exception:
        count = 0
    if count <= 0:
        with open(count_path, "w") as f:
            f.write("1")
        return 1
    return count + 1

def update_script_count(n):
    count_path = os.path.join(SCRIPTS_DIR, COUNT_FILE)
    with open(count_path, "w") as f:
        f.write(str(n))

def run_scene_info(label):
    print(f"\n--- {label} Scene Info ---")
    conn = get_connection()
    info = conn.send_command("get_scene_info", {})
    text = json.dumps(info, indent=2)
    print(text)
    return text

def save_and_run_script(script_name, code):
    # Scene info before
    before = run_scene_info("Before")
    n = get_next_script_number()
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    filename = f"{n:04d} {script_name}.py"
    script_path = os.path.join(SCRIPTS_DIR, filename)
    with open(script_path, "w") as f:
        f.write(code)
    update_script_count(n)
    print(f"Script saved as {filename}")
    # Run the script via Blender MCP addon
    print("Running script in Blender via execute_code...")
    conn = get_connection()
    exec_result = conn.send_command("execute_code", {"code": code})
    print("Execution result:", exec_result)

    # Ensure runs dir exists and capture a viewport screenshot
    os.makedirs(RUNS_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.abspath(os.path.join(RUNS_DIR, f"{n:04d}_{script_name}_{ts}.png"))
    try:
        shot_result = conn.send_command("get_viewport_screenshot", {
            "max_size": 800,
            "filepath": screenshot_path,
            "format": "png",
        })
        print("Screenshot saved:", screenshot_path)
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")
        shot_result = {"error": str(e)}
    # Scene info after
    after = run_scene_info("After")
    return filename, before, json.dumps(exec_result), after

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_and_run_blender_script.py <script_name> <script_file>")
        sys.exit(1)
    script_name = sys.argv[1]
    script_file = sys.argv[2]
    with open(script_file, "r") as f:
        code = f.read()
    save_and_run_script(script_name, code)
