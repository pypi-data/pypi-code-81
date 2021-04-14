'''_4960.py

FEPartCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2130
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4808
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4906
from mastapy._internal.python_net import python_net_import

_FE_PART_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'FEPartCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartCompoundModalAnalysis',)


class FEPartCompoundModalAnalysis(_4906.AbstractShaftOrHousingCompoundModalAnalysis):
    '''FEPartCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _FE_PART_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartCompoundModalAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_4808.FEPartModalAnalysis]':
        '''List[FEPartModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4808.FEPartModalAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[FEPartCompoundModalAnalysis]':
        '''List[FEPartCompoundModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartCompoundModalAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4808.FEPartModalAnalysis]':
        '''List[FEPartModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4808.FEPartModalAnalysis))
        return value
