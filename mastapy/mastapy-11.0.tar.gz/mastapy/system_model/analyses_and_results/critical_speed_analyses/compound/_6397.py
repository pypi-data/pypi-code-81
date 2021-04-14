'''_6397.py

PlanetCarrierCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2146
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6268
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6389
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'PlanetCarrierCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundCriticalSpeedAnalysis',)


class PlanetCarrierCompoundCriticalSpeedAnalysis(_6389.MountableComponentCompoundCriticalSpeedAnalysis):
    '''PlanetCarrierCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2146.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2146.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6268.PlanetCarrierCriticalSpeedAnalysis]':
        '''List[PlanetCarrierCriticalSpeedAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6268.PlanetCarrierCriticalSpeedAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6268.PlanetCarrierCriticalSpeedAnalysis]':
        '''List[PlanetCarrierCriticalSpeedAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6268.PlanetCarrierCriticalSpeedAnalysis))
        return value
