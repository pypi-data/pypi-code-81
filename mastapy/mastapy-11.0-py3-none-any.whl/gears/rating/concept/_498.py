'''_498.py

ConceptGearMeshRating
'''


from typing import List

from mastapy.gears.gear_designs.concept import _1088
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.concept import _499
from mastapy.gears.rating import _321
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Concept', 'ConceptGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshRating',)


class ConceptGearMeshRating(_321.GearMeshRating):
    '''ConceptGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def concept_gear_mesh(self) -> '_1088.ConceptGearMeshDesign':
        '''ConceptGearMeshDesign: 'ConceptGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1088.ConceptGearMeshDesign)(self.wrapped.ConceptGearMesh) if self.wrapped.ConceptGearMesh else None

    @property
    def concept_gear_ratings(self) -> 'List[_499.ConceptGearRating]':
        '''List[ConceptGearRating]: 'ConceptGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearRatings, constructor.new(_499.ConceptGearRating))
        return value
