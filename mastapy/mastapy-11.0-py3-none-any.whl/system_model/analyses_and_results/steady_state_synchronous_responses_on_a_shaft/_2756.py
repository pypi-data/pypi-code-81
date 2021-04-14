'''_2756.py

StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _2221
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6601
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2757, _2755, _2666
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft',)


class StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft(_2666.BevelGearSetSteadyStateSynchronousResponseOnAShaft):
    '''StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2221.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2221.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6601.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6601.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_diff_gears_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2757.StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelDiffGearsSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsSteadyStateSynchronousResponseOnAShaft, constructor.new(_2757.StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def straight_bevel_diff_meshes_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2755.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelDiffMeshesSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesSteadyStateSynchronousResponseOnAShaft, constructor.new(_2755.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft))
        return value
