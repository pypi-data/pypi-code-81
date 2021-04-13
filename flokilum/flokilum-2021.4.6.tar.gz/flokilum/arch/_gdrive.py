def gdrive():

    from pathlib import Path

    gdata  = "./data"

    print(F"{'gdrive'.rjust(50)} : {gdata}")

    return Path(gdata)
