import torch

class ColorToGrayscale:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    CATEGORY = "CGAnimittaTools"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "convert"

    def convert(self, image):
        # 确保输入是4D张量 [batch, height, width, channels]
        if image.dim() != 4:
            raise ValueError("Expected input to be 4D tensor")

        # 明度转换系数（CIE 601标准）
        weights = torch.tensor([0.299, 0.587, 0.114], device=image.device)

        # 转换颜色空间
        grayscale = torch.sum(image[..., :3] * weights, dim=-1, keepdim=True)

        # 将单通道灰度图像复制为3通道（兼容RGB格式）
        grayscale_rgb = grayscale.expand(-1, -1, -1, 3)

        # 保持alpha通道（如果有）
        if image.shape[-1] == 4:
            grayscale_rgb = torch.cat([grayscale_rgb, image[..., 3:4]], dim=-1)

        return (grayscale_rgb,)

