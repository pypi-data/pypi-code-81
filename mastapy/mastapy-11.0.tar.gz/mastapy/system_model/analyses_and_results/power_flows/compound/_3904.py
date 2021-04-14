'''_3904.py

MassDiscCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2139
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3772
from mastapy.system_model.analyses_and_results.power_flows.compound import _3951
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'MassDiscCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundPowerFlow',)


class MassDiscCompoundPowerFlow(_3951.VirtualComponentCompoundPowerFlow):
    '''MassDiscCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2139.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3772.MassDiscPowerFlow]':
        '''List[MassDiscPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3772.MassDiscPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3772.MassDiscPowerFlow]':
        '''List[MassDiscPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3772.MassDiscPowerFlow))
        return value
