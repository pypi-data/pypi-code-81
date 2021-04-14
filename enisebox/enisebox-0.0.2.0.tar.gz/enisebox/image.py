from guizero import Drawing
from PIL import Image, ImageTk
from Box2D import *
from .thing import *
from math import pi,sqrt
from time import time

class ebImage(ebThing):
    def __init__(self, box, x, y, width, height, **kwargs):
        world  = box.world
        canvas = box.canvas

        # mémorisation de la box
        self.box   = box

        # paramètres
        self._type      = kwargs.pop('type', 'dynamic')

        file            = kwargs.pop('image', None)

        angle           = kwargs.pop('angle', 0)
        dens            = kwargs.pop('density', 1)
        fric            = kwargs.pop('friction', 0)
        rest            = kwargs.pop('restitution', 0)

        fixedRot        = kwargs.pop('fixedRotation', False)
        noRot           = kwargs.pop('noRotation', False)

        bullet          = kwargs.pop('bullet', False)

        if noRot:
            fixedRot = True

        # body box2d
        if self._type=='static':
            constructor = world.CreateStaticBody
        elif self._type=='kinematic':
            constructor = world.CreateKinematicBody
        else:
            constructor = world.CreateDynamicBody
        body = constructor(
            position = (x/box.scale, box._height-y/box.scale),
            angle=angle,
            fixedRotation=fixedRot,
            bullet=bullet,
        )
        body.CreatePolygonFixture(
            box=(width/box.scale/2, height/box.scale/2, (0,0), 0),
            density=dens,
            friction=fric,
            restitution=rest,
        )
        # item canvas
        if file and not noRot:
            # calcul des dimensions de l'image
            shape  = body.fixtures[0].shape
            coords = shape.vertices
            width,height = coords[2][0]-coords[0][0], coords[2][1]-coords[0][1]
            # lecture de l'image
            img = Image.open(file)
            w,h = img.size
            ratio = (width/w, height/h)
            side  = int(sqrt(w**2+h**2))
            # on étend l'image avec des pixels transparents
            # pour pouvoir la tourner sans perdre de pixels
            new = Image.new('RGBA', (side, side), (0, 0, 0, 0))
            new.paste(  img,
                        (int((side-w)/2), int((side-h)/2)),
                        img.convert('RGBA')
            )
            # redimensionnement
            # w,h = new.size
            # new = new.resize(
            #         (int(w*ratio[0]*box.scale),int(h*ratio[1]*box.scale)),
            #         # Image.NEAREST,
            #         # Image.BICUBIC,
            #         Image.LANCZOS,
            # )
            img = new
            w,h = img.size
            # stockage de l'image
            self._ratio = ratio
            self._img = []
            t0 = time()
            for angle in range(360):
                # rotation
                new = img.rotate(angle)
                # redimensionnement
                # c'est plus long de le faire ici, mais le résultat est meilleur...
                new = new.resize(
                        (int(w*ratio[0]*box.scale),int(h*ratio[1]*box.scale)),
                        # Image.NEAREST,
                        # Image.BICUBIC,
                        Image.LANCZOS,
                )
                # stockage
                self._img.append(ImageTk.PhotoImage(new))
            print('{} : {}s'.format(file,
                            str(int(100*(time()-t0))/100))
                )
            # placement de l'image dans le Canvas
            pos    = body.position
            angle  = int(body.transform.angle*180/pi)
            item   = canvas.create_image(
                                pos[0]*box.scale,
                                (box._height - pos[1])*box.scale,
                                image=self._img[angle]
                    )
        elif file and noRot:
            # calcul des dimensions de l'image
            shape  = body.fixtures[0].shape
            coords = shape.vertices
            width,height = coords[2][0]-coords[0][0], coords[2][1]-coords[0][1]
            # lecture de l'image
            img = Image.open(file)
            w,h = img.size
            ratio = (width/w, height/h)
            side  = int(sqrt(w**2+h**2))
            # on étend l'image avec des pixels transparents
            # pour pouvoir la tourner sans perdre de pixels
            new = Image.new('RGBA', (side, side), (0, 0, 0, 0))
            new.paste(  img,
                        (int((side-w)/2), int((side-h)/2)),
                        img.convert('RGBA')
            )
            img = new
            w,h = img.size
            self._ratio = ratio
            self._img = []
            # rotation
            angle  = int(body.transform.angle*180/pi)
            new    = img.rotate(angle)
            # redimensionnement
            new = new.resize(
                    (int(w*ratio[0]*box.scale),int(h*ratio[1]*box.scale)),
                    # Image.NEAREST,
                    # Image.BICUBIC,
                    Image.LANCZOS,
            )
            # stockage
            self._img.append(ImageTk.PhotoImage(new))
            # placement de l'image dans le Canvas
            pos  = body.position
            item = canvas.create_image(
                                pos[0]*box.scale,
                                (box._height - pos[1])*box.scale,
                                image=self._img[0],
                    )

        else:
            item   = None

        # on garde les liens
        self.body = body
        body.userData = self
        self.item = item
        self.noRot = noRot


    def update_item(self):
        box    = self.box
        body   = self.body
        canvas = box.canvas
        pos    = body.position
        shape  = body.fixtures[0].shape
        angle  = int(body.transform.angle*180/pi)

        if not self.noRot:
            canvas.itemconfigure(self.item, image=self._img[angle])
        canvas.coords(self.item, box.toCanvasCoords(*pos))
