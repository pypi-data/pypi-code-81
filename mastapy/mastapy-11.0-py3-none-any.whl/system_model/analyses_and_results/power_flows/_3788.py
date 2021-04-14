'''_3788.py

RingPinsPowerFlow
'''


from mastapy.system_model.part_model.cycloidal import _2245
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6581
from mastapy.system_model.analyses_and_results.power_flows import _3774
from mastapy._internal.python_net import python_net_import

_RING_PINS_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'RingPinsPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsPowerFlow',)


class RingPinsPowerFlow(_3774.MountableComponentPowerFlow):
    '''RingPinsPowerFlow

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2245.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2245.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6581.RingPinsLoadCase':
        '''RingPinsLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6581.RingPinsLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
