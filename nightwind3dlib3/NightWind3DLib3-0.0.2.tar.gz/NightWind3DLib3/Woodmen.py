from panda3d.core import *
from NightWind3DLib3.Actor import LoadActor
import random


class Woodmen(LoadActor):
    def __init__(self, ModelName, AnimsName, pos, ColliderName, MaxSpeed, MaxHealth):
        # 初始化木头人类
        super().__init__(ModelName, AnimsName, pos, ColliderName, MaxSpeed, MaxHealth)

        # 设置任务放缩大小和攻击距离等初始化数据
        self.actor.setScale(1.2)
        self.acceleration = 100
        self.default_orientation = Vec2(0, -1)
        self.change_orientation = Vec2(0, -1)
        self.detection_distance = 450
        self.acceleration_chase = 400
        self.actor.enable_blend()

        # 添加伤害和攻击间隔
        self.harm_value = -5
        self.harm_interval_time = 0.5

    def WoodmenMove(self, player, dt):
        # 木头人移动方法
        self.move(dt)
        positionVec3 = player.actor.getPos() - self.actor.getPos()
        positionVec2 = positionVec3.getXy()
        distanceToPlayer = positionVec2.length()

        # 玩家身处在木头人侦测范围外
        if distanceToPlayer > self.detection_distance:
            self.walking = True
            self.heading = self.default_orientation.signedAngleDeg(
                self.change_orientation)
            self.actor.setH(self.heading)
            self.velocity.addY(self.acceleration * dt)
            self.actor.setControlEffect("walk", 0.7)
            self.actor.setControlEffect("attack", 0.3)

        # 玩家在侦测范围和攻击范围之间
        elif 30 < distanceToPlayer < self.detection_distance:
            self.walking = True
            self.heading = self.default_orientation.signedAngleDeg(positionVec2)
            self.actor.setH(self.heading)
            self.velocity.addY(self.acceleration_chase * dt)
            self.actor.setControlEffect("walk", 0.9)
            self.actor.setControlEffect("attack", 0.1)

        # 玩家在攻击范围内
        else:
            self.walking = False
            self.heading = self.default_orientation.signedAngleDeg(positionVec2)
            self.actor.setH(self.heading)
            self.actor.setControlEffect("walk", 0)
            self.actor.setControlEffect("attack", 1)

            self.harm_interval_time -= dt
            if self.harm_interval_time <= 0:
                player.CountHealth(player.harm_value)
                print("玩家生命值:", player.health)
                self.harm_interval_time = random.uniform(0.5, 1)

        # 播放动画
        if self.walking:
            woodmen_walk = self.actor.getAnimControl("walk")
            if not woodmen_walk.isPlaying():
                self.actor.loop("walk")
                self.actor.loop("attack")
        else:
            self.actor.loop("stand")
