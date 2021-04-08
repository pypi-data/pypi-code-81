from holowan.HoloWAN import HoloWAN

if __name__ == '__main__':
    # 上传文件
    # holowan_ip = "192.168.1.223"
    # holowan_port = "8080"
    # filePath = r"C:\Users\Administrator\Desktop\zeren\Holowan的Recorder文件\net_status_step.db"
    # holowan = HoloWAN()
    # response = holowan.upload_recorder(holowan_ip=holowan_ip,
    #                                    holowan_port=holowan_port,
    #                                    filePath=filePath)
    # print(response)

    # 获取上传文件信息
    # holowan_ip = "192.168.1.223"
    # holowan_port = "8080"
    # holowan = HoloWAN()
    # response = holowan.get_recorder_information(holowan_ip=holowan_ip,
    #                                         holowan_port=holowan_port)
    # print(response)

    # 配置recorder
    # holowan_ip = "192.168.1.223"
    # holowan_port = "8080"
    # server_id = 1
    # engine_id = 1
    # path_id = 2
    # loss_base = 10
    # holowan = HoloWAN()
    # response = holowan.set_recorder_config(holowan_ip=holowan_ip,
    #                                        holowan_port=holowan_port,
    #                                        server_id=server_id,
    #                                        engine_id=engine_id,
    #                                        path_id=path_id,
    #                                        loss_base=loss_base)
    # print(response)

    # 获取最后一次配置信息
    # holowan_ip = "192.168.1.223"
    # holowan_port = "8080"
    # holowan = HoloWAN()
    # response = holowan.get_recorder_config(holowan_ip=holowan_ip,
    #                                        holowan_port=holowan_port)
    # print(response)

    # 释放链路
    # holowan_ip = "192.168.1.223"
    # holowan_port = "8080"
    # engineID = 1
    # pathID = 12
    # holowan = HoloWAN()
    # response = holowan.remove_recorder_config(holowan_ip=holowan_ip,
    #                                           holowan_port=holowan_port,
    #                                           engineID=engineID,
    #                                           pathID=pathID)
    # print(response)

    # 删除recorder文件信息
    # holowan_ip = "192.168.1.222"
    # holowan_port = "8080"
    # holowan = HoloWAN()
    # response = holowan.remove_recorder_information(holowan_ip=holowan_ip,
    #                                                holowan_port=holowan_port)
    # print(response)

    holowan_ip = "192.168.1.222"
    holowan_port = "8080"
    holowan = HoloWAN()
    response = holowan.get_HoloWAN_information(holowan_ip=holowan_ip,
                                               holowan_port=holowan_port)
    print(response)
