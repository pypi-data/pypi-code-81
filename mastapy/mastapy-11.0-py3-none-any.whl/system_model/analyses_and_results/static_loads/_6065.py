'''_6065.py

LoadCase
'''


from typing import List

from mastapy.system_model.analyses_and_results import (
    _2193, _2188, _2171, _2179,
    _2186, _2187, _2173, _2190,
    _2191, _2192, _2184, _2174,
    _2183, _2182, _2180, _2181,
    _2194, _2189, _2172, _2177,
    _2176, _2175, _2178, _2185,
    _2170, _2197
)
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _1728
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.bearing_results.rolling import _1595
from mastapy.system_model import _1818, _1815, _1826
from mastapy.gears import _139
from mastapy.system_model.analyses_and_results.static_loads import (
    _6225, _6068, _6186, _6070,
    _6113, _6154, _6160, _6163,
    _6166, _6199, _6209, _6230,
    _6233, _6140, _6176, _6087,
    _6092, _6105, _6201, _6219,
    _6072, _6066, _6067, _6074,
    _6086, _6085, _6091, _6104,
    _6119, _6132, _6136, _6073,
    _6144, _6156, _6168, _6169,
    _6171, _6173, _6175, _6182,
    _6185, _6192, _6196, _6227,
    _6228, _6194, _6095, _6097,
    _6133, _6135, _6069, _6071,
    _6077, _6079, _6080, _6081,
    _6082, _6084, _6098, _6102,
    _6111, _6115, _6116, _6138,
    _6143, _6153, _6155, _6159,
    _6161, _6162, _6164, _6165,
    _6167, _6180, _6198, _6200,
    _6205, _6207, _6208, _6210,
    _6211, _6212, _6229, _6231,
    _6232, _6234, _6178, _6177,
    _6076, _6089, _6088, _6094,
    _6093, _6107, _6106, _6109,
    _6110, _6187, _6193, _6191,
    _6189, _6203, _6202, _6214,
    _6213, _6215, _6216, _6220,
    _6221, _6222, _6108, _6075,
    _6090, _6103, _6158, _6179,
    _6190, _6195, _6078, _6096,
    _6134, _6206, _6083, _6100
)
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3566
from mastapy.system_model.connections_and_sockets.gears import (
    _1875, _1885, _1891, _1894,
    _1895, _1896, _1899, _1903,
    _1905, _1907, _1889, _1877,
    _1881, _1887, _1901, _1879,
    _1883
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1915, _1909, _1911, _1913,
    _1917, _1919
)
from mastapy.system_model.part_model import (
    _1996, _1997, _2000, _2002,
    _2003, _2004, _2007, _2008,
    _2011, _2012, _1995, _2013,
    _2016, _2020, _2021, _2022,
    _2024, _2026, _2027, _2029,
    _2030, _2032, _2034, _2035,
    _2036
)
from mastapy.system_model.part_model.shaft_model import _2039
from mastapy.system_model.part_model.gears import (
    _2077, _2078, _2084, _2085,
    _2069, _2070, _2071, _2072,
    _2073, _2074, _2075, _2076,
    _2079, _2080, _2081, _2082,
    _2083, _2086, _2088, _2090,
    _2091, _2092, _2093, _2094,
    _2095, _2096, _2097, _2098,
    _2099, _2100, _2101, _2102,
    _2103, _2104, _2105, _2106,
    _2107, _2108, _2109, _2110
)
from mastapy.system_model.part_model.couplings import (
    _2139, _2140, _2128, _2130,
    _2131, _2133, _2134, _2135,
    _2136, _2137, _2138, _2141,
    _2149, _2147, _2148, _2150,
    _2151, _2152, _2154, _2155,
    _2156, _2157, _2158, _2160
)
from mastapy.system_model.connections_and_sockets import (
    _1852, _1847, _1848, _1851,
    _1860, _1863, _1867, _1871
)
from mastapy._internal.python_net import python_net_import

_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'LoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadCase',)


class LoadCase(_2197.Context):
    '''LoadCase

    This is a mastapy class.
    '''

    TYPE = _LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def system_deflection(self) -> '_2193.SystemDeflectionAnalysis':
        '''SystemDeflectionAnalysis: 'SystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.SystemDeflectionAnalysis)(self.wrapped.SystemDeflection) if self.wrapped.SystemDeflection else None

    @property
    def power_flow(self) -> '_2188.PowerFlowAnalysis':
        '''PowerFlowAnalysis: 'PowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2188.PowerFlowAnalysis)(self.wrapped.PowerFlow) if self.wrapped.PowerFlow else None

    @property
    def advanced_system_deflection(self) -> '_2171.AdvancedSystemDeflectionAnalysis':
        '''AdvancedSystemDeflectionAnalysis: 'AdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2171.AdvancedSystemDeflectionAnalysis)(self.wrapped.AdvancedSystemDeflection) if self.wrapped.AdvancedSystemDeflection else None

    @property
    def gear_whine_analysis(self) -> '_2179.GearWhineAnalysisAnalysis':
        '''GearWhineAnalysisAnalysis: 'GearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2179.GearWhineAnalysisAnalysis)(self.wrapped.GearWhineAnalysis) if self.wrapped.GearWhineAnalysis else None

    @property
    def multibody_dynamics(self) -> '_2186.MultibodyDynamicsAnalysis':
        '''MultibodyDynamicsAnalysis: 'MultibodyDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2186.MultibodyDynamicsAnalysis)(self.wrapped.MultibodyDynamics) if self.wrapped.MultibodyDynamics else None

    @property
    def parametric_study_tool(self) -> '_2187.ParametricStudyToolAnalysis':
        '''ParametricStudyToolAnalysis: 'ParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2187.ParametricStudyToolAnalysis)(self.wrapped.ParametricStudyTool) if self.wrapped.ParametricStudyTool else None

    @property
    def compound_parametric_study_tool(self) -> '_2173.CompoundParametricStudyToolAnalysis':
        '''CompoundParametricStudyToolAnalysis: 'CompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2173.CompoundParametricStudyToolAnalysis)(self.wrapped.CompoundParametricStudyTool) if self.wrapped.CompoundParametricStudyTool else None

    @property
    def steady_state_synchronous_response(self) -> '_2190.SteadyStateSynchronousResponseAnalysis':
        '''SteadyStateSynchronousResponseAnalysis: 'SteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.SteadyStateSynchronousResponseAnalysis)(self.wrapped.SteadyStateSynchronousResponse) if self.wrapped.SteadyStateSynchronousResponse else None

    @property
    def steady_state_synchronous_responseata_speed(self) -> '_2191.SteadyStateSynchronousResponseataSpeedAnalysis':
        '''SteadyStateSynchronousResponseataSpeedAnalysis: 'SteadyStateSynchronousResponseataSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2191.SteadyStateSynchronousResponseataSpeedAnalysis)(self.wrapped.SteadyStateSynchronousResponseataSpeed) if self.wrapped.SteadyStateSynchronousResponseataSpeed else None

    @property
    def steady_state_synchronous_responseona_shaft(self) -> '_2192.SteadyStateSynchronousResponseonaShaftAnalysis':
        '''SteadyStateSynchronousResponseonaShaftAnalysis: 'SteadyStateSynchronousResponseonaShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.SteadyStateSynchronousResponseonaShaftAnalysis)(self.wrapped.SteadyStateSynchronousResponseonaShaft) if self.wrapped.SteadyStateSynchronousResponseonaShaft else None

    @property
    def modal_analysis(self) -> '_2184.ModalAnalysisAnalysis':
        '''ModalAnalysisAnalysis: 'ModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2184.ModalAnalysisAnalysis)(self.wrapped.ModalAnalysis) if self.wrapped.ModalAnalysis else None

    @property
    def dynamic_analysis(self) -> '_2174.DynamicAnalysisAnalysis':
        '''DynamicAnalysisAnalysis: 'DynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2174.DynamicAnalysisAnalysis)(self.wrapped.DynamicAnalysis) if self.wrapped.DynamicAnalysis else None

    @property
    def modal_analysesat_stiffnesses(self) -> '_2183.ModalAnalysesatStiffnessesAnalysis':
        '''ModalAnalysesatStiffnessesAnalysis: 'ModalAnalysesatStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2183.ModalAnalysesatStiffnessesAnalysis)(self.wrapped.ModalAnalysesatStiffnesses) if self.wrapped.ModalAnalysesatStiffnesses else None

    @property
    def modal_analysesat_speeds(self) -> '_2182.ModalAnalysesatSpeedsAnalysis':
        '''ModalAnalysesatSpeedsAnalysis: 'ModalAnalysesatSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2182.ModalAnalysesatSpeedsAnalysis)(self.wrapped.ModalAnalysesatSpeeds) if self.wrapped.ModalAnalysesatSpeeds else None

    @property
    def modal_analysesata_speed(self) -> '_2180.ModalAnalysesataSpeedAnalysis':
        '''ModalAnalysesataSpeedAnalysis: 'ModalAnalysesataSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.ModalAnalysesataSpeedAnalysis)(self.wrapped.ModalAnalysesataSpeed) if self.wrapped.ModalAnalysesataSpeed else None

    @property
    def modal_analysesata_stiffness(self) -> '_2181.ModalAnalysesataStiffnessAnalysis':
        '''ModalAnalysesataStiffnessAnalysis: 'ModalAnalysesataStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.ModalAnalysesataStiffnessAnalysis)(self.wrapped.ModalAnalysesataStiffness) if self.wrapped.ModalAnalysesataStiffness else None

    @property
    def torsional_system_deflection(self) -> '_2194.TorsionalSystemDeflectionAnalysis':
        '''TorsionalSystemDeflectionAnalysis: 'TorsionalSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2194.TorsionalSystemDeflectionAnalysis)(self.wrapped.TorsionalSystemDeflection) if self.wrapped.TorsionalSystemDeflection else None

    @property
    def single_mesh_whine_analysis(self) -> '_2189.SingleMeshWhineAnalysisAnalysis':
        '''SingleMeshWhineAnalysisAnalysis: 'SingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2189.SingleMeshWhineAnalysisAnalysis)(self.wrapped.SingleMeshWhineAnalysis) if self.wrapped.SingleMeshWhineAnalysis else None

    @property
    def advanced_system_deflection_sub_analysis(self) -> '_2172.AdvancedSystemDeflectionSubAnalysisAnalysis':
        '''AdvancedSystemDeflectionSubAnalysisAnalysis: 'AdvancedSystemDeflectionSubAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2172.AdvancedSystemDeflectionSubAnalysisAnalysis)(self.wrapped.AdvancedSystemDeflectionSubAnalysis) if self.wrapped.AdvancedSystemDeflectionSubAnalysis else None

    @property
    def dynamic_modelfor_gear_whine(self) -> '_2177.DynamicModelforGearWhineAnalysis':
        '''DynamicModelforGearWhineAnalysis: 'DynamicModelforGearWhine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2177.DynamicModelforGearWhineAnalysis)(self.wrapped.DynamicModelforGearWhine) if self.wrapped.DynamicModelforGearWhine else None

    @property
    def dynamic_modelforat_speeds(self) -> '_2176.DynamicModelforatSpeedsAnalysis':
        '''DynamicModelforatSpeedsAnalysis: 'DynamicModelforatSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2176.DynamicModelforatSpeedsAnalysis)(self.wrapped.DynamicModelforatSpeeds) if self.wrapped.DynamicModelforatSpeeds else None

    @property
    def dynamic_modelata_stiffness(self) -> '_2175.DynamicModelataStiffnessAnalysis':
        '''DynamicModelataStiffnessAnalysis: 'DynamicModelataStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2175.DynamicModelataStiffnessAnalysis)(self.wrapped.DynamicModelataStiffness) if self.wrapped.DynamicModelataStiffness else None

    @property
    def dynamic_modelfor_steady_state_synchronous_response(self) -> '_2178.DynamicModelforSteadyStateSynchronousResponseAnalysis':
        '''DynamicModelforSteadyStateSynchronousResponseAnalysis: 'DynamicModelforSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2178.DynamicModelforSteadyStateSynchronousResponseAnalysis)(self.wrapped.DynamicModelforSteadyStateSynchronousResponse) if self.wrapped.DynamicModelforSteadyStateSynchronousResponse else None

    @property
    def modal_analysisfor_whine(self) -> '_2185.ModalAnalysisforWhineAnalysis':
        '''ModalAnalysisforWhineAnalysis: 'ModalAnalysisforWhine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2185.ModalAnalysisforWhineAnalysis)(self.wrapped.ModalAnalysisforWhine) if self.wrapped.ModalAnalysisforWhine else None

    @property
    def include_bearing_centrifugal(self) -> 'bool':
        '''bool: 'IncludeBearingCentrifugal' is the original name of this property.'''

        return self.wrapped.IncludeBearingCentrifugal

    @include_bearing_centrifugal.setter
    def include_bearing_centrifugal(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugal = bool(value) if value else False

    @property
    def include_bearing_centrifugal_ring_expansion(self) -> 'bool':
        '''bool: 'IncludeBearingCentrifugalRingExpansion' is the original name of this property.'''

        return self.wrapped.IncludeBearingCentrifugalRingExpansion

    @include_bearing_centrifugal_ring_expansion.setter
    def include_bearing_centrifugal_ring_expansion(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugalRingExpansion = bool(value) if value else False

    @property
    def include_planetary_centrifugal(self) -> 'bool':
        '''bool: 'IncludePlanetaryCentrifugal' is the original name of this property.'''

        return self.wrapped.IncludePlanetaryCentrifugal

    @include_planetary_centrifugal.setter
    def include_planetary_centrifugal(self, value: 'bool'):
        self.wrapped.IncludePlanetaryCentrifugal = bool(value) if value else False

    @property
    def include_gravity(self) -> 'bool':
        '''bool: 'IncludeGravity' is the original name of this property.'''

        return self.wrapped.IncludeGravity

    @include_gravity.setter
    def include_gravity(self, value: 'bool'):
        self.wrapped.IncludeGravity = bool(value) if value else False

    @property
    def stress_concentration_method_for_rating(self) -> 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod: 'StressConcentrationMethodForRating' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.StressConcentrationMethodForRating, value) if self.wrapped.StressConcentrationMethodForRating else None

    @stress_concentration_method_for_rating.setter
    def stress_concentration_method_for_rating(self, value: 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.StressConcentrationMethodForRating = value

    @property
    def number_of_strips_for_roller_calculation(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfStripsForRollerCalculation' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfStripsForRollerCalculation) if self.wrapped.NumberOfStripsForRollerCalculation else None

    @number_of_strips_for_roller_calculation.setter
    def number_of_strips_for_roller_calculation(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.NumberOfStripsForRollerCalculation = value

    @property
    def use_default_temperatures(self) -> 'bool':
        '''bool: 'UseDefaultTemperatures' is the original name of this property.'''

        return self.wrapped.UseDefaultTemperatures

    @use_default_temperatures.setter
    def use_default_temperatures(self, value: 'bool'):
        self.wrapped.UseDefaultTemperatures = bool(value) if value else False

    @property
    def include_fitting_effects(self) -> 'bool':
        '''bool: 'IncludeFittingEffects' is the original name of this property.'''

        return self.wrapped.IncludeFittingEffects

    @include_fitting_effects.setter
    def include_fitting_effects(self, value: 'bool'):
        self.wrapped.IncludeFittingEffects = bool(value) if value else False

    @property
    def include_thermal_expansion_effects(self) -> 'bool':
        '''bool: 'IncludeThermalExpansionEffects' is the original name of this property.'''

        return self.wrapped.IncludeThermalExpansionEffects

    @include_thermal_expansion_effects.setter
    def include_thermal_expansion_effects(self, value: 'bool'):
        self.wrapped.IncludeThermalExpansionEffects = bool(value) if value else False

    @property
    def include_ring_ovality(self) -> 'bool':
        '''bool: 'IncludeRingOvality' is the original name of this property.'''

        return self.wrapped.IncludeRingOvality

    @include_ring_ovality.setter
    def include_ring_ovality(self, value: 'bool'):
        self.wrapped.IncludeRingOvality = bool(value) if value else False

    @property
    def ring_ovality_scaling(self) -> 'float':
        '''float: 'RingOvalityScaling' is the original name of this property.'''

        return self.wrapped.RingOvalityScaling

    @ring_ovality_scaling.setter
    def ring_ovality_scaling(self, value: 'float'):
        self.wrapped.RingOvalityScaling = float(value) if value else 0.0

    @property
    def include_gear_blank_elastic_distortion(self) -> 'bool':
        '''bool: 'IncludeGearBlankElasticDistortion' is the original name of this property.'''

        return self.wrapped.IncludeGearBlankElasticDistortion

    @include_gear_blank_elastic_distortion.setter
    def include_gear_blank_elastic_distortion(self, value: 'bool'):
        self.wrapped.IncludeGearBlankElasticDistortion = bool(value) if value else False

    @property
    def include_inner_race_distortion_for_flexible_pin_spindle(self) -> 'bool':
        '''bool: 'IncludeInnerRaceDistortionForFlexiblePinSpindle' is the original name of this property.'''

        return self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle

    @include_inner_race_distortion_for_flexible_pin_spindle.setter
    def include_inner_race_distortion_for_flexible_pin_spindle(self, value: 'bool'):
        self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle = bool(value) if value else False

    @property
    def ball_bearing_contact_calculation(self) -> '_1595.BallBearingContactCalculation':
        '''BallBearingContactCalculation: 'BallBearingContactCalculation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BallBearingContactCalculation)
        return constructor.new(_1595.BallBearingContactCalculation)(value) if value else None

    @ball_bearing_contact_calculation.setter
    def ball_bearing_contact_calculation(self, value: '_1595.BallBearingContactCalculation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BallBearingContactCalculation = value

    @property
    def model_bearing_mounting_clearances_automatically(self) -> 'bool':
        '''bool: 'ModelBearingMountingClearancesAutomatically' is the original name of this property.'''

        return self.wrapped.ModelBearingMountingClearancesAutomatically

    @model_bearing_mounting_clearances_automatically.setter
    def model_bearing_mounting_clearances_automatically(self, value: 'bool'):
        self.wrapped.ModelBearingMountingClearancesAutomatically = bool(value) if value else False

    @property
    def maximum_shaft_section_length_to_diameter_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionLengthToDiameterRatio

    @maximum_shaft_section_length_to_diameter_ratio.setter
    def maximum_shaft_section_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_cross_sectional_area_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionCrossSectionalAreaRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio

    @maximum_shaft_section_cross_sectional_area_ratio.setter
    def maximum_shaft_section_cross_sectional_area_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionPolarAreaMomentOfInertiaRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio

    @maximum_shaft_section_polar_area_moment_of_inertia_ratio.setter
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio = float(value) if value else 0.0

    @property
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self) -> 'bool':
        '''bool: 'UseSingleNodeForSplineRigidBondDetailedConnectionConnections' is the original name of this property.'''

        return self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections

    @use_single_node_for_spline_rigid_bond_detailed_connection_connections.setter
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self, value: 'bool'):
        self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections = bool(value) if value else False

    @property
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        '''float: 'SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio

    @spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio.setter
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def use_single_node_for_cylindrical_gear_meshes(self) -> 'bool':
        '''bool: 'UseSingleNodeForCylindricalGearMeshes' is the original name of this property.'''

        return self.wrapped.UseSingleNodeForCylindricalGearMeshes

    @use_single_node_for_cylindrical_gear_meshes.setter
    def use_single_node_for_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.UseSingleNodeForCylindricalGearMeshes = bool(value) if value else False

    @property
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self) -> 'bool':
        '''bool: 'ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes' is the original name of this property.'''

        return self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes

    @force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes.setter
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes = bool(value) if value else False

    @property
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        '''float: 'GearMeshNodesPerUnitLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio

    @gear_mesh_nodes_per_unit_length_to_diameter_ratio.setter
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def minimum_number_of_gear_mesh_nodes(self) -> 'int':
        '''int: 'MinimumNumberOfGearMeshNodes' is the original name of this property.'''

        return self.wrapped.MinimumNumberOfGearMeshNodes

    @minimum_number_of_gear_mesh_nodes.setter
    def minimum_number_of_gear_mesh_nodes(self, value: 'int'):
        self.wrapped.MinimumNumberOfGearMeshNodes = int(value) if value else 0

    @property
    def peak_load_factor_for_shafts(self) -> 'float':
        '''float: 'PeakLoadFactorForShafts' is the original name of this property.'''

        return self.wrapped.PeakLoadFactorForShafts

    @peak_load_factor_for_shafts.setter
    def peak_load_factor_for_shafts(self, value: 'float'):
        self.wrapped.PeakLoadFactorForShafts = float(value) if value else 0.0

    @property
    def mesh_stiffness_model(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel':
        '''enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel: 'MeshStiffnessModel' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MeshStiffnessModel, value) if self.wrapped.MeshStiffnessModel else None

    @mesh_stiffness_model.setter
    def mesh_stiffness_model(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.MeshStiffnessModel = value

    @property
    def micro_geometry_model_in_system_deflection(self) -> 'overridable.Overridable_MicroGeometryModel':
        '''overridable.Overridable_MicroGeometryModel: 'MicroGeometryModelInSystemDeflection' is the original name of this property.'''

        value = overridable.Overridable_MicroGeometryModel.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MicroGeometryModelInSystemDeflection, value) if self.wrapped.MicroGeometryModelInSystemDeflection else None

    @micro_geometry_model_in_system_deflection.setter
    def micro_geometry_model_in_system_deflection(self, value: 'overridable.Overridable_MicroGeometryModel.implicit_type()'):
        wrapper_type = overridable.Overridable_MicroGeometryModel.wrapper_type()
        enclosed_type = overridable.Overridable_MicroGeometryModel.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value else None, is_overridden)
        self.wrapped.MicroGeometryModelInSystemDeflection = value

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumForceForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumForceForBearingToBeConsideredLoaded) if self.wrapped.MinimumForceForBearingToBeConsideredLoaded else None

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    def minimum_force_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MinimumForceForBearingToBeConsideredLoaded = value

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumMomentForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumMomentForBearingToBeConsideredLoaded) if self.wrapped.MinimumMomentForBearingToBeConsideredLoaded else None

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    def minimum_moment_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MinimumMomentForBearingToBeConsideredLoaded = value

    @property
    def energy_convergence_absolute_tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'EnergyConvergenceAbsoluteTolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.EnergyConvergenceAbsoluteTolerance) if self.wrapped.EnergyConvergenceAbsoluteTolerance else None

    @energy_convergence_absolute_tolerance.setter
    def energy_convergence_absolute_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.EnergyConvergenceAbsoluteTolerance = value

    @property
    def hypoid_gear_wind_up_removal_method_for_misalignments(self) -> '_1815.HypoidWindUpRemovalMethod':
        '''HypoidWindUpRemovalMethod: 'HypoidGearWindUpRemovalMethodForMisalignments' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments)
        return constructor.new(_1815.HypoidWindUpRemovalMethod)(value) if value else None

    @hypoid_gear_wind_up_removal_method_for_misalignments.setter
    def hypoid_gear_wind_up_removal_method_for_misalignments(self, value: '_1815.HypoidWindUpRemovalMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments = value

    @property
    def include_tilt_stiffness_for_bevel_hypoid_gears(self) -> 'bool':
        '''bool: 'IncludeTiltStiffnessForBevelHypoidGears' is the original name of this property.'''

        return self.wrapped.IncludeTiltStiffnessForBevelHypoidGears

    @include_tilt_stiffness_for_bevel_hypoid_gears.setter
    def include_tilt_stiffness_for_bevel_hypoid_gears(self, value: 'bool'):
        self.wrapped.IncludeTiltStiffnessForBevelHypoidGears = bool(value) if value else False

    @property
    def minimum_power_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumPowerForGearMeshToBeLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumPowerForGearMeshToBeLoaded) if self.wrapped.MinimumPowerForGearMeshToBeLoaded else None

    @minimum_power_for_gear_mesh_to_be_loaded.setter
    def minimum_power_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MinimumPowerForGearMeshToBeLoaded = value

    @property
    def minimum_torque_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumTorqueForGearMeshToBeLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumTorqueForGearMeshToBeLoaded) if self.wrapped.MinimumTorqueForGearMeshToBeLoaded else None

    @minimum_torque_for_gear_mesh_to_be_loaded.setter
    def minimum_torque_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MinimumTorqueForGearMeshToBeLoaded = value

    @property
    def tolerance_factor_for_outer_fit(self) -> 'float':
        '''float: 'ToleranceFactorForOuterFit' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForOuterFit

    @tolerance_factor_for_outer_fit.setter
    def tolerance_factor_for_outer_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForOuterFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_inner_fit(self) -> 'float':
        '''float: 'ToleranceFactorForInnerFit' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForInnerFit

    @tolerance_factor_for_inner_fit.setter
    def tolerance_factor_for_inner_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForInnerFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_outer_support(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterSupport' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterSupport) if self.wrapped.ToleranceFactorForOuterSupport else None

    @tolerance_factor_for_outer_support.setter
    def tolerance_factor_for_outer_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterSupport = value

    @property
    def tolerance_factor_for_outer_ring(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterRing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterRing) if self.wrapped.ToleranceFactorForOuterRing else None

    @tolerance_factor_for_outer_ring.setter
    def tolerance_factor_for_outer_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterRing = value

    @property
    def tolerance_factor_for_inner_support(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerSupport' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerSupport) if self.wrapped.ToleranceFactorForInnerSupport else None

    @tolerance_factor_for_inner_support.setter
    def tolerance_factor_for_inner_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerSupport = value

    @property
    def tolerance_factor_for_inner_ring(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerRing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerRing) if self.wrapped.ToleranceFactorForInnerRing else None

    @tolerance_factor_for_inner_ring.setter
    def tolerance_factor_for_inner_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerRing = value

    @property
    def tolerance_factor_for_inner_mounting_sleeve_bore(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerMountingSleeveBore' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerMountingSleeveBore) if self.wrapped.ToleranceFactorForInnerMountingSleeveBore else None

    @tolerance_factor_for_inner_mounting_sleeve_bore.setter
    def tolerance_factor_for_inner_mounting_sleeve_bore(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerMountingSleeveBore = value

    @property
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerMountingSleeveOuterDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter) if self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter else None

    @tolerance_factor_for_inner_mounting_sleeve_outer_diameter.setter
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter = value

    @property
    def tolerance_factor_for_outer_mounting_sleeve_bore(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterMountingSleeveBore' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterMountingSleeveBore) if self.wrapped.ToleranceFactorForOuterMountingSleeveBore else None

    @tolerance_factor_for_outer_mounting_sleeve_bore.setter
    def tolerance_factor_for_outer_mounting_sleeve_bore(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterMountingSleeveBore = value

    @property
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterMountingSleeveOuterDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter) if self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter else None

    @tolerance_factor_for_outer_mounting_sleeve_outer_diameter.setter
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter = value

    @property
    def tolerance_factor_for_radial_internal_clearances(self) -> 'float':
        '''float: 'ToleranceFactorForRadialInternalClearances' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForRadialInternalClearances

    @tolerance_factor_for_radial_internal_clearances.setter
    def tolerance_factor_for_radial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForRadialInternalClearances = float(value) if value else 0.0

    @property
    def tolerance_factor_for_axial_internal_clearances(self) -> 'float':
        '''float: 'ToleranceFactorForAxialInternalClearances' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForAxialInternalClearances

    @tolerance_factor_for_axial_internal_clearances.setter
    def tolerance_factor_for_axial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForAxialInternalClearances = float(value) if value else 0.0

    @property
    def relative_tolerance_for_convergence(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RelativeToleranceForConvergence' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RelativeToleranceForConvergence) if self.wrapped.RelativeToleranceForConvergence else None

    @relative_tolerance_for_convergence.setter
    def relative_tolerance_for_convergence(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.RelativeToleranceForConvergence = value

    @property
    def air_density(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AirDensity' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AirDensity) if self.wrapped.AirDensity else None

    @air_density.setter
    def air_density(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.AirDensity = value

    @property
    def speed_of_sound(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpeedOfSound' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpeedOfSound) if self.wrapped.SpeedOfSound else None

    @speed_of_sound.setter
    def speed_of_sound(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SpeedOfSound = value

    @property
    def characteristic_specific_acoustic_impedance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CharacteristicSpecificAcousticImpedance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CharacteristicSpecificAcousticImpedance) if self.wrapped.CharacteristicSpecificAcousticImpedance else None

    @characteristic_specific_acoustic_impedance.setter
    def characteristic_specific_acoustic_impedance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.CharacteristicSpecificAcousticImpedance = value

    @property
    def transmission_efficiency_settings(self) -> '_6225.TransmissionEfficiencySettings':
        '''TransmissionEfficiencySettings: 'TransmissionEfficiencySettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6225.TransmissionEfficiencySettings)(self.wrapped.TransmissionEfficiencySettings) if self.wrapped.TransmissionEfficiencySettings else None

    @property
    def additional_acceleration(self) -> '_6068.AdditionalAccelerationOptions':
        '''AdditionalAccelerationOptions: 'AdditionalAcceleration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6068.AdditionalAccelerationOptions)(self.wrapped.AdditionalAcceleration) if self.wrapped.AdditionalAcceleration else None

    @property
    def temperatures(self) -> '_1826.TransmissionTemperatureSet':
        '''TransmissionTemperatureSet: 'Temperatures' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1826.TransmissionTemperatureSet)(self.wrapped.Temperatures) if self.wrapped.Temperatures else None

    @property
    def input_power_load(self) -> '_6186.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'InputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6186.PowerLoadLoadCase)(self.wrapped.InputPowerLoad) if self.wrapped.InputPowerLoad else None

    @property
    def output_power_load(self) -> '_6186.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'OutputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6186.PowerLoadLoadCase)(self.wrapped.OutputPowerLoad) if self.wrapped.OutputPowerLoad else None

    @property
    def parametric_study_tool_options(self) -> '_3566.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricStudyToolOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3566.ParametricStudyToolOptions)(self.wrapped.ParametricStudyToolOptions) if self.wrapped.ParametricStudyToolOptions else None

    @property
    def power_loads(self) -> 'List[_6186.PowerLoadLoadCase]':
        '''List[PowerLoadLoadCase]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6186.PowerLoadLoadCase))
        return value

    def inputs_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1875.AGMAGleasonConicalGearMesh') -> '_6070.AGMAGleasonConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6070.AGMAGleasonConicalGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_cylindrical_gear_mesh(self, design_entity: '_1885.CylindricalGearMesh') -> '_6113.CylindricalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6113.CylindricalGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_hypoid_gear_mesh(self, design_entity: '_1891.HypoidGearMesh') -> '_6154.HypoidGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6154.HypoidGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1894.KlingelnbergCycloPalloidConicalGearMesh') -> '_6160.KlingelnbergCycloPalloidConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6160.KlingelnbergCycloPalloidConicalGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1895.KlingelnbergCycloPalloidHypoidGearMesh') -> '_6163.KlingelnbergCycloPalloidHypoidGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6163.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1896.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_6166.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6166.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_spiral_bevel_gear_mesh(self, design_entity: '_1899.SpiralBevelGearMesh') -> '_6199.SpiralBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6199.SpiralBevelGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_gear_mesh(self, design_entity: '_1903.StraightBevelGearMesh') -> '_6209.StraightBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6209.StraightBevelGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_worm_gear_mesh(self, design_entity: '_1905.WormGearMesh') -> '_6230.WormGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6230.WormGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_zerol_bevel_gear_mesh(self, design_entity: '_1907.ZerolBevelGearMesh') -> '_6233.ZerolBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6233.ZerolBevelGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_gear_mesh(self, design_entity: '_1889.GearMesh') -> '_6140.GearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6140.GearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_part_to_part_shear_coupling_connection(self, design_entity: '_1915.PartToPartShearCouplingConnection') -> '_6176.PartToPartShearCouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6176.PartToPartShearCouplingConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_clutch_connection(self, design_entity: '_1909.ClutchConnection') -> '_6087.ClutchConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6087.ClutchConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_concept_coupling_connection(self, design_entity: '_1911.ConceptCouplingConnection') -> '_6092.ConceptCouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6092.ConceptCouplingConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_coupling_connection(self, design_entity: '_1913.CouplingConnection') -> '_6105.CouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6105.CouplingConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_spring_damper_connection(self, design_entity: '_1917.SpringDamperConnection') -> '_6201.SpringDamperConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6201.SpringDamperConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_torque_converter_connection(self, design_entity: '_1919.TorqueConverterConnection') -> '_6219.TorqueConverterConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6219.TorqueConverterConnectionLoadCase)(method_result) if method_result else None

    def analysis_of(self, analysis_type: '_6072.AnalysisType') -> '_2170.SingleAnalysis':
        ''' 'AnalysisOf' is the original name of this method.

        Args:
            analysis_type (mastapy.system_model.analyses_and_results.static_loads.AnalysisType)

        Returns:
            mastapy.system_model.analyses_and_results.SingleAnalysis
        '''

        analysis_type = conversion.mp_to_pn_enum(analysis_type)
        method_result = self.wrapped.AnalysisOf(analysis_type)
        return constructor.new(_2170.SingleAnalysis)(method_result) if method_result else None

    def delete(self):
        ''' 'Delete' is the original name of this method.'''

        self.wrapped.Delete()

    def inputs_for_abstract_assembly(self, design_entity: '_1996.AbstractAssembly') -> '_6066.AbstractAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6066.AbstractAssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_abstract_shaft_or_housing(self, design_entity: '_1997.AbstractShaftOrHousing') -> '_6067.AbstractShaftOrHousingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6067.AbstractShaftOrHousingLoadCase)(method_result) if method_result else None

    def inputs_for_bearing(self, design_entity: '_2000.Bearing') -> '_6074.BearingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6074.BearingLoadCase)(method_result) if method_result else None

    def inputs_for_bolt(self, design_entity: '_2002.Bolt') -> '_6086.BoltLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6086.BoltLoadCase)(method_result) if method_result else None

    def inputs_for_bolted_joint(self, design_entity: '_2003.BoltedJoint') -> '_6085.BoltedJointLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6085.BoltedJointLoadCase)(method_result) if method_result else None

    def inputs_for_component(self, design_entity: '_2004.Component') -> '_6091.ComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6091.ComponentLoadCase)(method_result) if method_result else None

    def inputs_for_connector(self, design_entity: '_2007.Connector') -> '_6104.ConnectorLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6104.ConnectorLoadCase)(method_result) if method_result else None

    def inputs_for_datum(self, design_entity: '_2008.Datum') -> '_6119.DatumLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6119.DatumLoadCase)(method_result) if method_result else None

    def inputs_for_external_cad_model(self, design_entity: '_2011.ExternalCADModel') -> '_6132.ExternalCADModelLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6132.ExternalCADModelLoadCase)(method_result) if method_result else None

    def inputs_for_flexible_pin_assembly(self, design_entity: '_2012.FlexiblePinAssembly') -> '_6136.FlexiblePinAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6136.FlexiblePinAssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_assembly(self, design_entity: '_1995.Assembly') -> '_6073.AssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6073.AssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_guide_dxf_model(self, design_entity: '_2013.GuideDxfModel') -> '_6144.GuideDxfModelLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6144.GuideDxfModelLoadCase)(method_result) if method_result else None

    def inputs_for_imported_fe_component(self, design_entity: '_2016.ImportedFEComponent') -> '_6156.ImportedFEComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6156.ImportedFEComponentLoadCase)(method_result) if method_result else None

    def inputs_for_mass_disc(self, design_entity: '_2020.MassDisc') -> '_6168.MassDiscLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6168.MassDiscLoadCase)(method_result) if method_result else None

    def inputs_for_measurement_component(self, design_entity: '_2021.MeasurementComponent') -> '_6169.MeasurementComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6169.MeasurementComponentLoadCase)(method_result) if method_result else None

    def inputs_for_mountable_component(self, design_entity: '_2022.MountableComponent') -> '_6171.MountableComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6171.MountableComponentLoadCase)(method_result) if method_result else None

    def inputs_for_oil_seal(self, design_entity: '_2024.OilSeal') -> '_6173.OilSealLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6173.OilSealLoadCase)(method_result) if method_result else None

    def inputs_for_part(self, design_entity: '_2026.Part') -> '_6175.PartLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6175.PartLoadCase)(method_result) if method_result else None

    def inputs_for_planet_carrier(self, design_entity: '_2027.PlanetCarrier') -> '_6182.PlanetCarrierLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6182.PlanetCarrierLoadCase)(method_result) if method_result else None

    def inputs_for_point_load(self, design_entity: '_2029.PointLoad') -> '_6185.PointLoadLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6185.PointLoadLoadCase)(method_result) if method_result else None

    def inputs_for_power_load(self, design_entity: '_2030.PowerLoad') -> '_6186.PowerLoadLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6186.PowerLoadLoadCase)(method_result) if method_result else None

    def inputs_for_root_assembly(self, design_entity: '_2032.RootAssembly') -> '_6192.RootAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6192.RootAssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_specialised_assembly(self, design_entity: '_2034.SpecialisedAssembly') -> '_6196.SpecialisedAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6196.SpecialisedAssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_unbalanced_mass(self, design_entity: '_2035.UnbalancedMass') -> '_6227.UnbalancedMassLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6227.UnbalancedMassLoadCase)(method_result) if method_result else None

    def inputs_for_virtual_component(self, design_entity: '_2036.VirtualComponent') -> '_6228.VirtualComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6228.VirtualComponentLoadCase)(method_result) if method_result else None

    def inputs_for_shaft(self, design_entity: '_2039.Shaft') -> '_6194.ShaftLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6194.ShaftLoadCase)(method_result) if method_result else None

    def inputs_for_concept_gear(self, design_entity: '_2077.ConceptGear') -> '_6095.ConceptGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6095.ConceptGearLoadCase)(method_result) if method_result else None

    def inputs_for_concept_gear_set(self, design_entity: '_2078.ConceptGearSet') -> '_6097.ConceptGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6097.ConceptGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_face_gear(self, design_entity: '_2084.FaceGear') -> '_6133.FaceGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6133.FaceGearLoadCase)(method_result) if method_result else None

    def inputs_for_face_gear_set(self, design_entity: '_2085.FaceGearSet') -> '_6135.FaceGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6135.FaceGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_agma_gleason_conical_gear(self, design_entity: '_2069.AGMAGleasonConicalGear') -> '_6069.AGMAGleasonConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6069.AGMAGleasonConicalGearLoadCase)(method_result) if method_result else None

    def inputs_for_agma_gleason_conical_gear_set(self, design_entity: '_2070.AGMAGleasonConicalGearSet') -> '_6071.AGMAGleasonConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6071.AGMAGleasonConicalGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_differential_gear(self, design_entity: '_2071.BevelDifferentialGear') -> '_6077.BevelDifferentialGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6077.BevelDifferentialGearLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_differential_gear_set(self, design_entity: '_2072.BevelDifferentialGearSet') -> '_6079.BevelDifferentialGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6079.BevelDifferentialGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_differential_planet_gear(self, design_entity: '_2073.BevelDifferentialPlanetGear') -> '_6080.BevelDifferentialPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6080.BevelDifferentialPlanetGearLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_differential_sun_gear(self, design_entity: '_2074.BevelDifferentialSunGear') -> '_6081.BevelDifferentialSunGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6081.BevelDifferentialSunGearLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_gear(self, design_entity: '_2075.BevelGear') -> '_6082.BevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6082.BevelGearLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_gear_set(self, design_entity: '_2076.BevelGearSet') -> '_6084.BevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6084.BevelGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_conical_gear(self, design_entity: '_2079.ConicalGear') -> '_6098.ConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6098.ConicalGearLoadCase)(method_result) if method_result else None

    def inputs_for_conical_gear_set(self, design_entity: '_2080.ConicalGearSet') -> '_6102.ConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6102.ConicalGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_cylindrical_gear(self, design_entity: '_2081.CylindricalGear') -> '_6111.CylindricalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6111.CylindricalGearLoadCase)(method_result) if method_result else None

    def inputs_for_cylindrical_gear_set(self, design_entity: '_2082.CylindricalGearSet') -> '_6115.CylindricalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6115.CylindricalGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_cylindrical_planet_gear(self, design_entity: '_2083.CylindricalPlanetGear') -> '_6116.CylindricalPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6116.CylindricalPlanetGearLoadCase)(method_result) if method_result else None

    def inputs_for_gear(self, design_entity: '_2086.Gear') -> '_6138.GearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6138.GearLoadCase)(method_result) if method_result else None

    def inputs_for_gear_set(self, design_entity: '_2088.GearSet') -> '_6143.GearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6143.GearSetLoadCase)(method_result) if method_result else None

    def inputs_for_hypoid_gear(self, design_entity: '_2090.HypoidGear') -> '_6153.HypoidGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6153.HypoidGearLoadCase)(method_result) if method_result else None

    def inputs_for_hypoid_gear_set(self, design_entity: '_2091.HypoidGearSet') -> '_6155.HypoidGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6155.HypoidGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2092.KlingelnbergCycloPalloidConicalGear') -> '_6159.KlingelnbergCycloPalloidConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6159.KlingelnbergCycloPalloidConicalGearLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2093.KlingelnbergCycloPalloidConicalGearSet') -> '_6161.KlingelnbergCycloPalloidConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6161.KlingelnbergCycloPalloidConicalGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2094.KlingelnbergCycloPalloidHypoidGear') -> '_6162.KlingelnbergCycloPalloidHypoidGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6162.KlingelnbergCycloPalloidHypoidGearLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2095.KlingelnbergCycloPalloidHypoidGearSet') -> '_6164.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6164.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2096.KlingelnbergCycloPalloidSpiralBevelGear') -> '_6165.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6165.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2097.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_6167.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6167.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_planetary_gear_set(self, design_entity: '_2098.PlanetaryGearSet') -> '_6180.PlanetaryGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6180.PlanetaryGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_spiral_bevel_gear(self, design_entity: '_2099.SpiralBevelGear') -> '_6198.SpiralBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6198.SpiralBevelGearLoadCase)(method_result) if method_result else None

    def inputs_for_spiral_bevel_gear_set(self, design_entity: '_2100.SpiralBevelGearSet') -> '_6200.SpiralBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6200.SpiralBevelGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_diff_gear(self, design_entity: '_2101.StraightBevelDiffGear') -> '_6205.StraightBevelDiffGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6205.StraightBevelDiffGearLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_diff_gear_set(self, design_entity: '_2102.StraightBevelDiffGearSet') -> '_6207.StraightBevelDiffGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6207.StraightBevelDiffGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_gear(self, design_entity: '_2103.StraightBevelGear') -> '_6208.StraightBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6208.StraightBevelGearLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_gear_set(self, design_entity: '_2104.StraightBevelGearSet') -> '_6210.StraightBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6210.StraightBevelGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_planet_gear(self, design_entity: '_2105.StraightBevelPlanetGear') -> '_6211.StraightBevelPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6211.StraightBevelPlanetGearLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_sun_gear(self, design_entity: '_2106.StraightBevelSunGear') -> '_6212.StraightBevelSunGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6212.StraightBevelSunGearLoadCase)(method_result) if method_result else None

    def inputs_for_worm_gear(self, design_entity: '_2107.WormGear') -> '_6229.WormGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6229.WormGearLoadCase)(method_result) if method_result else None

    def inputs_for_worm_gear_set(self, design_entity: '_2108.WormGearSet') -> '_6231.WormGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6231.WormGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_zerol_bevel_gear(self, design_entity: '_2109.ZerolBevelGear') -> '_6232.ZerolBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6232.ZerolBevelGearLoadCase)(method_result) if method_result else None

    def inputs_for_zerol_bevel_gear_set(self, design_entity: '_2110.ZerolBevelGearSet') -> '_6234.ZerolBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6234.ZerolBevelGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_part_to_part_shear_coupling(self, design_entity: '_2139.PartToPartShearCoupling') -> '_6178.PartToPartShearCouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6178.PartToPartShearCouplingLoadCase)(method_result) if method_result else None

    def inputs_for_part_to_part_shear_coupling_half(self, design_entity: '_2140.PartToPartShearCouplingHalf') -> '_6177.PartToPartShearCouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6177.PartToPartShearCouplingHalfLoadCase)(method_result) if method_result else None

    def inputs_for_belt_drive(self, design_entity: '_2128.BeltDrive') -> '_6076.BeltDriveLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6076.BeltDriveLoadCase)(method_result) if method_result else None

    def inputs_for_clutch(self, design_entity: '_2130.Clutch') -> '_6089.ClutchLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6089.ClutchLoadCase)(method_result) if method_result else None

    def inputs_for_clutch_half(self, design_entity: '_2131.ClutchHalf') -> '_6088.ClutchHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6088.ClutchHalfLoadCase)(method_result) if method_result else None

    def inputs_for_concept_coupling(self, design_entity: '_2133.ConceptCoupling') -> '_6094.ConceptCouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6094.ConceptCouplingLoadCase)(method_result) if method_result else None

    def inputs_for_concept_coupling_half(self, design_entity: '_2134.ConceptCouplingHalf') -> '_6093.ConceptCouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6093.ConceptCouplingHalfLoadCase)(method_result) if method_result else None

    def inputs_for_coupling(self, design_entity: '_2135.Coupling') -> '_6107.CouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6107.CouplingLoadCase)(method_result) if method_result else None

    def inputs_for_coupling_half(self, design_entity: '_2136.CouplingHalf') -> '_6106.CouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6106.CouplingHalfLoadCase)(method_result) if method_result else None

    def inputs_for_cvt(self, design_entity: '_2137.CVT') -> '_6109.CVTLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6109.CVTLoadCase)(method_result) if method_result else None

    def inputs_for_cvt_pulley(self, design_entity: '_2138.CVTPulley') -> '_6110.CVTPulleyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6110.CVTPulleyLoadCase)(method_result) if method_result else None

    def inputs_for_pulley(self, design_entity: '_2141.Pulley') -> '_6187.PulleyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6187.PulleyLoadCase)(method_result) if method_result else None

    def inputs_for_shaft_hub_connection(self, design_entity: '_2149.ShaftHubConnection') -> '_6193.ShaftHubConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6193.ShaftHubConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_rolling_ring(self, design_entity: '_2147.RollingRing') -> '_6191.RollingRingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6191.RollingRingLoadCase)(method_result) if method_result else None

    def inputs_for_rolling_ring_assembly(self, design_entity: '_2148.RollingRingAssembly') -> '_6189.RollingRingAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6189.RollingRingAssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_spring_damper(self, design_entity: '_2150.SpringDamper') -> '_6203.SpringDamperLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6203.SpringDamperLoadCase)(method_result) if method_result else None

    def inputs_for_spring_damper_half(self, design_entity: '_2151.SpringDamperHalf') -> '_6202.SpringDamperHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6202.SpringDamperHalfLoadCase)(method_result) if method_result else None

    def inputs_for_synchroniser(self, design_entity: '_2152.Synchroniser') -> '_6214.SynchroniserLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6214.SynchroniserLoadCase)(method_result) if method_result else None

    def inputs_for_synchroniser_half(self, design_entity: '_2154.SynchroniserHalf') -> '_6213.SynchroniserHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6213.SynchroniserHalfLoadCase)(method_result) if method_result else None

    def inputs_for_synchroniser_part(self, design_entity: '_2155.SynchroniserPart') -> '_6215.SynchroniserPartLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6215.SynchroniserPartLoadCase)(method_result) if method_result else None

    def inputs_for_synchroniser_sleeve(self, design_entity: '_2156.SynchroniserSleeve') -> '_6216.SynchroniserSleeveLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6216.SynchroniserSleeveLoadCase)(method_result) if method_result else None

    def inputs_for_torque_converter(self, design_entity: '_2157.TorqueConverter') -> '_6220.TorqueConverterLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6220.TorqueConverterLoadCase)(method_result) if method_result else None

    def inputs_for_torque_converter_pump(self, design_entity: '_2158.TorqueConverterPump') -> '_6221.TorqueConverterPumpLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6221.TorqueConverterPumpLoadCase)(method_result) if method_result else None

    def inputs_for_torque_converter_turbine(self, design_entity: '_2160.TorqueConverterTurbine') -> '_6222.TorqueConverterTurbineLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6222.TorqueConverterTurbineLoadCase)(method_result) if method_result else None

    def inputs_for_cvt_belt_connection(self, design_entity: '_1852.CVTBeltConnection') -> '_6108.CVTBeltConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6108.CVTBeltConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_belt_connection(self, design_entity: '_1847.BeltConnection') -> '_6075.BeltConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6075.BeltConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_coaxial_connection(self, design_entity: '_1848.CoaxialConnection') -> '_6090.CoaxialConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6090.CoaxialConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_connection(self, design_entity: '_1851.Connection') -> '_6103.ConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6103.ConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_inter_mountable_component_connection(self, design_entity: '_1860.InterMountableComponentConnection') -> '_6158.InterMountableComponentConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6158.InterMountableComponentConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_planetary_connection(self, design_entity: '_1863.PlanetaryConnection') -> '_6179.PlanetaryConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6179.PlanetaryConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_rolling_ring_connection(self, design_entity: '_1867.RollingRingConnection') -> '_6190.RollingRingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6190.RollingRingConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_shaft_to_mountable_component_connection(self, design_entity: '_1871.ShaftToMountableComponentConnection') -> '_6195.ShaftToMountableComponentConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6195.ShaftToMountableComponentConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_differential_gear_mesh(self, design_entity: '_1877.BevelDifferentialGearMesh') -> '_6078.BevelDifferentialGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6078.BevelDifferentialGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_concept_gear_mesh(self, design_entity: '_1881.ConceptGearMesh') -> '_6096.ConceptGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6096.ConceptGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_face_gear_mesh(self, design_entity: '_1887.FaceGearMesh') -> '_6134.FaceGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6134.FaceGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1901.StraightBevelDiffGearMesh') -> '_6206.StraightBevelDiffGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6206.StraightBevelDiffGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_gear_mesh(self, design_entity: '_1879.BevelGearMesh') -> '_6083.BevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6083.BevelGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_conical_gear_mesh(self, design_entity: '_1883.ConicalGearMesh') -> '_6100.ConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6100.ConicalGearMeshLoadCase)(method_result) if method_result else None
