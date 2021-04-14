'''_921.py

FaceGearMeshDesign
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.face import _925, _919
from mastapy.gears.gear_designs import _879
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Face', 'FaceGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshDesign',)


class FaceGearMeshDesign(_879.GearMeshDesign):
    '''FaceGearMeshDesign

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def working_normal_pressure_angle(self) -> 'float':
        '''float: 'WorkingNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorkingNormalPressureAngle

    @property
    def offset(self) -> 'float':
        '''float: 'Offset' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Offset

    @property
    def face_gear_set(self) -> '_925.FaceGearSetDesign':
        '''FaceGearSetDesign: 'FaceGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_925.FaceGearSetDesign)(self.wrapped.FaceGearSet) if self.wrapped.FaceGearSet else None

    @property
    def face_gears(self) -> 'List[_919.FaceGearDesign]':
        '''List[FaceGearDesign]: 'FaceGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGears, constructor.new(_919.FaceGearDesign))
        return value
