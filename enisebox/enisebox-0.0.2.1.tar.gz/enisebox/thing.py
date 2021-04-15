from Box2D import *
from math import pi

class ebThing():
    def __init__(self, *args, **kwargs):
        pass

    def ApplyLinearImpulse(self, a, b):
        body = self.body
        body.ApplyLinearImpulse(
                impulse=b2Vec2(a,-b),
                point=body.position,
                wake=True,
        )

    def ApplyAngularImpulse(self, imp):
        body = self.body
        self.body.ApplyAngularImpulse(
                impulse=imp,
                wake=True,
        )

    def ApplyForce(self, a, b):
        body = self.body
        body.ApplyForce(
                force=b2Vec2(a,-b),
                point=body.position,
                wake=True,
        )

    def ApplyTorque(self, torque):
        body = self.body
        body.ApplyTorque(
                torque=torque,
                wake=True,
        )

    @property
    def boxCenter(self):
        # centre de gravité dans le repère de la boîte
        return self.body.worldCenter

    @property
    def canvasCenter(self):
        # centre de gravité dans le repère du canvas
        return self.box.toCanvasCoords(*self.body.worldCenter)

    @property
    def position(self):
        # centre géométrique dans le repère de la boîte
        return self.body.position

    @position.setter
    def position(self, pos):
        # centre géométrique dans le repère de la boîte
        self.body.position = pos

    @property
    def canvasPosition(self):
        # centre géométrique dans le repère du canvas
        return self.box.toCanvasCoords(*self.body.position)

    @canvasPosition.setter
    def canvasPosition(self, pos):
        # centre géométrique dans le repère du canvas
        self.body.position = self.box.toBoxCoords(*pos)

    @property
    def angle(self):
        # angle en radian
        return self.body.transform.angle

    @angle.setter
    def angle(self, value):
        self.body.transform.angle = value

    @property
    def angularDamping(self):
        return self.body.angularDamping

    @angularDamping.setter
    def angularDamping(self, damping):
        self.body.angularDamping = damping

    @property
    def linearDamping(self):
        return self.body.linearDamping

    @linearDamping.setter
    def linearDamping(self, damping):
        self.body.linearDamping = damping

    @property
    def angularVelocity(self):
        return self.body.angularVelocity

    @angularVelocity.setter
    def angularVelocity(self, velocity):
        self.body.angularVelocity = velocity

    @property
    def linearVelocity(self):
        return self.body.linearVelocity

    @linearVelocity.setter
    def linearVelocity(self, velocity):
        v = (velocity[0],-velocity[1])
        self.body.linearVelocity = v

    @property
    def groupIndex(self):
        return self.body.fixtures[0].filterData.groupIndex

    @groupIndex.setter
    def groupIndex(self, index):
        self.body.fixtures[0].filterData.groupIndex = index

    @property
    def categoryBits(self):
        return self.body.fixtures[0].filterData.categoryBits

    @categoryBits.setter
    def categoryBits(self, bits):
        self.body.fixtures[0].filterData.categoryBits = bits

    @property
    def maskBits(self):
        return self.body.fixtures[0].filterData.maskBits

    @maskBits.setter
    def maskBits(self, bits):
        self.body.fixtures[0].filterData.maskBits = bits

    @property
    def fixedRotation(self):
        return self.body.fixedRotation

    @fixedRotation.setter
    def fixedRotation(self, value):
        self.body.fixedRotation = value

    @property
    def bullet(self):
        return self.body.bullet

    @bullet.setter
    def bullet(self, value):
        self.body.bullet = value
