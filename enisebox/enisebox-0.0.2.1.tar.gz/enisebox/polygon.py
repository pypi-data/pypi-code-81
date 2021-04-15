from guizero import Drawing
from Box2D import *
from math import cos,sin,pi
from .thing import *

class ebPolygon(ebThing):
    def __init__(self, box, *args, **kwargs):
        world  = box.world
        canvas = box.canvas

        # mémorisation de la box
        self.box   = box

        # paramètres enisebox
        self._type      = kwargs.pop('type', 'dynamic')

        # paramètres body
        angle           = kwargs.pop('angle', 0)
        fixedRot        = kwargs.pop('fixedRotation', False)
        bullet          = kwargs.pop('bullet', False)

        # paramètres fixture
        dens            = kwargs.pop('density', 1)
        fric            = kwargs.pop('friction', 0)
        rest            = kwargs.pop('restitution', 0)

        # args est censé contenir la liste des sommets
        verts = args[0]
        # on recalcule tous les sommets dans le repère physique
        verts = [(v[0]/box.scale, box._height-v[1]/box.scale) for v in verts]
        # isobarycentre du polygone, centre du body
        (x, y) = self._poly_center(verts)
        # on recalcule tous les sommets par rapport au centre
        verts = [(v[0]-x, v[1]-y) for v in verts]
        # on applique la rotation par rapport au centre
        # verts = [self._vert_rotate(vert, angle) for vert in verts]
        # body box2d
        if self._type=='static':
            constructor = world.CreateStaticBody
        elif self._type=='kinematic':
            constructor = world.CreateKinematicBody
        else:
            constructor = world.CreateDynamicBody
        # on place le body sur l'isobarycentre du polygone
        body = constructor(
            position = (x,y),
            angle = angle,
            fixedRotation=fixedRot,
            bullet=bullet,
        )
        # si les sommets ne sont pas listés dans l'ordre trigo
        # on retourne la liste
        # if self._poly_area(verts)<0:
        #     pverts.reverse()

        # creation du polygone
        body.CreatePolygonFixture(
            vertices=verts,
            density=dens,
            friction=fric,
            restitution=rest,
        )
        # on garde le lien
        self.body = body
        body.userData = self

        # item canvas
        shape  = body.fixtures[0].shape
        coords = [ body.transform * v for v in shape.vertices ]
        coords = [(c[0]*box.scale, (box._height - c[1])*box.scale) for c in coords]
        self.item = canvas.create_polygon(coords, **kwargs)

    def _poly_center(self, verts):
        n  = len(verts)
        xG = 0
        yG = 0
        for i in range(n):
            xG += verts[i][0]
            yG += verts[i][1]
        return xG/n, yG/n

    def _poly_area(self, verts):
        """
        Return area of a simple (ie. non-self-intersecting) polygon.
        Will be negative for counterclockwise winding.
        """
        accum = 0.0
        for i in range(len(verts)):
            j = (i + 1) % len(verts)
            accum += verts[j][0] * verts[i][1] - verts[i][0] * verts[j][1]
        return accum / 2

    def _vert_rotate(self, vert, alpha):
        new = (
                    cos(alpha)*vert[0]-sin(alpha)*vert[1],
                    sin(alpha)*vert[0]+cos(alpha)*vert[1]
                )
        return new

    def update_item(self):
        box    = self.box
        body   = self.body
        canvas = box.canvas
        shape  = body.fixtures[0].shape
        coords = [ body.transform * v for v in shape.vertices ]
        new    = []
        for c in coords:
            new += box.toCanvasCoords(*c)
        canvas.coords(self.item, new)