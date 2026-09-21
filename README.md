# MediaSorter

MediaSorter is a Python-based terminal application that organizes photos and
videos into a Year/Month directory structure using media metadata.

## Features

- Metadata-based date extraction
- Supports photos and videos
- Automatic Year/Month directory creation
- Terminal-based progress and summary
- Reports files processed, directories created, failures, and data copied
- Copies files before deletion
- Explicit confirmation before deleting originals

## Requirements

- Python 3.x
- Pillow
- pymediainfo
- python-dotenv
- Rich

## Installation

```bash
git clone <repository-url>
cd MediaSorter

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

