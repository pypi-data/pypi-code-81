# -*- coding: utf-8 -*-

from typing import Union
from typing import Tuple

class AudioSystemComponentServer(object):
    def PlaySystemSound(self, playerId, soundId, pos, blockId, entityType, isBaby, isGlobal, dimensionId=-1):
        # type: (Union[str,None], int, Tuple[float,float,float], int, int, bool, bool, int) -> bool
        """
        播放游戏内原有内容
        """
        pass

