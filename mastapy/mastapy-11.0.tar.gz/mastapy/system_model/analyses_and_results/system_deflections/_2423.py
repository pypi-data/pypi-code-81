'''_2423.py

FEPartSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2130
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6523
from mastapy.system_model.analyses_and_results.power_flows import _3753
from mastapy.nodal_analysis.component_mode_synthesis import _203
from mastapy.nodal_analysis import _72
from mastapy.math_utility.measured_vectors import _1326, _1322
from mastapy.system_model.fe import _2087
from mastapy.system_model.analyses_and_results.system_deflections import _2359
from mastapy._internal.python_net import python_net_import

_FE_PART_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'FEPartSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartSystemDeflection',)


class FEPartSystemDeflection(_2359.AbstractShaftOrHousingSystemDeflection):
    '''FEPartSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FE_PART_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2130.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6523.FEPartLoadCase':
        '''FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6523.FEPartLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3753.FEPartPowerFlow':
        '''FEPartPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3753.FEPartPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def full_fe_results(self) -> '_203.StaticCMSResults':
        '''StaticCMSResults: 'FullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_203.StaticCMSResults)(self.wrapped.FullFEResults) if self.wrapped.FullFEResults else None

    @property
    def stiffness_in_world_coordinate_system_mn_rad(self) -> '_72.NodalMatrix':
        '''NodalMatrix: 'StiffnessInWorldCoordinateSystemMNRad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_72.NodalMatrix)(self.wrapped.StiffnessInWorldCoordinateSystemMNRad) if self.wrapped.StiffnessInWorldCoordinateSystemMNRad else None

    @property
    def mass_in_world_coordinate_system_mn_rad_s_kg(self) -> '_72.NodalMatrix':
        '''NodalMatrix: 'MassInWorldCoordinateSystemMNRadSKg' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_72.NodalMatrix)(self.wrapped.MassInWorldCoordinateSystemMNRadSKg) if self.wrapped.MassInWorldCoordinateSystemMNRadSKg else None

    @property
    def planetaries(self) -> 'List[FEPartSystemDeflection]':
        '''List[FEPartSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartSystemDeflection))
        return value

    @property
    def applied_internal_forces_in_world_coordinate_system(self) -> 'List[_1326.VectorWithLinearAndAngularComponents]':
        '''List[VectorWithLinearAndAngularComponents]: 'AppliedInternalForcesInWorldCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AppliedInternalForcesInWorldCoordinateSystem, constructor.new(_1326.VectorWithLinearAndAngularComponents))
        return value

    @property
    def node_results_in_shaft_coordinate_system(self) -> 'List[_1322.ForceAndDisplacementResults]':
        '''List[ForceAndDisplacementResults]: 'NodeResultsInShaftCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.NodeResultsInShaftCoordinateSystem, constructor.new(_1322.ForceAndDisplacementResults))
        return value

    @property
    def export(self) -> '_2087.SystemDeflectionFEExportOptions':
        '''SystemDeflectionFEExportOptions: 'Export' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2087.SystemDeflectionFEExportOptions)(self.wrapped.Export) if self.wrapped.Export else None

    def export_displacements(self):
        ''' 'ExportDisplacements' is the original name of this method.'''

        self.wrapped.ExportDisplacements()

    def export_forces(self):
        ''' 'ExportForces' is the original name of this method.'''

        self.wrapped.ExportForces()
