def imgtag(imgpath):

    import exifread

    # Open image file for reading (must be in binary mode)
    f = open(imgpath, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f, details=False)

    longitude = tags["GPS GPSLongitude"]
    latitude = tags["GPS GPSLatitude"]
    altitude = tags["GPS GPSAltitude"]
    date = tags["Image DateTime"]
    imgh = tags["EXIF ExifImageLength"]
    imgw = tags["EXIF ExifImageWidth"]
    model = tags["Image Model"]

    print("UAS Model: " + str(model))
    print("Capture Date: " + str(date))
    print("Image resolution: " + str(imgh) + " x " + str(imgw))
    print("Longitude: " + str(longitude))
    print("Latitude: " + str(latitude))
    
    longstr = str(longitude)
    long = longstr[1:3]

    latstr = str(latitude)
    lat = latstr[1:3]


    return [lat, long]