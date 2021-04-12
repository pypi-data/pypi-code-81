from direct.directbase.DirectStart import base
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectDialog import DirectDialog
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import *
from NightWind3DLib3.Friend import Friend
from NightWind3DLib3.Player import Player
from NightWind3DLib3.Woodmen import Woodmen
from NightWind3DLib3.Needle import Needle


class Window:
    def __init__(self):
        self.base = base
        self.window = WindowProperties()
        self.window.setSize(1400, 1000)
        self.base.win.requestProperties(self.window)
        self.StartDialog = self.CreateDialog(FrameSize=(-1.4 + 0.01, 1.4 + 0.01,
                                                        -1 + 0.01, 1 + 0.01),
                                             pos=(0, 0, 0), color=(1, 1, 1, 1),
                                             picture="start.png")
        self.font = loader.loadFont("font.ttc")
        self.CreateButton(pos=(0, 0, -0.8), text="开始游戏",
                          scale=0.15, parent=self.StartDialog,
                          command=self.Start, fg=(255 / 255,
                                                  220 / 255, 99 / 255, 1),
                          frameColor=(147 / 255, 88 / 255, 51 / 255, 1))

        # 创建玩家角色
        self.player = Player(ModelName="aduan",
                             AnimsName={"walk": "aduan_walk",
                                        "stand": "aduan_stand"},
                             pos=(-600, -60, 0), ColliderName="player",
                             MaxSpeed=30, MaxHealth=100)

        # 创建营救对象
        self.friend = Friend(ModelName="codemao",
                                AnimsName={"walk": "codemao_walk",
                                           "stand": "codemao_stand"},
                                pos=(450, 20, 0), ColliderName="friend",
                                MaxSpeed=40, MaxHealth=100)

        # 创建木头人敌人
        self.woodmen = Woodmen(ModelName="woodmen",
                               AnimsName={"walk": "woodmen_walk",
                                          "stand": "woodmen_stand",
                                          "die": "woodmen_die",
                                          "attack": "woodmen_attack"},
                               pos=(0, 0, 0), ColliderName="woodmen",
                               MaxSpeed=85, MaxHealth=100)

        # 创建地刺敌人
        self.needle = Needle(ModelName="GroundNeedle",
                             AnimsName={"motion": "GroundNeedle_motion",
                                        "stop": "GroundNeedle_stop"},
                             pos=(270, 0, -2), ColliderName="needle",
                             MaxSpeed=5, MaxHealth=100)

        # 添加键盘事件
        self.KeyState = {"up": False, "left": False,
                         "right": False, "shoot": False}
        self.KeyEvent()

        # 创建碰撞体
        self.base.pusher = CollisionHandlerPusher()
        self.base.cTrav = CollisionTraverser()
        self.base.pusher.setHorizontal(True)
        self.base.pusher.add_in_pattern("%fn-into-%in")
        self.base.pusher.addCollider(self.player.collider, self.player.actor)
        self.base.cTrav.addCollider(self.player.collider, self.base.pusher)
        self.base.pusher.addCollider(self.woodmen.collider, self.woodmen.actor)
        self.base.cTrav.addCollider(self.woodmen.collider, self.base.pusher)

        # 添加列表处理机制
        self.player.ray_queue = CollisionHandlerQueue()
        self.base.cTrav.addCollider(self.player.ray_collision,
                                    self.player.ray_queue)

        # 添加地刺的碰撞处理机制
        self.needle.hue_queue = CollisionHandlerQueue()
        self.base.cTrav.addCollider(self.needle.needle_1, self.needle.hue_queue)
        self.base.cTrav.addCollider(self.needle.needle_2, self.needle.hue_queue)

        self.base.run()

    def CreateDialog(self, FrameSize, pos, color, picture):
        return DirectDialog(frameSize=FrameSize,
                            pos=pos, frameColor=color,
                            frameTexture=picture)

    def CreateButton(self, text, parent, command, scale, pos, fg, frameColor):
        DirectButton(text=text, parent=parent, command=command, scale=scale,
                     pos=pos, text_font=self.font, text_fg=fg,
                     frameColor=frameColor)

    # 按下按钮触发此事件
    def Start(self):
        self.StartDialog.hide()
        self.load_model("FieldForest")
        self.base.cam.setHpr(-90, -4, 0)
        self.base.cam.setPos(-1000, -100, 100)
        self.CreateFence(580, 350, 0, 580, -350, 0, 5)
        self.CreateFence(-580, -350, 0, 580, -350, 0, 5)
        self.CreateFence(-580, -350, 0, -580, -150, 0, 5)
        self.CreateFence(-580, -40, 0, -580, 350, 0, 5)
        self.CreateFence(-580, 350, 0, 580, 350, 0, 5)
        self.base.disableMouse()
        taskMgr.add(self.update)

    def ChangeKeyState(self, direction, key_state):
        self.KeyState[direction] = key_state

    def KeyEvent(self):
        # 获取键盘事件
        self.base.accept('w', self.ChangeKeyState, ['up', True])
        self.base.accept('w-up', self.ChangeKeyState, ['up', False])
        self.base.accept('a', self.ChangeKeyState, ['left', True])
        self.base.accept('a-up', self.ChangeKeyState, ['left', False])
        self.base.accept('d', self.ChangeKeyState, ['right', True])
        self.base.accept('d-up', self.ChangeKeyState, ['right', False])
        self.base.accept('woodmen-into-fence', self.ChangeWoodmenState)
        self.base.accept("mouse1", self.ChangeKeyState, ["shoot", True])
        self.base.accept("mouse1-up", self.ChangeKeyState, ["shoot", False])

    def load_model(self, model):
        self.model = loader.loadModel(model)
        self.model.reparentTo(render)

    def CreateFence(self, ax, ay, az, bx, by, bz, r):
        solid = CollisionCapsule(ax, ay, az, bx, by, bz, r)
        node = CollisionNode("fence")
        node.addSolid(solid)
        render.attachNewNode(node)

    def update(self, task):
        dt = globalClock.getDt()
        self.player.PlayerMove(self.KeyState, self.woodmen, dt)
        self.woodmen.WoodmenMove(self.player, dt)
        self.needle.NeedleAttack(self.player, dt)
        return task.cont

    def ChangeWoodmenState(self, content):
        self.woodmen.acceleration = -self.woodmen.acceleration
        self.woodmen.change_orientation = -self.woodmen.change_orientation


if __name__ == "__main__":
    Window()
