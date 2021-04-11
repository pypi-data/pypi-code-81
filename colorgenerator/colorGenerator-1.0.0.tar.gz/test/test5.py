import colorGenerator as cG
from tkinter.colorchooser import askcolor

# Ask for a color
color = askcolor()
print(color[1])
r, g, b = color[0]

# Creating the color
new_color = cG.Color(rgb=(r, g, b))
new_color.show()