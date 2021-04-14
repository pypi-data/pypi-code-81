'''_3891.py

HypoidGearCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2209
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3760
from mastapy.system_model.analyses_and_results.power_flows.compound import _3833
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'HypoidGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearCompoundPowerFlow',)


class HypoidGearCompoundPowerFlow(_3833.AGMAGleasonConicalGearCompoundPowerFlow):
    '''HypoidGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2209.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2209.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3760.HypoidGearPowerFlow]':
        '''List[HypoidGearPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3760.HypoidGearPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3760.HypoidGearPowerFlow]':
        '''List[HypoidGearPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3760.HypoidGearPowerFlow))
        return value
