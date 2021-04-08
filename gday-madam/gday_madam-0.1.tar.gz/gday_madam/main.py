import datetime

def today():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")