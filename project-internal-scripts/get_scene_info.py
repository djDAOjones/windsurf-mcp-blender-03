import socket
import json

from blender_mcp.server import BlenderConnection

def get_scene_info(host: str = 'localhost', port: int = 9876):
    """Request scene info from the Blender MCP server using BlenderConnection."""
    conn = BlenderConnection(host, port)
    if not conn.connect():
        raise RuntimeError(f"Could not connect to Blender MCP at {host}:{port}")
    try:
        return conn.send_command("get_scene_info", {})
    finally:
        conn.disconnect()

if __name__ == "__main__":
    info = get_scene_info()
    print(json.dumps(info, indent=2))
