import requests
import socks
import socket


def saveImg(url, fileName="file", path=".\\"):
    """
        保存图片到本地
    :param url:
    :param fileName:
    :param path:
    :return:
    """
    response = requests.get(url, stream=True, verify=False)
    with open(f"{path}\\{fileName}", 'wb') as file:
        for chunk in response.iter_content():
            file.write(chunk)
    return True
