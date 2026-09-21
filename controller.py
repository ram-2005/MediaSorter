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



def main(progress_callback=None):

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


        try:

            extension = file.suffix.lower()

            if extension in IMAGE_EXTENSIONS:

                date = image_extractor(file)

                if date is None:
                    files_skipped += 1

                else:
                    year, month = date

                    directory_created = move_image_file(
                            file,
                            year,
                            month
                    )

                    files_sorted += 1

                    if directory_created:
                        directories_created += 1

                    sorted_files.append(file)

            elif extension in VIDEO_EXTENSIONS:

                date = video_extractor(file)

                if date is None:
                    files_skipped += 1

                else:
                    year, month = date

                    directory_created = move_video_file(
                            file,
                            year,
                            month
                    )

                    files_sorted += 1

                    if directory_created:
                        directories_created += 1

                    sorted_files.append(file)

            else:

                files_skipped += 1

        except Exception as error:

            files_failed += 1

            print(f"\nFailed to Process {file}")
            print(f"Error: {error}")

            raise

        finally:

            if progress_callback:
                progress_callback(
                    files_scanned,
                    files_sorted,
                    files_skipped,
                    files_failed,
                    directories_created,
                    file
                )

    return SortResult(
        files_scanned = files_scanned,
        files_sorted = files_sorted,
        files_skipped = files_skipped,
        files_failed = files_failed,
        directories_created = directories_created,
        sorted_files = sorted_files
    )

def delete_sorted_files(sorted_files):
    """
    Delete only files that were successfully copied.
    """

    deleted = 0
    failed = 0

    for file in sorted_files:

        try:
            file.unlink()
            deleted += 1

        except OSError as error:
            failed += 1
            print(
                    f"Failed to delete {file}: {error}"
                    )

    return deleted, failed


if __name__ == "__main__":
    main()

