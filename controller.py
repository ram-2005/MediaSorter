import os
import shutil
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# loading the required directories
unsoted_dir = Path(os.getenv("UNSORTED"))
videos_dir = Path(os.getenv("VIDEOS"))
photos_dir = Path(os.getenv("VIDEOS"))

# Initialising the file type that we are going to handle
image_extensions = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
video_extensions = {".mp4", ".mov", ".avi", ".mkv", ".3gp"}

count = 0

for file in unsoted_dir.iterdir():

    count += 1


print(count)
