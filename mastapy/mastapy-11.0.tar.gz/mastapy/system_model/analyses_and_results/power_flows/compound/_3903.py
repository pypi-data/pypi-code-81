'''_3903.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2216
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3901, _3902, _3897
from mastapy.system_model.analyses_and_results.power_flows import _3771
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow(_3897.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2216.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2216.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2216.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2216.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_power_flow(self) -> 'List[_3901.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundPowerFlow, constructor.new(_3901.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_power_flow(self) -> 'List[_3902.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundPowerFlow, constructor.new(_3902.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3771.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3771.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3771.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3771.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow))
        return value
