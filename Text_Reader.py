import os

class TxtReaderNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "", "multiline": False}),
            },
        }

    RETURN_TYPES = ("LIST", "LIST")  # 输出为列表类型
    RETURN_NAMES = ("file_names", "file_contents")
    FUNCTION = "read_txt_files"

    CATEGORY = "CGAnimittaTools"

    def read_txt_files(self, folder_path):
        if not os.path.isdir(folder_path):
            raise ValueError(f"The provided path '{folder_path}' is not a valid directory.")

        file_names = []
        file_contents = []

        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                # 去掉 .txt 后缀
                name_without_extension = os.path.splitext(filename)[0]
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    file_names.append(name_without_extension)  # 存储不带后缀的文件名
                    file_contents.append(content)  # 存储文件内容

        # 返回文件名列表和文件内容列表
        return (file_names, file_contents)

