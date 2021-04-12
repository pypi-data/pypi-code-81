import purei9_unofficial.cloud
import purei9_unofficial.local
import purei9_unofficial.util
import purei9_unofficial.message

from purei9_unofficial.test_credentials import username, password

purei9_unofficial.util.DEBUG = True
"""
cloudrobots = []

cc1 = purei9_unofficial.cloud.CloudClient(username, password)
cloudrobots += cc1.getRobots()

cc2 = purei9_unofficial.cloud.CloudClientv2(username, password)

cc2.settoken("eyJhbGciOiJSUzI1NiIsImtpZCI6IjZDNzFEODIxN0E1RDBGODFCRTc5OEJFMDMwNzVCNTVDREVDQUNDNzAiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJiSEhZSVhwZEQ0Ry1lWXZnTUhXMVhON0t6SEEifQ.eyJuYmYiOjE2MTc2Mzk0OTYsImV4cCI6MTYxNzcyNTg5NiwiaXNzIjoiaHR0cHM6Ly9hdXRoLmRlbHRhLmVsZWN0cm9sdXguY29tIiwiYXVkIjoiY29ubmVjdGl2aXR5LWFwaSIsImNsaWVudF9pZCI6IldlbGxiZWluZyIsImNsaWVudF9kZWx0YV9zY29wZSI6WyJoaW1hbGF5YSIsIm9zaXJpcyIsImFzcGVuIiwib3Blbl9haXIiXSwiY2xpZW50X2lzYWJsZXRvY2hlY2t1c2VyZXh0aXN0ZW5jZSI6InRydWUiLCJzdWIiOiI3OWJjNDQ5OC0xNWU4LTQ0MmQtYWRmOC01ZTVlMjE1NzJkYzkiLCJhdXRoX3RpbWUiOjE2MTc2Mzk0OTYsImlkcCI6ImxvY2FsIiwibmFtZSI6InAuamVpdG5lckBwb3N0ZW8uZGUiLCJlbWFpbCI6InAuamVpdG5lckBwb3N0ZW8uZGUiLCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIiwiY29ubmVjdGl2aXR5LWFwaSIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJwd2QiXX0.SH2qGiRj8XdF42L7avw0nhCJWFpdG_lpSAvkCc9q5lR0lroD7UsJDXYkJ6B-57-l4MWFg8G3fzrxHbq3NL2nUISs5PevpdX5sioC2ixch5Hwtko-5sx0FXIJMOt-32G_JJDekATSoo7PjNFTfhaZKlv19PXwXmAbNKNvGActinpZG01D_MdhJ2mi_Oo22nkDuBQIpLwCAzLThR9671yZj2hqcLMSw3zpbVJSR7MyQgSKW7pWctLoAEZfFnEa7wwHN1v89-x5FCywy7BHAWg9Kb8NEwlB5lHXGCCOhZ73u18c9bKIokEFR6inskzHkQw9ojmO121Vlx62PEyx-ZIArg")

cloudrobots += cc2.getRobots()

for r in cloudrobots:
    try:
        print("getstatus   ", r.getstatus())
    except:
        print("getstatus   ", "exception")
    try:
        print("startclean  ", r.startclean)
    except:
        print("startclean  ", "exception")
    try:
        print("gohome      ", r.gohome)
    except:
        print("gohome      ", "exception")
    try:
        print("getid       ", r.getid())
    except:
        print("getid       ", "exception")
    try:
        print("getname     ", r.getname())
    except:
        print("getname     ", "exception")
    try:
        print("getbattery  ", r.getbattery())
    except:
        print("getbattery  ", "exception")
    try:
        print("getfirmware ", r.getfirmware())
    except:
        print("getfirmware ", "exception")
    try:
        print("getlocalpw  ", r.getlocalpw())
    except:
        print("getlocalpw  ", "exception")
    try:
        print("isconnected ", r.isconnected())
    except:
        print("isconnected ", "exception")
    
"""

robot = purei9_unofficial.local.RobotClient("127.0.0.1")
robot.connect("65612674")

# robot.sendrecv(purei9_unofficial.message.BinaryMessage.HeaderOnly(1020))

# print(robot.getwifinetworks())
# print(robot.getcapabilities())
# print(robot.getpowermode())
# print(robot.getsettings())
# print(robot.getmessages())

# print(robot.setlocalpw("65612675")) # does not work, maybe restricted to onboarding mode 
