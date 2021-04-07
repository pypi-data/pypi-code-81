# -*- coding: utf-8 -*-

from typing import List
from mod.common.component.baseComponent import BaseComponent
from typing import Tuple

class DimensionCompServer(BaseComponent):
    def ChangePlayerDimension(self, dimensionId, pos):
        # type: (int, Tuple[int,int,int]) -> bool
        """
        传送玩家
        """
        pass

    def GetEntityDimensionId(self):
        # type: () -> int
        """
        获取实体所在维度
        """
        pass

    def ChangeEntityDimension(self, dimensionId, pos=None):
        # type: (int, Tuple[int,int,int]) -> bool
        """
        传送实体
        """
        pass

    def MirrorDimension(self, fromId, toId):
        # type: (int, int) -> bool
        """
        复制不同dimension的地形
        """
        pass

    def CreateDimension(self, dimensionId):
        # type: (int) -> bool
        """
        创建新的dimension
        """
        pass

    def RegisterEntityAOIEvent(self, dimension, name, aabb, ignoredEntities):
        # type: (int, str, Tuple[float,float,float,float,float,float], List[str]) -> bool
        """
        注册感应区域，有生物进入时和离开时会有消息通知
        """
        pass

    def UnRegisterEntityAOIEvent(self, dimension, name):
        # type: (int, str) -> bool
        """
        反注册感应区域
        """
        pass

