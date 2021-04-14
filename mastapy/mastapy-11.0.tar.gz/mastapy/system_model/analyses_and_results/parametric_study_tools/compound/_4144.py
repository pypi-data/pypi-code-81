'''_4144.py

CouplingHalfCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.analyses_and_results.parametric_study_tools import _3996
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4182
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'CouplingHalfCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfCompoundParametricStudyTool',)


class CouplingHalfCompoundParametricStudyTool(_4182.MountableComponentCompoundParametricStudyTool):
    '''CouplingHalfCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_3996.CouplingHalfParametricStudyTool]':
        '''List[CouplingHalfParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3996.CouplingHalfParametricStudyTool))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_3996.CouplingHalfParametricStudyTool]':
        '''List[CouplingHalfParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3996.CouplingHalfParametricStudyTool))
        return value
