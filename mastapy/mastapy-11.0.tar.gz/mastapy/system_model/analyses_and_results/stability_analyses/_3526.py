'''_3526.py

ShaftStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2158
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6588
from mastapy.system_model.analyses_and_results.stability_analyses import _3469, _3431
from mastapy._internal.python_net import python_net_import

_SHAFT_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ShaftStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftStabilityAnalysis',)


class ShaftStabilityAnalysis(_3431.AbstractShaftStabilityAnalysis):
    '''ShaftStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftStabilityAnalysis.TYPE'):
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
    def component_load_case(self) -> '_6588.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6588.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ShaftStabilityAnalysis]':
        '''List[ShaftStabilityAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftStabilityAnalysis))
        return value

    @property
    def critical_speeds(self) -> 'List[_3469.CriticalSpeed]':
        '''List[CriticalSpeed]: 'CriticalSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CriticalSpeeds, constructor.new(_3469.CriticalSpeed))
        return value
