import vpython as vn
import os
from vpython import color
from pathlib import Path
import shutil

__all__ = ["set_window", "tunnel", "text", "arch", "forward", "color"]

USER_DIR = None
SYS_DIR = None


def initialize():
    """
    初始设置相机和用户操作
    :return:
    """
    # 用户无法旋转、缩放、平移场景
    vn.scene.userspin = False
    vn.scene.userzoom = False
    vn.scene.userpan = False
    # 固定相机初始的位置和方向
    vn.scene.camera.pos = vn.vec(0, 0.85, 25)
    vn.scene.camera.axis = vn.vec(0, 0, -25)
    # 增加照片光源
    vn.scene.lights = []
    light_1 = vn.distant_light(direction=vn.vec(100, 0, 0), color=color.gray(0.5))
    light_2 = vn.distant_light(direction=vn.vec(-100, 0, 0), color=color.gray(0.5))
    light_3 = vn.distant_light(direction=vn.vec(0, -100, 0), color=color.gray(0.5))
    vn.scene.lights.append(light_1)
    vn.scene.lights.append(light_2)
    vn.scene.lights.append(light_3)
    # 获取用户目录
    global USER_DIR, SYS_DIR
    USER_DIR = os.getcwd()
    SYS_DIR = os.path.split(os.path.realpath(__file__))[0]


mouse_click = False  # 鼠标是否按下
sign = False  # 标识照片被单击，照片单击后设置为 True，否则为 False


def set_window(width=1200, height=800):
    """
    设置窗口大小
    :param width: 宽
    :param height: 高
    :return:
    """
    vn.scene.width = width
    vn.scene.height = height

    initialize()


def text(content="", time=5, text_color=color.white):
    """
    生成文本
    :param content: 文本内容
    :param time: 倒计时时间
    :param text_color: 文本颜色
    :return:
    """
    position = vn.vec(0, 0.7, 15)
    fontsize = 80
    t1 = vn.label(text=content, pos=position, align="center", color=text_color,
                  height=fontsize, linecolor=color.black, linewidth=0.01, opacity=0)
    vn.sleep(2)
    while time > 0:
        t1.text = f"{time}"
        time -= 1
        vn.sleep(1)
    t1.visible = False


def arch(num=10, distance=2):
    # 清空 tmp 目录下的图片
    shutil.rmtree(f"{SYS_DIR}{os.sep}tmp")
    os.mkdir("tmp")
    # 查找同级目录下的图片
    _files_jpg = Path(USER_DIR).rglob("*.jpg")
    _files_png = Path(USER_DIR).rglob("*.png")
    images = list(_files_jpg) + list(_files_png)
    # copy photo
    for img in images:
        path, filename = os.path.split(os.fspath(img))
        shutil.copyfile(os.fspath(img), SYS_DIR + os.sep + "tmp" + os.sep + filename)
    user_img_num = len(images)

    no = 0  # 照片索引
    sys_image_num = 300  # 内置照片数

    global photo_list, ratio_1
    photo_num = sys_image_num + user_img_num
    vn.scene.camera.pos = vn.vec(0, 0.85 * radius / 3, 25)
    vn.scene.camera.axis = vn.vec(0, 0, -25)
    ratio_1 = 8 * radius / 3
    photo_list = []
    change_angle = vn.pi / (num - 1)  # 角度变化值
    photo_name = 0
    # i为z坐标的变化，组成多个半圆，形成回廊
    for i in range(vn.ceil(photo_num / num)):
        # 照片组成一个圆
        for j in range(num):
            pos = vn.vec(radius * vn.cos(j * change_angle), radius *
                         vn.sin(j * change_angle), -i * (distance + 1))
            if photo_name < 300:
                a = vn.box(pos=pos, size=vn.vec(1, 1, 0.05),
                           texture=f'photos{os.sep}{photo_name}.jpg')
                photo_name += 1
            else:
                if no >= user_img_num:
                    break
                path, filename = os.path.split(os.fspath(images[no]))
                a = vn.box(pos=pos, size=vn.vec(1, 1, 0.05),
                           texture=f"tmp{os.sep}{filename}")
                no += 1
            # 调整照片角度
            if radius * vn.cos(j * change_angle) > 0:
                a.rotate(angle=-vn.pi / 2, axis=vn.vec(0, 1, 0))
                a.rotate(angle=j * change_angle, axis=vn.vec(0, 0, 1))
            else:
                a.rotate(angle=vn.pi / 2, axis=vn.vec(0, 1, 0))
                a.rotate(angle=-(vn.pi - j * change_angle), axis=vn.vec(0, 0, 1))
            a.angle_1 = j * change_angle
            photo_list.append(a)
    # 绑定键鼠
    vn.scene.bind("click keydown", control)


def click_photo(photo_list):
    """
    点击放大函数，会修改标志位 sign，True 表示处于点击放大状态，False 表示处于非放大状态
    :param photo_list:
    :return:
    """
    global mouse_click, sign, origin_pos, origin_axis
    obj = vn.scene.mouse.pick
    juli = 4

    if mouse_click:
        if obj in photo_list and vn.mag(vn.scene.camera.pos - obj.pos) < ratio_1:
            origin_pos = vn.vec(0, 0.85 * radius / 3, obj.pos.z + juli)
            origin_axis = vn.vec(0, 0, -10)
            vn.scene.camera.pos = vn.vec(0, 0, obj.pos.z)  # 关键
            vn.scene.camera.axis = (obj.pos - vn.scene.camera.pos)
            vn.scene.camera.pos = obj.pos - (obj.pos - vn.scene.camera.pos).norm() * 1.2
            sign = True
            mouse_click = False
        else:
            if sign:
                vn.scene.camera.pos = origin_pos
                vn.scene.camera.axis = origin_axis
                sign = False
                mouse_click = False
            else:
                mouse_click = False


def control(evt):
    """
    鼠标和键盘事件，绑定上下左右按键操作和鼠标单击操作
    :param evt: 事件类型
    :return:
    """
    global mouse_click, sign, photo_list
    # 记录点击鼠标的次数
    if evt.event == "click":
        mouse_click = True
        click_photo(photo_list)

    if evt.event == "keydown" and sign != True:
        if evt.key == "o":
            # 固定相机初始视角
            vn.scene.camera.pos = vn.vec(0, 0.85 * radius / 3, 5)
            vn.scene.camera.axis = vn.vec(0, 0, -100)
        # 控制相机左转、右转、前进、后退
        elif evt.key == "left":
            if vn.scene.camera.axis.z < 0 or vn.scene.camera.axis.x > 0:
                vn.scene.camera.rotate(axis=vn.vec(0, 1, 0), angle=vn.pi / 180)
        elif evt.key == "right":
            if vn.scene.camera.axis.z < 0 or vn.scene.camera.axis.x < 0:
                vn.scene.camera.rotate(axis=vn.vec(0, 1, 0), angle=-vn.pi / 180)
        elif evt.key == "up":
            vn.scene.camera.pos += vn.vec(0, 0, -0.1)
        elif evt.key == "down":
            vn.scene.camera.pos -= vn.vec(0, 0, -0.1)


def tunnel(r=6, background="", light_color=color.gray(0.7)):
    """
    生成隧道
    :param r: 隧道半径
    :param background: 窗体背景图
    :param light_color: 隧道光源颜色
    :return:
    """
    length = 300
    global radius
    radius = r
    # 默认创建半径为6的2D圆
    cr = vn.shapes.circle(radius=r)
    # 将圆拉长成圆柱，形成隧道
    os.chdir(SYS_DIR)
    vn.extrusion(path=[vn.vec(0, 0, 30), vn.vec(0, 0, -length)], shape=cr, texture=f'photos{os.sep}{background}')
    # 在圆柱的另一端设置一个灯光
    lamp = vn.local_light(pos=vn.vec(0, 0, -length), color=light_color)
    vn.sleep(1)


def forward(distance=30):
    """
    相机运动，调节 interval 改变匀减速效果
    :param v: 运动速度
    :param distance: 运动的距离
    :return:
    """
    a = 5  # 加速度
    t = 0  # 时间
    s = distance * 10
    v0 = vn.sqrt(2 * a * s)  # 初速度
    vt = (v0 - a * t)  # 瞬时速度
    k = vt * 9  # v0 折算为 0.1左右的系数
    _vt = vt / k  # 折算为 VPython 的相机偏移量
    # interval = distance * 10 / 5  # 时间间隔
    # _t = vn.sqrt(2*distance*10/a) # 运动时间
    _time = 0
    interval = 40  # 100次约等于 1s，加上程序运行时间取值为 30
    while _vt > 0:
        vn.rate(100)
        vn.scene.camera.pos += vn.vec(0, 0, -_vt)

        _time += 1
        if _time == interval:
            _time = 0
            t += 1
            vt = (v0 - a * t)  # 瞬时速度
            _vt = vt / k  # 折算为 VPython 的相机偏移量


# initialize()
