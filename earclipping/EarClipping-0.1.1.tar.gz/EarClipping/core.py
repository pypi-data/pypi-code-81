"""
Author:     LanHao
Date:       2020/11/10
Python:     python3.6

"""
from typing import List
import logging
import math

import numpy as np

EPISON = 1e-5

logger = logging.getLogger(__name__)


def _clock_wise(points: np.ndarray) -> bool:
    """

    通过格林公式/ 鞋带公式 判断顺拟时针

    大于0 表示逆时针,小于0 表示顺时针

    相关介绍:

    https://blog.csdn.net/qq_37602930/article/details/80496498
    https://blog.csdn.net/c___c18/article/details/89284965
    :param points: np.ndarry type,2D points with order
    :return bool: 格林公式的计算结果,是否是顺时针

    """
    length = len(points)

    d = 0
    for i in range(length):
        i_use = i % length
        i_add = (i + 1) % length

        d += -0.5 * (points[i_use][1] + points[i_add][1]) * (
                points[i_add][0] - points[i_use][0])
    return True if d < 0 else False


def _conver_vertex(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> bool:
    """
    points in ,which is 2D points,with counter clock wise  order ,a,b,c

    通过升维,判断该点是凸顶点与否

    需要满足逆时针给出点坐标
    :return:
    """
    back_value = True
    crossp = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if crossp > 0:
        back_value = False
    return back_value


def get_cos_by(v1: np.ndarray, v2: np.ndarray) -> float:
    # 仅保留计算值本身的精度,不人工进行取舍

    v1_length = np.linalg.norm(v1)
    v2_length = np.linalg.norm(v2)

    assert v1_length != 0, Exception(f"计算向量角度,向量长度不可以为0,{v1}")
    assert v2_length != 0, Exception(f"计算向量角度,向量长度不可以为0,{v2}")

    return v1.dot(v2) / (v1_length * v2_length)


def get_angle_by(v1, v2) -> float:
    cos_value = get_cos_by(v1, v2)

    if cos_value > 1:
        cos_value = 1
    elif cos_value < -1:
        cos_value = -1

    return math.acos(cos_value) / math.pi * 180


def _in_triangle(triangle: list, vertex: np.ndarray) -> int:
    """
    判断一个点与三角形位置关系

    0 表示在三角形上
    -1 表示在三角形内部
    1 表示在三角形外部

    :param triangle:
    :param vertex:
    :return:
    """

    back = 0

    v1 = triangle[0] - vertex
    v2 = triangle[1] - vertex
    v3 = triangle[2] - vertex
    angle1 = get_angle_by(v1, v2)
    angle2 = get_angle_by(v2, v3)
    angle3 = get_angle_by(v3, v1)

    angles_all = angle1 + angle2 + angle3
    if angle1 == 180 or angle2 == 180 or angle3 == 180:
        back = 0
    else:
        if abs((360 - angles_all)) <= EPISON:  # 误差判断
            back = -1
        else:
            back = 1

    return back


class UV(object):
    """
    定义一个相对坐标值

    """
    _origin: np.ndarray
    _u_basic: np.ndarray
    _v_basic: np.ndarray
    _place: np.ndarray

    _u = None
    _v = None
    _vertex: np.ndarray = None

    def __init__(self, origin: np.ndarray, u_basic: np.ndarray, v_basic: np.ndarray, place: np.ndarray):
        self._origin = origin
        self._u_basic = u_basic
        self._v_basic = v_basic
        self._place = place

    def _get_vertex(self) -> np.ndarray:
        if self._vertex is None:
            self._vertex = self._place - self._origin

        return self._vertex

    @property
    def U(self):
        """
        相对的X

        :return:
        """
        if self._u is None:
            self._u = np.dot(self._get_vertex(), self._u_basic)

        return self._u

    @property
    def V(self):
        """
        相对的Y

        :return:
        """
        if self._v is None:
            self._v = np.dot(self._get_vertex(), self._v_basic)
        return self._v

    @property
    def XYZ(self) -> np.ndarray:
        """
        得到三维空间中的位置(仍然是当前平面中的投影点)
        :return:
        """

        xyz = np.asarray([0, 0, 0])
        xyz += self._u_basic * self.U
        xyz += self._v_basic * self.V
        return xyz


class Plane3D(object):
    """
    定义三维空间中的一个平面

    """
    _u_bais: np.ndarray  # x 轴单位向量
    _v_bais: np.ndarray  # y 轴单位向量
    _origin: np.ndarray  # 中心点
    _normal: np.ndarray  # 法向量

    def __init__(self, u_bais: np.ndarray, v_bais: np.ndarray, origin: np.ndarray):
        self._u_bais = u_bais / np.linalg.norm(u_bais)
        self._v_bais = v_bais / np.linalg.norm(v_bais)
        cos_value = self._u_bais.dot(self._v_bais)
        if abs(cos_value) > EPISON:
            raise Exception(f"传入的两个基础向量并不垂直,cos value 为:{cos_value}")
        self._origin = origin
        self._normal = np.cross(self._u_bais, self._v_bais)
        self._normal /= np.linalg.norm(self._normal)  # 此处的处理,便于后面计算点到平面的投影

    def distance(self, vertex: np.ndarray):
        """
        计算平面内外到平面的距离

        :param vertex:
        :return:
        """
        value = np.dot(self._normal, (vertex - self._origin))

        return value  # TODO 此处是否需要处理精度问题

    def project(self, vertex: np.ndarray) -> UV:
        """

        通过点法式,计算点到平面的投影点

        https://www.cnblogs.com/nobodyzhou/p/6145030.html

        用于三维点坐标转平面相对坐标

        :param vertex:
        :return:
        """
        t = np.dot(self._normal, vertex)  #
        point = vertex - self._normal * t
        return UV(self._origin, self._u_bais, self._v_bais, point)

    @classmethod
    def create_by_points(cls, points: np.ndarray) -> "Plane3D":
        """
        通过不共线三点构建一个平面

        :param points:
        :return:
        """
        v1 = points[1] - points[0]
        v2 = points[2] - points[1]
        normal = np.cross(v1, v2)
        v1 = np.cross(normal, v2)
        plane = cls(v1, v2, points[0])
        return plane


class SingleLinkNode(object):
    """
    单向,不收尾相连的链表,特用于耳裁法中遍历点

    """
    vertex: np.ndarray  # 顶点
    next_node: "SingleLinkNode" = None

    def __init__(self, vertex: np.ndarray):
        self.vertex = vertex


def clip(vertices: np.ndarray) -> List:
    """
    通过耳裁剪将多个点信息转换为三角形信息

    此时,拿来处理的点数据必须是二维平面的数据,不需要收尾相连

    :param vertices: 按顺时针或者逆时针组织的平面点（2D）,形如[[1,2],[2,3],[3,4]] 这样的数据格式组成的矩阵
    :return: 返回三角形组,形如[ [[1,2],[1,2],[1,2]], [[1,2],[1,2],[1,2]]]
    """

    clock_wise = _clock_wise(vertices)  # 是否是顺时针
    if clock_wise:
        # 传入点采用顺时针构造,需要颠倒点顺序供后续计算")
        vertices = np.flipud(vertices)

    # 此时,确保二维平面中的点是按照逆时针完成的

    # 构造单向链表
    link_head = SingleLinkNode(vertices[0])
    link_end: SingleLinkNode
    last_node = link_head
    for i in range(1, len(vertices)):
        link_end = SingleLinkNode(vertices[i])
        last_node.next_node = link_end
        last_node = link_end  # 替换此部分

    data_back = []  # 需要返回的三角形数据

    node_current = link_head  # 简单平面多边形,不止一个凸角
    while node_current:
        node_next = node_current.next_node
        node_next_agin = node_next and node_next.next_node  # 内含and 判断省去if else
        v1 = node_current.vertex
        v2 = node_next and node_next.vertex
        v3 = node_next_agin and node_next_agin.vertex
        if v1 is not None and v2 is not None and v3 is not None:
            v_1 = v1 - v2
            v_2 = v3 - v2
            if np.linalg.norm(np.cross(v_2, v_1)) == 0:  # 三点共线,需要剔除中间的点
                node_current.next_node = node_next_agin
                node_next_agin.last_node = node_current  # 孤立中间点
                continue

            convex_status = _conver_vertex(np.asarray([v1, v2, v3]))
            if convex_status:  # 满足凸角,进而判断其他所有点是否在该点内部
                status = True
                next_in_triangle_check = node_next_agin.next_node

                # 向后循环迭代
                while next_in_triangle_check:
                    vertex_check_current = next_in_triangle_check.vertex
                    in_triangle_status = _in_triangle([v1, v2, v3], vertex_check_current)
                    if in_triangle_status <= 0:
                        status = False
                        break
                    next_in_triangle_check = next_in_triangle_check.next_node

                if status:
                    data_back.append([v1, v2, v3])
                    node_current.next_node = node_next_agin
                    node_next.next_node = None
                    continue
            # 转移到前面
            node_current.next_node = None
            link_end.next_node = node_current
            link_end = node_current
            node_current = node_next
        else:
            break

    return data_back

