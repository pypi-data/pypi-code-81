import socket
def getipaddress():
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)
    ipaddress=ipaddress.replace('.','-')
    return ipaddress
def gettheuserid():
    try:
        userid=getipaddress()
    except:
        userid="unknown"
    return userid