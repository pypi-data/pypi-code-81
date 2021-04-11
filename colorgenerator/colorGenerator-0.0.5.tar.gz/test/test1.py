import colorGenerator as cG

# Print some color
red = cG.Color(rgb=(255, 0, 0))

# Representation of red in RGB
print(f"Representation of red in RGB : {red}")

# References
# http://en.wikipedia.org/wiki/HLS_color_space
# Representation of red in HSL
h, s, l = red.hsl()
print(f"Representation of red in HSL : {(h*360, s*100, l*100)}")

# Show the color in the Terminal
red.show()

cG.credits()
