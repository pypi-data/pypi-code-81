'''_923.py

FaceGearMicroGeometry
'''


from mastapy.gears.gear_designs.face import _919, _924, _927
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1023
from mastapy.gears.analysis import _1129
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Face', 'FaceGearMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMicroGeometry',)


class FaceGearMicroGeometry(_1129.GearImplementationDetail):
    '''FaceGearMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def face_gear(self) -> '_919.FaceGearDesign':
        '''FaceGearDesign: 'FaceGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _919.FaceGearDesign.TYPE not in self.wrapped.FaceGear.__class__.__mro__:
            raise CastException('Failed to cast face_gear to FaceGearDesign. Expected: {}.'.format(self.wrapped.FaceGear.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FaceGear.__class__)(self.wrapped.FaceGear) if self.wrapped.FaceGear else None

    @property
    def micro_geometry(self) -> '_1023.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'MicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1023.CylindricalGearMicroGeometry)(self.wrapped.MicroGeometry) if self.wrapped.MicroGeometry else None
