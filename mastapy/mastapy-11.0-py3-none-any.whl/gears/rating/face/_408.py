'''_408.py

FaceGearMeshRating
'''


from typing import List

from mastapy.gears import _287
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.load_case.face import _817
from mastapy.gears.rating.face import _411, _409
from mastapy.gears.rating.cylindrical.iso6336 import _469, _471
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.face import _921
from mastapy.gears.rating import _321
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Face', 'FaceGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshRating',)


class FaceGearMeshRating(_321.GearMeshRating):
    '''FaceGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_flank(self) -> '_287.GearFlanks':
        '''GearFlanks: 'ActiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ActiveFlank)
        return constructor.new(_287.GearFlanks)(value) if value else None

    @property
    def mesh_load_case(self) -> '_817.FaceMeshLoadCase':
        '''FaceMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_817.FaceMeshLoadCase)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase else None

    @property
    def gear_set_rating(self) -> '_411.FaceGearSetRating':
        '''FaceGearSetRating: 'GearSetRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_411.FaceGearSetRating)(self.wrapped.GearSetRating) if self.wrapped.GearSetRating else None

    @property
    def mesh_single_flank_rating(self) -> '_469.ISO63362006MeshSingleFlankRating':
        '''ISO63362006MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _469.ISO63362006MeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO63362006MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def face_gear_mesh(self) -> '_921.FaceGearMeshDesign':
        '''FaceGearMeshDesign: 'FaceGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_921.FaceGearMeshDesign)(self.wrapped.FaceGearMesh) if self.wrapped.FaceGearMesh else None

    @property
    def face_gear_ratings(self) -> 'List[_409.FaceGearRating]':
        '''List[FaceGearRating]: 'FaceGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearRatings, constructor.new(_409.FaceGearRating))
        return value
