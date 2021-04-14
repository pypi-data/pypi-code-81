'''_5280.py

ShaftCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2158
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5142
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5186
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ShaftCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundMultibodyDynamicsAnalysis',)


class ShaftCompoundMultibodyDynamicsAnalysis(_5186.AbstractShaftCompoundMultibodyDynamicsAnalysis):
    '''ShaftCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2158.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2158.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5142.ShaftMultibodyDynamicsAnalysis]':
        '''List[ShaftMultibodyDynamicsAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5142.ShaftMultibodyDynamicsAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundMultibodyDynamicsAnalysis]':
        '''List[ShaftCompoundMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5142.ShaftMultibodyDynamicsAnalysis]':
        '''List[ShaftMultibodyDynamicsAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5142.ShaftMultibodyDynamicsAnalysis))
        return value
