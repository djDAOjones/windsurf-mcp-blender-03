# Auto-enable Blender MCP add-on and start its server
import time
import sys

try:
    import bpy
    import addon_utils
except Exception as e:
    print(f"Startup script error importing Blender modules: {e}")
    sys.exit(0)

print("[Autostart] Looking for Blender MCP add-on...")

# Try to enable likely module names
candidates = [
    "blender_mcp",          # most probable
    "blender-mcp",          # fallback
    "blender_mcp.addon",    # in case it's nested as a submodule
    "addon",                # observed module name when installed in user scripts
]

for mod in candidates:
    try:
        addon_utils.enable(mod, default_set=True, persistent=True)
        print(f"[Autostart] Enabled add-on module: {mod}")
    except Exception as e:
        # Not fatal, continue trying
        pass

# Install safer screenshot handler to avoid image load/resize instability
def _install_safe_screenshot_handler():
    try:
        mod = None
        try:
            import addon as _m
            mod = _m
        except Exception:
            mod = sys.modules.get("addon")
        if mod is None:
            try:
                import blender_mcp.addon as _m
                mod = _m
            except Exception:
                print("[Autostart] Could not locate add-on module for patching")
                return
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
        mod.BlenderMCPServer.get_viewport_screenshot = _safe_get_viewport_screenshot
        print("[Autostart] Installed safer screenshot handler.")
    except Exception as e:
        print(f"[Autostart] Patch error: {e}")

_install_safe_screenshot_handler()

# Wait for operator to be available and start server
for i in range(60):
    has_ns = hasattr(bpy.ops, "blendermcp")
    has_op = has_ns and hasattr(bpy.ops.blendermcp, "start_server")
    if has_op:
        try:
            print("[Autostart] Starting Blender MCP server via operator...")
            res = bpy.ops.blendermcp.start_server()
            print(f"[Autostart] Operator returned: {res}")
            break
        except Exception as e:
            print(f"[Autostart] Operator error: {e}")
    time.sleep(0.5)
else:
    print("[Autostart] Could not find blendermcp.start_server operator. Is the add-on installed and enabled?")
