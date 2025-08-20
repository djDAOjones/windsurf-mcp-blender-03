import bpy

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for block in bpy.data.meshes:
        bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        bpy.data.materials.remove(block)
    for block in bpy.data.textures:
        bpy.data.textures.remove(block)
    for block in bpy.data.images:
        bpy.data.images.remove(block)

def create_toy_train():
    body_mat = bpy.data.materials.new(name="TrainBody")
    body_mat.diffuse_color = (0.8, 0.1, 0.1, 1)
    wheel_mat = bpy.data.materials.new(name="TrainWheel")
    wheel_mat.diffuse_color = (0.1, 0.1, 0.1, 1)
    cabin_mat = bpy.data.materials.new(name="TrainCabin")
    cabin_mat.diffuse_color = (0.1, 0.2, 0.8, 1)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=2.0, location=(0, 0, 0.4))
    body = bpy.context.active_object
    body.data.materials.append(body_mat)

    bpy.ops.mesh.primitive_cube_add(size=0.7, location=(0.6, 0, 1.0))
    cabin = bpy.context.active_object
    cabin.scale[0] = 0.7
    cabin.scale[1] = 0.5
    cabin.scale[2] = 1.0
    cabin.data.materials.append(cabin_mat)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.5, location=(-0.7, 0, 1.0))
    chimney = bpy.context.active_object
    chimney.data.materials.append(body_mat)

    wheel_positions = [(-0.6, 0.35, 0.15), (0.6, 0.35, 0.15), (-0.6, -0.35, 0.15), (0.6, -0.35, 0.15)]
    wheels = []
    for pos in wheel_positions:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.18, location=pos, rotation=(1.5708, 0, 0))
        wheel = bpy.context.active_object
        wheel.data.materials.append(wheel_mat)
        wheels.append(wheel)

    # Parent all parts to the body
    for obj in [cabin, chimney] + wheels:
        obj.select_set(True)
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.parent_set(type='OBJECT')

if __name__ == "__main__":
    clear_scene()
    create_toy_train()
