'''_7106.py

GuideDxfModelCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2132
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6975
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7070
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'GuideDxfModelCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundAdvancedSystemDeflection',)


class GuideDxfModelCompoundAdvancedSystemDeflection(_7070.ComponentCompoundAdvancedSystemDeflection):
    '''GuideDxfModelCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2132.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2132.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6975.GuideDxfModelAdvancedSystemDeflection]':
        '''List[GuideDxfModelAdvancedSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6975.GuideDxfModelAdvancedSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6975.GuideDxfModelAdvancedSystemDeflection]':
        '''List[GuideDxfModelAdvancedSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6975.GuideDxfModelAdvancedSystemDeflection))
        return value
