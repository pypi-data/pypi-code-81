'''_4228.py

WormGearCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2226
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4100
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4163
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'WormGearCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearCompoundParametricStudyTool',)


class WormGearCompoundParametricStudyTool(_4163.GearCompoundParametricStudyTool):
    '''WormGearCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2226.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2226.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4100.WormGearParametricStudyTool]':
        '''List[WormGearParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4100.WormGearParametricStudyTool))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4100.WormGearParametricStudyTool]':
        '''List[WormGearParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4100.WormGearParametricStudyTool))
        return value
