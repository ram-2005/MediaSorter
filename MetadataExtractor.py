#importing the necessary libraries
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime


def imageExtractor(dir):

    image = Image.open(dir)
    exif = image.getexif()

    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)

        if tag == "DateTime":

            date_taken = datetime.strptime(value,"%Y:%m:%d %H:%M:%S")
            print(date_taken.year, date_taken.month)



#__main__

imageExtractor("/mnt/shared/COLD/Media/Photos/unsorted/sample/IMG_20230630_130901_363.jpg")
