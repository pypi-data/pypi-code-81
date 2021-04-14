# -*- coding: utf-8 -*-

from mod.common.component.baseComponent import BaseComponent

class TimeComponentServer(BaseComponent):
    def SetTime(self, time):
        # type: (int) -> bool
        """
        设置当前世界时间
        """
        pass

    def GetTime(self):
        # type: () -> int
        """
        获取当前世界时间
        """
        pass

