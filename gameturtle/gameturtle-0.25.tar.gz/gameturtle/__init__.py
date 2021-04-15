"""
   gameturtle.py   
   0.25版删除了切换造型的自动间隔时间机制。
   新增以下命令，
   1、splitgif,单独的拆帧函数。返回图形对象。   
   本模块的具体使用方法请查看李兴球编写的《Python海龟宝典》下册原理篇。
"""
__author__ = '李兴球'
__date__ = '2021/4/15'
__blog__ = 'www.lixingqiu.com'
__version__ = 0.25

import os
import time
import math
import numpy as np
from random import randint
from tkinter import Tk,Canvas
from PIL import Image,ImageTk,ImageGrab,ImageOps,ImageDraw,ImageColor,ImageFont,ImageSequence

def splitgif(imagepath):
    """拆帧，返回帧图形对象列表"""
    frames = []
    ext = os.path.splitext(imagepath)[-1]
    ext = ext.lower()
    im = Image.open(imagepath)
    if ext == '.gif':                 # 如果是gif扩展名则拆帧        
        for frame in ImageSequence.Iterator(im):
            frames.append(frame.copy())
    else:
        frames.append(im)
    return frames
        
def txt2image(txt,fontfile="simkai.ttf",fontsize=64,
              color=(255,255,255,255),stroke=None):
    """
        文本转图像实用函数,支持多行文本,默认为楷体,返回pillow图形对象。
        txt：文本        
        fontfile:ttf字体文件
        fontsize:字体大小
        color:颜色,通过写alpha值可支持半透明图形。如设定color=(0,0,255,127)蓝色透明字
        stroke：二元组，第一个值是一个整数，第二个值为描边颜色
    """    
    windowsdir = os.environ.get('WINDIR')
    try:
       fnt = ImageFont.truetype(fontfile,fontsize)
    except:
       fontfile = 'msyh.ttc'                      # win10的微软雅黑为ttc
       p = windowsdir + os.sep + 'fonts' + os.sep + fontfile
       fnt = ImageFont.truetype(p,fontsize)
    
    size = fnt.getsize(txt)                       # 获取文本的宽高

    pic = Image.new('RGBA', size)
    d = ImageDraw.Draw(pic)
    if stroke == None:
       size = d.multiline_textsize(text=txt, font=fnt,spacing=4)
    else:
       size = d.multiline_textsize(text=txt, font=fnt,spacing=4,stroke_width=stroke[0])
    
    pic = pic.resize(size)                        # 根据多行文本尺寸重调图形
    d = ImageDraw.Draw(pic)                       # 重新生成绘图对象
    
    if stroke == None:
        d.multiline_text((0,0),txt,font=fnt,fill=color)
    else:
        d.multiline_text((0,0),txt,font=fnt,fill=color,stroke_width=stroke[0], stroke_fill=stroke[1])
        
    return pic

def turtleimage(color='green'):
    """画海龟图形,返回图形"""
    size = (49,37)                 # 海龟图的分辨率
    cors = ((48.0, 18.0), (44.0, 22.0), (36.0, 20.0), (30.0, 26.0),
            (34.0, 32.0), (32.0, 36.0), (26.0, 30.0), (18.0, 32.0),
            (10.0, 28.0), (4.0, 34.0), (0.0, 30.0), (6.0, 26.0),
            (2.0, 18.0), (6.0, 10.0), (0.0, 6.0), (4.0, 2.0),
            (10.0, 8.0), (18.0, 4.0), (26.0, 6.0), (32.0, 0.0),
            (34.0, 4.0), (30.0, 10.0), (36.0, 16.0), (44.0, 14.0))
    
    im = Image.new("RGBA",size)
    d  = ImageDraw.Draw(im)
    d.polygon(cors,fill=color)
    return im

def _find_pixels(im_array,pixel,ignore_alpha=True):
    """im_array：二维像素阵列
       pixel：RGBA三或四元组或列表
       ignore_alpha:：是否忽略alpha通道
       返回行列号集合。
    """
    if ignore_alpha:
        im_array = im_array[:,:,:3]
        pixel = pixel[:3]
    pixel = np.array(list(pixel),dtype=np.uint8)
    rows,cols = np.where(np.all(im_array==pixel, axis=-1))
    rc = set(zip(rows,cols))
    return rc
    
def _make_croped_area(overlaped,rectangle):
    """
       overlapped是rectangle上面的一个子矩形。
       但它们的坐标都是相对于画布坐标系的。
       这个函数返回overlaped相对于rectangle左上角坐标的待剪裁区域。
       overlaped:Rect对象，
       rectangle:Rect对象，
       返回left,top,right,bottom，相对于rectangle的
    """
    left = overlaped.left - rectangle.left
    top = overlaped.top - rectangle.top
    right = left + overlaped.width
    bottom = top + overlaped.height
    return left,top,right,bottom

def _make_mask(image,area):
    """
       image:pillow图形对象
       area:图形对象上的一个区域(left,top,right,bottom)
    """
    im = image.crop(area)          # 根据area剪裁图形
    im_array = np.array(im)        # 转换成二维阵列
    mask = im_array[:,:,3] > 127   # 大于127的值变成1，否则变为0
    mask.dtype=np.uint8            # 类型转换
    return mask,im_array           # 返回mask和图形的二维数组

# 给画布增加一个方法，用来获取鼠标指针在画布的坐标
def _mouse_pos(self):    
     """获取鼠标指针的坐标，相对于画布的"""
     root = self.winfo_toplevel()
     mx = self.winfo_pointerx() - root.winfo_rootx() - self.winfo_x()
     my = self.winfo_pointery() - root.winfo_rooty() - self.winfo_y()
     return mx,my
Canvas.mouse_pos = _mouse_pos
Canvas.mouse_position = _mouse_pos
Canvas.mousepos = _mouse_pos
Canvas.mousepositioin = _mouse_pos

# 给画布增加一个方法，用来截图
def _grab(self):
    root = self.winfo_toplevel()    
    x = root.winfo_rootx() + self.winfo_x()        
    y = root.winfo_rooty() + self.winfo_y()
    width = self.cget('width')
    height = self.cget('height')
    right = x + int(width)
    bottom = y + int(height)
    size = (x,y,right,bottom)
    im = ImageGrab.grab(size)
    return im        
Canvas.grab = _grab

# 给画布增加一个方法，用来获取画布中心点坐标
def _center(self):
    width = self.cget('width')
    height = self.cget('height')    
    w = int(width)
    h = int(height)
    return w/2,h/2
Canvas.center = _center

def group(canvas,tag):
    """在画布中查找标签为tag的所有角色，返回角色列表"""
    items = canvas.find_withtag(tag)  # 在画布上查找标签为tag的item  
    sprites = list(map(lambda i:GameTurtle.sprites[i],items))
    return sprites

class Rect:
    """
    操作矩形的类，有left,top,right,bottom,width和height属性。
    有collidepoint，isintersect用来判断两个矩形是否相交的方法，
    overlap方法用来返回和另一个矩形的重叠区域，也用一个矩形表示。
    还有contain包含方法，用来判断一个矩形是否完全包含另一个矩形。 
    """
    def __init__(self, x,y,w,h):
        """
        x,y,w,h：最左x坐标，最顶y坐标，宽度，高度
        """
        self.resize(x,y,w,h)

        self.raw_left = x                # 原始x坐标
        self.raw_top = y                 # 原始y坐标
        self.raw_right = x + w           
        self.raw_bottom = y + h 
        self.raw_width = w
        self.raw_height = h
        
    def resize(self,x,y,w,h):
        self.left = x                    # 左上角x坐标
        self.top = y                     # 左上角y坐标
        self.width = w                   # 矩形宽度
        self.height = h                  # 矩形高度
        self.right = x + w               # 矩形右下角x坐标
        self.bottom = y + h              # 矩形右下角y坐标
        
    def collidepoint(self, x,y):
        """
        测试一个点是否在矩形内，在边界上也算。
        """
        c1 = (x >= self.left) and  (x <= self.right) # 在左右之间
        c2 = (y >= self.top) and (y <= self.bottom)  # 在上下之间
        return  c1 and  c2             # 两个条件同时成立则返回真 

    def isintersect(self, other):
        """
        测试是否和另一个矩形有重叠区域。
        """
        if self.left > other.right: return False
        if self.right < other.left: return False
        if self.bottom < other.top: return False
        if self.top > other.bottom: return False
        return True 

    def overlap(self, other):
        """
        返回和另一个矩形的重叠区域。
        """
        left = max((self.left, other.left))
        bottom = min((self.bottom, other.bottom))    # 两个矩形更大的bottom值
        right = min((self.right, other.right))
        top = max((self.top, other.top))             # 两个矩形更小的top        
        if (right - left)>=1 and (bottom-top)>=1 :
            return Rect(left,top,right-left,bottom-top)
        else:
            return None

    def contain(self, other):
        """
        如果other这个矩形包含在self内，则返回真。
        """
        if other.left >= self.left and other.right <= self.right:
            if other.top >= self.top and other.bottom <= self.bottom:
                return True
        return False

    def move(self,dx,dy):
        """
           在水平和垂直方向移动矩形分别为dx和dy个单位
        """
        self.left = self.left + dx
        self.top = self.top + dy
        
        self.right = self.left + self.width
        self.bottom = self.top + self.height

    def scale(self,scalew,scaleh=None,pos='center'):
        """缩放矩形，pos缩放的中心点，它有2个值，分别是:
           lefttop,center。
           scalew：横向缩放因子，为一个小数。
           scaleh：纵向缩放因子，为一个小数。
        """
        if scaleh == None:scaleh = scalew
        left = self.raw_left             # 记录最左x坐标
        top = self.raw_top               # 记录最顶y坐标
        right = self.raw_right           # 记录最右x坐标 
        bottom = self.raw_bottom         # 记录最下y坐标
        new_width = self.raw_width * scalew   # 新宽度
        new_height = self.raw_height * scaleh # 新高度
        if pos == 'lefttop' or pos == 'topleft':
            self.resize(left,top,new_width,new_height)                 
        elif pos == 'center' or pos=='' or pos==None:
            dw = self.raw_width - new_width  
            dh = self.raw_height - new_height 
            left = left + dw/2
            top = top + dh /2
            self.resize(left,top,new_width,new_height)
            
    def cross_left(self):
        """矩形内十字架左部"""
        if self.width < 3 or self.height <3:return self
        top = self.top + self.height//3
        w = self.width//3
        h = self.height//3        
        return Rect(self.left,top,w,h)        
        
    def cross_right(self):
        """矩形内十字架右部"""
        if self.width < 3 or self.height <3:return self
        left = self.left + self.width * 2 //3
        top = self.top + self.height//3
        w = self.width//3 
        h = self.height//3  
        return Rect(left,top,w,h)        
        
    def cross_top(self):
        """矩形内十字架上部"""
        if self.width < 3 or self.height <3:return self
        left = self.left + self.width//3
        w = self.width//3
        h = self.height//3 
        return Rect(left,self.top,w,h)

    def cross_bottom(self):
        """矩形内十字架下部"""
        if self.width < 3 or self.height <3:return self
        left = self.left + self.width//3
        top = self.top + self.height * 2//3
        w = self.width//3
        h = self.height//3     
        return Rect(left,top,w,h)
    
    def __repr__(self):
        """把自己显示为供解释器更好读的方式"""
        return "%s(left:%s,top:%s,width:%s,height:%s)@%d" % \
               (self.__class__.__name__, self.left, self.top, \
                self.width, self.height ,id(self))
    
class GameTurtle:
    sprites = {}                               # 所有角色字典
    def __init__(self,canvas,frames=None,pos=None,visible=True,heading=0,tag='sprite'):
        """
           canvas：海龟所在的画布
           frames：用Image.open打开的图形列表。
           pos：坐标
           visible：可见性，True或者Faslse。
           heading：初始方向
           tag：标签用于分组，值为字符串，或者数据为字符串的元组。
        """    
        self._canvas = canvas                   # 画布
        self._root = self._canvas.winfo_toplevel()
        canvas.update()                         # 更新一下，要不然获取不到宽高
        self._cv_width = int(canvas.config('width')[-1])        # 画布边框这里应该是获取
        self._cv_height = int(canvas.config('height')[-1])       
        self.item = self._canvas.create_image((0,0),image='',tags=tag) # 一个图形对象
        GameTurtle.sprites[self.item] = self    # 把自己存在所有角色字典中
        self._pendown = False                   # 落笔为否
        self._pensize = 2                       # 画笔线宽
        self._pencolor = 'blue'                 # 画笔颜色
        
        if pos==None:                           # 不写坐标，默认为画布中间
            pos = self._cv_width/2,self._cv_height/2 
        self.goto(pos)      

        if not visible:
            self.hide()                        # 如果不可见，则调用hide方法
        else:
            self._visible = True
        self._heading = heading                 # 初始朝向        
        self._stretchfactor = [1,1]             # 造型的伸展因子
        self._rotationstyle = 0                # 旋转模式0:all around, 1:left-right,2:no(don't rotate),

        self._loadshapes(frames)                # 加载frames造型列表,frames是pillow图形对象
        self._lineitems = []                    # 保存线条项目
        self._stampitems = []                   # 保存图章列表
        self._stampimages = []                  # 保存图章的PhotoImage造型列表(原因是需要全局引用)
        self._alive = True                      # 描述是否活着的逻辑变量 

    def setrotmode(self,mode=1):
        """设置旋转模式，默认为左右翻转:)。
           mode:值为0表示角色将会360度旋转,1表示只会左右翻转，2表示不旋转 
        """
        if mode in (0,1,2,360):
           self._rotationstyle = mode
           self._process_shape()                # 在造型列表中修改造型
           self._setshape()                     # 还需要重新设定造型并显示造型

    def getrotmode(self):
        """得到旋转模式"""
        return self._rotationstyle

    def shapesize(self,width=None,length=None):
        """角色变形，设定伸展因子
           width：以角色前进方向为准的造型的横向伸展因子
           length：以角色前进方向为准的造型的纵向伸展因子
           如果一个参数也不写，则返回伸展因子列表。
        """
        if width==None and length==None:
            return self._stretchfactor
        elif width!=None and length==None:
            length = width
        self._stretchfactor = [width,length]
        self._process_shape()
        self._setshape()                        # 设置造型         
        
    def pencolor(self,c=None):
        """设定或返回画笔颜色"""
        if c==None:
            return self._pencolor
        self._pencolor = c

    def pendown(self):
        """落笔，别名是down"""
        self._pendown = True

    def penup(self):
        """抬笔，别名是up或者pu"""
        self._pendown = False

    def pensize(self,w=None):
        """设定或返回线宽"""
        if w==None:
            return self._pensize
        self._pensize = w

    def dot(self,radius=None,color=None):
        """打圆点"""
        if radius==None:radius=2
        if color==None:color=self._pencolor
        x,y = self.position()
        x0,y0 = x - radius,y - radius
        x1,y1 = x + radius,y + radius
        return self._canvas.create_oval(x0,y0,x1,y1,fill=color,width=0)
        
    def _getrect(self):
        """
          获取当前造型的矩形,
          返回Rect(left,top,width,height)对象
        """
        w,h = self._current_shape.size    # 造型宽高
        x,y = self.pos()                  # 中心点坐标
        left = int(x) - int(w/2) 
        top = int(y) - int(h/2)
        return Rect(left,top,w,h)
    
    def _cross_left(self):
        """获取角色十字架左部分矩形"""
        r = self._getrect()
        return r.cross_left()
    
    def _cross_right(self):
        """获取角色十字架右部分矩形"""
        r = self._getrect()
        return r.cross_right()

    def _cross_top(self):
        """获取角色十字架上部分矩形"""
        r = self._getrect()
        return r.cross_top()
    
    def _cross_bottom(self):
        """获取角色十字架下部分矩形"""
        r = self._getrect()
        return r.cross_bottom()
    
    def rect_overlap(self,other,area=None):
        """和另一个角色的矩形碰撞，两个角色要在同一画布上。
           返回相对于画布的重叠区域。
        """
        if self._canvas != other._canvas:return None
        if self._visible == False or other._visible == False:return None
        if area==None:
            self._rect = self._getrect()
        elif area =='left':
            self._rect = self._cross_left()
        elif area =='right':
            self._rect = self._cross_right()
        elif area =='top':
            self._rect = self._cross_top()
        elif area =='bottom':
            self._rect = self._cross_bottom()

        other._rect = other._getrect()
        r = self._rect.overlap(other._rect)
        return r       
    
    def left_collide(self,other):
        """自己的左边区域和另一个角色，或者另一种颜色的碰撞。
           other：角色或者颜色，如果是角色，返回矩形重叠区域，
           如果是颜色，返回的和每个角色的(array,im_a,im_b,r)信息。
        """
        if isinstance(other,GameTurtle):          # 如果other是GameTurtle对象
            return self.rect_overlap(other,area='left')
        elif isinstance(other,(tuple,list,str)):  # 如果是序列则认为是颜色
            return self.collide_color(color=other,area='left')
    
    def right_collide(self,other):
        """自己的右边区域和另一个角色，或者另一种颜色的碰撞。
           other：角色或者颜色，如果是角色，返回矩形重叠区域，
           如果是颜色，返回的和每个角色的(array,im_a,im_b,r)信息。
        """
        if isinstance(other,GameTurtle):
            return self.rect_overlap(other,area='right')
        elif isinstance(other,(tuple,list,str)):  # 如果是序列则认为是颜色
            return self.collide_color(color=other,area='right')
    
    def top_collide(self,other):
        """自己的上边区域和另一个角色，或者另一种颜色的碰撞。
           other：角色或者颜色，如果是角色，返回矩形重叠区域，
           如果是颜色，返回的和每个角色的(array,im_a,im_b,r)信息。
        """
        if isinstance(other,GameTurtle):
            return self.rect_overlap(other,area='top')
        elif isinstance(other,(tuple,list,str)):  # 如果是序列则认为是颜色
            return self.collide_color(color=other,area='top')
    
    def bottom_collide(self,other):
        """自己的下边区域和另一个角色，或者另一种颜色的碰撞。
           other：角色或者颜色，如果是角色，返回矩形重叠区域，
           如果是颜色，返回的和每个角色的(array,im_a,im_b,r)信息。
        """
        if isinstance(other,GameTurtle):
            return self.rect_overlap(other,area='bottom')
        elif isinstance(other,(tuple,list,str)):  # 如果是序列则认为是颜色            
            return self.collide_color(color=other,area='bottom')
    
    def _pixels_overlapped(self,other):
        """
           和另一个角色的像素重叠检测，两个角色要在同一画布上。
           返回空或者重叠区域所有像素点的行列号及两图形分别的重叠子图array。
        """
        r = self.rect_overlap(other)        
        if not r : return None
        r_a = _make_croped_area(r,self._rect)  # 返回在self图上的待剪区域
        r_b = _make_croped_area(r,other._rect) # 返回在other图上的待剪区域
        mask_a,im_a = _make_mask(self._current_shape,r_a)  # 剪后形成mask_a
        mask_b,im_b = _make_mask(other._current_shape,r_b)
        mask = mask_a  + mask_b                # 最终所需要的mask  
        overlapped = np.argwhere(mask == 2)    # 所有像素重叠点的行列号
        
        if overlapped.size > 0:
            return overlapped,im_a,im_b,r,other # im_a和im_b都是numpy array 
        else:
            return None
            
    def _first_overlapped_pixel(self,other,ignore_alpha=True):
        """和另一个角色的像素重叠检测，两个角色要在同一画布上。
           返回第一个重叠点相对于画布的坐标和在两张图片上相应点的像素值。
        """
        result = self._pixels_overlapped(other)
        if not result : return False
        overlapped_pixels,im_a,im_b,r,other = result           
        top,left = overlapped_pixels[0]       # 第一个点的行列号          
        x = left + r.left                     # 相对于画布的x坐标
        y = top + r.top                       # 相对于画布的y坐标
        p1 = im_a[top,left]
        p2 = im_b[top,left]
        if ignore_alpha:
            p1 = p1[:3]
            p2 = p2[:3]
        return x,y,tuple(p1),tuple(p2)  # 注意只返回第一个点

    def near(self,other,distance):
        """通过距离进行的‘碰撞检测’
           self和other的距离小于或者等于distance则认为发生碰撞,
           适合于圆形角色。
        """
        if self.distance(other) <= distance:
            return True
        else:
            return False
        
    def collide(self,other,mode='pixel', ignore_alpha=True,distance=None):
        """和另一个角色的碰撞检测方法，可以用矩形，像素级与距离三种模式
           other：GameTurtle对象
           mode：碰撞检测的模式，pixel为像素级，rect为矩形，distance为距离
           ignore_alpha：是否忽略alpha通道
           
           根据mode返回不同的值
        """
        if mode == 'pixel':
            return self._first_overlapped_pixel(other,ignore_alpha=ignore_alpha)
        elif mode == 'rect':
            return self.rect_overlap(other)
        elif mode == 'distance':
            if distance == None:
                distance = self._rect.width
            return self.near(other,distance)

    def _overlapped_items(self,area=None):
        """
           查找自己的矩形区域，或者部分矩形区域的画布items。
           area的值为left,top,right,bottom，用于区分基于十字架模型的碰撞区域。
           返回item集合。
        """
        if area==None:
           a,b,c,d = self._canvas.bbox(self.item) # 注意和自定义的_getrect返回的矩形的区别
        else:
            if area=="left":
               r = self._cross_left()  # 这里返回的是自己定义的Rect对象              
            if area=="right":
               r = self._cross_right()
            if area=="top":
               r = self._cross_top()
            if area=="bottom":
               r = self._cross_bottom()
            a,b,c,d = r.left,r.top,r.left + r.width,r.top + r.height            

        items = set(self._canvas.find_overlapping(a,b,c,d))
        items.remove(self.item)             # 移除自己
        return items        
        
    def collide_tag(self,tag=None,area=None,pixel=True):
        """根据area找出重叠的item，然后检测item是否对应角色。
           再调用_pixels_overlapped和每个角色进行检测，看有没有发生像素级重叠。
           有则返回和其它所有角色发生的像素等信息。
           tag参数用于分组。area的值为left,top,right,bottom，
           用于区分基于十字架模型的碰撞区域。
           pixel参数用来决定是否还要进一步进行像素级检测。
        """            
        items = self._overlapped_items(area=area) # left,top,right,bottom        
        if tag != None:    # 相应标签的角色才会检测
            items = items.intersection(set(self._canvas.find_withtag(tag))) 
         
        others = [GameTurtle.sprites.get(item) for item in items] # item对应的角色
        others = list(filter(bool,others))                    # 去掉None,(不是角色) 
        if not others:return False                            # 没有碰到其它角色

        if pixel==False:return others          # 如果pixel为假，返回所有找到的角色
        
        # 下面的results是一个个的(array,im_a,im_b,r,ot)，每个array是和角色的所有碰撞点       
        results = [self._pixels_overlapped(other) for other in others]       
        results = filter(bool,results)   # 把没有发生像素级碰撞的过滤掉
        results = list(results)
        return results
        
    def collide_color(self,color,ignore_alpha=True,area=None):
        """对所有重叠的角色进行像素极检测，           。 
           在下面中rets解包的array、im_a和im_b及r解释分别如下:
           array：重叠区域所有碰撞点的行列号
           im_a：重叠区域转换成numpy数组的主碰方图像
           im_b：重叠区域转换成numpy数组的被碰方图像
           返回所碰到的角色列表。
        """
        results = self.collide_tag(area=area)        
        if not results:return False
        if isinstance(color,str):color = ImageColor.getrgb(color) # 0.23版增加
        if len(color)==3 : ignore_alpha=True
        sprites = []                                       # 待返回的角色列表 
        for rets in results:
            array,im_a,im_b ,r ,ot= rets
            others = _find_pixels(im_b,color,ignore_alpha) # 查找像素
            
            array = list(array)
            array = set(map(tuple,array))
            if array.intersection(others): sprites.append(ot)       
        return sprites
    
    def color_collide_color(self,color1,color2,ignore_alpha=True):
        """自己上面的颜色碰到其它角色们上的颜色
           返回所碰到的角色列表。
        """
        results = self.collide_tag()        
        if not results:return False
        if isinstance(color1,str):color1 = ImageColor.getrgb(color1) # 0.23版增加                
        if isinstance(color2,str):color2 = ImageColor.getrgb(color2) # 0.23版增加        if len(color1)==3 or len(color2)==3 : ignore_alpha=True
        sprites = []                                       # 待返回的角色列表 
        for rets in results:
            array,im_a,im_b ,r ,ot = rets            
            selfs = _find_pixels(im_a,color1,ignore_alpha) # 找到像素的行列号
            others = _find_pixels(im_b,color2,ignore_alpha)# 找到像素的行列号
            array = list(array)
            array = set(map(tuple,array))
            
            if array.intersection(selfs) and array.intersection(others):
                  if selfs.intersection(others):sprites.append(ot)         
        return sprites
        
    def color_collide_other_color(self,selfcolor,other,
                                  othercolor,ignore_alpha=True):
        """自己上面的颜色碰到单个角色上面的颜色的碰撞检测。
           selfcolor：自己图形区域的像素点值，RGBA四元组，alpha通道忽略则是三元组，下同。
           other：其它角色。
           othercolor：其它角色上面的像素点值，RGBA四元组。
           ignore_alpha：是否忽略透明通道，默认为忽略。
           返回真或者假。
        """
        if isinstance(selfcolor,str):selfcolor = ImageColor.getrgb(selfcolor) # 0.23版增加
        if isinstance(othercolor,str):othercolor = ImageColor.getrgb(othercolor) # 0.23版增加
        if len(selfcolor)==3 or len(othercolor)==3:
            ignore_alpha = True            
        
        result = self._pixels_overlapped(other)  # 测试是否发生像素级重叠
        if not result : return False
        array,im_a,im_b ,r,other = result

        selfs = _find_pixels(im_a,selfcolor,ignore_alpha)
        others = _find_pixels(im_b,othercolor,ignore_alpha)

        # 如果有相同的行列号，说明这个点的两种颜色发生“碰撞”
        if selfs.intersection(others):
            return True
        else:
            return False
        
    def _loadshapes(self,frames):
        """加载造型列表"""
        if frames == None:                              # 如果是空则画个海龟
            frames = [turtleimage('green')]
                      
        if not isinstance(frames,(list,tuple)):frames = [frames]
        self._raw_shapes = [im.copy() for im in frames] # 保留原始造型(用于图像处理)

        # 左右翻转时的造型列表
        #self._left_right_shapes =[[ImageOps.mirror(im) for im in self._raw_shapes],self._raw_shapes ]
        
        self._shapes = [im.copy() for im in frames]     # 当前的造型列表
        self._shape_amounts = len(self._shapes)         # 造型数量
        self._shapeindex = 0                            # 当前造型索引号
        self._current_shape = self._shapes[self._shapeindex] # 当前造型
        
        self._process_shape()                           # 根据方向，伸展因子处理当前造型
        self._setshape()                                # 设置造型
        
    def randomshape(self):
        """随机选择一个造型"""
        r = randint(0,self._shape_amounts-1)
        self._shapeindex = r
        self._setshape()
        
    def setindex(self,index):
        """指定造型索引号"""       
        self._shapeindex = index
        self._setshape()
        
    def shapeamounts(self):
        return self._shape_amounts
    
    def nextshape(self):
        """下一个造型"""
        self._shapeindex += 1                       # 索引号加1
        self._shapeindex %= self._shape_amounts     # 对数量求余
        self._process_shape()
        self._setshape()                            # 配置造型            

    def previousshape(self):
        """上一个造型"""       
        self._shapeindex -= 1                       # 索引号加1
        self._shapeindex %= self._shape_amounts     # 对数量求余
        self._process_shape()
        self._setshape()                            # 配置造型

    def _setshape(self):
        """设置造型"""
        self._current_shape = self._shapes[self._shapeindex]
        self._rect = self._getrect()                    # 换造型后要修改自己的矩形  
        self._PhotoImage = ImageTk.PhotoImage(self._current_shape)
        self._canvas.itemconfig(self.item,image=self._PhotoImage)        

    def _process_shape(self):
        """当前造型图形处理"""
        rawshape = self._raw_shapes[self._shapeindex] # 取出原始造型
         
        w,h = rawshape.size    
        newwidth = int(w * self._stretchfactor[1])
        newheight = int(h * self._stretchfactor[0])
        size = (newwidth,newheight)
        rawshape  = rawshape.resize(size,Image.ANTIALIAS)

        if self._rotationstyle==0 or self._rotationstyle==360: # 360度旋转
           self._current_shape = rawshape.rotate(-self.heading(),expand=1)# 旋转后的原始造型
        elif self._rotationstyle==1:                          # 左右翻转
            if self._heading>90 and self._heading<270:
                self._current_shape = ImageOps.mirror(rawshape)
            else:
                self._current_shape = rawshape
        elif self._rotationstyle==2:                          # 不旋转 
            self._current_shape = rawshape
        
        self._shapes[self._shapeindex] = self._current_shape   # 写回造型列表       
        
    def setheading(self,angle):
        """设置朝向，y轴向下，向右转,方向值增加"""
        self._heading = angle
        self._heading = self._heading % 360
        self._process_shape()
        self._setshape()
        
    def right(self,a):
        """向右旋转一定的角度，y轴向下，所以角度值增加"""
        self._heading += a
        self.setheading(self._heading)

    def left(self,a):
        """向左旋转一定的角度，y轴向下，所以角度值减少"""
        self.right(-a)

    def heading(self):
        """返回方向值"""
        return self._heading

    def towards(self,x,y=None):
        """朝向某个坐标"""
        if y == None:                # 如果y是空值，把x当成有两个数值的坐标
            x,y = x
        dx,dy = x - self.xcor(),y - self.ycor()
        angle = round(math.atan2(dy, dx)*180.0/math.pi, 10)            
        self.setheading(angle)

    def distance(self, x, y=None):
        """到某点或个角色的距离"""
        if y == None:
            # 如果它是Sprite实例的话，取它的x,y坐标
            if isinstance(x,GameTurtle):
                x,y = self._canvas.coords(x.item)
            else:                    # 否则认为x是一个元组
                x,y = x
        a,b = self._canvas.coords(self.item)
        dx = a - x
        dy = b - y
        return math.sqrt(dx*dx + dy*dy)        

    def goto(self,x,y=None):
        pos = self._canvas.coords(self.item)
        if y==None:                    # 如果y是None，把x当成有两个数据的序列
            x,y = x
        self._canvas.coords(self.item,x,y)
        self._drawline(pos,(x,y))

    def position(self):
        """返回(x,y)坐标"""
        return self._canvas.coords(self.item)

    def xcor(self):
        """返回x坐标"""
        return self._canvas.coords(self.item)[0]
    
    def ycor(self):
        """返回y坐标"""
        return self._canvas.coords(self.item)[1]

    def setx(self,newx):
        """设置x坐标"""
        x,y = self._canvas.coords(self.item)
        self._canvas.coords(self.item,newx,y)
        self._drawline((x,y),(newx,y))
        
    def sety(self,newy):
        """设置y坐标"""
        x,y = self._canvas.coords(self.item)
        self._canvas.coords(self.item,x,newy)
        self._drawline((x,y),(x,newy))

    def addx(self,dx):
        """增加x坐标的值为dx"""
        x,y = self._canvas.coords(self.item)
        self._canvas.coords(self.item,x+dx,y)
        self._drawline((x,y),(x+dx,y))
        
    def addy(self,dy):
        """增加y坐标的值为dy"""
        x,y = self._canvas.coords(self.item)
        self._canvas.coords(self.item,x,y+dy)
        self._drawline((x,y),(x,y+dy))  
        
    def forward(self,distance):
        """前进distance距离"""
        start = self._canvas.coords(self.item)       # 开始坐标
        r = math.radians(self._heading)              # 转换成弧度单位
        dx = distance * math.cos(r)                  # 计算需要前进的水平距离
        dy = distance * math.sin(r)                  # 计算需要前进的垂直距离
        self._canvas.move(self.item,dx,dy)           # 移动角色           
        end  = self._canvas.coords(self.item)        # 终点坐标  
        self._drawline(start,end)                    # 画线条     
            
    def backward(self,distance):
        """倒退"""
        self.forward(-distance)

    def _drawline(self,start,end):
        """画线"""
        if self._pendown:
            i = self._canvas.create_line(*start,*end,fill=self._pencolor,
                                         width=self._pensize,cap='round')
            self._canvas.tag_raise(self.item)
            self._lineitems.append(i)
     
    def hide(self):
        """隐藏"""
        self._visible=False            # 描述角色是否可见的逻辑变量
        self._canvas.itemconfig(self.item,state='hidden')
        self._canvas.update()

    def show(self):
        """显示"""
        self._visible=True
        self._canvas.itemconfig(self.item,state='normal')
        self._canvas.update()

    def isvisible(self):
        return self._visible

    def stamp(self):
        """盖图章"""
        pos = self.position()
        current_shape = self._shapes[self._shapeindex]
        phim = ImageTk.PhotoImage(current_shape)       
        item = self._canvas.create_image(pos,image=phim)
        self._canvas.tag_raise(self.item)
        self._canvas.update()
        self._stampitems.append(item)
        self._stampimages.append(phim)
        return item
    
    def clearstamp(self, stampid):
        """清除一个图章
        """
        if stampid in self._stampitems:
            self._canvas.delete(stampid)
            index = self._stampitems.index(stampid) # 根据编号求所在索引号
            self._stampitems.remove(stampid)
            self._stampimages.pop(index)            # 弹出对应索引的图章造型 
            self._canvas.update()
            
    def clearstamps(self, n=None):
        """清除多个图章
        """
        if n is None:
            toDelete = self._stampitems[:]
        elif n >= 0:
            toDelete = self._stampitems[:n]
        else:
            toDelete = self._stampitems[n:]
        [self.clearstamp(item) for item in toDelete]        
        
    def clear(self):
        """清除所画或所盖图章"""
        [self._canvas.delete(item) for item in self._lineitems]
        self._lineitems = []
        self.clearstamps()

    def home(self):
        """到画布中央,别名为center"""
        pos = self._canvas.coords(self.item)
        x = self._cv_width//2
        y = self._cv_height//2
        self.goto(x,y)
        self.setheading(0)
        self._drawline(pos,(x,y))        

    def reset(self):
        self.clear()
        self.home()

    def kill(self):
        self.clear()
        GameTurtle.sprites.pop(self.item)
        self._canvas.delete(self.item)
        self._alive = False            # 死了
        
    def is_alive(self):
        return self._alive

    def out_canvas(self):
        """超出画布区域的范围"""
        x,y = self.position()
        if x >=self._cv_width or x <=0 or \
           y >=self._cv_height or y<=0:
            return True
        else:
            return False
        
    def ondrag(self, fun, num=1, add=None):
        """
        绑定鼠标按钮的移动事件到海龟，fun函数要有两个整数参数，用来接收鼠标指针坐标，
        默认是左键(num=1)。最简单的用法就是t.ondrag(t.goto)，这样可拖动海龟。
        """
        if fun is None:
            self._canvas.tag_unbind(self.item, "<Button%s-Motion>" % num)
        else:
            def eventfun(event):
                try:                   
                    fun(event.x, event.y)
                except Exception:
                    pass
            self._canvas.tag_bind(self.item, "<Button%s-Motion>" % num, eventfun, add)    
    # 定义别名
    isalive =is_alive
    up = penup
    down = pendown
    pu = penup
    width = pensize
    center = home
    fd = forward
    rt = right
    lt = left
    seth = setheading
    setposition = goto
    setpos = goto
    pos = position
    bk = backward
    back = backward
    next_shape = nextshape
    previous_shape = previousshape
    ccc = color_collide_color
    ccoc = color_collide_other_color
    shape = _loadshapes
    rotationmode = setrotmode
    randomcostume = randomshape
    ht = hide
    hideturtle = hide
    st = show
    showturtle = show    

Sprite = GameTurtle                         # 定义类的别名

def main():  
    
    title = '游戏海龟模块0.25版本测试'
    root = Tk()
    root.title(title)
    
    cv = Canvas(root,width=400,height=300,bg='cyan')
    cv.pack()

    # 测试splitgif
    import os
    image = 'starshinning.gif'
    if os.path.exists(image):
        frames = splitgif(image)       
        flower = Sprite(cv,frames)
        while True:
            flower.nextshape()
            cv.update()
            time.sleep(0.2)
    else:
        cv.create_text(200,150,text='请放置'+image+'文件')
    
if __name__ == "__main__":

    main()




