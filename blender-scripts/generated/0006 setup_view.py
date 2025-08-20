import bpy
from mathutils import Vector


def ensure_camera(target=Vector((0.0, 0.0, 0.5))):
    # Use existing camera or create one
    cam_obj = None
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            cam_obj = obj
            break
    if cam_obj is None:
        cam_data = bpy.data.cameras.new(name="Camera")
        cam_obj = bpy.data.objects.new("Camera", cam_data)
        bpy.context.scene.collection.objects.link(cam_obj)

    # Position and aim at target
    cam_obj.location = Vector((5.0, -5.0, 3.0))
    direction = (target - cam_obj.location)
    if direction.length > 0:
        quat = direction.to_track_quat('-Z', 'Y')
        cam_obj.rotation_euler = quat.to_euler()

    if bpy.context.scene.camera != cam_obj:
        bpy.context.scene.camera = cam_obj
    return cam_obj


def ensure_sun():
    sun = None
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT' and obj.data.type == 'SUN':
            sun = obj
            break
    if sun is None:
        light_data = bpy.data.lights.new(name="Sun", type='SUN')
        sun = bpy.data.objects.new(name="Sun", object_data=light_data)
        bpy.context.scene.collection.objects.link(sun)
    sun.location = Vector((0.0, 0.0, 5.0))
    sun.rotation_euler = (0.0, 0.0, 0.0)
    sun.data.energy = 3.0
    return sun


def setup_view():
    # Try to compute a reasonable target from all mesh objects
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    if meshes:
        # Average location as a simple centroid
        avg = Vector((0.0, 0.0, 0.0))
        for o in meshes:
            avg += o.location
        avg /= len(meshes)
    else:
        avg = Vector((0.0, 0.0, 0.0))

    ensure_camera(avg)
    ensure_sun()

    # Configure the first 3D view area
    area3d = None
    for a in bpy.context.screen.areas:
        if a.type == 'VIEW_3D':
            area3d = a
            break
    if area3d is None:
        return

    # Set shading and perspective, then frame all
    for space in area3d.spaces:
        if space.type == 'VIEW_3D':
            space.shading.type = 'SOLID'
            if hasattr(space, 'region_3d') and space.region_3d:
                space.region_3d.view_perspective = 'PERSP'

    # Frame all objects in the area
    override = bpy.context.copy()
    override['area'] = area3d
    # pick a WINDOW region if present
    for r in area3d.regions:
        if r.type == 'WINDOW':
            override['region'] = r
            break
    bpy.ops.view3d.view_all(override, center=True)

setup_view()
