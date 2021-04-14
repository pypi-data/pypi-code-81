'''_2466.py

RootAssemblySystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2151
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2491, _2498, _2384, _2365
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6915
from mastapy.system_model.analyses_and_results.power_flows import _3793
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'RootAssemblySystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblySystemDeflection',)


class RootAssemblySystemDeflection(_2365.AssemblySystemDeflection):
    '''RootAssemblySystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblySystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2151.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2151.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def system_deflection_inputs(self) -> '_2491.SystemDeflection':
        '''SystemDeflection: 'SystemDeflectionInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2491.SystemDeflection.TYPE not in self.wrapped.SystemDeflectionInputs.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_inputs to SystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionInputs.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionInputs.__class__)(self.wrapped.SystemDeflectionInputs) if self.wrapped.SystemDeflectionInputs else None

    @property
    def power_flow_results(self) -> '_3793.RootAssemblyPowerFlow':
        '''RootAssemblyPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3793.RootAssemblyPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def shaft_deflection_results(self) -> 'List[_2384.ConcentricPartGroupCombinationSystemDeflectionResults]':
        '''List[ConcentricPartGroupCombinationSystemDeflectionResults]: 'ShaftDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftDeflectionResults, constructor.new(_2384.ConcentricPartGroupCombinationSystemDeflectionResults))
        return value
