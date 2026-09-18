#importing the necessary libraries
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from pymediainfo import MediaInfo



'''
Function to
Extract the metadata of a Image
'''
def imageExtractor(dir):

    #Opening the file and extracting the metadata
    image = Image.open(dir)
    exif = image.getexif()

    #Iterating through all the metadata
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)

        #Selecting the needed metadata which is Date and Time
        if tag == "DateTime":

            #Pushing the DateTime into Modifier
            return dateModifier(value)




'''
Function to Extract the
metadata of a Video
'''
def videoExtractor(dir):

    #Opening the video file and extracting the metadata
    video = MediaInfo.parse(dir)

    #Iterating through the metadata
    for track in video.tracks:
        data = track.to_data()
        for key,value in data.items():

            #Finding the Date and time metadata
            if key == "encoded_date":
                if track.track_type == 'General':

                    #Pushing the DateTime into Modifier
                    value = value.replace("UTC", "")#The output of this function has a UTC at end whic we dont want
                    value = value.replace("-", ":")#The output of this function has a - instead of : so we are replacing it
                    value = value.strip()#removing the trailing space

                    return dateModifier(value)




'''
Function to Extract the details
that we need from the metadata
'''
def dateModifier(value):

    #The given datetime will be a string thus converting to usable format
    date_taken = datetime.strptime(value,"%Y:%m:%d %H:%M:%S")

    #returing the values in a list [year, month]
    return [date_taken.year, date_taken.month]


