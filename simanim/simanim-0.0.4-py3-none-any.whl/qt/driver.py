import os
import math
from typing import Tuple, Dict, Union
from contextlib import contextmanager, AbstractContextManager
from PySide2.QtCore import  Qt, QRectF, QLineF, QPointF
from PySide2.QtGui import QPainter, QPen, QBrush, QColor, QImage, QPainterPath,  QFont
from PySide2.QtSvg import QSvgRenderer
from simanim.abstract.core import DrawingPrimitive, DrawingDriver, AnimSettings
from simanim.abstract.api_primitives import Circle, Box, Line, Image, PolyLine, Arrow, Text

_image_cache: Dict[str,Union[QImage,QSvgRenderer]] = dict()
class DrawingDriverQt(DrawingDriver):


    def point_u_to_px(self, point: Tuple[float,float]):
        return self.settings.point_u_to_px(point)

    def scalar_u_to_px(self, scalar: float):
        return self.settings.scalar_u_to_px(scalar)

    def rect_u_to_px(self, xy_min_u: Tuple[float,float], w_u: float, h_u: float) -> Tuple[float,float,float,float]:
        x_min_u, y_min_u = xy_min_u
        x_px, y_px = self.point_u_to_px((x_min_u,y_min_u +h_u))
        w_px = self.scalar_u_to_px(w_u)
        h_px = self.scalar_u_to_px(h_u)
        return x_px, y_px, w_px, h_px

    def __init__(self, painter: QPainter, anim_settings:AnimSettings):
        self.painter = painter
        self.settings = anim_settings
        self.draw_functions_map = {Circle: self.drawCircle, Box: self.drawBox, Line: self.drawLine, 
                                   Image: self.drawImage, PolyLine: self.drawPolyLine, Arrow: self.drawArrow,
                                   Text: self.drawText}

        self.image_cache = _image_cache

    def draw(self, primitive: DrawingPrimitive):
        try:
            self.painter.save()
            self.draw_functions_map[type(primitive)](primitive)
        finally:
            self.painter.restore()

    def _common_painter_setings(self, primitive:DrawingPrimitive):
        pen = Qt.NoPen
        if primitive.pen_color is not None or primitive.line_width is not None:
            pen_color = '#000000' if primitive.pen_color is None else primitive.pen_color
            line_width = 0 if primitive.line_width is None else primitive.line_width
            w = self.scalar_u_to_px(line_width)
            if w > 0:
                if primitive.line_dashed:
                    pen_style = Qt.DashLine
                else:
                    pen_style = Qt.SolidLine
                pen = QPen(QColor(pen_color), w, pen_style, Qt.FlatCap, Qt.MiterJoin)
            else:
                pen = QPen(QColor(pen_color))
        self.painter.setPen(pen)

        brush = Qt.NoBrush
        if primitive.fill_color is not None:
            brush=QBrush(QColor(primitive.fill_color), Qt.SolidPattern)
        self.painter.setBrush(brush)
        self.painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.painter.setRenderHint(QPainter.Antialiasing, True)

    def drawCircle(self, circle:Circle):
        self._common_painter_setings(circle)
        cx_px, cy_px = self.point_u_to_px(circle.center)
        r_px = self.scalar_u_to_px(circle.radius)
        rect = QRectF(cx_px - r_px, cy_px - r_px, 2*r_px ,2*r_px)
        self.painter.drawEllipse(rect)

    def drawBox(self, box:Box):
        self._common_painter_setings(box)
        x_px, y_px, w_px, h_px = self.rect_u_to_px(box.xy_min, box.width, box.height)
        rect = QRectF(x_px, y_px, w_px, h_px)
        self.painter.drawRect(rect)


    def _drawLine(self, point1:Tuple[float,float], point2:Tuple[float,float]):
        x1, y1 = self.point_u_to_px(point1)
        x2, y2 = self.point_u_to_px(point2)
        l = QLineF(x1,y1,x2,y2)
        self.painter.drawLine(l)
    
    def drawLine(self, line:Line):
        self._common_painter_setings(line)
        self._drawLine(line.point1, line.point2)

    def _drawArrowhead(self, point1:Tuple[float,float], point2:Tuple[float,float],head_len:float, head_angle:float ):
        
        head_r = math.sin(head_angle) * head_len

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

        cx = x2 - head_len * ux
        cy = y2 - head_len * uy

        lx = cx + head_r * px
        ly = cy + head_r * py

        rx = cx - head_r * px
        ry = cy - head_r * py

        path = QPainterPath()
        path.moveTo(*self.point_u_to_px((x2,y2)))
        path.lineTo(*self.point_u_to_px((rx,ry)))
        path.lineTo(*self.point_u_to_px((lx,ly)))
        path.closeSubpath()
        self.painter.fillPath(path, self.painter.pen().color())
        
        return cx,cy

    def drawArrow(self, line:Line):
        self._common_painter_setings(line)
        point1, point2 = line.point1, line.point2
        if line.head_len:
            point2 = self._drawArrowhead(point1, point2, line.head_len, line.head_angle)
        self._drawLine(point1, point2)

    def drawPolyLine(self, polyLine:Line):
        self._common_painter_setings(polyLine)
        if len(polyLine.points) < 2:
            return
        path = QPainterPath()
        for i, point in enumerate(polyLine.points):
            x_px, y_px = self.point_u_to_px(point)
            if i == 0:
                path.moveTo(x_px, y_px)
            else:
                path.lineTo(x_px, y_px)
        self.painter.drawPath(path)
    
    def drawImage(self, image:Image):
        img_key = image.file
        is_svg = image.file.lower().endswith(".svg")
        if img_key in self.image_cache:
            qimg = self.image_cache[img_key]
        else:
            img_path = os.path.join(image.folder, image.file)
            if is_svg:
                qimg = QSvgRenderer(img_path)
            else:
                qimg = QImage(img_path)
            self.image_cache[img_key] = qimg
        
        x_px, y_px, w_px, h_px = self.rect_u_to_px(image.xy_min, image.width, image.height)

        if is_svg:
            bounds = QRectF(x_px, y_px, w_px, h_px)
            qimg.render(self.painter, bounds)
        else:
            img_rect = qimg.rect()
            w_src_px = img_rect.width()
            h_src_px = img_rect.height()
            x_scale = w_px / w_src_px
            y_scale = h_px / h_src_px
            self.painter.save()
            try:
                self.painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
                self.painter.setRenderHint(QPainter.Antialiasing, True)
                self.painter.scale(x_scale, y_scale)
                self.painter.drawImage(x_px / x_scale, y_px / y_scale, qimg)
            finally:
                pass
                self.painter.restore()

    def drawText(self, text:Text):
        self._common_painter_setings(text)
        x_px, y_px = self.point_u_to_px(text.position)
        fs_px = self.scalar_u_to_px(text.font_size)
        font = QFont()
        font.setFamily("Courier New")
        font.setFixedPitch(True)
        font.setBold(True)
        font.setStyleHint(QFont.TypeWriter)
        font.setPixelSize(fs_px)
        self.painter.setFont(font)
        #td = QTextDocument()
        #td.setHtml(text.content)
        #self.painter.translate(QPointF(x_px, y_px))
        #td.drawContents(self.painter)
        self.painter.drawText(x_px, y_px, text.content)


    def Rotate(self, point:Tuple[float,float], angle:float) -> AbstractContextManager:
        @contextmanager
        def rotate_context_manager():
            self.painter.save()
            try:
                self.painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
                self.painter.setRenderHint(QPainter.Antialiasing, True)
                self.painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
                v = QPointF(*self.point_u_to_px(point))
                self.painter.translate(v)
                self.painter.rotate(180*angle/math.pi)
                v *= -1
                self.painter.translate(v)
                yield
            finally:
                self.painter.restore()
        return rotate_context_manager()