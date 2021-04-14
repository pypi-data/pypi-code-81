'''_4990.py

PointLoadCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2148
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4843
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5026
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'PointLoadCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundModalAnalysis',)


class PointLoadCompoundModalAnalysis(_5026.VirtualComponentCompoundModalAnalysis):
    '''PointLoadCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2148.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2148.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4843.PointLoadModalAnalysis]':
        '''List[PointLoadModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4843.PointLoadModalAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4843.PointLoadModalAnalysis]':
        '''List[PointLoadModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4843.PointLoadModalAnalysis))
        return value
