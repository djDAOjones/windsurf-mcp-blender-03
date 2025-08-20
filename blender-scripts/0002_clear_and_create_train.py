import bpy

def clear_scene():
    # Deselect all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    # Remove all meshes, materials, etc. from data blocks
    for block in bpy.data.meshes:
        bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        bpy.data.materials.remove(block)
    for block in bpy.data.textures:
        bpy.data.textures.remove(block)
    for block in bpy.data.images:
        bpy.data.images.remove(block)

def create_train():
    # Create train base (cube)
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    base = bpy.context.active_object
    base.name = "TrainBase"
    # Create train cabin (smaller cube)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.8, 0, 2))
    cabin = bpy.context.active_object
    cabin.name = "TrainCabin"
    # Create front cylinder (boiler)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2, location=(-1.2, 0, 1))
    boiler = bpy.context.active_object
    boiler.name = "TrainBoiler"
    # Create wheels (4 cylinders)
    wheel_y = 0.7
    for x in [-1.5, -0.5, 0.5, 1.5]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.3, location=(x, wheel_y, 0.3), rotation=(1.5708, 0, 0))
        wheel = bpy.context.active_object
        wheel.name = f"WheelR_{x:.1f}"
        bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.3, location=(x, -wheel_y, 0.3), rotation=(1.5708, 0, 0))
        wheel = bpy.context.active_object
        wheel.name = f"WheelL_{x:.1f}"
    # Optionally, join main parts (base, cabin, boiler) into a single object
    bpy.ops.object.select_all(action='DESELECT')
    for obj_name in ["TrainBase", "TrainCabin", "TrainBoiler"]:
        bpy.data.objects[obj_name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["TrainBase"]
    bpy.ops.object.join()

def main():
    clear_scene()
    create_train()

if __name__ == "__main__":
    main()
