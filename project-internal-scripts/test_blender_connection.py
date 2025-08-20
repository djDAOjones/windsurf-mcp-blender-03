from blender_mcp.server import BlenderConnection

# Attempt to connect to the Blender MCP server
host = 'localhost'
port = 9876

try:
    conn = BlenderConnection(host, port)
    if conn.connect():
        print(f"SUCCESS: Connected to Blender MCP at {host}:{port}")
        conn.disconnect()
    else:
        print(f"FAIL: Could not connect to Blender MCP at {host}:{port}")
except Exception as e:
    print(f"ERROR: {e}")
