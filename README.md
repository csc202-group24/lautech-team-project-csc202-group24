# README.md
# Image Metadata Extractor and Organizer

A CLI tool to manage photo collections by extracting metadata, organizing files, detecting duplicates, analyzing storage, renaming files, and generating reports.

## Setup
- Requires Python 3.8+.
- No external dependencies; uses only standard library modules.
- Clone the repository and navigate to the `photo_manager` directory.

## Usage
Run commands from the terminal:
```bash
python main.py <command> [options]
```

### Commands
1. **Extract Metadata**:
   ```bash
   python main.py extract <directory>
   ```
   Extracts metadata (file size, date, etc.) from images.

2. **Organize Images**:
   ```bash
   python main.py organize <directory> --by [date|camera]
   ```
   Organizes images into subdirectories by date (YYYY-MM) or camera model.

3. **Detect Duplicates**:
   ```bash
   python main.py duplicates <directory> --action [list|move]
   ```
   Lists or moves duplicate images to a `Duplicates` folder.

4. **Analyze Storage**:
   ```bash
   python main.py storage <directory>
   ```
   Reports total storage usage and compression recommendations.

5. **Batch Rename**:
   ```bash
   python main.py rename <directory> --pattern <pattern>
   ```
   Renames images using metadata patterns (e.g., `YYYY-MM-DD_Model`).

6. **Generate Report**:
   ```bash
   python main.py report <directory> --format [text|csv]
   ```
   Generates a summary report in text or CSV format.

## Notes
- Supported formats: `.jpg`, `.jpeg`, `.png`.
- Metadata extraction is limited to basic file attributes due to standard library constraints.
- Run `python tests.py` to execute unit tests.

## Example
```bash
python main.py extract ./photos
python main.py organize ./photos --by date
python main.py report ./photos --format csv
```
