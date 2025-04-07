import socket
from pathlib import Path

class BlenderBridgeNode:
    """
    Custom node for sending 3D models to Blender

    Inputs:
        model_path: Absolute path to 3D model file
        port: Blender's listening port (must match)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "dynamicPrompts": False,
                }),
                "port": ("INT", {
                    "default": 54321,
                    "min": 1024,
                    "max": 65535,
                    "step": 1,
                }),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "send_model"
    OUTPUT_NODE = True
    CATEGORY = "CGAnimittaTools"

    def send_model(self, model_path, port):
        clean_path = Path(model_path.strip())

        # 验证文件
        if not clean_path.exists():
            raise ValueError(f"File does not exist: {clean_path}")

        if clean_path.suffix.lower() not in ['.obj', '.fbx', '.glb', '.gltf']:
            raise ValueError(f"Unsupported format: {clean_path.suffix}")

        # 发送到Blender
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect(('localhost', port))
                s.sendall(str(clean_path.resolve()).encode())
                print(f"[Comfy->Blender] Sent: {clean_path}")
        except ConnectionRefusedError:
            raise RuntimeError(
                f"Connection refused (port {port}). "
                "Ensure Blender server is running!"
            )
        except Exception as e:
            raise RuntimeError(f"Network error: {str(e)}")

        return ()
