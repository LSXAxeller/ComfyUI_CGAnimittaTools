import os

class ListSubfoldersNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "", "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING", "INT", "STRING")  # 输出类型：字符串列表、整数、字符串
    RETURN_NAMES = ("subfolders", "subfolder_count", "folder_name")  # 输出端口名称
    FUNCTION = "list_subfolders"
    OUTPUT_NODE = True
    CATEGORY = "custom"

    def list_subfolders(self, folder_path):
        # 初始化默认值
        subfolders = []
        subfolder_count = 0
        folder_name = ""

        # 检查路径是否有效
        if os.path.isdir(folder_path):
            # 获取所有子文件夹路径
            subfolders = [os.path.join(folder_path, name) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
            # 获取子文件夹数量
            subfolder_count = len(subfolders)
            # 获取输入路径的最后一个文件夹名称
            folder_name = os.path.basename(os.path.normpath(folder_path))

        # 返回子文件夹路径列表、子文件夹数量和文件夹名称
        return (subfolders, subfolder_count, folder_name)
