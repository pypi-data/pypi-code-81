'''_4193.py

PulleyCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2265, _2262
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4064
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4144
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'PulleyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundParametricStudyTool',)


class PulleyCompoundParametricStudyTool(_4144.CouplingHalfCompoundParametricStudyTool):
    '''PulleyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2265.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2265.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4064.PulleyParametricStudyTool]':
        '''List[PulleyParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4064.PulleyParametricStudyTool))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4064.PulleyParametricStudyTool]':
        '''List[PulleyParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4064.PulleyParametricStudyTool))
        return value
