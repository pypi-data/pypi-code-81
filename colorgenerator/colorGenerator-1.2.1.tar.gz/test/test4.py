import colorGenerator as cG
import cv2, requests
from PIL import Image, ImageDraw, ImageFont

# Let's Download the background image at
url = "https://raw.githubusercontent.com/tttienthinh/colorGenerator/main/test/test4-bg.jpg"
image = requests.get(url)
open("test4-bg.jpg", "wb").write(image.content)

# Pick two colors from the image
img = cv2.imread("test4-bg.jpg")
up_left_color = cG.Color(rgb=img[300, 480, ::-1])
down_right_color = cG.Color(rgb=img[1500, 2400, ::-1])

# This is the 2 picked colors from the image
up_left_color.show()
down_right_color.show()

# Creating the palette
palette = cG.Palette(colors=[
    up_left_color,
    down_right_color,
])

# Extrating the text color as the average
text_color = palette.average_hsl().invert_luminosity()
text_color.show()

# opening the image and writing text
img = Image.open("test4-bg.jpg")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("test4-font.ttf", 335)
draw.text((150, 320), text="colorGenerator", font=font, fill=text_color.__repr__())
img.save("test4-result.jpg")