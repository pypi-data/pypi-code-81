"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
RFF 4：Control Message Protocol(CMP)
Authors: jdh99 <jdh821@163.com>
"""

# 版本
CMP_VERSION_NAME = '1.1'

# 消息类型
# 申请从机
CMP_MSG_TYPE_REQUEST_SLAVE_ROUTER = 0x88
# 分配从机
CMP_MSG_TYPE_ASSIGN_SLAVE_ROUTER = 0x89
# 连接父路由
CMP_MSG_TYPE_CONNECT_PARENT_ROUTER = 0x8A
# 确认连接父路由
CMP_MSG_TYPE_ACK_CONNECT_PARENT_ROUTER = 0x8B
