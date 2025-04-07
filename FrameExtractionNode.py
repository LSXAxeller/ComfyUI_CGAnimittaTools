# import comfy

class FrameSelector:
    """
    根据倍速参数从总帧数中提取关键帧
    输出结果从0开始计数，确保不超出最大帧号（总数-1）
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "total_frames": ("INT", {
                    "default": 81,
                    "min": 1,
                    "step": 1,
                    "display": "总帧数"
                }),
                "speed": ("INT", {
                    "default": 8,
                    "min": 1,
                    "step": 1,
                    "display": "采样间隔"
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_frames",)
    FUNCTION = "process"
    CATEGORY = "CGAnimittaTools"

    def process(self, total_frames, speed):
        max_frame = total_frames - 1
        start_frame = speed - 1

        # 生成关键帧序列
        selected = []
        current = start_frame
        while current <= max_frame:
            selected.append(str(current))
            current += speed

        return (",".join(selected),)


