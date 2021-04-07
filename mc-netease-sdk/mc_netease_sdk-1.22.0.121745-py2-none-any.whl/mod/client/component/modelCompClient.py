# -*- coding: utf-8 -*-

from typing import List
from mod.common.component.baseComponent import BaseComponent
from typing import Tuple

class ModelComponentClient(BaseComponent):
    def SetModel(self, modelName):
        # type: (str) -> int
        """
        替换实体的骨骼模型
        """
        pass

    def GetModelId(self):
        # type: () -> int
        """
        获取骨骼模型的Id，主要用于特效绑定骨骼模型
        """
        pass

    def ResetModel(self):
        # type: () -> bool
        """
        恢复实体为原版模型
        """
        pass

    def PlayAnim(self, aniName, isLoop):
        # type: (str, bool) -> bool
        """
        播放骨骼动画
        """
        pass

    def GetPlayingAnim(self):
        # type: () -> str
        """
        获取当前播放的骨骼动画名称
        """
        pass

    def GetAnimLength(self, aniName):
        # type: (str) -> float
        """
        获取某个骨骼动画的长度，单位为秒
        """
        pass

    def SetAnimSpeed(self, aniName, speed):
        # type: (str, float) -> bool
        """
        设置某个骨骼动画的播放速度
        """
        pass

    def BindModelToModel(self, boneName, modelName):
        # type: (str, str) -> int
        """
        在骨骼模型上挂接其他骨骼模型
        """
        pass

    def UnBindModelToModel(self, modelId):
        # type: (int) -> bool
        """
        取消骨骼模型上挂接的某个骨骼模型。取消挂接后，这个modelId的模型便会销毁，无法再使用，如果是临时隐藏可以使用HideModel
        """
        pass

    def BindModelToEntity(self, boneName, modelName):
        # type: (str, str) -> int
        """
        实体替换骨骼模型后，再往上其他挂接骨骼模型。对实体播骨骼动作时，其上面挂接的模型也会播相同的动作。
        """
        pass

    def UnBindModelToEntity(self, modelId):
        # type: (int) -> bool
        """
        取消实体上挂接的某个骨骼模型。取消挂接后，这个modelId的模型便会销毁，无法再使用，如果是临时隐藏可以使用HideModel
        """
        pass

    def GetAllBindModelToEntity(self, boneName):
        # type: (str) -> List[int]
        """
        获取实体上某个骨骼上挂接的所有骨骼模型的id
        """
        pass

    def PlayBodyAnim(self, bodyAniName, bodyIsLoop):
        # type: (str, bool) -> bool
        """
        上下半身分离时，对上半身播放动画
        """
        pass

    def StopBodyAnim(self):
        # type: () -> bool
        """
        停止上半身动画
        """
        pass

    def PlayLegAnim(self, legAniName, legIsLoop):
        # type: (str, bool) -> bool
        """
        上下半身分离时，对下半身播放动画
        """
        pass

    def StopLegAnim(self):
        # type: () -> bool
        """
        停止下半身动画
        """
        pass

    def SetTexture(self, texture):
        # type: (str) -> bool
        """
        替换骨骼模型的贴图
        """
        pass

    def SetSkin(self, skin):
        # type: (str) -> bool
        """
        更换原版自定义皮肤
        """
        pass

    def SetLegacyBindRot(self, enable):
        # type: (bool) -> bool
        """
        用于修复特效挂接到骨骼时的方向
        """
        pass

    def GetBoneWorldPos(self, boneName):
        # type: (str) -> Tuple[int,int,int]
        """
        获取骨骼的坐标
        """
        pass

    def GetEntityBoneWorldPos(self, entityId, boneName):
        # type: (str, str) -> Tuple[int,int,int]
        """
        获取换了骨骼模型的实体的骨骼坐标
        """
        pass

    def CreateFreeModel(self, modelName):
        # type: (str) -> int
        """
        创建自由的模型（无需绑定Entity）
        """
        pass

    def RemoveFreeModel(self, modelId):
        # type: (int) -> bool
        """
        移除自由模型
        """
        pass

    def SetFreeModelPos(self, modelId, x, y, z):
        # type: (int, float, float, float) -> bool
        """
        设置自由模型的位置
        """
        pass

    def SetFreeModelRot(self, modelId, x, y, z):
        # type: (int, float, float, float) -> bool
        """
        设置自由模型的方向
        """
        pass

    def SetFreeModelScale(self, modelId, x, y, z):
        # type: (int, float, float, float) -> bool
        """
        设置自由模型的大小
        """
        pass

    def ModelPlayAni(self, modelId, aniName, isLoop=False):
        # type: (int, str, bool) -> None
        """
        纯骨骼播放动作
        """
        pass

    def HideModel(self, modelId):
        # type: (int) -> None
        """
        隐藏纯模型
        """
        pass

    def ShowModel(self, modelId):
        # type: (int) -> None
        """
        显示纯模型
        """
        pass

    def SetFreeModelBoundingBox(self, modelId, min, max):
        # type: (int, Tuple[float,float,float], Tuple[float,float,float]) -> bool
        """
        设置模型包围盒
        """
        pass

    def BindEntityToEntity(self, bindEntityId):
        # type: (str) -> bool
        """
        绑定骨骼模型跟随其他entity,摄像机也跟随其他entity
        """
        pass

    def ResetBindEntity(self):
        # type: () -> bool
        """
        取消目标entity的绑定实体，取消后不再跟随任何其他entity
        """
        pass

    def SetModelOffset(self, offset):
        # type: (Tuple[float,float,float]) -> None
        """
        模型增加偏移量
        """
        pass

    def SetModelPerspectiveEffect(self, isPerspective, color):
        # type: (bool, Tuple[float,float,float,float]) -> None
        """
        设置模型透视效果。注：只对自定义骨骼模型生效
        """
        pass

    def SetEntityOpacity(self, opacity):
        # type: (float) -> None
        """
        设置生物模型的透明度
        """
        pass

    def ShowCommonHurtColor(self, show):
        # type: (bool) -> bool
        """
        设置挂接骨骼模型的实体是否显示通用的受伤变红效果
        """
        pass

