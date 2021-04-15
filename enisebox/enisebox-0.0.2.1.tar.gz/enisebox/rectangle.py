from guizero import Drawing
from Box2D import *
from .thing import *

class ebRectangle(ebThing):
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

        if len(args)==4:
            x0, y0, x1, y1 = args

        width  = (x1-x0)/box.scale
        height = (y1-y0)/box.scale

        # body box2d
        if self._type=='static':
            constructor = world.CreateStaticBody
        elif self._type=='kinematic':
            constructor = world.CreateKinematicBody
        else:
            constructor = world.CreateDynamicBody
        x,y = (    min(x0,x1)/box.scale+width/2,
                            box._height-max(y0,y1)/box.scale+height/2  )
        body = constructor(
            position = (x,y),
            angle = angle,
            fixedRotation=fixedRot,
            bullet=bullet,
        )
        body.CreatePolygonFixture(
            # box=(width/2, height/2),
            box=(width/2, height/2, (0,0), 0),
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