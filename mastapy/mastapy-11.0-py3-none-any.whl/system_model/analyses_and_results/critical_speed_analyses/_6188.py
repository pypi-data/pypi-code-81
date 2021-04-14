'''_6188.py

AssemblyCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2112, _2151
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6454, _6586
from mastapy.system_model.analyses_and_results.critical_speed_analyses import (
    _6189, _6191, _6194, _6200,
    _6201, _6203, _6208, _6212,
    _6224, _6226, _6228, _6232,
    _6238, _6239, _6240, _6247,
    _6254, _6257, _6258, _6259,
    _6261, _6264, _6268, _6269,
    _6270, _6279, _6272, _6274,
    _6278, _6284, _6286, _6290,
    _6293, _6296, _6301, _6304,
    _6308, _6311, _6181
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'AssemblyCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCriticalSpeedAnalysis',)


class AssemblyCriticalSpeedAnalysis(_6181.AbstractAssemblyCriticalSpeedAnalysis):
    '''AssemblyCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
    def assembly_load_case(self) -> '_6454.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6454.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_6189.BearingCriticalSpeedAnalysis]':
        '''List[BearingCriticalSpeedAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6189.BearingCriticalSpeedAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_6191.BeltDriveCriticalSpeedAnalysis]':
        '''List[BeltDriveCriticalSpeedAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6191.BeltDriveCriticalSpeedAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6194.BevelDifferentialGearSetCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCriticalSpeedAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6194.BevelDifferentialGearSetCriticalSpeedAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_6200.BoltCriticalSpeedAnalysis]':
        '''List[BoltCriticalSpeedAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6200.BoltCriticalSpeedAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_6201.BoltedJointCriticalSpeedAnalysis]':
        '''List[BoltedJointCriticalSpeedAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6201.BoltedJointCriticalSpeedAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_6203.ClutchCriticalSpeedAnalysis]':
        '''List[ClutchCriticalSpeedAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6203.ClutchCriticalSpeedAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_6208.ConceptCouplingCriticalSpeedAnalysis]':
        '''List[ConceptCouplingCriticalSpeedAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6208.ConceptCouplingCriticalSpeedAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6212.ConceptGearSetCriticalSpeedAnalysis]':
        '''List[ConceptGearSetCriticalSpeedAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6212.ConceptGearSetCriticalSpeedAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_6224.CVTCriticalSpeedAnalysis]':
        '''List[CVTCriticalSpeedAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6224.CVTCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6226.CycloidalAssemblyCriticalSpeedAnalysis]':
        '''List[CycloidalAssemblyCriticalSpeedAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6226.CycloidalAssemblyCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6228.CycloidalDiscCriticalSpeedAnalysis]':
        '''List[CycloidalDiscCriticalSpeedAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6228.CycloidalDiscCriticalSpeedAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6232.CylindricalGearSetCriticalSpeedAnalysis]':
        '''List[CylindricalGearSetCriticalSpeedAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6232.CylindricalGearSetCriticalSpeedAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6238.FaceGearSetCriticalSpeedAnalysis]':
        '''List[FaceGearSetCriticalSpeedAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6238.FaceGearSetCriticalSpeedAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_6239.FEPartCriticalSpeedAnalysis]':
        '''List[FEPartCriticalSpeedAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6239.FEPartCriticalSpeedAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6240.FlexiblePinAssemblyCriticalSpeedAnalysis]':
        '''List[FlexiblePinAssemblyCriticalSpeedAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6240.FlexiblePinAssemblyCriticalSpeedAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6247.HypoidGearSetCriticalSpeedAnalysis]':
        '''List[HypoidGearSetCriticalSpeedAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6247.HypoidGearSetCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6254.KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6254.KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6257.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6257.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_6258.MassDiscCriticalSpeedAnalysis]':
        '''List[MassDiscCriticalSpeedAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6258.MassDiscCriticalSpeedAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_6259.MeasurementComponentCriticalSpeedAnalysis]':
        '''List[MeasurementComponentCriticalSpeedAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6259.MeasurementComponentCriticalSpeedAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_6261.OilSealCriticalSpeedAnalysis]':
        '''List[OilSealCriticalSpeedAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6261.OilSealCriticalSpeedAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6264.PartToPartShearCouplingCriticalSpeedAnalysis]':
        '''List[PartToPartShearCouplingCriticalSpeedAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6264.PartToPartShearCouplingCriticalSpeedAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_6268.PlanetCarrierCriticalSpeedAnalysis]':
        '''List[PlanetCarrierCriticalSpeedAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6268.PlanetCarrierCriticalSpeedAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_6269.PointLoadCriticalSpeedAnalysis]':
        '''List[PointLoadCriticalSpeedAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6269.PointLoadCriticalSpeedAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_6270.PowerLoadCriticalSpeedAnalysis]':
        '''List[PowerLoadCriticalSpeedAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6270.PowerLoadCriticalSpeedAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6279.ShaftHubConnectionCriticalSpeedAnalysis]':
        '''List[ShaftHubConnectionCriticalSpeedAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6279.ShaftHubConnectionCriticalSpeedAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_6272.RingPinsCriticalSpeedAnalysis]':
        '''List[RingPinsCriticalSpeedAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6272.RingPinsCriticalSpeedAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6274.RollingRingAssemblyCriticalSpeedAnalysis]':
        '''List[RollingRingAssemblyCriticalSpeedAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6274.RollingRingAssemblyCriticalSpeedAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_6278.ShaftCriticalSpeedAnalysis]':
        '''List[ShaftCriticalSpeedAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6278.ShaftCriticalSpeedAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6284.SpiralBevelGearSetCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearSetCriticalSpeedAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6284.SpiralBevelGearSetCriticalSpeedAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_6286.SpringDamperCriticalSpeedAnalysis]':
        '''List[SpringDamperCriticalSpeedAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6286.SpringDamperCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6290.StraightBevelDiffGearSetCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearSetCriticalSpeedAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6290.StraightBevelDiffGearSetCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6293.StraightBevelGearSetCriticalSpeedAnalysis]':
        '''List[StraightBevelGearSetCriticalSpeedAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6293.StraightBevelGearSetCriticalSpeedAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_6296.SynchroniserCriticalSpeedAnalysis]':
        '''List[SynchroniserCriticalSpeedAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6296.SynchroniserCriticalSpeedAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_6301.TorqueConverterCriticalSpeedAnalysis]':
        '''List[TorqueConverterCriticalSpeedAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6301.TorqueConverterCriticalSpeedAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6304.UnbalancedMassCriticalSpeedAnalysis]':
        '''List[UnbalancedMassCriticalSpeedAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6304.UnbalancedMassCriticalSpeedAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6308.WormGearSetCriticalSpeedAnalysis]':
        '''List[WormGearSetCriticalSpeedAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6308.WormGearSetCriticalSpeedAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6311.ZerolBevelGearSetCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearSetCriticalSpeedAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6311.ZerolBevelGearSetCriticalSpeedAnalysis))
        return value
