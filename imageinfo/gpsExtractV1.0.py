#! /usr/bin/env python

"""
Purpose: This script contains functions
that extract and return image information.
It is specifically geared towards
extracting GPS information from images.

##### USAGE EXAMPLES ######
Example 1:
>>>from imageinfo import gpsExtract
#load an image through PIL's Image object
>>>image = Image.open('C:/northfarmexp/cannon/can1.jpg') 
>>>exif_data = gpsExtract.get_exif_data(image)
>>>gpsInfo = gpsExtract.get_gps_info(exif_data)
>>>print gpsInfo


Example 2:
>>>from imageinfo import gpsExtract
>>>getgps = gpsExtract.gpsInfo
>>>gpsInfo = getgps("C:/northfarmexp/cannon/can1.jpg")
>>>gpsInfo



"""
__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/06/12 12:21:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
Author: Chris Zarzar & erans (from internet: https://gist.github.com/erans/983821)

Original creations: October 2011
Adopted by Chris Zarzar: June 2016

Notes: The majority of this scripts was adopted from the link above. Minor edits
were made to adjust this program to my needs.

Purpose: This script extracts and returns image information. It is specifically
geared towards extracting GPS information from images. There are four supporting
functions and there are two callable functions:
1. get_exif_data #Returns exif data extracted from an image file that has already been read in as a PIL Image item (i.e. Image.open()).
2. get_gps_info #Specifically extracts and returns GPS information about the given image.
3. gpsInfo #Combines functinos 1 and 2 to make it easier extract GPS information


Requirements:
1. Python Image Library (PIL)
2. ExifRead
______________________________________________________________________________
#### HISTORY ####

11-jun-2016 [Chris Zarzar]: Added altitude retreival to the
get_lat_lon_alt(exif_data) function. Added line of code to convert
rational number provided to actual meters.

12-jun-2016 [Chris Zarzar]: Added demo at end of script. Added new callable function
so someone can simply add the image path and make the two processes of collecting the
exif image information and then collecting the GPS information into 1 function
______________________________________________________________________________
"""
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    """Returns a dictionary from the exif data
    of a PIL Image item created by opening
    the image using Image.open('image'). Also
    converts the GPS Tags."""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
		
    return None
	
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    """This helper function simply takes the first and second value output for the
    Latitude and Longitude and calcualts the ratio. It then converts that value to degrees"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def _convert_to_meters(value):
    """Helper function to convert the altitude rational output to actual meters in float format"""
    v0 = value[0]
    v1 = value[1]
    v = float(v0) / float(v1)    

    return v



def _convert_to_feet(value):
    """Helper function to convert the altitude in meters to altitude in feet"""
    #First turn the rational altitude meter output to irrational number
    m0 = value[0]
    m1 = value[1]
    m = float(m0) / float(m1)    

    #Now convert m meters to feet

    f = m*3.28084

    return f

    
def get_gps_info(exif_data):
    """Returns the latitude, longitude, and altitude,
    if available, from the provided exif_data
    (exif_data obtained through get_exif_data() above)"""
    lat = None
    lon = None
    alt = None
    altft = None

    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')
        gps_altitude = _get_if_exist(gps_info, 'GPSAltitude')
        gps_altitude_ref = _get_if_exist(gps_info, 'GPSAltitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat
        
            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon
                

        if gps_altitude and str(gps_altitude_ref): #Had to make gps alt ref into string for if statement test to work.
            #Confirm that gps altitude is measured from ground level (i.e. 0)
            if gps_altitude_ref == 0: 
                alt = _convert_to_meters(gps_altitude)
                altft = _convert_to_feet(gps_altitude)
                    
    #Latitude and longitude are in decimal degrees. Altitude is provided first in meters, then in feet."
    return lat, lon, alt, altft

def gpsInfo(imagePath):
    """Takes the two prior functions and combines
    them to extract exif and gps information in one
    function. Returns the GPS latitude, longtitude,
    and altitude. Latitude and longitude are in
    decimal degrees, altitude is in meters and feet."""
    image = Image.open(imagePath)
    exif_data = get_exif_data(image)
    gpsinfo = get_gps_info(exif_data) 
    return gpsinfo #Latitude and longitude are in decimal degrees. Altitude is provided first in meters, then in feet."




#### DEMO ####
if __name__ == "__main__":
    image = Image.open(input("Insert path to an image:"))
    exif_data = get_exif_data(image)
    print get_gps_info(exif_data)


