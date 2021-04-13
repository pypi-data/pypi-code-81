import arcade
import os
from pathlib import Path

__all__ = ["window", "rocket"]

# 文件目录
USER_DIR = os.getcwd()
SYS_DIR = os.path.split(os.path.realpath(__file__))[0]
SYS_RESOURCES_DIR = SYS_DIR + os.sep + "rkimg"

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 650
SCREEN_TITLE = "火箭发射"

# 游戏状态
GAME_INIT = 0
GAME_WIN = 1
GAME_LOSE = 2

# 火箭状态
ROCKET_FLY = False
ROCKET_LAUNCHING = 0
ROCKET_TOWER_DROP = 1
ROCKET_BOOSTER_DROP = 2
ROCKET_FIRST_DROP = 3
ROCKET_MASK_DROP = 4
ROCKET_SECOND_DROP = 5

MOVE_SPEED = 4  # 火箭的初速度和加速度

KEY_SPACE_ENABLED = False  # 空格键使能


class Launcher(arcade.Sprite):
    def __init__(self):
        super().__init__(filename=f"{SYS_RESOURCES_DIR}{os.sep}launcher.png", scale=1.2)
        self.position = SCREEN_WIDTH // 2, 170

    def move(self):
        self.center_y += -3
        if self.top < -10:
            self.change_y = 0


class Mountain(arcade.Sprite):
    def __init__(self):
        super().__init__(filename=f"{SYS_RESOURCES_DIR}{os.sep}mountain_image.png", scale=1)
        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    def move(self):
        self.center_y += -3
        if self.top < -10:
            self.change_y = 0


class Notice(arcade.Sprite):
    def __init__(self):
        super().__init__(filename=f"{SYS_RESOURCES_DIR}{os.sep}height_bottom.png", scale=0.8)
        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50


class BottomImage(arcade.Sprite):
    def __init__(self, img):
        super().__init__(filename=f"{SYS_RESOURCES_DIR}{os.sep}{img}{os.sep}bottom_image.png", scale=1.2)
        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2


class TopImage(arcade.Sprite):
    def __init__(self, img, position_x=SCREEN_WIDTH // 2, position_y=SCREEN_HEIGHT // 2):
        super().__init__(filename=f"{SYS_RESOURCES_DIR}{os.sep}{img}{os.sep}top_image.png", scale=1)
        self.position = position_x, position_y


class Fire:
    def __init__(self):
        super().__init__()
        self.change = False
        self.rocket_list = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}fire1.png", scale=0.15)
        self.rocket_list.index = 0
        self.rocket_list.position = SCREEN_WIDTH / 2, 52
        for a in range(5):
            self.rocket_list.append_texture(arcade.load_texture(f"{SYS_RESOURCES_DIR}{os.sep}fire{a + 2}.png"))

    def set_position(self, x, y):
        self.rocket_list.position = x, y

    # 改变火焰造型
    def change_texture(self):
        if not self.change:
            self.rocket_list.index += 1
            if self.rocket_list.index > 2:
                self.rocket_list.index = 0
            self.rocket_list.set_texture(self.rocket_list.index)
        if self.change:
            self.rocket_list.index += 1
            if self.rocket_list.index > 5:
                self.rocket_list.index = 3
            self.rocket_list.set_texture(self.rocket_list.index)

    def move(self):
        self.rocket_list.center_y += MOVE_SPEED

    def stop(self):
        self.rocket_list.center_y += 0


class Rocket:
    def __init__(self):
        super().__init__()
        self.status = 0
        self.rocket_list = arcade.SpriteList()
        self.fail_speed = -2.5  # 火箭各个组件脱落的速度
        self.accelerate_speed = MOVE_SPEED  # 火箭的加速度
        self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        self._color = "white"  # 火箭颜色
        self.change_num = 30

        self.load_rocket(self._color)

        # 分离高度
        self.range0 = 0  # 逃逸塔脱落对应的高度范围(虚拟数据)
        self.range0_1 = 0

        self.range1 = 0  # 助推器脱落（同上）
        self.range1_1 = 0

        self.range2 = 0  # 一级火箭脱落（同上）
        self.range2_1 = 0

        self.range3 = 0  # 整流罩（同上）
        self.range3_1 = 0

        self.range4 = 0  # 二级火箭脱落（同上）
        self.range4_1 = 0

        # 高度次数
        self.height_count = 1  # 第一次起飞不计数

    def load_rocket(self, color):
        self.space_vehicle = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}{color}{os.sep}space_vehicle.png",
                                           scale=0.1)
        self.space_vehicle.position = self.width / 2 + 0.5, self.height / 2 - 70 + self.change_num

        self.tower = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}{color}{os.sep}tower.png", scale=0.15)
        self.tower.position = self.width / 2 + 1, self.space_vehicle.center_y + self.space_vehicle.height / 2 + 5

        self.mask1 = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}{color}{os.sep}mask1.png", scale=0.1)
        self.mask1.position = self.width / 2 + 10, self.space_vehicle.center_y

        self.mask2 = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}{color}{os.sep}mask2.png", scale=0.1)
        self.mask2.position = self.width / 2 - 8, self.space_vehicle.center_y

        self.second = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}{color}{os.sep}second.png", scale=0.1)
        self.second.position = self.width / 2 + 2.5, self.space_vehicle.center_y - \
                               self.space_vehicle.height / 2 - self.second.height / 2 + 17

        self.first_img = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}{color}{os.sep}first_image.png", scale=0.1)
        self.first_img.position = self.width / 2 + 2, self.space_vehicle.bottom - \
                                  self.second.height - self.first_img.height / 2 + 35

        self.push1 = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}{color}{os.sep}push1.png", scale=0.1)
        self.push1.position = self.width / 2 - \
                              27, self.space_vehicle.bottom - self.second.height - 50

        self.push2 = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}{color}{os.sep}push2.png", scale=0.1)
        self.push2.position = self.width / \
                              2, self.space_vehicle.bottom - self.second.height - 50

        self.push3 = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}{color}{os.sep}push3.png", scale=0.1)
        self.push3.position = self.width / 2 + \
                              30, self.space_vehicle.bottom - self.second.height - 53

        self.push4 = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}{color}{os.sep}push2.png", scale=0.07)
        self.push4.position = self.width / \
                              2, self.space_vehicle.bottom - self.second.height - 50

        self.rocket_list.append(self.tower)
        self.rocket_list.append(self.space_vehicle)
        self.rocket_list.append(self.second)
        self.rocket_list.append(self.push4)  # 背后的助推器，索引值为4
        self.rocket_list.append(self.first_img)
        self.rocket_list.append(self.push1)
        self.rocket_list.append(self.push2)
        self.rocket_list.append(self.push3)
        self.rocket_list.append(self.mask1)
        self.rocket_list.append(self.mask2)

    # 火箭移动
    def move(self):
        for i in self.rocket_list:
            i.center_y += self.accelerate_speed

    # 火箭停止移动
    def stop(self):
        for i in self.rocket_list:
            i.center_y += 0

    # 逃逸塔脱落
    def tower_drop(self):
        self.rocket_list[0].change_y = self.fail_speed
        self.rocket_list[0].change_x = self.fail_speed * 0.4
        self.rocket_list[0].change_angle = 2

    # 助推器脱落
    def booster_drop(self):
        self.rocket_list[3].change_y = self.fail_speed * 0.5
        self.rocket_list[3].change_x = -self.fail_speed * 0.1
        self.rocket_list[3].change_angle = -3

        self.rocket_list[5].change_y = self.fail_speed
        self.rocket_list[5].change_x = self.fail_speed * 0.5
        self.rocket_list[5].change_angle = 3

        self.rocket_list[6].change_y = self.fail_speed * 0.8
        self.rocket_list[6].change_x = self.fail_speed * 0.1
        self.rocket_list[6].change_angle = 3

        self.rocket_list[7].change_y = self.fail_speed
        self.rocket_list[7].change_angle = -3
        self.rocket_list[7].change_x = -self.fail_speed * 0.5

    # 一级脱落
    def first_drop(self):
        self.rocket_list[4].change_y = self.fail_speed
        self.rocket_list[4].change_angle = -1
        self.rocket_list[4].change_x = self.fail_speed * 0.2

    # 整流罩分离
    def mask_drop(self):
        self.rocket_list[8].change_y = self.fail_speed
        self.rocket_list[8].change_angle = -3
        self.rocket_list[8].change_x = -self.fail_speed * 0.3
        self.rocket_list[9].change_y = self.fail_speed
        self.rocket_list[9].change_angle = 3
        self.rocket_list[9].change_x = self.fail_speed * 0.3

    # 二级脱落
    def second_drop(self):
        self.rocket_list[2].change_y = self.fail_speed
        self.rocket_list[2].change_angle = 3
        self.rocket_list[2].change_x = -self.fail_speed * 0.2

    @staticmethod
    def fly():
        global KEY_SPACE_ENABLED
        KEY_SPACE_ENABLED = True

    # 高度
    def et(self, *value):
        self.range0, self.range0_1 = value
        self.height_count += 1

    def booster(self, *value):
        self.range1, self.range1_1 = value
        self.height_count += 1

    def first(self, *value):
        self.range2, self.range2_1 = value
        self.height_count += 1

    def fairing(self, *value):
        self.range3, self.range3_1 = value
        self.height_count += 1

    def sa(self, *value):
        self.range4, self.range4_1 = value
        self.height_count += 1

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self.rocket_list = arcade.SpriteList()
        self.load_rocket(value)


class Window(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.game_status = 0
        # alter
        self.rocket = None
        self.fire = None
        self.launcher = Launcher()
        self.mountain = Mountain()
        self.notice = Notice()
        self.bottom_pic = None
        self.bg_list = arcade.SpriteList()  # 存储背景图
        self.hint_list = arcade.SpriteList()  # 存储各种提示图
        self.result_list = arcade.SpriteList()  # 存储游戏结果图
        self.smoke = None  # 烟雾精灵列表
        self.bg_music = None  # 背景音乐
        self.accelerate_music = None  # 火箭加速音乐
        self.failure_music = None  # 游戏失败音乐

        self.total_time = 0  # 游戏计时
        self.last_time = 0  # 记录火箭加速时，当下的时间
        self.press_count = 0  # 记录空格按下的次数 （1：发射  2：逃逸塔脱落  3：助推器脱落  4：一级脱落  5：整流罩分离 6：船箭分离）

    def setup(self):
        # 设置素材图片
        self.set_hint_photo()
        self.set_result_photo()
        self.set_smoke_photo()
        # 设置背景音乐
        self.bg_music = arcade.Sound(f"{SYS_RESOURCES_DIR}{os.sep}music.mp3")
        self.accelerate_music = arcade.Sound(f"{SYS_RESOURCES_DIR}{os.sep}accelerate.mp3")
        self.failure_music = arcade.Sound(f"{SYS_RESOURCES_DIR}{os.sep}failure.mp3")
        self.bg_music_player = self.bg_music.play(loop=True)

    def on_draw(self):
        arcade.start_render()
        if self.bg_list:
            self.bottom_pic.draw()
            self.bg_list.draw()
            self.mountain.draw()
            self.launcher.draw()  # 绘制发射台
            self.notice.draw()

            if self.rocket:
                self.rocket.rocket_list.draw()
                arcade.draw_text(str(int(self.rocket.height)), self.width / 2, self.notice.center_y,
                                 arcade.color.WHITE,
                                 font_size=33, font_name=("simhei", "PingFang"), anchor_x="center", anchor_y="center")
                # 绘制脱落提示图
                if self.rocket.range0 < self.rocket.height < self.rocket.range0_1:
                    self.hint_list[0].draw()
                if self.rocket.range1 < self.rocket.height < self.rocket.range1_1:
                    self.hint_list[1].draw()
                if self.rocket.range2 < self.rocket.height < self.rocket.range2_1:
                    self.hint_list[2].draw()
                if self.rocket.range3 < self.rocket.height < self.rocket.range3_1:
                    self.hint_list[3].draw()
                if self.rocket.range4 < self.rocket.height < self.rocket.range4_1:
                    self.hint_list[4].draw()

            # 火箭未发射时，绘制“火箭发射”的图片
            if not ROCKET_FLY:
                self.hint_list[5].draw()

            # 一旦火箭发射，绘制烟雾和火焰
            if ROCKET_FLY:
                self.smoke.draw()
                self.fire.rocket_list.draw()

            # 绘制结果提示图
            if self.game_status == GAME_LOSE:
                self.result_list[1].draw()
            if self.game_status == GAME_WIN:
                self.result_list[0].draw()

    def on_update(self, delta_time: float):
        if self.game_status == GAME_INIT:
            if ROCKET_FLY:
                self.bg_list.update()
                self.rocket.rocket_list.update()
                self.fire.rocket_list.update()
                self.smoke.update()
                self.launcher.update()
                self.mountain.update()
                self.fire.change_texture()
                self.total_time += delta_time
                # 当火箭的整流罩上升到设定的高度前，火箭移动
                if self.rocket.space_vehicle.center_y < self.height / 2 + 75:
                    self.rocket.move()
                    self.fire.move()
                # 火箭上升到设定的高度后，火箭停止移动，背景开始移动
                else:
                    # 背景移动
                    self.bg_move()
                    self.smoke_move()
                    self.launcher.move()
                    self.mountain.move()
                    self.rocket.stop()
                    self.fire.stop()

                # 逃逸塔脱离时，不加速，高度正常增加
                if self.rocket.status == ROCKET_TOWER_DROP or self.rocket.status == ROCKET_MASK_DROP:
                    # 显示高度数值
                    self.rocket.height = (
                            self.rocket.height + (
                            self.rocket.accelerate_speed * (self.press_count - 1)) * delta_time * 10)
                # 其它组件脱落时，高度按对应的速度增加
                else:
                    # 显示高度数值
                    self.rocket.height = (
                            self.rocket.height + (self.rocket.accelerate_speed * self.press_count) * delta_time * 10)

                # 抛逃逸塔
                if self.rocket.status == ROCKET_TOWER_DROP:
                    self.rocket.tower_drop()
                # 助推器分离
                elif self.rocket.status == ROCKET_BOOSTER_DROP:
                    self.rocket.booster_drop()
                # 一级分离
                elif self.rocket.status == ROCKET_FIRST_DROP:
                    self.rocket.first_drop()
                    self.fire.rocket_list.scale = 0.09
                    self.fire.set_position(self.width / 2,
                                           self.rocket.second.bottom - self.fire.rocket_list.height / 2 + 16)

                # 整流罩分离
                elif self.rocket.status == ROCKET_MASK_DROP:
                    self.rocket.mask_drop()
                # 船箭分离
                elif self.rocket.status == ROCKET_SECOND_DROP:
                    self.rocket.second_drop()
                    self.fire.rocket_list.scale = 0.07
                    self.fire.set_position(self.width / 2,
                                           self.rocket.space_vehicle.bottom - self.fire.rocket_list.height / 2 + 10)

                # 加速火焰造型维持1s
                if self.accelerate:
                    if int(self.total_time - self.last_time) > 1:
                        self.fire.change = False
                        self.accelerate = False

                # 逃逸塔分离失败
                if self.rocket.range0 and (self.rocket.height > self.rocket.range0_1 and self.press_count == 1) or (
                        self.rocket.height < self.rocket.range0 and self.press_count > 1):
                    self.lose()

                # 助推器分离失败
                elif self.rocket.range1 and (self.rocket.height > self.rocket.range1_1 and self.press_count == 2) or (
                        self.rocket.height < self.rocket.range1 and self.press_count > 2):
                    self.lose()

                # 一级火箭分离失败
                elif self.rocket.range2 and (self.rocket.height > self.rocket.range2_1 and self.press_count == 3) or (
                        self.rocket.height < self.rocket.range2 and self.press_count > 3):
                    self.lose()

                # 整流罩分离失败
                elif self.rocket.range3 and (self.rocket.height > self.rocket.range3_1 and self.press_count == 4) or (
                        self.rocket.height < self.rocket.range3 and self.press_count > 4):
                    self.lose()

                # 船箭分离失败
                elif self.rocket.range4 and (self.rocket.height > self.rocket.range4_1 and self.press_count == 5) or \
                        (self.rocket.height < self.rocket.range4 and self.press_count > 5) or \
                        (self.rocket.range4 < self.rocket.height < self.rocket.range4_1 and self.press_count > 6):
                    self.lose()

                # 火箭发射成功
                elif self.rocket.height > self.rocket.range4_1 and self.press_count == 6:
                    self.win()

    def on_key_press(self, symbol: int, modifiers: int):
        global ROCKET_FLY
        if self.game_status == GAME_INIT:
            if symbol == arcade.key.SPACE and KEY_SPACE_ENABLED:
                ROCKET_FLY = True
                # 控制按键次数
                if self.press_count < self.rocket.height_count:
                    self.press_count += 1
                    self.accelerate = True
                    self.accelerate_music_player = self.accelerate_music.play()
                    self.last_time = self.total_time
                    self.fire.change = True
                    if self.press_count == 1:
                        self.rocket.status = ROCKET_LAUNCHING
                        arcade.schedule(self.change_smoke, 0.2)
                    elif self.press_count == 2:
                        self.rocket.status = ROCKET_TOWER_DROP
                        self.accelerate = False
                        self.fire.change = False
                        self.accelerate_music.stop(self.accelerate_music_player)
                    elif self.press_count == 3:
                        self.rocket.status = ROCKET_BOOSTER_DROP
                    elif self.press_count == 4:
                        self.rocket.status = ROCKET_FIRST_DROP
                    elif self.press_count == 5:
                        self.rocket.status = ROCKET_MASK_DROP
                        self.accelerate = False
                        self.fire.change = False
                        self.accelerate_music.stop(self.accelerate_music_player)
                    elif self.press_count == 6:
                        self.rocket.status = ROCKET_SECOND_DROP

    # 设置背景图
    def set_bg_photo(self, img):
        # TODO: 用户目录->系统目录
        # 底图
        self.bottom_pic = BottomImage(img)
        _bg = TopImage(img)
        self.bg_list.append(_bg)
        _bg1 = TopImage(img, self.width / 2, self.height / 2 + self.height)
        self.bg_list.append(_bg1)

    # 设置提示图
    def set_hint_photo(self):
        for i in range(5):
            self.hint = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}drop{i}.png", scale=0.2)
            self.hint.position = self.width / 2, self.height - 150
            self.hint_list.append(self.hint)
        self.hint = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}launching.png", scale=0.2)
        self.hint.position = self.width / 2, self.height - 150
        self.hint_list.append(self.hint)

    # 设置结果图
    def set_result_photo(self):
        win = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}win.png", scale=0.4)
        win.position = self.width / 2, self.height / 2
        self.result_list.append(win)
        lose = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}lose.png", scale=0.4)
        lose.position = self.width / 2, self.height / 2
        self.result_list.append(lose)

    # 设置烟雾图
    def set_smoke_photo(self):
        self.smoke = arcade.Sprite(f"{SYS_RESOURCES_DIR}{os.sep}smoke1.png", scale=1.2)
        self.smoke.index = 0
        self.smoke.position = self.width / 2 - 50, 290
        for j in range(2):
            self.smoke.append_texture(arcade.load_texture(f"{SYS_RESOURCES_DIR}{os.sep}smoke{j + 2}.png"))

    def change_smoke(self, delta_time):
        self.smoke.index += 1
        if self.smoke.index > 2:
            self.smoke.index = 0
        self.smoke.set_texture(self.smoke.index)

    def smoke_move(self):
        self.smoke.center_y += -3
        if self.smoke.top < -10:
            self.smoke.change_y = 0

    # 背景移动
    def bg_move(self):
        if self.rocket.status == ROCKET_TOWER_DROP or self.rocket.status == ROCKET_MASK_DROP:
            change_speed = (self.press_count - 1) * self.rocket.accelerate_speed
        else:
            change_speed = self.press_count * self.rocket.accelerate_speed

        self.bg_list[0].change_y = -change_speed
        self.bg_list[1].change_y = -change_speed

        for bg in [self.bg_list[0], self.bg_list[1]]:
            if bg.top < 0:
                bg.bottom = self.height

    def win(self):
        self.game_status = GAME_WIN

    def lose(self):
        self.game_status = GAME_LOSE
        self.failure_music.play()
        self.bg_music.stop(self.bg_music_player)

    # alter
    @staticmethod
    def run():
        arcade.run()

    @property
    def bg(self):
        return self.bg_list

    @bg.setter
    def bg(self, img):
        self.set_bg_photo(img)
        self.setup()

    def add(self, sprite):
        self.rocket = sprite
        self.rocket.height = 0  # 设置火箭高度
        self.fire = Fire()


window = Window
rocket = Rocket
