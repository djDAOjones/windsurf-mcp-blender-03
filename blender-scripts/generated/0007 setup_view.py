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
    # Compute world-space bounds using object bounding boxes
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    all_corners = []
    for o in meshes:
        try:
            for c in o.bound_box:
                all_corners.append(o.matrix_world @ Vector(c))
        except Exception:
            pass
    if all_corners:
        min_x = min(v.x for v in all_corners)
        min_y = min(v.y for v in all_corners)
        min_z = min(v.z for v in all_corners)
        max_x = max(v.x for v in all_corners)
        max_y = max(v.y for v in all_corners)
        max_z = max(v.z for v in all_corners)
        center = Vector(((min_x + max_x) * 0.5, (min_y + max_y) * 0.5, (min_z + max_z) * 0.5))
        # Radius as half of the max dimension
        radius = max(max_x - min_x, max_y - min_y, max_z - min_z) * 0.5
        radius = max(radius, 0.5)
    else:
        center = Vector((0.0, 0.0, 0.0))
        radius = 2.0

    cam = ensure_camera(center)
    # Place camera at an offset relative to the bounds so everything fits
    offset = Vector((radius * 2.2, -radius * 2.2, radius * 1.2))
    cam.location = center + offset
    direction = (center - cam.location)
    if direction.length > 0:
        cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    sun = ensure_sun()
    sun.location = center + Vector((0.0, 0.0, radius * 3.0))

    # Configure the first 3D view area
    area3d = None
    for a in bpy.context.screen.areas:
        if a.type == 'VIEW_3D':
            area3d = a
            break
    if area3d is None:
        return

    # Set shading and perspective, and directly position the view without operators
    for space in area3d.spaces:
        if space.type == 'VIEW_3D':
            space.shading.type = 'SOLID'
            r3d = getattr(space, 'region_3d', None)
            if r3d is not None:
                r3d.view_perspective = 'PERSP'
                r3d.view_location = center
                # Use a generous distance so the model fits comfortably
                try:
                    r3d.view_distance = max(radius * 3.0, 3.0)
                except Exception:
                    pass

setup_view()
