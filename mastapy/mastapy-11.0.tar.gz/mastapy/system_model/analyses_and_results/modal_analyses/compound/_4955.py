'''_4955.py

DatumCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2126
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4803
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4929
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'DatumCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundModalAnalysis',)


class DatumCompoundModalAnalysis(_4929.ComponentCompoundModalAnalysis):
    '''DatumCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2126.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2126.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4803.DatumModalAnalysis]':
        '''List[DatumModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4803.DatumModalAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4803.DatumModalAnalysis]':
        '''List[DatumModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4803.DatumModalAnalysis))
        return value
