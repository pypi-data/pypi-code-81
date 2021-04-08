from holowan.HoloWAN import HoloWAN
import json

def remove_all():
    holowan = HoloWAN()
    holowan_ip = "192.168.1.222"
    holowan_port = "8080"
    engine_id = 1
    for i in range(1, 11):
        path_id = i
        response = holowan.remove_playback(holowan_ip=holowan_ip,
                                           holowan_port=holowan_port,
                                           engineID=engine_id,
                                           pathID=path_id)
        print(response)

if __name__ == '__main__':
    # holowan_ip = "192.168.1.222"
    # holowan_port = "8080"
    # engine_id = 1
    # path_id = 1
    # holowan = HoloWAN()
    # filePath = r"C:\Users\Administrator\Desktop\recorder\data\3-19\合并B1.txt"
    # response = holowan.upload_and_apply_playback(holowan_ip=holowan_ip,
    #                                              holowan_port=holowan_port,
    #                                              engineID=engine_id,
    #                                              pathID=path_id,
    #                                              filePath=filePath)
    # print(response)

    remove_all()

    # holowan_ip = "192.168.1.222"
    # holowan_port = "8080"
    # engine_id = 1
    # path_id = 1
    # type = 1
    # holowan = HoloWAN()
    # response = holowan.get_playback_data(holowan_ip=holowan_ip,
    #                                      holowan_port=holowan_port,
    #                                      engineID=engine_id,
    #                                      pathID=path_id,
    #                                      type=type)
    # print(response)

    # holowan_ip = "192.168.1.222"
    # holowan_port = "8080"
    # engine_id = 1
    # path_id = 1
    # holowan = HoloWAN()
    # response = holowan.get_playback_status(holowan_ip=holowan_ip,
    #                                        holowan_port=holowan_port,
    #                                        engineID=engine_id,
    #                                        pathID=path_id)
    # print(response)