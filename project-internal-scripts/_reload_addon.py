from blender_mcp.server import BlenderConnection

CODE = r'''
import sys, importlib
print("[Reload] Attempting to reload blender_mcp.addon...")
mod = sys.modules.get('blender_mcp.addon')
if mod is None:
    import blender_mcp.addon as addon
    mod = addon
try:
    try:
        mod.unregister()
        print('[Reload] Unregistered existing add-on classes.')
    except Exception as e:
        print('[Reload] Unregister warning:', e)
    importlib.reload(mod)
    mod.register()
    print('[Reload] Reload complete.')
    result = 'ok'
except Exception as e:
    print('[Reload] Reload failed:', e)
    result = 'error: ' + str(e)
'''

if __name__ == "__main__":
    c = BlenderConnection('localhost', 9876)
    if not c.connect():
        print("FAIL: Could not connect to Blender MCP at localhost:9876")
        raise SystemExit(1)
    try:
        resp = c.send_command('execute_code', { 'code': CODE })
        print(resp)
    finally:
        c.disconnect()
