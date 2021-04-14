'''_5255.py

AbstractStaticLoadCaseGroup
'''


from typing import Callable, List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.analyses_and_results.load_case_groups import (
    _5266, _5265, _5253, _5264,
    _5254
)
from mastapy.system_model.analyses_and_results.static_loads import (
    _6208, _6078, _6190, _6189,
    _6115, _6117, _6119, _6160
)
from mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import _5268, _5271, _5272
from mastapy.system_model.part_model import (
    _2004, _2034, _2033, _2020
)
from mastapy.system_model.part_model.gears import _2086, _2085
from mastapy.system_model.connections_and_sockets.gears import _1889
from mastapy.system_model.analyses_and_results.power_flows.compound import _3406
from mastapy._internal.python_net import python_net_import

_ABSTRACT_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'AbstractStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractStaticLoadCaseGroup',)


class AbstractStaticLoadCaseGroup(_5254.AbstractLoadCaseGroup):
    '''AbstractStaticLoadCaseGroup

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_STATIC_LOAD_CASE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def max_number_of_load_cases_to_display(self) -> 'int':
        '''int: 'MaxNumberOfLoadCasesToDisplay' is the original name of this property.'''

        return self.wrapped.MaxNumberOfLoadCasesToDisplay

    @max_number_of_load_cases_to_display.setter
    def max_number_of_load_cases_to_display(self, value: 'int'):
        self.wrapped.MaxNumberOfLoadCasesToDisplay = int(value) if value else 0

    @property
    def clear_user_specified_excitation_data_for_all_load_cases(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ClearUserSpecifiedExcitationDataForAllLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClearUserSpecifiedExcitationDataForAllLoadCases

    @property
    def run_power_flow(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'RunPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RunPowerFlow

    @property
    def set_face_widths_for_specified_safety_factors_from_power_flow(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow

    @property
    def calculate_candidates(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateCandidates' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateCandidates

    @property
    def number_of_possible_system_designs(self) -> 'int':
        '''int: 'NumberOfPossibleSystemDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfPossibleSystemDesigns

    @property
    def perform_system_optimisation(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'PerformSystemOptimisation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PerformSystemOptimisation

    @property
    def create_designs(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CreateDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateDesigns

    @property
    def optimise_gear_sets_quick(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'OptimiseGearSetsQuick' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OptimiseGearSetsQuick

    @property
    def system_optimiser_log(self) -> 'str':
        '''str: 'SystemOptimiserLog' is the original name of this property.'''

        return self.wrapped.SystemOptimiserLog

    @system_optimiser_log.setter
    def system_optimiser_log(self, value: 'str'):
        self.wrapped.SystemOptimiserLog = str(value) if value else None

    @property
    def optimum_tooth_numbers_target(self) -> '_5266.SystemOptimiserTargets':
        '''SystemOptimiserTargets: 'OptimumToothNumbersTarget' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.OptimumToothNumbersTarget)
        return constructor.new(_5266.SystemOptimiserTargets)(value) if value else None

    @optimum_tooth_numbers_target.setter
    def optimum_tooth_numbers_target(self, value: '_5266.SystemOptimiserTargets'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OptimumToothNumbersTarget = value

    @property
    def gear_set_optimisation(self) -> '_5265.SystemOptimiserGearSetOptimisation':
        '''SystemOptimiserGearSetOptimisation: 'GearSetOptimisation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.GearSetOptimisation)
        return constructor.new(_5265.SystemOptimiserGearSetOptimisation)(value) if value else None

    @gear_set_optimisation.setter
    def gear_set_optimisation(self, value: '_5265.SystemOptimiserGearSetOptimisation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearSetOptimisation = value

    @property
    def number_of_configurations_to_create(self) -> 'int':
        '''int: 'NumberOfConfigurationsToCreate' is the original name of this property.'''

        return self.wrapped.NumberOfConfigurationsToCreate

    @number_of_configurations_to_create.setter
    def number_of_configurations_to_create(self, value: 'int'):
        self.wrapped.NumberOfConfigurationsToCreate = int(value) if value else 0

    @property
    def static_loads(self) -> 'List[_6208.StaticLoadCase]':
        '''List[StaticLoadCase]: 'StaticLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StaticLoads, constructor.new(_6208.StaticLoadCase))
        return value

    @property
    def static_loads_limited_by_max_number_of_load_cases_to_display(self) -> 'List[_6208.StaticLoadCase]':
        '''List[StaticLoadCase]: 'StaticLoadsLimitedByMaxNumberOfLoadCasesToDisplay' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StaticLoadsLimitedByMaxNumberOfLoadCasesToDisplay, constructor.new(_6208.StaticLoadCase))
        return value

    @property
    def bearings(self) -> 'List[_5268.ComponentStaticLoadCaseGroup[_2004.Bearing, _6078.BearingLoadCase]]':
        '''List[ComponentStaticLoadCaseGroup[Bearing, BearingLoadCase]]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5268.ComponentStaticLoadCaseGroup)[_2004.Bearing, _6078.BearingLoadCase])
        return value

    @property
    def power_loads(self) -> 'List[_5268.ComponentStaticLoadCaseGroup[_2034.PowerLoad, _6190.PowerLoadLoadCase]]':
        '''List[ComponentStaticLoadCaseGroup[PowerLoad, PowerLoadLoadCase]]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5268.ComponentStaticLoadCaseGroup)[_2034.PowerLoad, _6190.PowerLoadLoadCase])
        return value

    @property
    def point_loads(self) -> 'List[_5268.ComponentStaticLoadCaseGroup[_2033.PointLoad, _6189.PointLoadLoadCase]]':
        '''List[ComponentStaticLoadCaseGroup[PointLoad, PointLoadLoadCase]]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5268.ComponentStaticLoadCaseGroup)[_2033.PointLoad, _6189.PointLoadLoadCase])
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5271.GearSetStaticLoadCaseGroup[_2086.CylindricalGearSet, _2085.CylindricalGear, _6115.CylindricalGearLoadCase, _1889.CylindricalGearMesh, _6117.CylindricalGearMeshLoadCase, _6119.CylindricalGearSetLoadCase]]':
        '''List[GearSetStaticLoadCaseGroup[CylindricalGearSet, CylindricalGear, CylindricalGearLoadCase, CylindricalGearMesh, CylindricalGearMeshLoadCase, CylindricalGearSetLoadCase]]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5271.GearSetStaticLoadCaseGroup)[_2086.CylindricalGearSet, _2085.CylindricalGear, _6115.CylindricalGearLoadCase, _1889.CylindricalGearMesh, _6117.CylindricalGearMeshLoadCase, _6119.CylindricalGearSetLoadCase])
        return value

    @property
    def parts_with_excitations(self) -> 'List[_5272.PartStaticLoadCaseGroup]':
        '''List[PartStaticLoadCaseGroup]: 'PartsWithExcitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartsWithExcitations, constructor.new(_5272.PartStaticLoadCaseGroup))
        return value

    @property
    def fe_components(self) -> 'List[_5268.ComponentStaticLoadCaseGroup[_2020.ImportedFEComponent, _6160.ImportedFEComponentLoadCase]]':
        '''List[ComponentStaticLoadCaseGroup[ImportedFEComponent, ImportedFEComponentLoadCase]]: 'FEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEComponents, constructor.new(_5268.ComponentStaticLoadCaseGroup)[_2020.ImportedFEComponent, _6160.ImportedFEComponentLoadCase])
        return value

    @property
    def design_states(self) -> 'List[_5253.AbstractDesignStateLoadCaseGroup]':
        '''List[AbstractDesignStateLoadCaseGroup]: 'DesignStates' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DesignStates, constructor.new(_5253.AbstractDesignStateLoadCaseGroup))
        return value

    @property
    def loaded_gear_sets(self) -> 'List[_3406.CylindricalGearSetCompoundPowerFlow]':
        '''List[CylindricalGearSetCompoundPowerFlow]: 'LoadedGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadedGearSets, constructor.new(_3406.CylindricalGearSetCompoundPowerFlow))
        return value

    @property
    def system_optimisation_gear_sets(self) -> 'List[_5264.SystemOptimisationGearSet]':
        '''List[SystemOptimisationGearSet]: 'SystemOptimisationGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SystemOptimisationGearSets, constructor.new(_5264.SystemOptimisationGearSet))
        return value
