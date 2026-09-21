import shutil
from pathlib import Path

from dotenv import load_dotenv
import os


load_dotenv()


videos_dir = Path(os.getenv("VIDEOS"))
image_dir = Path(os.getenv("PHOTOS"))




MONTH_MATCHER = {

        1 : "January",
        2 : "February",
        3 : "March",
        4 : "April",
        5 : "May",
        6 : "June",
        7 : "July",
        8 : "August",
        9 : "September",
        10 : "October",
        11 : "November",
        12 : "December",

}




def move_video_file(source_file,year,month):
    month_name = MONTH_MATCHER[month]

    destination_dir = (
            videos_dir
            / str(year)
            / month_name
    )

    return move_file(source_file, destination_dir)




def move_image_file(source_file,year,month):
    month = MONTH_MATCHER[month]

    destination_dir = (
            image_dir
            / str(year)
            / month
    )

    return move_file(source_file, destination_dir)



def move_file(source_file, destination_dir):

    directory_created = not destination_dir.exists()

    destination_dir.mkdir(
            parents=True,
            exist_ok=True
            )

    destination_file = destination_dir / source_file.name

    shutil.copy2(
            source_file,
            destination_file
    )

    return directory_created
