from PIL import Image, ImageDraw, ImageFont
from platform import system
import ctypes
import textwrap
import requests

class Wallpaper:

    def __init__(self, wallpaper_size=(3008, 1692), font_size=40, bg_color=(76, 74, 72), text_color=(255, 255, 255), top=50, left=1200):
        self.wallpaper_size = wallpaper_size
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.top = top
        self.left = left

    def generate(self, text='', file_name=''):
        if not file_name:
            file_name = 'C:/tmp/wall_tmp.png' if self.is_win() else '/tmp/wall_tmp.png'

        img = Image.new('RGB', self.wallpaper_size, color=self.bg_color)
        d = ImageDraw.Draw(img)
        texts = textwrap.wrap(text, 100, break_long_words=False)

        if len(texts) == 1:
            d.text((self.left, self.top), texts[0], font=self.get_font(), fill=self.text_color)
        else:
            for txt in texts:
                d.text((self.left, self.top), txt, font=self.get_font(), fill=self.text_color)
                self.top += 50

        img.save(file_name)
        self.change_wallpaper(file_name)

    def get_font(self):
        font_path = 'C:/Windows/Fonts/' if self.is_win() else '/Library/Fonts/'
        return ImageFont.truetype(font_path + 'Arial.ttf', self.font_size)

    def change_wallpaper(self, uri):
        ''' http://codingdict.com/sources/py/win32gui/16607.html '''
        if self.is_win():
            if uri.startswith('http'):
                file = 'C:/tmp/wall_tmp.png'
                img_data = requests.get(uri).content
                with open(file, 'wb') as handler:
                    handler.write(img_data)
                uri = file

            uri = uri.replace("/", "\\")
            ctypes.windll.user32.SystemParametersInfoW(20, 26, uri, 1)
        else:
            from os import system as s
            s('osascript -e \'tell application "Finder" to set desktop picture to POSIX file "{0}"\''.format(uri))

        return uri

    def is_win(self):
        return system() == "Windows"


if __name__ == '__main__':
    w = Wallpaper()

    # text = 'What the fuck am I doing ?!'
    # w.generate(text)
