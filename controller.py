import os
from pathlib import Path

from dotenv import load_dotenv

from dataclasses import dataclass

from MetadataExtractor import (
        video_extractor,
        image_extractor,
)

from FolderStructureController import (
        move_video_file,
        move_image_file,
)


load_dotenv()


UNSORTED_DIR = Path(os.getenv("UNSORTED"))


IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".heic",
        ".webp",
}

VIDEO_EXTENSIONS = {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".3gp"
}



@dataclass
class SortResult:
    files_scanned: int
    files_sorted: int
    files_skipped: int
    files_failed: int
    directories_created: int
    sorted_files: list



def main():

    files_scanned = 0
    files_sorted = 0
    files_skipped = 0
    files_failed = 0
    directories_created = 0

    sorted_files = []

    for file in UNSORTED_DIR.iterdir():

        if not file.is_file():
            continue

        files_scanned += 1

        extension = file.suffix.lower()

        try:

            if extension in IMAGE_EXTENSIONS:

                date = image_extractor(file)

                if date is None:
                    files_skipped += 1
                    continue

                year, month = date

                directory_created = move_image_file(
                        file,
                        year,
                        month
                )

            elif extension in VIDEO_EXTENSIONS:

                date = video_extractor(file)

                if date is None:
                    files_skipped += 1
                    continue

                year, month = date

                directory_created = move_video_file(
                        file,
                        year,
                        month
                )

            else:

                files_skipped += 1
                continue

            files_sorted += 1

            if directory_created:
                directories_created += 1

            sorted_files.append(file)

        except Exception as error:

            files_failed += 1

            print(f"\nFailed to Process {file}")
            print(f"Error: {error}")

            raise

    return SortResult(
        files_scanned = files_scanned,
        files_sorted = files_sorted,
        files_skipped = files_skipped,
        files_failed = files_failed,
        directories_created = directories_created,
        sorted_files = sorted_files
    )


if __name__ == "__main__":
    result = main()

    print()
    print("Sorting complete.")
    print()
    print(f"Files scanned:      {result.files_scanned}")
    print(f"Files sorted:       {result.files_sorted}")
    print(f"Files skipped:      {result.files_skipped}")
    print(f"Files failed:       {result.files_failed}")
    print(f"Directories created:{result.directories_created}")


