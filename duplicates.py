# duplicates.py
"""
Duplicate detection module.

Uses a simple hash-based approach to detect duplicate images.
"""
from pathlib import Path
import hashlib
import shutil

class DuplicateDetector:
    """Detects duplicate images using file content hashing."""
    def find_duplicates(self, images: list) -> list:
        """Find duplicate images based on file content."""
        hash_dict = {}
        duplicates = []
        for img in images:
            try:
                with open(img["path"], "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                if file_hash in hash_dict:
                    hash_dict[file_hash].append(img["path"])
                else:
                    hash_dict[file_hash] = [img["path"]]
            except Exception as e:
                print(f"Warning: Could not hash {img['path']}: {e}")
        for paths in hash_dict.values():
            if len(paths) > 1:
                duplicates.append(paths)
        return duplicates

    def handle_duplicates(self, duplicates: list, base_dir: Path, action: str):
        """Handle duplicates by listing or moving them."""
        if action == "list":
            for dup_set in duplicates:
                print(f"Duplicate set: {', '.join(dup_set)}")
        elif action == "move":
            dup_dir = base_dir / "Duplicates"
            dup_dir.mkdir(exist_ok=True)
            for dup_set in duplicates:
                for path in dup_set[1:]:  # Keep first file, move others
                    try:
                        shutil.move(path, dup_dir / Path(path).name)
                    except Exception as e:
                        print(f"Warning: Could not move {path}: {e}")