import os
import json

# config 路径
def _config_filepath():
    home = "USERPROFILE" if os.name == "nt" else "HOME"
    configDir = os.path.join(os.environ[home], ".tda/")
    if not os.path.exists(configDir):
        os.makedirs(configDir)

    return os.path.join(configDir, "tda.conf")


# 未设置信息消息提示
def _noLoginMessage():
    print("您还未设置access_ke和secret_key, 请执行")
    print("\n")
    print("    tda config <access_key> <secret_key> [endpoint] 来设置您的tda")
    print("\n")
    print("关于tda config 更多帮助请执行：\n")
    print("    tda config --help")
    print("\n")
    exit()


# 检查登录
def _check():
    configFile = _config_filepath()
    if not os.path.exists(configFile):
        _noLoginMessage()

    with open(configFile, "r") as config:
        try:
            jsonObj = json.load(config)
        except:
            _noLoginMessage()

        if "access_key" not in jsonObj.keys():
            _noLoginMessage()

        if jsonObj["access_key"] == None or jsonObj["secret_key"] == None:
            _noLoginMessage()

        if jsonObj["access_key"] == "" or jsonObj["secret_key"] == "":
            _noLoginMessage()

    return True


# 获取conf
def _getConf():
    configFile = _config_filepath()
    if _check():
        with open(configFile, "r") as config:
            return json.load(config)
