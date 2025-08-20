# Project Plan: Blender MPC Control with Windsurf Cascade and Anthropic MPC

## Overview
This project sets up an environment to control Blender using Windsurf Cascade and Anthropic's MPC, leveraging ahujasid's Blender MPC implementation. The setup is designed for macOS and assumes Blender is launched from the project environment (after activating the virtual environment), not from the global system install.

## Steps
1. Create and activate a Python virtual environment.
2. Clone ahujasid's Blender MPC implementation.
3. Install required Python dependencies (Anthropic MPC, Windsurf/Cascade SDKs, etc.).
4. Configure Blender, Cascade, and MPC to work together.
5. Use the provided script to initialize the environment and launch Blender.

---

# README.md

## Blender MPC Control Project

### Prerequisites
- macOS
- Blender installed at `/Applications/Blender.app/Contents/MacOS/Blender`
- Python 3.10+
- Git

### Setup Instructions

```sh
# 1. Create virtual environment
python3 -m venv blender-mpc-venv
source blender-mpc-venv/bin/activate

# 2. Clone Blender MPC implementation
# (This repo will be cloned by the setup script or manually)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the setup and launch script
./setup_and_launch.sh
```

### What the Script Does
- Activates the virtual environment
- Installs dependencies
- Clones ahujasid's Blender MPC repo (if not already present)
- Launches Blender with the correct configuration

---

# Next Steps
- Fill in `requirements.txt` with the necessary dependencies.
- Configure integration scripts for Cascade, MPC, and Blender.
- Test the setup using the provided script.
