from pymkup import pymkup

x = pymkup("/tests/test2.pdf")
x.csv_export()
print(x.spaces_hierarchy())