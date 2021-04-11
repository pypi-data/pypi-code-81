from chtool.install.common import *
from chtool.common import *




if __name__ == '__main__':

    pin = [
    ["root@172.16.16.4:22","@jacky666","seg3"],
    ["root@172.16.16.5:22","@jacky666","seg2"],
    ["root@172.16.16.6:22","@jacky666","seg1"]
    ]

    # threadpool(pin,yum).run(1)
    # threadpool(pin,firewalld).run(1)
    # threadpool(pin,hostname).run(3)
    # threadpool(pin,dns).run(3)

