'''_5667.py

GearMeshExcitationDetail
'''


from mastapy.system_model.analyses_and_results.system_deflections import (
    _2425, _2362, _2369, _2374,
    _2388, _2392, _2407, _2408,
    _2409, _2420, _2429, _2434,
    _2437, _2440, _2473, _2479,
    _2482, _2502, _2505
)
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6611
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5619, _5594
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'GearMeshExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshExcitationDetail',)


class GearMeshExcitationDetail(_5594.AbstractPeriodicExcitationDetail):
    '''GearMeshExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_mesh(self) -> '_2425.GearMeshSystemDeflection':
        '''GearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2425.GearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to GearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_agma_gleason_conical_gear_mesh_system_deflection(self) -> '_2362.AGMAGleasonConicalGearMeshSystemDeflection':
        '''AGMAGleasonConicalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2362.AGMAGleasonConicalGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to AGMAGleasonConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_bevel_differential_gear_mesh_system_deflection(self) -> '_2369.BevelDifferentialGearMeshSystemDeflection':
        '''BevelDifferentialGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2369.BevelDifferentialGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to BevelDifferentialGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_bevel_gear_mesh_system_deflection(self) -> '_2374.BevelGearMeshSystemDeflection':
        '''BevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2374.BevelGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to BevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_concept_gear_mesh_system_deflection(self) -> '_2388.ConceptGearMeshSystemDeflection':
        '''ConceptGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2388.ConceptGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to ConceptGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_conical_gear_mesh_system_deflection(self) -> '_2392.ConicalGearMeshSystemDeflection':
        '''ConicalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2392.ConicalGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to ConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_cylindrical_gear_mesh_system_deflection(self) -> '_2407.CylindricalGearMeshSystemDeflection':
        '''CylindricalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2407.CylindricalGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to CylindricalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_cylindrical_gear_mesh_system_deflection_timestep(self) -> '_2408.CylindricalGearMeshSystemDeflectionTimestep':
        '''CylindricalGearMeshSystemDeflectionTimestep: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2408.CylindricalGearMeshSystemDeflectionTimestep.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to CylindricalGearMeshSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_cylindrical_gear_mesh_system_deflection_with_ltca_results(self) -> '_2409.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        '''CylindricalGearMeshSystemDeflectionWithLTCAResults: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2409.CylindricalGearMeshSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to CylindricalGearMeshSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_face_gear_mesh_system_deflection(self) -> '_2420.FaceGearMeshSystemDeflection':
        '''FaceGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2420.FaceGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to FaceGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_hypoid_gear_mesh_system_deflection(self) -> '_2429.HypoidGearMeshSystemDeflection':
        '''HypoidGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2429.HypoidGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to HypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(self) -> '_2434.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidConicalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2434.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to KlingelnbergCycloPalloidConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(self) -> '_2437.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2437.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(self) -> '_2440.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2440.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_spiral_bevel_gear_mesh_system_deflection(self) -> '_2473.SpiralBevelGearMeshSystemDeflection':
        '''SpiralBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2473.SpiralBevelGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to SpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_straight_bevel_diff_gear_mesh_system_deflection(self) -> '_2479.StraightBevelDiffGearMeshSystemDeflection':
        '''StraightBevelDiffGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2479.StraightBevelDiffGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to StraightBevelDiffGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_straight_bevel_gear_mesh_system_deflection(self) -> '_2482.StraightBevelGearMeshSystemDeflection':
        '''StraightBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2482.StraightBevelGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to StraightBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_worm_gear_mesh_system_deflection(self) -> '_2502.WormGearMeshSystemDeflection':
        '''WormGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2502.WormGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to WormGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_zerol_bevel_gear_mesh_system_deflection(self) -> '_2505.ZerolBevelGearMeshSystemDeflection':
        '''ZerolBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2505.ZerolBevelGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to ZerolBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMesh.__class__)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    def get_compliance_and_force_data(self, excitation_type: '_6611.TEExcitationType') -> '_5619.ComplianceAndForceData':
        ''' 'GetComplianceAndForceData' is the original name of this method.

        Args:
            excitation_type (mastapy.system_model.analyses_and_results.static_loads.TEExcitationType)

        Returns:
            mastapy.system_model.analyses_and_results.harmonic_analyses.ComplianceAndForceData
        '''

        excitation_type = conversion.mp_to_pn_enum(excitation_type)
        method_result = self.wrapped.GetComplianceAndForceData(excitation_type)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
