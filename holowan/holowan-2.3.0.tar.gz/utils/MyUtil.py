import hashlib
import re
import requests
import os
from utils import XmlUtil as xt
from configparser import ConfigParser
import socket


# md5加密
def md5_encryption(raw_data):
    m = hashlib.md5()
    data = raw_data.encode(encoding='utf-8')
    m.update(data)
    data_md5 = m.hexdigest()
    return data_md5


# 压缩xml
def compress_xml(xml):
    return re.sub('>\s+<', "><", xml)


# post调用原始api
def post_original_api(url, body):
    if url == "" or url is None:
        raise RuntimeError("url为空")
    if body == "" or body is None:
        raise RuntimeError("body为空")
    body = compress_xml(body)
    url_md5 = md5_encryption("/" + url.split("/")[-1])
    body_md5 = md5_encryption(body)
    headers = {
        "URL-MD5": url_md5,
        "Body-MD5": body_md5,
        "Content-Type": "text/xml;charset=UTF-8"
    }
    response = requests.post(url, data=body, headers=headers)
    response.encoding = "utf-8"
    return response.text


# get调用原始api
def get_original_api(url):
    response = requests.get(url)
    response.encoding = "utf-8"
    return response.text


# 发送xml数据（xml数据在文件中）
def send_xml_infile(api, xml_file):
    body_data = open(xml_file, encoding='utf-8').read()
    return post_original_api(api, body_data)


# 发送xml数据
def send_xml(api, xml):
    return post_original_api(api, xml)


# 发送get请求，获取数据
def get(api):
    return get_original_api(api)


# 判断文件是否存在
def file_exists(file_dir):
    return os.path.exists(file_dir)


# 删除文件
def del_file(file_dir):
    if file_exists(file_dir):
        os.remove(file_dir)


# 创建文件， 并写入内容
def create_and_write_file(file_dir, text):
    f = open(file_dir, "w+")
    f.write(text)
    f.close()


# 判断字符串是否为ip地址
def isIP(ipStr: str) -> bool:
    if isIPV4(ipStr) or isIPV6(ipStr):
        return True
    else:
        return False


# 判断字符串是否为IPV4地址
def isIPV4(ipStr: str) -> bool:
    if re.compile("^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$").match(ipStr):
        return True
    else:
        return False


# 判断字符串是否为IPV6地址
def isIPV6(ipStr: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET6, ipStr)
    except socket.error:
        return False
    return True


# 判断字符串是否为端口号
def isPort(portStr: str) -> bool:
    if int(portStr) >= 1 and int(portStr) <= 65535:
        return True
    else:
        return False


# 判断字符串是否为两位十六进制数
def isDoubleHexadecimal(theStr):
    if len(theStr) == 2:
        pattern = "[0-9a-fA-F]{2}"
        p = re.compile(pattern)
        if p.match(theStr):
            return True
        else:
            return False
    else:
        return False


# 获取HoloWAN_parameter.xml数据
def getProperties(nodeTag):
    project_path = os.path.dirname(os.path.dirname(__file__))
    fileName = r"{}\holowan\resources\HoloWAN_parameter.xml".format(project_path)
    tree = xt.xmlFile_to_Object(fileName)
    return xt.get_node(tree, r"./{}".format(nodeTag)).text


# 判断四位整数
def isFourInteger(num: int) -> bool:
    if isinstance(num, int):
        if len(str(num)) == 4:
            return True
        else:
            return False
    else:
        return False


# 判断是整数
def isInteger(theNum: int) -> bool:
    if isinstance(theNum, int):
        return True
    else:
        raise RuntimeError('{"errCode":"-1","errMsg":"ERROE","errReason":"Parameter type error"}')


# 读取ini文件
def open_ini(filePath):
    config = ConfigParser()
    config.read(filePath)
    return config




if __name__ == '__main__':
    url = "http://192.168.1.222:8080/emulator_config"
    body = '''<?xml version="1.0" encoding="UTF-8"?><clc><engine_id>1</engine_id><port><port_id>1</port_id><comb><ipv4><src>192.168.1.111</src><smask>32</smask><dst any="1"/><dmask>32</dmask><tos any="1"/></ipv4><tcp_udp><type>2</type><src>5222</src><dst>5333</dst><check>0</check></tcp_udp><path_id>1</path_id></comb><ipv4><src any="1" ></src><smask>32</smask><dst any="1" ></dst><dmask>32</dmask><tos any="1" ></tos><path_id>1</path_id></ipv4></port><port><port_id>2</port_id><ipv4><src>192.168.1.222</src><smask>32</smask><dst any="1" ></dst><dmask>32</dmask><tos any="1" ></tos><path_id>3</path_id></ipv4><ipv4><src>192.168.1.222</src><smask>32</smask><dst any="1" ></dst><dmask>32</dmask><tos any="1" ></tos><path_id>-2</path_id></ipv4><ipv4><src>192.168.1.222</src><smask>32</smask><dst any="1" ></dst><dmask>32</dmask><tos any="1" ></tos><path_id>-1</path_id></ipv4><ipv4><src any="1" ></src><smask>32</smask><dst any="1" ></dst><dmask>32</dmask><tos any="1" ></tos><path_id>1</path_id></ipv4></port></clc>'''
    response = post_original_api(url, body)
    print(response)

