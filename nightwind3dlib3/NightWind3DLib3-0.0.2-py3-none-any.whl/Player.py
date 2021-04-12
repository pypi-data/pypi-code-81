from direct.directbase.DirectStart import base
from panda3d.core import *
from NightWind3DLib3.Actor import LoadActor
import random


class Player(LoadActor):
    def __init__(self, ModelName, AnimsName, pos, ColliderName, MaxSpeed, MaxHealth):
        # 初始化玩家类
        super().__init__(ModelName, AnimsName, pos, ColliderName, MaxSpeed, MaxHealth)

        # 设置玩家的放缩大小
        self.actor.setScale(4.5)
        self.acceleration = 100
        self.ray = CollisionRay(0, 0, 0, 0, -1, 0)

        # 添加玩家激光武器
        rayNode = CollisionNode("playerRay")
        rayNode.addSolid(self.ray)
        self.ray_collision = self.actor.attachNewNode(rayNode)

        # 添加碰撞蒙版
        mask = BitMask32()
        mask.setBit(0)
        self.collider.node().setIntoCollideMask(mask)
        mask = BitMask32()
        mask.setBit(0)
        self.collider.node().setFromCollideMask(mask)
        mask = BitMask32()
        self.ray_collision.node().setIntoCollideMask(mask)
        mask = BitMask32()
        mask.setBit(1)
        self.ray_collision.node().setFromCollideMask(mask)

        # 添加激光武器
        self.laser_weapon = loader.loadModel("laser")
        self.laser_weapon.reparentTo(self.actor)

        # 设置伤害值和间隔时间
        self.harm_value = -3
        self.harm_interval_time = 0.5

    def PlayerMove(self, keys, woodmen, dt):
        # 玩家移动方法
        self.move(dt)
        self.walking = False

        # 前进
        if keys["up"]:
            self.velocity.addY(self.acceleration * dt)
            self.walking = True
            base.cam.setPos(self.actor, (0, 60, 150))
            base.cam.setHpr(self.actor, (180, -65, 0))

        # 左转
        if keys["left"]:
            self.actor.setH(self.actor.getH() + 1)
            self.walking = True
            base.cam.setPos(self.actor, (0, 60, 150))
            base.cam.setHpr(self.actor, (180, -65, 0))
            self.velocity = Vec3(0, 0, 0)

        # 右转
        if keys["right"]:
            self.actor.setH(self.actor.getH() - 1)
            self.walking = True
            base.cam.setPos(self.actor, (0, 60, 150))
            base.cam.setHpr(self.actor, (180, -65, 0))
            self.velocity = Vec3(0, 0, 0)

        # 循环播放动画
        if self.walking:
            player_walk = self.actor.getAnimControl("walk")
            if not player_walk.isPlaying():
                self.actor.loop("walk")
        else:
            self.actor.loop("stand")

        # 获取碰撞信息条目
        if keys["shoot"] and self.ray_queue.getNumEntries() > 0:
            self.ray_queue.sortEntries()
            ray_info = self.ray_queue.getEntry(0)

            # 如果和木头人产生碰撞
            if ray_info.getIntoNode().getName() == "woodmen":
                collision_position = ray_info.getSurfacePoint(render)
                dis = (collision_position - self.actor.getPos()).length()
                # 设置激光剑
                self.laser_weapon.setSy(dis * 1 / 5)

                self.harm_interval_time -= dt
                if self.harm_interval_time <= 0:
                    # 攻击木头人
                    woodmen.CountHealth(self.harm_value)
                    print("木头人生命值:", woodmen.health)
                    self.harm_interval_time = random.uniform(0.5, 0.8)
