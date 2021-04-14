'''_5341.py

AssemblyHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model import _2112, _2151
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6454, _6586
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
    _5342, _5344, _5347, _5354,
    _5353, _5357, _5362, _5365,
    _5375, _5377, _5379, _5383,
    _5389, _5390, _5391, _5399,
    _5406, _5409, _5410, _5411,
    _5413, _5417, _5420, _5421,
    _5422, _5431, _5424, _5426,
    _5430, _5436, _5439, _5442,
    _5445, _5449, _5453, _5456,
    _5460, _5463, _5334
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'AssemblyHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyHarmonicAnalysisOfSingleExcitation',)


class AssemblyHarmonicAnalysisOfSingleExcitation(_5334.AbstractAssemblyHarmonicAnalysisOfSingleExcitation):
    '''AssemblyHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyHarmonicAnalysisOfSingleExcitation.TYPE'):
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
    def bearings(self) -> 'List[_5342.BearingHarmonicAnalysisOfSingleExcitation]':
        '''List[BearingHarmonicAnalysisOfSingleExcitation]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5342.BearingHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def belt_drives(self) -> 'List[_5344.BeltDriveHarmonicAnalysisOfSingleExcitation]':
        '''List[BeltDriveHarmonicAnalysisOfSingleExcitation]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5344.BeltDriveHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5347.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5347.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def bolts(self) -> 'List[_5354.BoltHarmonicAnalysisOfSingleExcitation]':
        '''List[BoltHarmonicAnalysisOfSingleExcitation]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5354.BoltHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def bolted_joints(self) -> 'List[_5353.BoltedJointHarmonicAnalysisOfSingleExcitation]':
        '''List[BoltedJointHarmonicAnalysisOfSingleExcitation]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5353.BoltedJointHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def clutches(self) -> 'List[_5357.ClutchHarmonicAnalysisOfSingleExcitation]':
        '''List[ClutchHarmonicAnalysisOfSingleExcitation]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5357.ClutchHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def concept_couplings(self) -> 'List[_5362.ConceptCouplingHarmonicAnalysisOfSingleExcitation]':
        '''List[ConceptCouplingHarmonicAnalysisOfSingleExcitation]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5362.ConceptCouplingHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5365.ConceptGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[ConceptGearSetHarmonicAnalysisOfSingleExcitation]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5365.ConceptGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def cv_ts(self) -> 'List[_5375.CVTHarmonicAnalysisOfSingleExcitation]':
        '''List[CVTHarmonicAnalysisOfSingleExcitation]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5375.CVTHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5377.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation]':
        '''List[CycloidalAssemblyHarmonicAnalysisOfSingleExcitation]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_5377.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5379.CycloidalDiscHarmonicAnalysisOfSingleExcitation]':
        '''List[CycloidalDiscHarmonicAnalysisOfSingleExcitation]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_5379.CycloidalDiscHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5383.CylindricalGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[CylindricalGearSetHarmonicAnalysisOfSingleExcitation]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5383.CylindricalGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5389.FaceGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearSetHarmonicAnalysisOfSingleExcitation]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5389.FaceGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def fe_parts(self) -> 'List[_5390.FEPartHarmonicAnalysisOfSingleExcitation]':
        '''List[FEPartHarmonicAnalysisOfSingleExcitation]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_5390.FEPartHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5391.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation]':
        '''List[FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5391.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5399.HypoidGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[HypoidGearSetHarmonicAnalysisOfSingleExcitation]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5399.HypoidGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5406.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5406.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5409.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5409.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def mass_discs(self) -> 'List[_5410.MassDiscHarmonicAnalysisOfSingleExcitation]':
        '''List[MassDiscHarmonicAnalysisOfSingleExcitation]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5410.MassDiscHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def measurement_components(self) -> 'List[_5411.MeasurementComponentHarmonicAnalysisOfSingleExcitation]':
        '''List[MeasurementComponentHarmonicAnalysisOfSingleExcitation]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5411.MeasurementComponentHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def oil_seals(self) -> 'List[_5413.OilSealHarmonicAnalysisOfSingleExcitation]':
        '''List[OilSealHarmonicAnalysisOfSingleExcitation]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5413.OilSealHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5417.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation]':
        '''List[PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5417.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def planet_carriers(self) -> 'List[_5420.PlanetCarrierHarmonicAnalysisOfSingleExcitation]':
        '''List[PlanetCarrierHarmonicAnalysisOfSingleExcitation]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5420.PlanetCarrierHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def point_loads(self) -> 'List[_5421.PointLoadHarmonicAnalysisOfSingleExcitation]':
        '''List[PointLoadHarmonicAnalysisOfSingleExcitation]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5421.PointLoadHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def power_loads(self) -> 'List[_5422.PowerLoadHarmonicAnalysisOfSingleExcitation]':
        '''List[PowerLoadHarmonicAnalysisOfSingleExcitation]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5422.PowerLoadHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5431.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]':
        '''List[ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5431.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def ring_pins(self) -> 'List[_5424.RingPinsHarmonicAnalysisOfSingleExcitation]':
        '''List[RingPinsHarmonicAnalysisOfSingleExcitation]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5424.RingPinsHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5426.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation]':
        '''List[RollingRingAssemblyHarmonicAnalysisOfSingleExcitation]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5426.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def shafts(self) -> 'List[_5430.ShaftHarmonicAnalysisOfSingleExcitation]':
        '''List[ShaftHarmonicAnalysisOfSingleExcitation]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5430.ShaftHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5436.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5436.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def spring_dampers(self) -> 'List[_5439.SpringDamperHarmonicAnalysisOfSingleExcitation]':
        '''List[SpringDamperHarmonicAnalysisOfSingleExcitation]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5439.SpringDamperHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5442.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5442.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5445.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5445.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def synchronisers(self) -> 'List[_5449.SynchroniserHarmonicAnalysisOfSingleExcitation]':
        '''List[SynchroniserHarmonicAnalysisOfSingleExcitation]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5449.SynchroniserHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def torque_converters(self) -> 'List[_5453.TorqueConverterHarmonicAnalysisOfSingleExcitation]':
        '''List[TorqueConverterHarmonicAnalysisOfSingleExcitation]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5453.TorqueConverterHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5456.UnbalancedMassHarmonicAnalysisOfSingleExcitation]':
        '''List[UnbalancedMassHarmonicAnalysisOfSingleExcitation]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5456.UnbalancedMassHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5460.WormGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[WormGearSetHarmonicAnalysisOfSingleExcitation]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5460.WormGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5463.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5463.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value
