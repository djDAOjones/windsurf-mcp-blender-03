import os
import json
from datetime import datetime
from blender_mcp.server import BlenderConnection

HOST = 'localhost'
PORT = 9876

conn = BlenderConnection(HOST, PORT)
if not conn.connect():
    print(f"FAIL: Could not connect to Blender MCP at {HOST}:{PORT}")
    raise SystemExit(1)

try:
    info = conn.send_command('get_scene_info', {})
    print('Scene info:')
    print(json.dumps(info, indent=2))

    os.makedirs('runs', exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = os.path.abspath(os.path.join('runs', f'connection_proof_{ts}.png'))
    _ = conn.send_command('get_viewport_screenshot', {
        'max_size': 800,
        'filepath': out_path,
        'format': 'png'
    })
    print('Screenshot written to:')
    print(out_path)
finally:
    conn.disconnect()
