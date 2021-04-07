# -*- coding: utf-8 -*-

from typing import Union
from mod.common.component.baseComponent import BaseComponent
from typing import Tuple

class FeatureCompServer(BaseComponent):
    def AddNeteaseFeatureWhiteList(self, structureName):
        # type: (str) -> bool
        """
        添加结构对PlaceNeteaseStructureFeatureEvent事件的脚本层监听
        """
        pass

    def RemoveNeteaseFeatureWhiteList(self, structureName):
        # type: (str) -> bool
        """
        移除structureName对PlaceNeteaseStructureFeatureEvent事件的脚本层监听
        """
        pass

    def ClearAllNeteaseFeatureWhiteList(self):
        # type: () -> bool
        """
        清空所有已添加Netease Structure Feature对PlaceNeteaseStructureFeatureEvent事件的脚本层监听
        """
        pass

    def LocateStructureFeature(self, featureType, dimensionId, pos):
        # type: (int, int, Tuple[int,int,int]) -> Union[Tuple[float,float],None]
        """
        与/locate指令相似，用于定位原版的部分结构，如海底神殿、末地城等。
        """
        pass

    def LocateNeteaseFeature(self, featureName, dimensionId, pos):
        # type: (str, int, Tuple[int,int,int]) -> Union[Tuple[float,float,float],None]
        """
        与/locate指令相似，用于定位由网易自定义特征放置的结构，**通过PlaceStructure接口、/placestructure指令或结构方块手动放置的结构无法被定位到。如有需要，建议开发者自行记录这些手动放置的结构位置**
        """
        pass

