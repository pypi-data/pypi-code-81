"""imagetag module
"""
def imgtag(imgpath):
    """Extracts EXIF metadata from photo and outputs relevant information

    Args:
        imgpath (str): path to image file

    Returns:
        dict: metadata information
    """    

    import exifread
    from exifread.utils import get_gps_coords

    # Open image file for reading (must be in binary mode)
    f = open(imgpath, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f, details=False)
    gps = get_gps_coords(tags)

    latdd = round(gps[0], 7)
    longdd = round(gps[1], 7)
    
    gpsaltval = [c.decimal() for c in tags["GPS GPSAltitude"].values]
    gpsalt = round(gpsaltval[0], 2)

    date = tags["Image DateTime"]
    imgh = tags["EXIF ExifImageLength"]
    imgw = tags["EXIF ExifImageWidth"]
    model = tags["Image Model"]

    print("UAS Model: " + str(model))
    print("Capture Date: " + str(date))
    print("Image resolution: " + str(imgh) + " x " + str(imgw))
    print("Latitude: " + str(latdd))
    print("Longitude: " + str(longdd))
    print("Altitude: " + str(gpsalt) + " meters")

    return [latdd, longdd, gpsalt]
