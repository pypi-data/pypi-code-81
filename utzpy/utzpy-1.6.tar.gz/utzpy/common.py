"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
通用模块
Authors: jdh99 <jdh821@163.com>
"""

# IA地址字节数
_IA_LEN = 8


def bytes_to_ia(data: bytearray) -> int:
    """从字节流中取出IA地址.字节流是大端"""
    if len(data) < _IA_LEN:
        return 0

    ia = 0
    for i in range(_IA_LEN):
        ia += data[i] << ((_IA_LEN - 1 - i) << 3)
    return ia


def ia_to_bytes(ia: int) -> bytearray:
    """将IA地址转换为字节流.字节流是大端"""
    data = bytearray()
    for i in range(_IA_LEN):
        data.append((ia >> ((_IA_LEN - 1 - i) << 3)) & 0xff)
    return data
