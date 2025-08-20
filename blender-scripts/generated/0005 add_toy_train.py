import bpy

def clear_scene():
    # Select all objects
    bpy.ops.object.select_all(action='SELECT')
    # Delete all selected objects
    bpy.ops.object.delete()
    # Remove all meshes, materials, etc. from memory
    for block in bpy.data.meshes:
        bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        bpy.data.materials.remove(block)
    for block in bpy.data.textures:
        bpy.data.textures.remove(block)
    for block in bpy.data.images:
        bpy.data.images.remove(block)

def create_toy_train():
    # Materials
    body_mat = bpy.data.materials.new(name="TrainBody")
    body_mat.diffuse_color = (0.8, 0.1, 0.1, 1)  # Red
    wheel_mat = bpy.data.materials.new(name="TrainWheel")
    wheel_mat.diffuse_color = (0.1, 0.1, 0.1, 1)  # Black
    cabin_mat = bpy.data.materials.new(name="TrainCabin")
    cabin_mat.diffuse_color = (0.1, 0.2, 0.8, 1)  # Blue

    # Main body (cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=2.0, location=(0, 0, 0.4))
    body = bpy.context.active_object
    body.data.materials.append(body_mat)

    # Cabin (cube)
    bpy.ops.mesh.primitive_cube_add(size=0.7, location=(0.6, 0, 1.0))
    cabin = bpy.context.active_object
    cabin.scale[0] = 0.7
    cabin.scale[1] = 0.5
    cabin.scale[2] = 1.0
    cabin.data.materials.append(cabin_mat)

    # Chimney (cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.5, location=(-0.7, 0, 1.0))
    chimney = bpy.context.active_object
    chimney.data.materials.append(body_mat)

    # Wheels (4 cylinders)
    wheel_positions = [(-0.6, 0.35, 0.15), (0.6, 0.35, 0.15), (-0.6, -0.35, 0.15), (0.6, -0.35, 0.15)]
    for pos in wheel_positions:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.18, location=pos, rotation=(1.5708, 0, 0))
        wheel = bpy.context.active_object
        wheel.data.materials.append(wheel_mat)

    # Optional: Parent all parts to the body
    for obj in [cabin, chimney] + [ob for ob in bpy.context.scene.objects if ob.name.startswith('Cylinder') and ob != body]:
        obj.select_set(True)
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.parent_set(type='OBJECT')

clear_scene()
create_toy_train()
