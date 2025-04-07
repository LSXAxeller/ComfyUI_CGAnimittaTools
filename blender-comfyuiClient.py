import bpy
import socket
import threading
from pathlib import Path
from bpy.props import IntProperty, StringProperty, BoolProperty
from bpy.types import Operator, Panel

bl_info = {
    "name": "ComfyUI Bridge",
    "author": "无相CG艺术CGAnimitta",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > ComfyUI",
    "description": "Real-time bridge for importing models from ComfyUI",
    "warning": "",
    "doc_url": "",
    "category": "Import",
}

# 全局服务器控制变量
server_running = False
server_thread = None

def import_model_safe(filepath):
    """线程安全的模型导入函数"""
    SUPPORTED_FORMATS = {
        '.obj': 'import_scene.obj',
        '.fbx': 'import_scene.fbx',
        '.glb': 'import_scene.gltf',
        '.gltf': 'import_scene.gltf',
    }

    def import_operator():
        try:
            ext = Path(filepath).suffix.lower()
            if ext in SUPPORTED_FORMATS:
                # 先取消所有选择
                bpy.ops.object.select_all(action='DESELECT')
                # 执行导入
                module_name = SUPPORTED_FORMATS[ext]
                module_parts = module_name.split('.')
                if len(module_parts) == 2:
                    module = getattr(bpy.ops, module_parts[0])
                    operator = getattr(module, module_parts[1])
                    operator(filepath=filepath)
                    print(f"[ComfyUI Bridge] 成功导入: {filepath}")
                    bpy.context.scene.comfy_last_import = filepath
                else:
                    print(f"[ComfyUI Bridge] 不支持的导入格式配置: {module_name}")
            else:
                print(f"[ComfyUI Bridge] 不支持的格式: {ext}")
        except Exception as e:
            print(f"[ComfyUI Bridge] 导入失败: {str(e)}")

    # 在主线程中执行导入操作
    bpy.app.timers.register(import_operator)

def comfy_server_loop(port):
    """服务器主循环"""
    global server_running

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.bind(('localhost', port))
            s.listen()
            print(f"[ComfyUI Bridge] 正在监听端口 {port}")

            while server_running:
                try:
                    conn, addr = s.accept()
                    with conn:
                        data = conn.recv(1024).decode().strip()
                        if data:
                            print(f"[ComfyUI Bridge] 收到模型路径: {data}")
                            import_model_safe(data)
                except socket.timeout:
                    continue
        finally:
            print("[ComfyUI Bridge] 服务器已停止")

class COMFY_OT_StartServer(Operator):
    """启动ComfyUI桥接服务器"""
    bl_idname = "comfy.start_server"
    bl_label = "启动服务器"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return not server_running

    def execute(self, context):
        global server_running, server_thread

        port = context.scene.comfy_bridge_port

        # 检查端口是否可用
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind(('localhost', port))
            test_socket.close()
        except OSError as e:
            self.report({'ERROR'}, f"端口 {port} 不可用: {str(e)}")
            return {'CANCELLED'}

        server_running = True
        server_thread = threading.Thread(
            target=comfy_server_loop,
            args=(port,),
            daemon=True
        )
        server_thread.start()

        context.scene.comfy_server_running = True
        self.report({'INFO'}, f"服务器已在端口 {port} 启动")
        return {'FINISHED'}

class COMFY_OT_StopServer(Operator):
    """停止ComfyUI桥接服务器"""
    bl_idname = "comfy.stop_server"
    bl_label = "停止服务器"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return server_running

    def execute(self, context):
        global server_running, server_thread

        server_running = False

        if server_thread:
            server_thread.join(timeout=2)
            server_thread = None

        context.scene.comfy_server_running = False
        self.report({'INFO'}, "服务器已停止")
        return {'FINISHED'}

class COMFY_PT_MainPanel(Panel):
    """主控制面板"""
    bl_label = "ComfyUI Bridge"
    bl_idname = "COMFY_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ComfyUI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # 服务器控制区域
        box = layout.box()
        box.label(text="服务器设置", icon='SETTINGS')

        row = box.row()
        row.prop(scene, "comfy_bridge_port", text="端口号")

        row = box.row()
        if server_running:
            row.operator("comfy.stop_server", text="停止服务器", icon='CANCEL')
            row.label(text="状态: 运行中", icon='CHECKMARK')
        else:
            row.operator("comfy.start_server", text="启动服务器", icon='PLAY')
            row.label(text="状态: 已停止", icon='X')

        # 最近导入显示
        if scene.comfy_last_import:
            box = layout.box()
            box.label(text="最近导入的模型", icon='IMPORT')
            box.label(text=scene.comfy_last_import)

def register():
    # 注册场景属性
    bpy.types.Scene.comfy_bridge_port = IntProperty(
        name="端口号",
        description="通信端口号 (1024-65535)",
        default=54321,
        min=1024,
        max=65535
    )
    bpy.types.Scene.comfy_server_running = BoolProperty(
        name="服务器状态",
        default=False
    )
    bpy.types.Scene.comfy_last_import = StringProperty(
        name="最后导入",
        default="",
        subtype='FILE_PATH'
    )

    # 注册操作类和面板
    classes = (
        COMFY_OT_StartServer,
        COMFY_OT_StopServer,
        COMFY_PT_MainPanel,
    )
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # 停止服务器
    global server_running
    if server_running:
        server_running = False

    # 注销类和属性
    classes = (
        COMFY_OT_StartServer,
        COMFY_OT_StopServer,
        COMFY_PT_MainPanel,
    )
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.comfy_bridge_port
    del bpy.types.Scene.comfy_server_running
    del bpy.types.Scene.comfy_last_import

if __name__ == "__main__":
    register()
