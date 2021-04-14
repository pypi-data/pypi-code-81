'''_3307.py

AssemblyCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2112, _2151
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3174
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3308, _3310, _3313, _3319,
    _3320, _3321, _3326, _3331,
    _3341, _3343, _3345, _3349,
    _3355, _3356, _3357, _3364,
    _3371, _3374, _3375, _3376,
    _3378, _3380, _3385, _3386,
    _3387, _3396, _3389, _3391,
    _3395, _3401, _3402, _3407,
    _3410, _3413, _3417, _3421,
    _3425, _3428, _3300
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'AssemblyCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSteadyStateSynchronousResponse',)


class AssemblyCompoundSteadyStateSynchronousResponse(_3300.AbstractAssemblyCompoundSteadyStateSynchronousResponse):
    '''AssemblyCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2112.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2112.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2112.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2112.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3174.AssemblySteadyStateSynchronousResponse]':
        '''List[AssemblySteadyStateSynchronousResponse]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3174.AssemblySteadyStateSynchronousResponse))
        return value

    @property
    def bearings(self) -> 'List[_3308.BearingCompoundSteadyStateSynchronousResponse]':
        '''List[BearingCompoundSteadyStateSynchronousResponse]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3308.BearingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def belt_drives(self) -> 'List[_3310.BeltDriveCompoundSteadyStateSynchronousResponse]':
        '''List[BeltDriveCompoundSteadyStateSynchronousResponse]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3310.BeltDriveCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3313.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3313.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bolts(self) -> 'List[_3319.BoltCompoundSteadyStateSynchronousResponse]':
        '''List[BoltCompoundSteadyStateSynchronousResponse]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3319.BoltCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bolted_joints(self) -> 'List[_3320.BoltedJointCompoundSteadyStateSynchronousResponse]':
        '''List[BoltedJointCompoundSteadyStateSynchronousResponse]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3320.BoltedJointCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def clutches(self) -> 'List[_3321.ClutchCompoundSteadyStateSynchronousResponse]':
        '''List[ClutchCompoundSteadyStateSynchronousResponse]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3321.ClutchCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def concept_couplings(self) -> 'List[_3326.ConceptCouplingCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptCouplingCompoundSteadyStateSynchronousResponse]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3326.ConceptCouplingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3331.ConceptGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptGearSetCompoundSteadyStateSynchronousResponse]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3331.ConceptGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cv_ts(self) -> 'List[_3341.CVTCompoundSteadyStateSynchronousResponse]':
        '''List[CVTCompoundSteadyStateSynchronousResponse]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3341.CVTCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3343.CycloidalAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[CycloidalAssemblyCompoundSteadyStateSynchronousResponse]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3343.CycloidalAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3345.CycloidalDiscCompoundSteadyStateSynchronousResponse]':
        '''List[CycloidalDiscCompoundSteadyStateSynchronousResponse]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3345.CycloidalDiscCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3349.CylindricalGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[CylindricalGearSetCompoundSteadyStateSynchronousResponse]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3349.CylindricalGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3355.FaceGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[FaceGearSetCompoundSteadyStateSynchronousResponse]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3355.FaceGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def fe_parts(self) -> 'List[_3356.FEPartCompoundSteadyStateSynchronousResponse]':
        '''List[FEPartCompoundSteadyStateSynchronousResponse]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3356.FEPartCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3357.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3357.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3364.HypoidGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[HypoidGearSetCompoundSteadyStateSynchronousResponse]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3364.HypoidGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3371.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3371.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3374.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3374.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def mass_discs(self) -> 'List[_3375.MassDiscCompoundSteadyStateSynchronousResponse]':
        '''List[MassDiscCompoundSteadyStateSynchronousResponse]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3375.MassDiscCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def measurement_components(self) -> 'List[_3376.MeasurementComponentCompoundSteadyStateSynchronousResponse]':
        '''List[MeasurementComponentCompoundSteadyStateSynchronousResponse]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3376.MeasurementComponentCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def oil_seals(self) -> 'List[_3378.OilSealCompoundSteadyStateSynchronousResponse]':
        '''List[OilSealCompoundSteadyStateSynchronousResponse]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3378.OilSealCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3380.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse]':
        '''List[PartToPartShearCouplingCompoundSteadyStateSynchronousResponse]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3380.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def planet_carriers(self) -> 'List[_3385.PlanetCarrierCompoundSteadyStateSynchronousResponse]':
        '''List[PlanetCarrierCompoundSteadyStateSynchronousResponse]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3385.PlanetCarrierCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def point_loads(self) -> 'List[_3386.PointLoadCompoundSteadyStateSynchronousResponse]':
        '''List[PointLoadCompoundSteadyStateSynchronousResponse]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3386.PointLoadCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def power_loads(self) -> 'List[_3387.PowerLoadCompoundSteadyStateSynchronousResponse]':
        '''List[PowerLoadCompoundSteadyStateSynchronousResponse]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3387.PowerLoadCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3396.ShaftHubConnectionCompoundSteadyStateSynchronousResponse]':
        '''List[ShaftHubConnectionCompoundSteadyStateSynchronousResponse]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3396.ShaftHubConnectionCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def ring_pins(self) -> 'List[_3389.RingPinsCompoundSteadyStateSynchronousResponse]':
        '''List[RingPinsCompoundSteadyStateSynchronousResponse]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3389.RingPinsCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3391.RollingRingAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[RollingRingAssemblyCompoundSteadyStateSynchronousResponse]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3391.RollingRingAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def shafts(self) -> 'List[_3395.ShaftCompoundSteadyStateSynchronousResponse]':
        '''List[ShaftCompoundSteadyStateSynchronousResponse]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3395.ShaftCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3401.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[SpiralBevelGearSetCompoundSteadyStateSynchronousResponse]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3401.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def spring_dampers(self) -> 'List[_3402.SpringDamperCompoundSteadyStateSynchronousResponse]':
        '''List[SpringDamperCompoundSteadyStateSynchronousResponse]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3402.SpringDamperCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3407.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3407.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3410.StraightBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelGearSetCompoundSteadyStateSynchronousResponse]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3410.StraightBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def synchronisers(self) -> 'List[_3413.SynchroniserCompoundSteadyStateSynchronousResponse]':
        '''List[SynchroniserCompoundSteadyStateSynchronousResponse]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3413.SynchroniserCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def torque_converters(self) -> 'List[_3417.TorqueConverterCompoundSteadyStateSynchronousResponse]':
        '''List[TorqueConverterCompoundSteadyStateSynchronousResponse]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3417.TorqueConverterCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3421.UnbalancedMassCompoundSteadyStateSynchronousResponse]':
        '''List[UnbalancedMassCompoundSteadyStateSynchronousResponse]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3421.UnbalancedMassCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3425.WormGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[WormGearSetCompoundSteadyStateSynchronousResponse]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3425.WormGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3428.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSetCompoundSteadyStateSynchronousResponse]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3428.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3174.AssemblySteadyStateSynchronousResponse]':
        '''List[AssemblySteadyStateSynchronousResponse]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3174.AssemblySteadyStateSynchronousResponse))
        return value
