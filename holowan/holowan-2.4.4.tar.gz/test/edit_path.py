from holowan.HoloWAN import HoloWAN
import sys

# holowan_ip = "192.168.1.198"
# holowan_port = "8080"
# engineID = 1
# pathID = 1
# pathDirection = 1
# delay = 2.0
# holowan = HoloWAN()
# response = holowan.set_Delay_Constant(holowan_ip=holowan_ip,
#                                       holowan_port=holowan_port,
#                                       engineID=engineID,
#                                       pathID=pathID,
#                                       pathDirection=pathDirection,
#                                       delay=delay)
# print(response)






if __name__ == '__main__':
    argvs = sys.argv
    ip = argvs[1]
    port = argvs[2]
    engine = argvs[3]
    pathID = argvs[4]
    directory = argvs[5]
    delay = argvs[6]
    rate = argvs[7]
    holowan = HoloWAN()

    response1 = holowan.set_Delay_Constant(holowan_ip=ip,
                                          holowan_port=port,
                                          engineID=int(engine),
                                          pathID=int(pathID),
                                          pathDirection=int(directory),
                                          delay=float(delay))

    response2 = holowan.set_Loss_Random(holowan_ip=ip,
                                       holowan_port=port,
                                       engineID=int(engine),
                                       pathID=int(pathID),
                                       pathDirection=int(directory),
                                       rate=float(rate))
    print(response1)
    print(response2)