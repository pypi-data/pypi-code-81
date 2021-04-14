# -*- coding: utf-8 -*-

from mod.common.component.baseComponent import BaseComponent

class FlyComponentServer(BaseComponent):
    def IsPlayerFlying(self):
        # type: () -> bool
        """
        获取玩家是否在飞行
        """
        pass

    def ChangePlayerFlyState(self, isFly):
        # type: (bool) -> bool
        """
        改变玩家的飞行状态
        """
        pass

