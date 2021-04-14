'''_3148.py

StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2223
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3146, _3147, _3056
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3018
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed',)


class StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed(_3056.BevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed):
    '''StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2223.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2223.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2223.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2223.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_gears_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3146.StraightBevelGearCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearCompoundSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelGearsCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundSteadyStateSynchronousResponseAtASpeed, constructor.new(_3146.StraightBevelGearCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_meshes_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3147.StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelMeshesCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundSteadyStateSynchronousResponseAtASpeed, constructor.new(_3147.StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3018.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3018.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3018.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3018.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value
