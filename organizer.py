# organizer.py
"""
File organization module.

Organizes images into directories based on metadata criteria.
"""
from pathlib import Path
import shutil
import os

class Organizer:
    """Organizes image files based on metadata."""
    def organize(self, images: list, base_dir: Path, criterion: str):
        """Organize images into subdirectories."""
        for img in images:
            try:
                src = Path(img["path"])
                if criterion == "date":
                    sub_dir = base_dir / img["date"][:7]  # YYYY-MM
                else:  # camera
                    sub_dir = base_dir / img["camera"]
                sub_dir.mkdir(exist_ok=True)
                dst = sub_dir / src.name
                if src != dst:
                    shutil.move(str(src), str(dst))
                    img["path"] = str(dst)  # Update path in metadata
            except Exception as e:
                print(f"Warning: Could not move {img['path']}: {e}")