from guizero import App, Drawing
from PIL import Image, ImageTk
from Box2D import *
from random import randint

from .rectangle import ebRectangle
from .circle import ebCircle
from .image import ebImage
from .polygon import ebPolygon

class enisebox():
    def __init__(self, canvas, *args, **kwargs):
        # paramètres pour le canvas
        canvas.update()
        self.scale     = kwargs.pop('scale', 20)
        self.canvas    = canvas
        self._width     = canvas.winfo_width()/self.scale
        self._height    = canvas.winfo_height()/self.scale
        # contactListener
        self._contact   = kwargs.pop('contact', None)
        if self._contact is not None:
            contactListener = ebContactListener(self._contact)
            kwargs['contactListener'] = contactListener
        # le monde box2d
        self.world     = b2World(**kwargs)
        # les images
        self._images  = {}
        # les objets du monde
        self.things   = []

    def create_rectangle(self, *args, **kwargs):
        obj = ebRectangle(self, *args, **kwargs)
        self.things.append(obj)
        return obj

    def create_polygon(self, *args, **kwargs):
        obj = ebPolygon(self, *args, **kwargs)
        self.things.append(obj)
        return obj

    def create_circle(self, *args, **kwargs):
        obj = ebCircle(self, *args, **kwargs)
        self.things.append(obj)
        return obj

    def create_image(self, *args, **kwargs):
        obj = ebImage(self, *args, **kwargs)
        self.things.append(obj)
        return obj

    def itemconfigure(self, thing, **kwargs):
        item = thing.item
        if kwargs:
            self.canvas.itemconfigure(item, **kwargs)
        else:
            return self.canvas.itemconfigure(item)

    def Step(self, *args):
        self.world.Step(*args)
        for obj in self.things:
            obj.update_item()

    def CreateDistanceJoint(self, thingA, thingB, anchorA, anchorB, **kwargs):
        return self.world.CreateDistanceJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            anchorA=self.toBoxCoords(*anchorA),
            anchorB=self.toBoxCoords(*anchorB),
            **kwargs,
        )

    def CreateRevoluteJoint(self, thingA, thingB, anchor, **kwargs):
        return self.world.CreateRevoluteJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            anchor=self.toBoxCoords(*anchor),
            **kwargs,
        )

    def CreatePrismaticJoint(self, thingA, thingB, anchor, axis, **kwargs):
        lowerTranslation = kwargs.pop('lowerTranslation', 0)
        upperTranslation = kwargs.pop('upperTranslation', 0)
        if lowerTranslation:
            kwargs['lowerTranslation']=lowerTranslation/self.scale
        if upperTranslation:
            kwargs['upperTranslation']=upperTranslation/self.scale
        return self.world.CreatePrismaticJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            anchor=self.toBoxCoords(*anchor),
            axis=axis,
            **kwargs,
        )

    # def CreateWheelJoint(self, thingA, thingB, **kwargs):
    #     return self.world.CreateWheelJoint(
    #         bodyA=thingA.body,
    #         bodyB=thingB.body,
    #         **kwargs,
    #     )
    #
    # def CreateRopeJoint(self, thingA, thingB, **kwargs):
    #     return self.world.CreateRopeJoint(
    #         bodyA=thingA.body,
    #         bodyB=thingB.body,
    #         **kwargs,
    #     )
    #
    # def CreateFrictionJoint(self, thingA, thingB, **kwargs):
    #     return self.world.CreateFrictionJoint(
    #         bodyA=thingA.body,
    #         bodyB=thingB.body,
    #         **kwargs,
    #     )
    #
    # def CreateGearJoint(self, thingA, thingB, **kwargs):
    #     return self.world.CreateGearJoint(
    #         bodyA=thingA.body,
    #         bodyB=thingB.body,
    #         **kwargs,
    #     )
    #
    # def CreateMouseJoint(self, thingA, thingB, **kwargs):
    #     return self.world.CreateMouseJoint(
    #         bodyA=thingA.body,
    #         bodyB=thingB.body,
    #         **kwargs,
    #     )
    #
    # def CreatePulleyJoint(self, thingA, thingB, **kwargs):
    #     return self.world.CreatePulleyJoint(
    #         bodyA=thingA.body,
    #         bodyB=thingB.body,
    #         **kwargs,
    #     )
    #
    # def CreateWeldJoint(self, thingA, thingB, **kwargs):
    #     return self.world.CreateWeldJoint(
    #         bodyA=thingA.body,
    #         bodyB=thingB.body,
    #         **kwargs,
    #     )

    def DestroyThing(self, thing):
        if thing in self.things:
            self.things.remove(thing)
            self.canvas.delete(thing.item)
            self.world.DestroyBody(thing.body)
            thing.body = None
        else:
            print("enisebox .DestroyThing : vous essayez de détruire un objet qui n'existe pas !")

    def DestroyJoint(self, joint):
        self.world.DestroyJoint(joint)

    def toBoxCoords(self, x, y):
        return (x/self.scale, (self._height*self.scale-y)/self.scale)

    def toCanvasCoords(self, x, y):
        return (int(x*self.scale), int((self._height-y)*self.scale))

    def find_overlapping2(self, bbox, callback):
        (x1, y1, x2, y2) = bbox
        queryCallback = ebQueryCallback2(callback)
        aabb = b2AABB(
            lowerBound=self.toBoxCoords(x1,y2),
            upperBound=self.toBoxCoords(x2,y1),
        )
        self.world.QueryAABB(queryCallback, aabb)

    def find_overlapping(self, x1, y1, x2, y2):
        queryCallback = ebQueryCallback()
        aabb = b2AABB(
            lowerBound=self.toBoxCoords(x1,y2),
            upperBound=self.toBoxCoords(x2,y1),
        )
        self.world.QueryAABB(queryCallback, aabb)
        return queryCallback.objects

    @property
    def gravity(self):
        # gravité en m/s/s
        return self.world.gravity

    @gravity.setter
    def gravity(self, value):
        self.world.gravity = value

    def bbox(self, thing):
        return self.canvas.bbox(thing.item)

class ebContactListener(b2ContactListener):
    def __init__(self, contactManagement):
        b2ContactListener.__init__(self)
        self._contactManagement = contactManagement

    def BeginContact(self, contact):
        thingA = contact.fixtureA.body.userData
        thingB = contact.fixtureB.body.userData
        self._contactManagement(thingA, thingB, 'begin', contact)

    def EndContact(self, contact):
        thingA = contact.fixtureA.body.userData
        thingB = contact.fixtureB.body.userData
        self._contactManagement(thingA, thingB, 'end', contact)

    def PreSolve(self, contact, oldManifold):
        pass

    def PostSolve(self, contact, impulse):
        pass

class ebQueryCallback2(b2QueryCallback):
    def __init__(self, query):
        b2QueryCallback.__init__(self)
        self._query = query

    def ReportFixture(self, fixture):
        # get the associated thing
        thing = fixture.body.userData
        # continues the query if returns True
        return self._query(thing)

class ebQueryCallback(b2QueryCallback):
    def __init__(self):
        b2QueryCallback.__init__(self)
        self.objects = []

    def ReportFixture(self, fixture):
        # remember the associated thing
        self.objects.append(fixture.body.userData)
        # continues the query if returns True
        return True

class ebRayCastCallback(b2RayCastCallback):
    # travail en cours...
    def __init__(self, raycast):
        b2RayCastCallback.__init__(self)
        self.fixture = None
        self._raycast = raycast

    # Called for each fixture found in the query. You control how the ray proceeds
    # by returning a float that indicates the fractional length of the ray. By returning
    # 0, you set the ray length to zero. By returning the current fraction, you proceed
    # to find the closest point. By returning 1, you continue with the original ray
    # clipping.
    def ReportFixture(self, fixture, point, normal, fraction):
        self.fixture = fixture
        self.point  = b2Vec2(point)
        self.normal = b2Vec2(normal)
        # You will get this error: "TypeError: Swig director type mismatch in output value of type 'float32'"
        # without returning a value
        # get the associated thing
        thing = fixture.body.userData
        return self._raycast(thing, fraction)

