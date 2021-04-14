'''_3663.py

SpringDamperCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2275
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3534
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3598
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'SpringDamperCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundStabilityAnalysis',)


class SpringDamperCompoundStabilityAnalysis(_3598.CouplingCompoundStabilityAnalysis):
    '''SpringDamperCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2275.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2275.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3534.SpringDamperStabilityAnalysis]':
        '''List[SpringDamperStabilityAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3534.SpringDamperStabilityAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3534.SpringDamperStabilityAnalysis]':
        '''List[SpringDamperStabilityAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3534.SpringDamperStabilityAnalysis))
        return value
