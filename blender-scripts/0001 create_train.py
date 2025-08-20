from blender_mcp.server import BlenderConnection

host = 'localhost'
port = 9876

# Python code to run in Blender to create a simple train model
template_code = '''
import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        bpy.data.materials.remove(block)

def add_train():
    # Engine body
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=4, location=(0, 0, 1))
    engine = bpy.context.active_object
    engine.name = 'EngineBody'

    # Smokestack
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=1, location=(0, 0, 3))
    smokestack = bpy.context.active_object
    smokestack.name = 'Smokestack'

    # Cab
    bpy.ops.mesh.primitive_cube_add(size=1.5, location=(-1.2, 0, 2))
    cab = bpy.context.active_object
    cab.name = 'Cab'

    # Wheels
    wheel_positions = [(-1.2, 1.1, 0.4), (-0.4, 1.1, 0.4), (0.4, 1.1, 0.4), (1.2, 1.1, 0.4),
                      (-1.2, -1.1, 0.4), (-0.4, -1.1, 0.4), (0.4, -1.1, 0.4), (1.2, -1.1, 0.4)]
    for pos in wheel_positions:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.3, location=pos, rotation=(math.radians(90), 0, 0))
        wheel = bpy.context.active_object
        wheel.name = f'Wheel_{pos[0]:.1f}_{pos[1]:.1f}'

clear_scene()
add_train()
'''

try:
    conn = BlenderConnection(host, port)
    if conn.connect():
        print("Connected to Blender MCP. Sending train creation code...")
        result = conn.send_command("execute_code", {"code": template_code})
        print("Result:", result)
        conn.disconnect()
    else:
        print(f"Could not connect to Blender MCP at {host}:{port}")
except Exception as e:
    print(f"ERROR: {e}")
