from .sup import AlwaysEqualProxy

class ExtractFromListNode:
    def __init__(self):
        self.title = "Extract From List"
        self.inputs = [{"name": "input_data", "type": AlwaysEqualProxy("*")}, {"name": "value", "type": "int"}]
        self.outputs = [{"name": "output_data", "type": AlwaysEqualProxy("*")}]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_data": (AlwaysEqualProxy("*"),),  # 通配符类型，允许任意输入
                "value": ("INT", {"default": 0, "min": 0}),  # int类型，默认值为0
            },
        }

    RETURN_TYPES = ("*",)  # 输出类型可以是任意类型
    FUNCTION = "process"
    CATEGORY = "CGAnimittaTools"

    def process(self, input_data, value):
        if isinstance(input_data, list) and len(input_data) > value:
            return (input_data[value],)
        else:
            return (None,)  # 如果索引超出范围，返回None
