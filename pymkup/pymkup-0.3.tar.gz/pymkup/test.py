from pymkup import pymkup
import json

x = pymkup("/tests/9.pdf")
y = x.markups(space_hierarchy=False)
print(json.dumps(y, indent=4, default=str))