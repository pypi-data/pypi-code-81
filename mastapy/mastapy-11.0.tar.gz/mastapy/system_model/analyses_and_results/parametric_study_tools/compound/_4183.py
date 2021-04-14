'''_4183.py

OilSealCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2143
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4044
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4141
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'OilSealCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundParametricStudyTool',)


class OilSealCompoundParametricStudyTool(_4141.ConnectorCompoundParametricStudyTool):
    '''OilSealCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2143.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2143.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4044.OilSealParametricStudyTool]':
        '''List[OilSealParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4044.OilSealParametricStudyTool))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4044.OilSealParametricStudyTool]':
        '''List[OilSealParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4044.OilSealParametricStudyTool))
        return value
