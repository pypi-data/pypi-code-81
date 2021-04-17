"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
RFF 2：Extension Header Protocol(EHP)
Authors: jdh99 <jdh821@163.com>
"""

import utzpy.nlv1 as nlv1
import utzpy.common as common

# 版本
EHP_VERSION_NAME = '1.1'

# 扩展头部
# 逐跳可选项头部
HEADER_HOP_BY_HOP_OPTIONS = 0x0
# 路由头部
HEADER_ROUTE = 0x1
# 分片头部
HEADER_FRAGMENT = 0x2
# 加密头部
HEADER_ENCRYPTION = 0x3
# FLP
HEADER_FLP = 0x4
# CMP
HEADER_CMP = 0x5
# WTS
HEADER_WTS = 0x5
# DUP
HEADER_DUP = 0x7
# SFTPA
HEADER_SFTP_A = 0x8
# SFTPB
HEADER_SFTP_B = 0x9
# STCP
HEADER_STCP = 0xA
# ITCP
HEADER_ITCP = 0xB
# DAP
HEADER_DAP = 0xC
# A类RSSI头部
HEADER_RSSI_A = 0xD
# B类RSSI头部
HEADER_RSSI_B = 0xE
# A类发送控制头部
HEADER_RADIO_TX_CONTROL_A = 0xF
# 125K激发RSSI头部
HEADER_EXCITER_RSSI = 0x10
# A类TOF定位头部
HEADER_TOF_LOCATION_A = 0x11
# A类DW1000接收头部
HEADER_DW1000_RX_A = 0x12
# A类DW1000发送完成头部
HEADER_DW1000_TX_END_A = 0x13
# A类坐标头部
HEADER_COORDINATE_A = 0x14
# 时间戳头部
HEADER_TIMESTAMP = 0x15
# 代理头部
HEADER_AGENT = 0x16
# 自组网控制头部
HEADER_ADHOCC = 0x17
# 压缩头部复合帧
HEADER_COMPRESS_COMPLEX = 0x18
# 标准头部复合帧
HEADER_STANDARD_COMPLEX = 0x19
# 全球单播地址分配服务器访问协议
HEADER_GUAAP = 0x1A
# 固定地址解析服务器访问协议
# 订阅服务器访问协议
# 简单安全头部
HEADER_SIMPLE_SECURITY = 0x1D
# 定长传输控制头部
HEADER_FIXED_LENGTH_TRANSFER_CONTROL = 0x1E
# 中继头部
HEADER_REPEAT = 0x1F
# 子分片头部
HEADER_SUB_FRAGMENT = 0x20
# 系统日志协议
HEADER_SLP = 0x22
# 设备间通信协议
HEADER_DCOM = 0x23
# 物联网终端协议
HEADER_ISH = 0x24


class RouteHeader:
    """路由头部结构"""

    def __init__(self):
        self.next_head = 0
        # 剩余路由数
        self.route_num = 0
        # 是否是严格源路由
        self.is_strict = False
        # 路由地址列表
        self.ia_list = list()


class SimpleSecurityHeader:
    """简单安全头部结构"""

    def __init__(self, next_head=0, pwd=''):
        self.next_head = next_head
        self.pwd = pwd


def bytes_to_route_header(data: bytearray) -> (RouteHeader, int):
    """
    字节流转换为路由头部
    :param data: 字节流data必须大于头部长度
    :return: 返回头部以及头部字节数.头部为None或者字节数为0表示转换失败
    """
    # 头部数据必须完整
    size = len(data)
    if size < 3:
        return None, 0

    header = RouteHeader()
    header.next_head = data[0]
    header_payload_len = data[1]
    if size < 2 + header_payload_len:
        return None, 0

    # 总长度不应该小于路由地址总长度
    header.route_num = data[2] & 0x7f
    header.is_strict = (data[2] >> 7) == 0x1
    if size < 3 + header.route_num * nlv1.IA_LEN:
        return None, 0

    header.ia_list.clear()
    offset = 3
    for i in range(header.route_num):
        header.ia_list.append(common.bytes_to_ia(data[offset:]))
        offset += nlv1.IA_LEN
    return header, offset


def route_header_to_bytes(header: RouteHeader) -> bytearray:
    """路由头部转换为字节流"""
    data = bytearray()
    data.append(header.next_head)
    # 头部数据长度
    header_payload_len = len(header.ia_list) * nlv1.IA_LEN + 1
    data.append(header_payload_len)

    route_num = header.route_num & 0x7f
    if header.is_strict:
        route_num |= 0x80
    data.append(route_num)

    for i in range(header.route_num):
        data += common.ia_to_bytes(header.ia_list[i])
    return data


def is_payload_header(head: int) -> bool:
    """是否载荷头部"""
    return (head == HEADER_FLP or head == HEADER_WTS or head == HEADER_DUP or head == HEADER_SFTP_A or
            head == HEADER_SFTP_B or head == HEADER_STCP or head == HEADER_ITCP or head == HEADER_DAP or
            head == HEADER_COMPRESS_COMPLEX or head == HEADER_STANDARD_COMPLEX or head == HEADER_GUAAP or
            head == HEADER_SLP or head == HEADER_DCOM or head == HEADER_ISH)


def bytes_to_simple_security_header(data: bytearray) -> (SimpleSecurityHeader, int):
    """
    字节流转换为简单安全头部
    :param data: 字节流data必须大于头部长度
    :return: 返回头部以及头部字节数.头部为None或者字节数为0表示转换失败
    """
    # 头部数据必须完整
    size = len(data)
    if size < 2:
        return None, 0

    header = SimpleSecurityHeader()
    header.next_head = data[0]
    header_payload_len = data[1]
    if size < 2 + header_payload_len:
        return None, 0

    header.pwd = data[2:2 + header_payload_len].decode('utf-8')
    return header, 2 + header_payload_len


def simple_security_header_to_bytes(header: SimpleSecurityHeader) -> bytearray:
    """简单安全头部转换为字节流"""
    data = bytearray()
    data.append(header.next_head)
    # 头部数据长度
    header_payload_len = len(header.pwd)
    data.append(header_payload_len)

    data += bytearray(header.pwd.encode())
    return data
