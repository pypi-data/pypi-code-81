'''_6373.py

GuideDxfModelCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2132
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6244
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6337
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'GuideDxfModelCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundCriticalSpeedAnalysis',)


class GuideDxfModelCompoundCriticalSpeedAnalysis(_6337.ComponentCompoundCriticalSpeedAnalysis):
    '''GuideDxfModelCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundCriticalSpeedAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_6244.GuideDxfModelCriticalSpeedAnalysis]':
        '''List[GuideDxfModelCriticalSpeedAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6244.GuideDxfModelCriticalSpeedAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6244.GuideDxfModelCriticalSpeedAnalysis]':
        '''List[GuideDxfModelCriticalSpeedAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6244.GuideDxfModelCriticalSpeedAnalysis))
        return value
