# Blender MPC Control Project

This project enables control of Blender through Windsurf Cascade using Anthropic's MPC and ahujasid's Blender MPC implementation.

## Prerequisites
- macOS
- Blender (launch from the project environment after activating the virtual environment)
- Python 3.10+
- Git

## Setup

Option A — Quickstart (recommended)

```sh
./setup_and_launch.sh
```

This script will:
- Create/activate a virtual environment (prefers `blender-mcp-venv`, falls back to existing `blender-mpc-venv`).
- Install dependencies from `requirements.txt` and the local `blender-mcp/` package in editable mode.
- Launch Blender and start the `blender-mcp` server (connects to Blender at `localhost:9876`).

Option B — Manual steps

```sh
python3 -m venv blender-mcp-venv
source blender-mcp-venv/bin/activate
pip install -r requirements.txt
pip install -e blender-mcp
blender &
blender-mcp &
```

## Folder Structure

- `blender-scripts/`: Creative Blender scripts.
  - `library/`: Curated, hand-authored scripts checked into source control.
  - `generated/`: Auto-generated scripts created by `create_and_run_blender_script.py` (tracked via a local `.script_count`).
- `project-internal-scripts/`: Internal automation scripts used by Cascade and tooling (e.g., connection tests, utilities). Avoid placing creative content here.
- `runs/`: Artifacts like screenshots captured after code execution, timestamped for traceability.

## Usage
- Start everything:
  ```sh
  ./setup_and_launch.sh
  ```

- Verify connection:
  ```sh
  blender-mcp-venv/bin/python project-internal-scripts/test_blender_connection.py
  # If you are using an older env name, adjust to blender-mpc-venv
  ```

- Run a script through the persistent MCP connection and auto-capture a screenshot:
  ```sh
  blender-mcp-venv/bin/python create_and_run_blender_script.py "add_red_cube" project-internal-scripts/_smoke_add_red_cube.py
  ```

Notes:
- `create_and_run_blender_script.py` saves your code into `blender-scripts/generated/#### <name>.py`, executes it via the MCP server, prints scene info (before/after), and saves a viewport screenshot into `runs/`.
- Prefer using MCP tools via `blender_mcp.server.BlenderConnection` (e.g., `get_scene_info`, `execute_code`, `get_viewport_screenshot`).

Refer to the folder descriptions above when adding new scripts to the project.
---

## References
- [ahujasid/blender-mpc](https://github.com/ahujasid/blender-mpc)
- Anthropic MPC documentation
- Windsurf Cascade documentation
