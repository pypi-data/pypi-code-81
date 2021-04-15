from guizero import Drawing
from Box2D import *
from .thing import *
from math import pi,cos,sin

class ebCircle(ebThing):
    def rotation(self,x,y,alpha):
        return cos(alpha)*x+sin(alpha)*y, -sin(alpha)*x+cos(alpha)*y

    def __init__(self, box, x, y, r, **kwargs):
        world  = box.world
        canvas = box.canvas

        # mémorisation de la box
        self.box   = box

        # paramètres
        self._type      = kwargs.pop('type', 'dynamic')

        dens            = kwargs.pop('density', 1)
        fric            = kwargs.pop('friction', 0)
        rest            = kwargs.pop('restitution', 0)

        angle           = kwargs.pop('angle', 0)
        fixedRot        = kwargs.pop('fixedRotation', False)

        bullet          = kwargs.pop('bullet', False)

        # body box2d
        if self._type=='static':
            constructor = world.CreateStaticBody
        elif self._type=='kinematic':
            constructor = world.CreateKinematicBody
        else:
            constructor = world.CreateDynamicBody
        body = constructor(
            position=(x/box.scale, box._height - y/box.scale),
            angle=angle,
            fixedRotation=fixedRot,
            bullet=bullet,
        )

        # fixture circle
        body.CreateCircleFixture(
            radius=r/box.scale,
            density=dens,
            friction=fric,
            restitution=rest,
        )

        # fixture polygone
        # verts = []
        # for i in range(16):
        #     verts.append(self.rotation(r/box.scale,0,(i+1)*2*pi/16))
        # body.CreatePolygonFixture(
        #     vertices=verts,
        #     density=dens,
        #     friction=fric,
        #     restitution=rest,
        # )

        # item canvas oval
        pos = body.position
        x = pos[0]*box.scale
        y = (box._height - pos[1])*box.scale
        r = body.fixtures[0].shape.radius*box.scale
        item = canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

        # item canvas polygone
        # shape  = body.fixtures[0].shape
        # coords = [ body.transform * v for v in shape.vertices ]
        # coords = [(c[0]*box.scale, (box._height - c[1])*box.scale) for c in coords]
        # item = canvas.create_polygon(coords, **kwargs)

        # on garde les liens vers ce qui vient d'être créé
        self.body  = body
        body.userData = self
        self.item  = item

    def update_item(self):
        box    = self.box
        body   = self.body
        canvas = box.canvas

        # update pour oval
        pos  = body.position
        x = pos[0]*box.scale
        y = (box._height - pos[1])*box.scale
        r = body.fixtures[0].shape.radius*box.scale
        canvas.coords(self.item, x - r, y - r, x + r, y + r)

        # update pour polygon
        # shape  = body.fixtures[0].shape
        # coords = [ body.transform * v for v in shape.vertices ]
        # new    = []
        # for c in coords:
        #     new += box.toCanvasCoords(*c)
        # for c in coords:
        #     new += [int(c[0]*box.scale), int((box._height - c[1])*box.scale)]
        # canvas.coords(self.item, new)
