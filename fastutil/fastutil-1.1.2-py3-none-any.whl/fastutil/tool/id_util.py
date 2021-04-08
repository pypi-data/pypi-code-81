import socket
import uuid


def get_uid():
    host_name = socket.getfqdn(socket.gethostname())
    host_ip = socket.gethostbyname(host_name)
    uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, __file__ + '@' + host_ip))
    return uid
