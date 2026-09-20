from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS
from pymediainfo import MediaInfo



def date_modifier(value):
    """
    Convert a metadata date string into [year, month].
    """

    value = value.replace("UTC","")
    value = value.replace("-",":")
    value = value.strip()

    date_taken = datetime.strptime(
            value,
            "%Y:%m:%d %H:%M:%S"
    )

    return date_taken.year, date_taken.month



def image_extractor(file_path):
    """
    Extract the capture date from an image.

    Returns:
        tuple[int, int] | None
        (year, month) if available, otherwise None.
    """

    with Image.open(file_path) as image:

        exif = image.getexif()

        for tag_id, value in exif.items():

            tag = TAGS.get(tag_id, tag_id)

            if tag == "DateTimeOriginal":
                return date_modifier(value)

        #Fallback
        for tag_id, value in exif.items():

            tag = TAGS.get(tag_id, tag_id)

            if tag == "DateTime":
                return date_modifier(value)

    return None



def video_extractor(file_path):
    """
    Extract the encoded date from a video

    Returns:
        tuple[int, int] | None:
        (year, month) if available, otherwise None.
    """

    video = MediaInfo.parse(file_path)

    for track in video.tracks:

        if track.track_type != "General":
            continue

        data = track.to_data()

        value = data.get("encoded_date")

        if value:
            return date_modifier(value)

    return None



