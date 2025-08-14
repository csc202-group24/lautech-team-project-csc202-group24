# main.py
"""
Image Metadata Extractor and Organizer CLI Application.

This module provides the command-line interface to manage photo collections by
extracting metadata, organizing files, detecting duplicates, analyzing storage,
renaming files, and generating reports.
"""
import argparse
import sys
from pathlib import Path
from metadata import MetadataExtractor
from organizer import Organizer
from duplicates import DuplicateDetector
from storage import StorageAnalyzer
from renamer import Renamer
from datetime import datetime

def setup_arg_parser():
    """Set up the CLI argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        description="Image Metadata Extractor and Organizer",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract metadata from images")
    extract_parser.add_argument("directory", help="Directory containing images")

    # Organize command
    organize_parser = subparsers.add_parser("organize", help="Organize images by metadata")
    organize_parser.add_argument("directory", help="Directory containing images")
    organize_parser.add_argument(
        "--by", choices=["date", "camera"], default="date",
        help="Organize by: date (default) or camera"
    )

    # Duplicates command
    duplicates_parser = subparsers.add_parser("duplicates", help="Detect duplicate images")
    duplicates_parser.add_argument("directory", help="Directory containing images")
    duplicates_parser.add_argument(
        "--action", choices=["list", "move"], default="list",
        help="Action: list duplicates (default) or move to Duplicates folder"
    )

    # Storage command
    storage_parser = subparsers.add_parser("storage", help="Analyze storage usage")
    storage_parser.add_argument("directory", help="Directory containing images")

    # Rename command
    rename_parser = subparsers.add_parser("rename", help="Batch rename images")
    rename_parser.add_argument("directory", help="Directory containing images")
    rename_parser.add_argument(
        "--pattern", default="YYYY-MM-DD_Model",
        help="Rename pattern (e.g., 'YYYY-MM-DD_Model')"
    )

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate summary report")
    report_parser.add_argument("directory", help="Directory containing images")
    report_parser.add_argument(
        "--format", choices=["text", "csv"], default="text",
        help="Report format: text (default) or csv"
    )

    return parser

def main():
    """Main function to handle CLI commands."""
    parser = setup_arg_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    directory = Path(args.directory)
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a valid directory")
        sys.exit(1)

    extractor = MetadataExtractor()
    images = extractor.extract_directory(directory)

    if args.command == "extract":
        for img in images:
            print(f"File: {img['path']}")
            for key, value in img.items():
                if key != "path":
                    print(f"  {key}: {value}")

    elif args.command == "organize":
        organizer = Organizer()
        organizer.organize(images, directory, args.by)
        print(f"Images organized by {args.by} in {directory}")

    elif args.command == "duplicates":
        detector = DuplicateDetector()
        duplicates = detector.find_duplicates(images)
        detector.handle_duplicates(duplicates, directory, args.action)
        print(f"Duplicate detection complete. Action: {args.action}")

    elif args.command == "storage":
        analyzer = StorageAnalyzer()
        total_size, recommendations = analyzer.analyze(images)
        print(f"Total storage: {total_size / (1024**2):.2f} MB")
        print("Compression recommendations:")
        for rec in recommendations:
            print(f"  {rec}")

    elif args.command == "rename":
        renamer = Renamer()
        renamer.rename(images, directory, args.pattern)
        print(f"Images renamed using pattern: {args.pattern}")

    elif args.command == "report":
        analyzer = StorageAnalyzer()
        total_size, _ = analyzer.analyze(images)
        detector = DuplicateDetector()
        duplicates = detector.find_duplicates(images)
        with open(directory / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}", "w") as f:
            if args.format == "text":
                f.write("Image Collection Report\n")
                f.write(f"Total Images: {len(images)}\n")
                f.write(f"Total Size: {total_size / (1024**2):.2f} MB\n")
                f.write(f"Duplicates Found: {len(duplicates)}\n")
                for dup_set in duplicates:
                    f.write(f"Duplicate set: {', '.join(dup_set)}\n")
            else:
                import csv
                writer = csv.writer(f)
                writer.writerow(["Metric", "Value"])
                writer.writerow(["Total Images", len(images)])
                writer.writerow(["Total Size (MB)", f"{total_size / (1024**2):.2f}"])
                writer.writerow(["Duplicates Found", len(duplicates)])
                for i, dup_set in enumerate(duplicates, 1):
                    writer.writerow([f"Duplicate Set {i}", ", ".join(dup_set)])
        print(f"Report generated in {directory}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

