import bpy
import math
import os
import mathutils

def select_all_and_frame():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.view3d.view_selected(use_all_regions=False)

def set_view_and_capture(context, view_matrix, out_path):
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = context.copy()
                    override['area'] = area
                    override['region'] = region
                    # Set the view matrix
                    space = area.spaces.active
                    space.region_3d.view_matrix = view_matrix
                    bpy.ops.screen.screenshot(override, filepath=out_path)
                    return

def get_cube_views_and_capture(output_dir):
    context = bpy.context
    select_all_and_frame()
    # Define 6 directions (cube map): +X, -X, +Y, -Y, +Z, -Z
    views = {
        'posx': ((0, math.radians(90), 0)),
        'negx': ((0, math.radians(-90), 0)),
        'posy': ((math.radians(-90), 0, 0)),
        'negy': ((math.radians(90), 0, 0)),
        'posz': ((0, 0, 0)),
        'negz': ((math.radians(180), 0, 0)),
    }
    for name, rot in views.items():
        # Set the view rotation
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                space = area.spaces.active
                space.region_3d.view_perspective = 'PERSP'
                space.region_3d.view_rotation = mathutils.Euler(rot).to_quaternion()
                out_path = os.path.join(output_dir, f'scene_{name}.png')
                bpy.ops.screen.screenshot(filepath=out_path)

if __name__ == "__main__":
    output_dir = bpy.path.abspath('//')  # Save to current blend file directory
    get_cube_views_and_capture(output_dir)
    print(f"Screenshots saved to {output_dir}")
