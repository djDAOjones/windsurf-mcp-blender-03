import bpy

# Ensure we're in object mode
if bpy.ops.object.mode_set.poll():
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass

# Add a UV sphere at origin with radius 1
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0.0, 0.0, 0.0))
