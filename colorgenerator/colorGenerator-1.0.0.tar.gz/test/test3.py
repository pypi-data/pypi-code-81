import colorGenerator as cG

red = cG.Color(rgb=(255, 0, 0))
blue = cG.Color(rgb=(0, 255, 0))

# Save red into test3-red.json
red.save("test3-red.json")
# Loading saved color
load_red = cG.Color.load("test3-red.json")
print("The saved color is : ", end="")
load_red.show()

# We create a palette
palette = cG.Palette(colors=[red, blue])
# Save the palette test3-palette.json
palette.save("test3-palette.json")
# Loading saved palette
load_palette = cG.Palette.load("test3-palette.json")
print("The saved palette of red and blue is : ", end="")
load_palette.show()