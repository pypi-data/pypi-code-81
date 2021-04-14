'''_4124.py

BoltCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2120
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3978
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4130
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'BoltCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundParametricStudyTool',)


class BoltCompoundParametricStudyTool(_4130.ComponentCompoundParametricStudyTool):
    '''BoltCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2120.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3978.BoltParametricStudyTool]':
        '''List[BoltParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3978.BoltParametricStudyTool))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3978.BoltParametricStudyTool]':
        '''List[BoltParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3978.BoltParametricStudyTool))
        return value
