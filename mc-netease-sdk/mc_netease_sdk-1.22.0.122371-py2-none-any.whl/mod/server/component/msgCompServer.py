# -*- coding: utf-8 -*-

from mod.common.component.baseComponent import BaseComponent

class MsgComponentServer(BaseComponent):
    def SendMsg(self, name, msg):
        # type: (str, str) -> bool
        """
        创建消息实体
        """
        pass

    def SendMsgToPlayer(self, fromEntityId, toEntityId, msg):
        # type: (str, str, str) -> None
        """
        创建消息实体，然后发送给某个玩家
        """
        pass

    def NotifyOneMessage(self, playerId, msg, color='\xc2\xa7f'):
        # type: (str, str, str) -> None
        """
        给指定玩家发送聊天框消息
        """
        pass

