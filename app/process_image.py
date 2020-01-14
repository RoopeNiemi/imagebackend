from PIL.ExifTags import GPSTAGS, TAGS
from PIL import Image
import os

def extract_coordinates(image):
    image = Image.open(image)
    decoded = get_decoded(image)
    if decoded == None:
        return "", ""
    lat, lon = get_gps_info(decoded)
    return lat, lon

def get_gps_info(decoded):
    try:
        GPSdict = decoded['GPSInfo']
        dlat = GPSdict[2][0][0]/GPSdict[2][0][1]
        mlat = (GPSdict[2][1][0]/GPSdict[2][1][1])/60
        slat = (GPSdict[2][2][0]/GPSdict[2][2][1])/3600
        dlon = GPSdict[4][0][0]/GPSdict[4][0][1]
        mlon = (GPSdict[4][1][0]/GPSdict[4][1][1])/60
        slon = (GPSdict[4][2][0]/GPSdict[4][2][1])/3600
        if GPSdict[1] == 'N':
            lat = dlat+mlat+slat
        else:
            lat = (dlat+mlat+slat)*-1
        if GPSdict[3] == 'E':
            lon = dlon+mlon+slon
        else:
            lon = (dlon+mlon+slon)*-1
        return "%.8f" % lat, "%.8f" % lon
    except:
        print('JPG file but no GPS')
        print('--------------- ')
        print('  ')
        return "", ""

def get_decoded(image):
    info = image._getexif()
    if info == None:
        return None
    ret = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


