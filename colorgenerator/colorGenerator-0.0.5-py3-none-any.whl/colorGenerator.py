from colorsys import *
import json

"""
This module is created by Tran-Thuong Tien-Thinh using the native colorsys :

Conversion functions between RGB and other color systems.
This modules provides two functions for each color system ABC:
  rgb_to_abc(r, g, b) --> a, b, c
  abc_to_rgb(a, b, c) --> r, g, b
All inputs and outputs are triples of floats in the range [0.0...1.0]
(with the exception of I and Q, which covers a slightly larger range).
Inputs outside the valid range may cause exceptions or invalid outputs.
Supported color systems:
RGB: Red, Green, Blue components
YIQ: Luminance, Chrominance (used by composite video signals)
HLS: Hue, Luminance, Saturation
HSV: Hue, Saturation, Value

"""




class Color:
    def __init__(self, rgb=None, hsl=None, s_rgb=None):
        """
        Color will be store in rgb format [0; 1], Color is white by default rgb = (250, 250, 250)
        :param rgb: (int/float, int/float, int/float) from 0 to 250
        :param hsl: (int/float [0; 360], int/float [0; 100], int/float [0; 100])
        :param s_rgb: (float, float, float) from 0 to 1
        """
        self.r, self.g, self.b = (1, 1, 1) # represent (250, 250, 250)
        if rgb is not None:
            self.r, self.g, self.b = self.scale_rgb(rgb)
        elif hsl is not None:
            h, s, l = hsl
            h, s, l = h/360, s/100, l/100
            self.r, self.g, self.b = hls_to_rgb(h, l, s)
        elif s_rgb is not None:
            self.r, self.g, self.b = s_rgb

    def __repr__(self):
        return self.unscale_rgb((self.r, self.g, self.b))

    def __str__(self):
        r, g, b = self.__repr__()
        return hex(r*(16**4) + g*(16**2) + b)

    def change(self, s_rgb):
        self.r, self.g, self.b = s_rgb

    def hsl(self):
        h, l, s = rgb_to_hls(self.r, self.g, self.b)
        return h, s, l

    def complementary(self):
        h, l, s = rgb_to_hls(self.r, self.g, self.b)
        h = (h+0.5) % 1
        return Color(s_rgb=hls_to_rgb(h, l, s))

    def invert_luminosity(self):
        h, l, s = rgb_to_hls(self.r, self.g, self.b)
        l = 1-l
        return Color(s_rgb=hls_to_rgb(h, l, s))

    def show(self):
        r, g, b = self.__repr__()
        print(f"\x1b[38;2;{r};{g};{b}m--- COLOR ---\x1b[0m")

    def save(self, name="color.json"):
        data = {}
        data['rgb'] = self.__repr__()
        data['hex'] = self.__str__()
        json.dump(data, open(name, 'w'))

    @staticmethod
    def load(name="color.json"):
        data = json.load(open(name))
        rgb = data['rgb']
        return Color(rgb=rgb)

    @staticmethod
    def scale_rgb(rgb):
        return tuple([x/255 for x in rgb])

    @staticmethod
    def unscale_rgb(rgb):
        return tuple([int(x*255) for x in rgb])


class Palette:
    """
    Palette is a list of color to store color
    """

    def __init__(self, colors=[]):
        self.colors = colors

    def average_rgb(self):
        r, g, b = 0, 0, 0
        n = len(self.colors)
        for color in self.colors:
            r += color.r / n
            g += color.g / n
            b += color.b / n
        new_color = Color()
        new_color.change((r, g, b))
        return new_color


    def average_hsl(self):
        h, s, l = 0, 0, 0
        n = len(self.colors)
        for color in self.colors:
            color_h, color_s, color_l = color.hsl()
            h += color_h / n
            s += color_s / n
            l += color_l / n
        new_color = Color()
        new_color.change(hls_to_rgb(h, l, s))
        return new_color

    def save(self, name="color.json"):
        data = []
        for color in self.colors:
            d_color = {}
            d_color['rgb'] = color.__repr__()
            d_color['hex'] = color.__str__()
        json.dump(data, open(name, 'w'))

    @staticmethod
    def load(name="color.json"):
        datas = json.load(open(name))
        colors = []
        for data in datas:
            rgb = data['rgb']
            colors.append(Color(rgb=rgb))
        return Palette(colors=colors)


def credits():
    print(f"\x1b[0;36;40mThanks for using ColorGenerator by \x1b[1;31;40mTien-Thinh Tran-Thuong\x1b[0m")
