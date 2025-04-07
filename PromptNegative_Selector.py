class PromptNegativeSelector:
    def __init__(self):
        self.presets = [
            "fake eyes, deformed eyes, bad eyes, cgi, 3D, digital, airbrushed",
            "cgi, 3D, digital, airbrushed",
            "(worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch),",
            "color, cartoonish, digital, (modern:1.1), cgi, 3D, airbrushed",
            "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime), text, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, embedding:BadDream, ",
            "None"  # 无内容选项
        ]
        self.selected_preset = self.presets[0]
        self.custom_prompt = ""

    @classmethod
    def INPUT_TYPES(cls):
        shortened_presets = [
            preset[:35] + "..." if len(preset) > 35 else preset
            for preset in cls().presets[:-1]
        ] + ["None"]
        return {
            "required": {
                "preset": (shortened_presets,),
            },
            "optional": {
                "custom_prompt": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompt"
    CATEGORY = "CGAnimittaTools"

    def generate_prompt(self, preset, custom_prompt=""):
        # 处理“None”选项
        if preset == "None":
            return (custom_prompt,)  # 仅输出自定义文本框内容
        else:
            # 获取预设内容
            index = [p[:35] + "..." if len(p) > 35 else p for p in self.presets[:-1]].index(preset)
            selected_prompt = self.presets[index]
            # 返回文本框内容 + 预设内容
            return (f"{custom_prompt} {selected_prompt}",)
