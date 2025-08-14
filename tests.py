# tests.py
"""
Unit tests for critical functions in the photo manager application.
"""
import unittest
from pathlib import Path
from metadata import MetadataExtractor
from duplicates import DuplicateDetector
import tempfile
import shutil

class TestPhotoManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        # Create dummy files for testing
        for i in range(2):
            with open(self.temp_dir / f"test{i}.jpg", "wb") as f:
                f.write(b"Dummy image content")
        with open(self.temp_dir / "test2.jpg", "wb") as f:  # Duplicate content
            f.write(b"Dummy image content")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_metadata_extraction(self):
        extractor = MetadataExtractor()
        images = extractor.extract_directory(self.temp_dir)
        self.assertEqual(len(images), 3)
        self.assertIn("path", images[0])
        self.assertIn("size", images[0])
        self.assertIn("date", images[0])

    def test_duplicate_detection(self):
        extractor = MetadataExtractor()
        images = extractor.extract_directory(self.temp_dir)
        detector = DuplicateDetector()
        duplicates = detector.find_duplicates(images)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(len(duplicates[0]), 2)  # test0.jpg and test2.jpg

if __name__ == "__main__":
    unittest.main()