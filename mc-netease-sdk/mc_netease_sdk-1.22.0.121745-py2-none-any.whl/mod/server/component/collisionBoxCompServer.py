# -*- coding: utf-8 -*-

from typing import Tuple

class CollisionBoxComponentServer(object):
    def SetSize(self, size):
        # type: (Tuple[int,int]) -> bool
        """
        设置实体的包围盒
        """
        pass

    def GetSize(self):
        # type: () -> Tuple[int,int]
        """
        获取实体的包围盒
        """
        pass

