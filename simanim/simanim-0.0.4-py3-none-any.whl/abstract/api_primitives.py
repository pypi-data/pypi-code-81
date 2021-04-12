from typing import Tuple, List
from .core import DrawingPrimitive
import os
import inspect
import math

__all__ = ["Circle", "Box", "Line", "Image", "PolyLine", "Arrow", "Text"]

class Circle(DrawingPrimitive):
    def __init__(self, center: Tuple[float, float], radius: float):
        super().__init__()
        self.center = center
        self.radius = radius

class Box(DrawingPrimitive):
    def __init__(self, xy_min: Tuple[float, float], width:float, height:float):
        super().__init__()
        self.xy_min = xy_min
        self.width = width
        self.height = height

class Line(DrawingPrimitive):
    def __init__(self, point1: Tuple[float, float], point2: Tuple[float, float]):
        super().__init__()
        self.point1 = point1
        self.point2 = point2

class Arrow(DrawingPrimitive):
    def __init__(self, point1: Tuple[float, float], point2: Tuple[float, float]):
        super().__init__()
        self.point1 = point1
        self.point2 = point2
        self.head_len = self._default("head_len")
        self.head_angle = self._default("head_angle", math.pi / 6)

class Text(DrawingPrimitive):
    def __init__(self, position: Tuple[float, float], content: str):
         super().__init__()
         self.position = position
         self.content = content
         self.font_size = self._default("font_size", 5)

class PolyLine(DrawingPrimitive):
    def __init__(self, points: List[Tuple[float, float]]):
        super().__init__()
        self.points = points

class Image(DrawingPrimitive):
    def __init__(self, file: str, xy_min: Tuple[float, float], width:float, height:float):
        super().__init__()
        caller_module = inspect.getmodule(inspect.stack()[1].frame)
        self.folder = os.path.abspath((os.path.dirname(caller_module.__file__))) if caller_module else None
        self.file = file
        self.xy_min = xy_min
        self.width = width
        self.height = height

