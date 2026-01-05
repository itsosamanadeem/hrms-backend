import base64
from pathlib import Path

class Base64:
    def image_to_base64(self, modules_images):
        result = []

        for module in modules_images:
            image_path = module.get("cover_image")
            if image_path and Path(image_path).exists():
                with open(image_path, "rb") as img:
                    encoded = base64.b64encode(img.read()).decode("utf-8")
            else:
                encoded = None

            result.append({
                "name": module["name"],
                "cover_image_base64": encoded
            })

        return result