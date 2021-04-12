from panda3d.core import*
from NightWind3DLib3.Actor import LoadActor
import random


class Needle(LoadActor):
    def __init__(self, ModelName, AnimsName, pos, ColliderName, MaxSpeed, MaxHealth):
        # 初始化地刺类
        super().__init__(ModelName, AnimsName, pos, ColliderName, MaxSpeed, MaxHealth)

        # 设置初始值
        self.actor.setScale(0.6)
        self.actor.loop("motion")

        # 加载多个地刺
        self_node = NodePath("needlelist")
        for i in range(50, 220, 20):
            needle = self_node.attachNewNode("needle")
            needle.setPos(80, i, 0)
            self.actor.instanceTo(needle)

        for i in range(-220, -50, 20):
            needle = self_node.attachNewNode("needle")
            needle.setPos(40, i, 0)
            self.actor.instanceTo(needle)

        self_node.reparentTo(render)

        # 添加新的碰撞体
        self.collider.removeNode()
        needle_solid_1 = CollisionCapsule(350, 220, 0, 350, 40, 0, 5)
        needle_node_1 = CollisionNode("needle")
        needle_node_1.addSolid(needle_solid_1)
        self.needle_1 = render.attachNewNode(needle_node_1)

        needle_solid_2 = CollisionCapsule(310, -50, 0, 310, -230, 0, 5)
        needle_node_2 = CollisionNode("needle")
        needle_node_2.addSolid(needle_solid_2)
        self.needle_2 = render.attachNewNode(needle_node_2)

        # 添加时间间隔和攻击伤害
        self.harm_value = -2
        self.harm_interval_time = 0.6

        # 关闭蒙版
        mask = BitMask32()
        needle_node_1.setIntoCollideMask(mask)
        mask = BitMask32()
        needle_node_2.setIntoCollideMask(mask)

    def NeedleAttack(self, player, dt):
        # 木头人攻击方法
        if self.hue_queue.getNumEntries() > 0:
            self.hue_queue.sortEntries()
            hue_information = self.hue_queue.getEntry(0)
            if hue_information.getIntoNode().getName() == "player":
                self.harm_interval_time -= dt
                if self.harm_interval_time <= 0:
                    player.CountHealth(self.harm_value)
                    print("玩家生命值:", player.health)
                    self.harm_interval_time = random.uniform(0.6, 1)
