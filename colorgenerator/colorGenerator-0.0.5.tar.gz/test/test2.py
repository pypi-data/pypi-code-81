import colorGenerator as cG

red = cG.Color(rgb=(255, 0, 0))
blue = cG.Color(rgb=(0, 255, 0))

# Find the complementary of red
c_red = red.complementary()
print("The complementary of red is : ", end="")
c_red.show()

# Find the median of red and blue
# We create a palette
palette = cG.Palette(colors=[red, blue])
med = palette.average_hsl()
print("The median of red and blue is : ", end="")
med.show()