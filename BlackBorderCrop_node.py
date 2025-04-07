import torch
import numpy as np
from PIL import Image, ImageOps

class BlackBorderCrop:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "threshold": ("INT", {
                    "default": 10,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "display": "slider"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "crop_black_border"
    CATEGORY = "CGAnimittaTools"

    def crop_black_border(self, image, threshold=10):
        # Convert tensor to PIL image
        image = image.squeeze().numpy()
        image = (image * 255).astype(np.uint8)
        pil_image = Image.fromarray(image)

        # Convert to grayscale
        grayscale = pil_image.convert("L")

        # Create a binary mask of non-black regions
        binary_mask = grayscale.point(lambda p: p > threshold and 255)

        # Find the bounding box of non-black regions
        bbox = binary_mask.getbbox()

        if bbox:
            # Crop the image to the bounding box
            cropped_image = pil_image.crop(bbox)
        else:
            # If no bounding box found, return the original image
            cropped_image = pil_image

        # Convert back to tensor
        cropped_image = np.array(cropped_image).astype(np.float32) / 255.0
        cropped_image = torch.from_numpy(cropped_image).unsqueeze(0)

        return (cropped_image,)


