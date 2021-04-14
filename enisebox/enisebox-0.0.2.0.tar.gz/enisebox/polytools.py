def poly_area(verts):
    """
    Return area of a simple (ie. non-self-intersecting) polygon.
    Will be negative for counterclockwise winding.
    """
    accum = 0.0
    for i in range(len(verts)):
        j = (i + 1) % len(verts)
        accum += verts[j][0] * verts[i][1] - verts[i][0] * verts[j][1]
    return accum / 2

def poly_center(verts):
    n  = len(verts)
    xG = 0
    yG = 0
    for i in range(n):
        xG += verts[i][0]
        yG += verts[i][1]
    return xG/n, yG/n


verts = [(200,200),(100,300),(200,400),(250,300),(200,100)]


print(poly_area(verts))
print(poly_center(verts))