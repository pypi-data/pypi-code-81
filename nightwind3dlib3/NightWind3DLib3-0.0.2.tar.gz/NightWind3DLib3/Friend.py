from panda3d.core import *
from NightWind3DLib3.Actor import LoadActor


class Friend(LoadActor):
    def __init__(self, ModelName, AnimsName, pos, ColliderName, MaxSpeed, MaxHealth):
        # 初始化营救对象类
        super().__init__(ModelName, AnimsName, pos, ColliderName, MaxSpeed, MaxHealth)

        # 设置初始数据
        self.actor.setScale(0.6)

        # 添加冰封效果
        self.ice_solid = CollisionBox((0, 0, 60), 45, 40, 80)
        self.ice_node = CollisionNode("codemao")
        self.ice_node.addSolid(self.ice_solid)
        self.ice = self.actor.attachNewNode(self.ice_node)
        self.ice.show()
