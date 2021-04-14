'''_4157.py

ExternalCADModelCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2129
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4017
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4130
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ExternalCADModelCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundParametricStudyTool',)


class ExternalCADModelCompoundParametricStudyTool(_4130.ComponentCompoundParametricStudyTool):
    '''ExternalCADModelCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2129.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2129.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4017.ExternalCADModelParametricStudyTool]':
        '''List[ExternalCADModelParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4017.ExternalCADModelParametricStudyTool))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4017.ExternalCADModelParametricStudyTool]':
        '''List[ExternalCADModelParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4017.ExternalCADModelParametricStudyTool))
        return value
