# renamer.py
"""
Batch renaming module.

Renames images based on metadata patterns.
"""
from pathlib import Path
import shutil
from datetime import datetime

class Renamer:
    """Renames image files based on metadata patterns."""
    def rename(self, images: list, base_dir: Path, pattern: str):
        """Rename images using the specified pattern."""
        for img in images:
            try:
                src = Path(img["path"])
                name = pattern.replace("YYYY-MM-DD", img["date"]).replace("Model", img["camera"])
                base_name = name
                counter = 1
                dst = base_dir / f"{base_name}{src.suffix}"
                while dst.exists():
                    dst = base_dir / f"{base_name}_{counter:03d}{src.suffix}"
                    counter += 1
                shutil.move(str(src), str(dst))
                img["path"] = str(dst)  # Update path in metadata
            except Exception as e:
                print(f"Warning: Could not rename {img['path']}: {e}")
