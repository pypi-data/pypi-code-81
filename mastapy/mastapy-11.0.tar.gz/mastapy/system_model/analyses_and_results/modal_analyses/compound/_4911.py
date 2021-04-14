'''_4911.py

AssemblyCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2112, _2151
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses import _4758
from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
    _4912, _4914, _4917, _4923,
    _4924, _4925, _4930, _4935,
    _4945, _4947, _4949, _4953,
    _4959, _4960, _4961, _4968,
    _4975, _4978, _4979, _4980,
    _4982, _4984, _4989, _4990,
    _4991, _5000, _4993, _4995,
    _4999, _5005, _5006, _5011,
    _5014, _5017, _5021, _5025,
    _5029, _5032, _4904
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'AssemblyCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysis',)


class AssemblyCompoundModalAnalysis(_4904.AbstractAssemblyCompoundModalAnalysis):
    '''AssemblyCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysis.TYPE'):
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
    def assembly_analysis_cases_ready(self) -> 'List[_4758.AssemblyModalAnalysis]':
        '''List[AssemblyModalAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4758.AssemblyModalAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_4912.BearingCompoundModalAnalysis]':
        '''List[BearingCompoundModalAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4912.BearingCompoundModalAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_4914.BeltDriveCompoundModalAnalysis]':
        '''List[BeltDriveCompoundModalAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4914.BeltDriveCompoundModalAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4917.BevelDifferentialGearSetCompoundModalAnalysis]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4917.BevelDifferentialGearSetCompoundModalAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_4923.BoltCompoundModalAnalysis]':
        '''List[BoltCompoundModalAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4923.BoltCompoundModalAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_4924.BoltedJointCompoundModalAnalysis]':
        '''List[BoltedJointCompoundModalAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4924.BoltedJointCompoundModalAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_4925.ClutchCompoundModalAnalysis]':
        '''List[ClutchCompoundModalAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4925.ClutchCompoundModalAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_4930.ConceptCouplingCompoundModalAnalysis]':
        '''List[ConceptCouplingCompoundModalAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4930.ConceptCouplingCompoundModalAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4935.ConceptGearSetCompoundModalAnalysis]':
        '''List[ConceptGearSetCompoundModalAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4935.ConceptGearSetCompoundModalAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_4945.CVTCompoundModalAnalysis]':
        '''List[CVTCompoundModalAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4945.CVTCompoundModalAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_4947.CycloidalAssemblyCompoundModalAnalysis]':
        '''List[CycloidalAssemblyCompoundModalAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_4947.CycloidalAssemblyCompoundModalAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_4949.CycloidalDiscCompoundModalAnalysis]':
        '''List[CycloidalDiscCompoundModalAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_4949.CycloidalDiscCompoundModalAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4953.CylindricalGearSetCompoundModalAnalysis]':
        '''List[CylindricalGearSetCompoundModalAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4953.CylindricalGearSetCompoundModalAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4959.FaceGearSetCompoundModalAnalysis]':
        '''List[FaceGearSetCompoundModalAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4959.FaceGearSetCompoundModalAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_4960.FEPartCompoundModalAnalysis]':
        '''List[FEPartCompoundModalAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_4960.FEPartCompoundModalAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4961.FlexiblePinAssemblyCompoundModalAnalysis]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4961.FlexiblePinAssemblyCompoundModalAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4968.HypoidGearSetCompoundModalAnalysis]':
        '''List[HypoidGearSetCompoundModalAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4968.HypoidGearSetCompoundModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4975.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4975.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4978.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4978.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_4979.MassDiscCompoundModalAnalysis]':
        '''List[MassDiscCompoundModalAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4979.MassDiscCompoundModalAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_4980.MeasurementComponentCompoundModalAnalysis]':
        '''List[MeasurementComponentCompoundModalAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4980.MeasurementComponentCompoundModalAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_4982.OilSealCompoundModalAnalysis]':
        '''List[OilSealCompoundModalAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4982.OilSealCompoundModalAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4984.PartToPartShearCouplingCompoundModalAnalysis]':
        '''List[PartToPartShearCouplingCompoundModalAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4984.PartToPartShearCouplingCompoundModalAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_4989.PlanetCarrierCompoundModalAnalysis]':
        '''List[PlanetCarrierCompoundModalAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4989.PlanetCarrierCompoundModalAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_4990.PointLoadCompoundModalAnalysis]':
        '''List[PointLoadCompoundModalAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4990.PointLoadCompoundModalAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_4991.PowerLoadCompoundModalAnalysis]':
        '''List[PowerLoadCompoundModalAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4991.PowerLoadCompoundModalAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5000.ShaftHubConnectionCompoundModalAnalysis]':
        '''List[ShaftHubConnectionCompoundModalAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5000.ShaftHubConnectionCompoundModalAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_4993.RingPinsCompoundModalAnalysis]':
        '''List[RingPinsCompoundModalAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_4993.RingPinsCompoundModalAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4995.RollingRingAssemblyCompoundModalAnalysis]':
        '''List[RollingRingAssemblyCompoundModalAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4995.RollingRingAssemblyCompoundModalAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_4999.ShaftCompoundModalAnalysis]':
        '''List[ShaftCompoundModalAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4999.ShaftCompoundModalAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5005.SpiralBevelGearSetCompoundModalAnalysis]':
        '''List[SpiralBevelGearSetCompoundModalAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5005.SpiralBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5006.SpringDamperCompoundModalAnalysis]':
        '''List[SpringDamperCompoundModalAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5006.SpringDamperCompoundModalAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5011.StraightBevelDiffGearSetCompoundModalAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5011.StraightBevelDiffGearSetCompoundModalAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5014.StraightBevelGearSetCompoundModalAnalysis]':
        '''List[StraightBevelGearSetCompoundModalAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5014.StraightBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5017.SynchroniserCompoundModalAnalysis]':
        '''List[SynchroniserCompoundModalAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5017.SynchroniserCompoundModalAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5021.TorqueConverterCompoundModalAnalysis]':
        '''List[TorqueConverterCompoundModalAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5021.TorqueConverterCompoundModalAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5025.UnbalancedMassCompoundModalAnalysis]':
        '''List[UnbalancedMassCompoundModalAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5025.UnbalancedMassCompoundModalAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5029.WormGearSetCompoundModalAnalysis]':
        '''List[WormGearSetCompoundModalAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5029.WormGearSetCompoundModalAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5032.ZerolBevelGearSetCompoundModalAnalysis]':
        '''List[ZerolBevelGearSetCompoundModalAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5032.ZerolBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4758.AssemblyModalAnalysis]':
        '''List[AssemblyModalAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4758.AssemblyModalAnalysis))
        return value
