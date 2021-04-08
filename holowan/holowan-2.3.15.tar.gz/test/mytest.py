from holowan.HoloWAN import HoloWAN
from holowan.HoloWAN import SubHoloWAN

if __name__ == '__main__':
    holowan_ip = "192.168.1.223"
    holowan_port = "8080"
    engineID = 1
    portID = 1
    holowan = HoloWAN()
    response = holowan.remove_all_IPV4_from_Classifier(holowan_ip=holowan_ip,
                                                       holowan_port=holowan_port,
                                                       engineID=engineID,
                                                       portID=portID)
    print(response)
    # subHolowan = SubHoloWAN(holowan_ip, holowan_port)
    # response = subHolowan.add_IPV4_to_Classifier()
    # print(type(response))
    # print(response)