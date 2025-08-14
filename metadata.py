# metadata.py
"""
Metadata extraction module.

Handles extraction of basic file metadata using standard library tools.
"""
import os
from pathlib import Path
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

class MetadataExtractor:
    """Extracts metadata from image files."""
    VALID_EXTENSIONS = {".jpg", ".jpeg", ".png"}

    def extract_directory(self, directory: Path) -> list:
        """Extract metadata from all images in a directory."""
        images = []
        for file_path in directory.iterdir():
            if file_path.suffix.lower() in self.VALID_EXTENSIONS:
                try:
                    metadata = self.extract(file_path)
                    images.append(metadata)
                except Exception as e:
                    print(f"Warning: Could not process {file_path}: {e}")
        return images

    def extract(self, file_path: Path) -> dict:
        """Extract metadata from a single image file."""
        try:
            stat = file_path.stat()
            with Image.open(file_path) as img:
