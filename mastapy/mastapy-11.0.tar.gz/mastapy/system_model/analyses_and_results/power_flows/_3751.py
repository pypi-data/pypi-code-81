'''_3751.py

FaceGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2203
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6520
from mastapy.gears.rating.face import _409
from mastapy.system_model.analyses_and_results.power_flows import _3756
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'FaceGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearPowerFlow',)


class FaceGearPowerFlow(_3756.GearPowerFlow):
    '''FaceGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2203.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2203.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6520.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6520.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_409.FaceGearRating':
        '''FaceGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_409.FaceGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
