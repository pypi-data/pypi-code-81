'''_3582.py

ClutchCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2253
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3452
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3598
from mastapy._internal.python_net import python_net_import

_CLUTCH_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ClutchCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchCompoundStabilityAnalysis',)


class ClutchCompoundStabilityAnalysis(_3598.CouplingCompoundStabilityAnalysis):
    '''ClutchCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2253.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.Clutch)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2253.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3452.ClutchStabilityAnalysis]':
        '''List[ClutchStabilityAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3452.ClutchStabilityAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3452.ClutchStabilityAnalysis]':
        '''List[ClutchStabilityAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3452.ClutchStabilityAnalysis))
        return value
