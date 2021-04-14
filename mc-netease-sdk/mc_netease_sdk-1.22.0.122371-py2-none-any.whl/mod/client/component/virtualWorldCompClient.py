# -*- coding: utf-8 -*-

from typing import Tuple
from mod.common.component.baseComponent import BaseComponent
from mod.common.minecraftEnum import TimeEaseType

class VirtualWorldCompClient(BaseComponent):
    def VirtualWorldCreate(self):
        # type: () -> bool
        """
        创建虚拟世界，虚拟世界只允许存在一个，已经存在虚拟世界的情况下再调用此方法则无效
        """
        pass

    def VirtualWorldDestroy(self):
        # type: () -> bool
        """
        销毁虚拟世界
        """
        pass

    def VirtualWorldToggleVisibility(self, isVisible):
        # type: (bool) -> bool
        """
        设置虚拟世界是否显示
        """
        pass

    def VirtualWorldSetCollidersVisible(self, isVisible):
        # type: (bool) -> bool
        """
        设置虚拟世界中模型的包围盒是否显示,主要用于调试,默认为不显示
        """
        pass

    def CameraSetPos(self, pos):
        # type: (Tuple[float,float,float]) -> bool
        """
        设置相机位置
        """
        pass

    def CameraGetPos(self):
        # type: () -> Tuple[float,float,float]
        """
        返回相机位置
        """
        pass

    def CameraSetFov(self, fov):
        # type: (float) -> bool
        """
        设置相机视野大小
        """
        pass

    def CameraGetFov(self):
        # type: () -> float
        """
        获取相机视野大小
        """
        pass

    def CameraSetZoom(self, zoom):
        # type: (float) -> bool
        """
        设置相机缩放
        """
        pass

    def CameraLookAt(self, targetPos, upVector):
        # type: (Tuple[float,float,float], Tuple[float,float,float]) -> bool
        """
        修改相机朝向
        """
        pass

    def CameraMoveTo(self, pos, targetPos, upVector, zoom, time, ease='linear'):
        # type: (Tuple[float,float,float], Tuple[float,float,float], Tuple[float,float,float], float, float, TimeEaseType) -> bool
        """
        设置相机移动动画, 会根据当前相机状态与传入参数按时间进行插值显示
        """
        pass

    def CameraStopActions(self):
        # type: () -> bool
        """
        停止相机移动动画
        """
        pass

    def CameraGetZoom(self):
        # type: () -> float
        """
        获取相机的缩放值
        """
        pass

    def CameraGetClickModel(self):
        # type: () -> int
        """
        获取相机当前指向的模型的id，会返回离相机最近的，通常与GetEntityByCoordEvent配合使用
        """
        pass

    def ModelCreateObject(self, modelName, animationName):
        # type: (str, str) -> int
        """
        在虚拟世界中创建模型
        """
        pass

    def ModelSetVisible(self, objId, isVisible):
        # type: (int, bool) -> bool
        """
        设置模型可见性
        """
        pass

    def ModelIsVisible(self, objId):
        # type: (int) -> bool
        """
        返回模型可见性
        """
        pass

    def ModelPlayAnimation(self, objId, animationName, loop):
        # type: (int, str, bool) -> bool
        """
        模型播放动画
        """
        pass

    def ModelSetBoxCollider(self, objId, lengths, offset=(0.0, 0.0, 0.0)):
        # type: (int, Tuple[float,float,float], Tuple[float,float,float]) -> bool
        """
        设置模型的包围盒
        """
        pass

    def ModelRemove(self, objId):
        # type: (int) -> bool
        """
        销毁虚拟世界中的模型
        """
        pass

    def ModelRotate(self, objId, degreeAngle, axis):
        # type: (int, float, Tuple[float,float,float]) -> bool
        """
        模型绕某个轴旋转多少度
        """
        pass

    def ModelSetPos(self, objId, pos):
        # type: (int, Tuple[float,float,float]) -> bool
        """
        设置模型坐标
        """
        pass

    def ModelGetPos(self, objId):
        # type: (int) -> Tuple[float,float,float]
        """
        获取模型的坐标
        """
        pass

    def ModelSetRot(self, objId, rot):
        # type: (int, Tuple[float,float,float]) -> bool
        """
        设置模型的旋转角度
        """
        pass

    def ModelGetRot(self, objId):
        # type: (int) -> Tuple[float,float,float]
        """
        返回模型的旋转角度
        """
        pass

    def ModelSetScale(self, objId, scales):
        # type: (int, Tuple[float,float,float]) -> bool
        """
        设置模型的缩放值
        """
        pass

    def ModelMoveTo(self, objId, pos, time, ease='linear'):
        # type: (int, Tuple[float,float,float], float, TimeEaseType) -> bool
        """
        设置模型平移运动
        """
        pass

    def ModelRotateTo(self, objId, rot, time, ease='linear'):
        # type: (int, Tuple[float,float,float], float, TimeEaseType) -> bool
        """
        设置模型旋转运动
        """
        pass

    def ModelStopActions(self, objId):
        # type: (int) -> bool
        """
        停止模型的移动和旋转运动
        """
        pass

    def MoveToVirtualWorld(self, virtualWorldObjectType, objId):
        # type: (int, int) -> bool
        """
        把对象从主世界移到虚拟世界, 非绑定的序列帧，文本，粒子需要调用该方法后才会出现在虚拟世界中，绑定的可以省略调用该方法。
        """
        pass

    def BindModel(self, virtualWorldObjectType, objId, targetId, posOffset, rotOffset, boneName='root'):
        # type: (int, int, int, Tuple[float,float,float], Tuple[float,float,float], str) -> bool
        """
        把对象绑定到模型上, 支持绑定序列帧，粒子，文本和其它模型
        """
        pass

