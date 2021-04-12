import os
import math
from typing import Tuple, Dict, Union
from contextlib import contextmanager, AbstractContextManager
from simanim.abstract.core import DrawingPrimitive, DrawingDriver, AnimSettings
from simanim.abstract.api_primitives import Circle, Box, Line, Image, PolyLine, Arrow, Text
import js

class DrawingDriverJs(DrawingDriver):
    # Treba prepraviti da umesto paintera ide nešto iz čega će moći da se dohvati canvas na kome se crta
    
    def __init__(self, anim_settings:AnimSettings, animation_key: str):
        self.settings = anim_settings
        self.animation_key = animation_key
        self.draw_functions_map = {Circle: self.drawCircle, Box: self.drawBox, Line: self.drawLine, 
                                   Image: self.drawImage, PolyLine: self.drawPolyLine, Arrow: self.drawArrow,
                                   Text: self.drawText}


    def draw(self, primitive: DrawingPrimitive):
            self.draw_functions_map[type(primitive)](primitive)


    # sve dalje može ili da preko js modula direktno pristupa browser API-u
    # kao da si u javascriptu ili da poziva JavaScript funkciju u koju se prebaci deo 
    # koda koji pristupa browser API-u (uključujući canvas API)
    def _common_painter_setings(self, primitive:DrawingPrimitive):
        if primitive.pen_color is None:
            primitive.pen_color = '#000000'
        if primitive.line_width is  None:
            primitive.line_width = 0

   
    def drawCircle(self, circle:Circle):
        self._common_painter_setings(circle)
        js.queDrawEvent({'type':'circle', 'object' : circle, 'animation_key' : self.animation_key})

    def drawBox(self, box:Box):
        self._common_painter_setings(box)
        js.queDrawEvent({'type':'box', 'object' : box, 'animation_key' : self.animation_key})

    
    def drawLine(self, line:Line):
        self._common_painter_setings(line)
        js.queDrawEvent({'type':'line', 'object' : line, 'animation_key' : self.animation_key})


    def _drawArrowhead(self, point1:Tuple[float,float], point2:Tuple[float,float], line: Arrow):
        
        head_r = math.sin(line.head_angle) * line.head_len

        x1, y1 = point1
        x2, y2 = point2
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx**2 + dy**2)

        # normalized direction vector
        ux = (x2 - x1) / distance
        uy = (y2 - y1) / distance

        # perpendicular vector
        px, py = -uy, ux

        cx = x2 - line.head_len * ux
        cy = y2 - line.head_len * uy

        lx = cx + head_r * px
        ly = cy + head_r * py

        rx = cx - head_r * px
        ry = cy - head_r * py

        js.queDrawEvent({'type':'triangle', 'object' : [x2,y2, rx,ry, lx,ly, line], 'animation_key' : self.animation_key})
        return cx, cy

    def drawArrow(self, arrow:Arrow):
        self._common_painter_setings(arrow)
        point1, point2 = arrow.point1, arrow.point2
        line = Line(point1, point2)
        line.line_dashed = arrow.line_dashed
        line.line_width = arrow.line_width
        line.pen_color = arrow.pen_color
        line.fill_color = arrow.pen_color
        if arrow.head_len:
             line.point2 = self._drawArrowhead(point1, point2, arrow)
        self.drawLine(line)

    def drawPolyLine(self, polyLine:PolyLine):
        self._common_painter_setings(polyLine)     
        js.queDrawEvent({'type':'polyLine', 'object' : polyLine, 'animation_key' : self.animation_key})

    def drawImage(self, image:Image):
        self._common_painter_setings(image)
        js.queDrawEvent({'type':'image', 'object' : image, 'animation_key' : self.animation_key})

    def drawText(self, text:Text):
        self._common_painter_setings(text)
        js.queDrawEvent({'type':'text', 'object' : text, 'animation_key' : self.animation_key})

    def Rotate(self, point:Tuple[float,float], angle:float) -> AbstractContextManager:
        @contextmanager
        def rotate_context_manager():
            try:
                js.queDrawEvent({'type':'rotate', 'object' : [point,angle], 'animation_key' : self.animation_key})
                yield
            finally:
                js.queDrawEvent({'type':'restore', 'object' : None, 'animation_key' : self.animation_key})
        return rotate_context_manager()