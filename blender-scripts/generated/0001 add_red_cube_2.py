import bpy

# Add a red glossy cube and make it the active object
bpy.ops.mesh.primitive_cube_add(size=2)
obj = bpy.context.active_object

mat = bpy.data.materials.new(name="CascadeRedMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (1.0, 0.0, 0.0, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.2

if obj is not None:
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
