'''_3436.py

AssemblyStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2112, _2151
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6454, _6586
from mastapy.system_model.analyses_and_results.stability_analyses import (
    _3437, _3439, _3441, _3449,
    _3448, _3452, _3457, _3459,
    _3472, _3473, _3476, _3478,
    _3484, _3486, _3487, _3493,
    _3500, _3503, _3505, _3506,
    _3508, _3512, _3515, _3516,
    _3517, _3525, _3519, _3521,
    _3526, _3530, _3534, _3538,
    _3541, _3548, _3551, _3553,
    _3556, _3559, _3429
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'AssemblyStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyStabilityAnalysis',)


class AssemblyStabilityAnalysis(_3429.AbstractAssemblyStabilityAnalysis):
    '''AssemblyStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyStabilityAnalysis.TYPE'):
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
    def bearings(self) -> 'List[_3437.BearingStabilityAnalysis]':
        '''List[BearingStabilityAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3437.BearingStabilityAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_3439.BeltDriveStabilityAnalysis]':
        '''List[BeltDriveStabilityAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3439.BeltDriveStabilityAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3441.BevelDifferentialGearSetStabilityAnalysis]':
        '''List[BevelDifferentialGearSetStabilityAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3441.BevelDifferentialGearSetStabilityAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_3449.BoltStabilityAnalysis]':
        '''List[BoltStabilityAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3449.BoltStabilityAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_3448.BoltedJointStabilityAnalysis]':
        '''List[BoltedJointStabilityAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3448.BoltedJointStabilityAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_3452.ClutchStabilityAnalysis]':
        '''List[ClutchStabilityAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3452.ClutchStabilityAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_3457.ConceptCouplingStabilityAnalysis]':
        '''List[ConceptCouplingStabilityAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3457.ConceptCouplingStabilityAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3459.ConceptGearSetStabilityAnalysis]':
        '''List[ConceptGearSetStabilityAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3459.ConceptGearSetStabilityAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_3472.CVTStabilityAnalysis]':
        '''List[CVTStabilityAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3472.CVTStabilityAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3473.CycloidalAssemblyStabilityAnalysis]':
        '''List[CycloidalAssemblyStabilityAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3473.CycloidalAssemblyStabilityAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3476.CycloidalDiscStabilityAnalysis]':
        '''List[CycloidalDiscStabilityAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3476.CycloidalDiscStabilityAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3478.CylindricalGearSetStabilityAnalysis]':
        '''List[CylindricalGearSetStabilityAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3478.CylindricalGearSetStabilityAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3484.FaceGearSetStabilityAnalysis]':
        '''List[FaceGearSetStabilityAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3484.FaceGearSetStabilityAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_3486.FEPartStabilityAnalysis]':
        '''List[FEPartStabilityAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3486.FEPartStabilityAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3487.FlexiblePinAssemblyStabilityAnalysis]':
        '''List[FlexiblePinAssemblyStabilityAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3487.FlexiblePinAssemblyStabilityAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3493.HypoidGearSetStabilityAnalysis]':
        '''List[HypoidGearSetStabilityAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3493.HypoidGearSetStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3500.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3500.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3503.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3503.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_3505.MassDiscStabilityAnalysis]':
        '''List[MassDiscStabilityAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3505.MassDiscStabilityAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_3506.MeasurementComponentStabilityAnalysis]':
        '''List[MeasurementComponentStabilityAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3506.MeasurementComponentStabilityAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_3508.OilSealStabilityAnalysis]':
        '''List[OilSealStabilityAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3508.OilSealStabilityAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3512.PartToPartShearCouplingStabilityAnalysis]':
        '''List[PartToPartShearCouplingStabilityAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3512.PartToPartShearCouplingStabilityAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_3515.PlanetCarrierStabilityAnalysis]':
        '''List[PlanetCarrierStabilityAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3515.PlanetCarrierStabilityAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_3516.PointLoadStabilityAnalysis]':
        '''List[PointLoadStabilityAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3516.PointLoadStabilityAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_3517.PowerLoadStabilityAnalysis]':
        '''List[PowerLoadStabilityAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3517.PowerLoadStabilityAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3525.ShaftHubConnectionStabilityAnalysis]':
        '''List[ShaftHubConnectionStabilityAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3525.ShaftHubConnectionStabilityAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_3519.RingPinsStabilityAnalysis]':
        '''List[RingPinsStabilityAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3519.RingPinsStabilityAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3521.RollingRingAssemblyStabilityAnalysis]':
        '''List[RollingRingAssemblyStabilityAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3521.RollingRingAssemblyStabilityAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_3526.ShaftStabilityAnalysis]':
        '''List[ShaftStabilityAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3526.ShaftStabilityAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3530.SpiralBevelGearSetStabilityAnalysis]':
        '''List[SpiralBevelGearSetStabilityAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3530.SpiralBevelGearSetStabilityAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_3534.SpringDamperStabilityAnalysis]':
        '''List[SpringDamperStabilityAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3534.SpringDamperStabilityAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3538.StraightBevelDiffGearSetStabilityAnalysis]':
        '''List[StraightBevelDiffGearSetStabilityAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3538.StraightBevelDiffGearSetStabilityAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3541.StraightBevelGearSetStabilityAnalysis]':
        '''List[StraightBevelGearSetStabilityAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3541.StraightBevelGearSetStabilityAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_3548.SynchroniserStabilityAnalysis]':
        '''List[SynchroniserStabilityAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3548.SynchroniserStabilityAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_3551.TorqueConverterStabilityAnalysis]':
        '''List[TorqueConverterStabilityAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3551.TorqueConverterStabilityAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3553.UnbalancedMassStabilityAnalysis]':
        '''List[UnbalancedMassStabilityAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3553.UnbalancedMassStabilityAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3556.WormGearSetStabilityAnalysis]':
        '''List[WormGearSetStabilityAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3556.WormGearSetStabilityAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3559.ZerolBevelGearSetStabilityAnalysis]':
        '''List[ZerolBevelGearSetStabilityAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3559.ZerolBevelGearSetStabilityAnalysis))
        return value
