from blender_mcp.server import BlenderConnection

CODE = r'''
import sys
print('[Patch] Installing safer get_viewport_screenshot handler...')
try:
    import addon as addon_mod
except Exception as e:
    print('[Patch] Could not import addon module directly:', e)
    addon_mod = sys.modules.get('addon')

if not addon_mod:
    print('[Patch] ERROR: addon module not found in Blender. Is the MCP add-on enabled?')
    result = 'error'
else:
    import bpy
    def _safe_get_viewport_screenshot(self, max_size=800, filepath=None, format='png'):
        try:
            if not filepath:
                return {'error': 'No filepath provided'}
            area = None
            for a in bpy.context.screen.areas:
                if a.type == 'VIEW_3D':
                    area = a
                    break
            if not area:
                return {'error': 'No 3D viewport found'}
            width = height = None
            for r in area.regions:
                if r.type == 'WINDOW':
                    width, height = int(r.width), int(r.height)
                    break
            with bpy.context.temp_override(area=area):
                bpy.ops.screen.screenshot_area(filepath=filepath)
            if width is None or height is None:
                width = height = 0
            return {
                'success': True,
                'width': width,
                'height': height,
                'filepath': filepath,
                'note': 'safer handler (no image load/resize)'
            }
        except Exception as e:
            return {'error': str(e)}
    addon_mod.BlenderMCPServer.get_viewport_screenshot = _safe_get_viewport_screenshot
    print('[Patch] Handler replaced successfully.')
    result = 'ok'
'''

if __name__ == '__main__':
    c = BlenderConnection('localhost', 9876)
    if not c.connect():
        print('FAIL: Could not connect to Blender MCP at localhost:9876')
        raise SystemExit(1)
    try:
        resp = c.send_command('execute_code', {'code': CODE})
        print(resp)
    finally:
        c.disconnect()
