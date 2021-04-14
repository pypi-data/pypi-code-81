'''_2467.py

ShaftHubConnectionSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.couplings import _2273
from mastapy.system_model.analyses_and_results.static_loads import _6587
from mastapy.system_model.analyses_and_results.power_flows import _3794
from mastapy.detailed_rigid_connectors.rating import _1200
from mastapy.detailed_rigid_connectors.splines.ratings import (
    _1188, _1190, _1192, _1194,
    _1196
)
from mastapy._internal.cast_exception import CastException
from mastapy.detailed_rigid_connectors.keyed_joints.rating import _1206
from mastapy.detailed_rigid_connectors.interference_fits.rating import _1213
from mastapy.bearings.bearing_results import _1645
from mastapy.system_model.analyses_and_results.system_deflections.reporting import _2516
from mastapy.system_model.analyses_and_results.system_deflections import _2396
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ShaftHubConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionSystemDeflection',)


class ShaftHubConnectionSystemDeflection(_2396.ConnectorSystemDeflection):
    '''ShaftHubConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def node_pair_separations(self) -> 'List[float]':
        '''List[float]: 'NodePairSeparations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NodePairSeparations)
        return value

    @property
    def number_of_teeth_in_contact(self) -> 'int':
        '''int: 'NumberOfTeethInContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfTeethInContact

    @property
    def number_of_major_diameter_contacts(self) -> 'int':
        '''int: 'NumberOfMajorDiameterContacts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfMajorDiameterContacts

    @property
    def normal_deflection_right_flank(self) -> 'List[float]':
        '''List[float]: 'NormalDeflectionRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalDeflectionRightFlank)
        return value

    @property
    def normal_deflection_left_flank(self) -> 'List[float]':
        '''List[float]: 'NormalDeflectionLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalDeflectionLeftFlank)
        return value

    @property
    def normal_deflection_tooth_centre(self) -> 'List[float]':
        '''List[float]: 'NormalDeflectionToothCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalDeflectionToothCentre)
        return value

    @property
    def normal_stiffness_right_flank(self) -> 'List[float]':
        '''List[float]: 'NormalStiffnessRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalStiffnessRightFlank)
        return value

    @property
    def normal_stiffness_left_flank(self) -> 'List[float]':
        '''List[float]: 'NormalStiffnessLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalStiffnessLeftFlank)
        return value

    @property
    def normal_stiffness_tooth_centre(self) -> 'List[float]':
        '''List[float]: 'NormalStiffnessToothCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalStiffnessToothCentre)
        return value

    @property
    def normal_force_right_flank(self) -> 'List[float]':
        '''List[float]: 'NormalForceRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalForceRightFlank)
        return value

    @property
    def normal_force_left_flank(self) -> 'List[float]':
        '''List[float]: 'NormalForceLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalForceLeftFlank)
        return value

    @property
    def normal_force_tooth_centre(self) -> 'List[float]':
        '''List[float]: 'NormalForceToothCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalForceToothCentre)
        return value

    @property
    def tangential_force_right_flank(self) -> 'List[float]':
        '''List[float]: 'TangentialForceRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.TangentialForceRightFlank)
        return value

    @property
    def tangential_force_left_flank(self) -> 'List[float]':
        '''List[float]: 'TangentialForceLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.TangentialForceLeftFlank)
        return value

    @property
    def tangential_force_tooth_centre(self) -> 'List[float]':
        '''List[float]: 'TangentialForceToothCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.TangentialForceToothCentre)
        return value

    @property
    def node_radial_forces_on_inner(self) -> 'List[float]':
        '''List[float]: 'NodeRadialForcesOnInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NodeRadialForcesOnInner)
        return value

    @property
    def tangential_force_on_spline(self) -> 'float':
        '''float: 'TangentialForceOnSpline' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TangentialForceOnSpline

    @property
    def limiting_friction(self) -> 'float':
        '''float: 'LimitingFriction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LimitingFriction

    @property
    def will_spline_slip(self) -> 'bool':
        '''bool: 'WillSplineSlip' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WillSplineSlip

    @property
    def component_design(self) -> '_2273.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2273.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6587.ShaftHubConnectionLoadCase':
        '''ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6587.ShaftHubConnectionLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3794.ShaftHubConnectionPowerFlow':
        '''ShaftHubConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3794.ShaftHubConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def component_detailed_analysis(self) -> '_1200.ShaftHubConnectionRating':
        '''ShaftHubConnectionRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1200.ShaftHubConnectionRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to ShaftHubConnectionRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_agma6123_spline_joint_rating(self) -> '_1188.AGMA6123SplineJointRating':
        '''AGMA6123SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1188.AGMA6123SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to AGMA6123SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_din5466_spline_rating(self) -> '_1190.DIN5466SplineRating':
        '''DIN5466SplineRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1190.DIN5466SplineRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to DIN5466SplineRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_gbt17855_spline_joint_rating(self) -> '_1192.GBT17855SplineJointRating':
        '''GBT17855SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1192.GBT17855SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to GBT17855SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_sae_spline_joint_rating(self) -> '_1194.SAESplineJointRating':
        '''SAESplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1194.SAESplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SAESplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_spline_joint_rating(self) -> '_1196.SplineJointRating':
        '''SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1196.SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_keyway_rating(self) -> '_1206.KeywayRating':
        '''KeywayRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1206.KeywayRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to KeywayRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_interference_fit_rating(self) -> '_1213.InterferenceFitRating':
        '''InterferenceFitRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1213.InterferenceFitRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to InterferenceFitRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def stiffness_matrix_in_local_coordinate_system(self) -> '_1645.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'StiffnessMatrixInLocalCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1645.BearingStiffnessMatrixReporter)(self.wrapped.StiffnessMatrixInLocalCoordinateSystem) if self.wrapped.StiffnessMatrixInLocalCoordinateSystem else None

    @property
    def stiffness_matrix_in_unrotated_coordinate_system(self) -> '_1645.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'StiffnessMatrixInUnrotatedCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1645.BearingStiffnessMatrixReporter)(self.wrapped.StiffnessMatrixInUnrotatedCoordinateSystem) if self.wrapped.StiffnessMatrixInUnrotatedCoordinateSystem else None

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionSystemDeflection]':
        '''List[ShaftHubConnectionSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionSystemDeflection))
        return value

    @property
    def left_flank_contacts(self) -> 'List[_2516.SplineFlankContactReporting]':
        '''List[SplineFlankContactReporting]: 'LeftFlankContacts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LeftFlankContacts, constructor.new(_2516.SplineFlankContactReporting))
        return value

    @property
    def right_flank_contacts(self) -> 'List[_2516.SplineFlankContactReporting]':
        '''List[SplineFlankContactReporting]: 'RightFlankContacts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RightFlankContacts, constructor.new(_2516.SplineFlankContactReporting))
        return value

    @property
    def tip_contacts(self) -> 'List[_2516.SplineFlankContactReporting]':
        '''List[SplineFlankContactReporting]: 'TipContacts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TipContacts, constructor.new(_2516.SplineFlankContactReporting))
        return value
