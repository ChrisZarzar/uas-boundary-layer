#! /usr/bin/env python

"""
Purpose: This script contains functions
that extract and return image information.
It is specifically geared towards
extracting date information from images.
This script needs to be imported from
a python script. So this script 
should be placed in the site-packages.
I put it in a folder called imageInfo 
where I call this module and I call other
modules that extract other exif information. 

##### USAGE EXAMPLES ######
Example 1:



"""
__version__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2016/06/12 12:21:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
Author: Chris Zarzar 

Created by Chris Zarzar: September 2016



Purpose: This script extracts and returns image information. It is specifically
geared towards extracting date information from images. 


Requirements:
1. exifread
______________________________________________________________________________
#### HISTORY ####

CREATED Chris Zarzar 21-Sep-2016:

______________________________________________________________________________
"""
import exifread
from datetime import datetime

def get_exif_data(image):
    """Returns a dictionary from the exif data
    of a PIL Image item created by opening
    the image using Image.open('image'). Also
    converts the GPS Tags."""
    exif_data = exifread.process_file(image)
    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
		
    return None
	
    
def get_date_info(exif_data):
    """Returns date information,
    if available, from the provided exif_data
    (exif_data obtained through get_exif_data() above)"""

    org_datetime = _get_if_exist(exif_data, 'EXIF DateTimeOriginal').values
    d = datetime.strptime(org_datetime, '%Y:%m:%d %H:%M:%S')
    date = d.strftime('%Y-%m-%d')
    time = d.strftime('%H:%M:%S')

    return date, time

def dateInfo(imagePath):
    """Takes the two prior functions and combines
    them to extract exif and gps information in one
    function. Returns the GPS latitude, longtitude,
    and altitude. Latitude and longitude are in
    decimal degrees, altitude is in meters and feet."""
    image = open(imagePath, 'rb')
    exif_data = get_exif_data(image)
    dateinfo = get_date_info(exif_data) 
    return dateinfo 




