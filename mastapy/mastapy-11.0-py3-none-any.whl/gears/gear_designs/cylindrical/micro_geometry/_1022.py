'''_1022.py

CylindricalGearMeshMicroGeometryDutyCycle
'''


from typing import List

from mastapy.gears.rating.cylindrical import _422
from mastapy._internal import constructor, conversion
from mastapy.gears.ltca.cylindrical import _793
from mastapy.gears.analysis import _1130
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_MICRO_GEOMETRY_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearMeshMicroGeometryDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshMicroGeometryDutyCycle',)


class CylindricalGearMeshMicroGeometryDutyCycle(_1130.GearMeshDesignAnalysis):
    '''CylindricalGearMeshMicroGeometryDutyCycle

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_MICRO_GEOMETRY_DUTY_CYCLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshMicroGeometryDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cylindrical_gear_set_duty_cycle_rating(self) -> '_422.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'CylindricalGearSetDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_422.CylindricalGearSetDutyCycleRating)(self.wrapped.CylindricalGearSetDutyCycleRating) if self.wrapped.CylindricalGearSetDutyCycleRating else None

    @property
    def meshes_analysis(self) -> 'List[_793.CylindricalGearMeshLoadDistributionAnalysis]':
        '''List[CylindricalGearMeshLoadDistributionAnalysis]: 'MeshesAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesAnalysis, constructor.new(_793.CylindricalGearMeshLoadDistributionAnalysis))
        return value
