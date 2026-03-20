from pathlib import Path
import os
from uuid import uuid4

class StorageService:
    def __init__(self):
        self.media_root = Path(os.getenv("MEDIA_DIRECTORY", "./storage/media/apps"))
        self.base_url = os.getenv("MEDIA_BASE_URL", "/media/apps")

        # Ensure directory exists
        self.media_root.mkdir(parents=True, exist_ok=True)

    def _generate_filename(self, original_filename: str, prefix: str = ""):
        ext = original_filename.split(".")[-1]
        unique_name = f"{prefix}_{uuid4().hex}.{ext}" if prefix else f"{uuid4().hex}.{ext}"
        return unique_name

    def save(self, file, original_filename: str, prefix: str = ""):
        filename = self._generate_filename(original_filename, prefix)
        file_path = self.media_root / filename

        with file_path.open("wb") as f:
            f.write(file)

        return f"{self.base_url}/{filename}"

    def delete(self, file_url: str):
        if not file_url:
            return

        filename = file_url.split("/")[-1]
        file_path = self.media_root / filename

        if file_path.exists():
            file_path.unlink()