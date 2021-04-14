'''_4163.py

GearCompoundParametricStudyTool
'''


from typing import List

from mastapy.gears.rating import _319
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _333
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _406
from mastapy.gears.rating.cylindrical import _413
from mastapy.gears.rating.conical import _486
from mastapy.gears.rating.concept import _496
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4024
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4182
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'GearCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundParametricStudyTool',)


class GearCompoundParametricStudyTool(_4182.MountableComponentCompoundParametricStudyTool):
    '''GearCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_duty_cycle_results(self) -> '_319.GearDutyCycleRating':
        '''GearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _319.GearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to GearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None

    @property
    def gear_duty_cycle_results_of_type_worm_gear_duty_cycle_rating(self) -> '_333.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _333.WormGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to WormGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None

    @property
    def gear_duty_cycle_results_of_type_face_gear_duty_cycle_rating(self) -> '_406.FaceGearDutyCycleRating':
        '''FaceGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _406.FaceGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to FaceGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None

    @property
    def gear_duty_cycle_results_of_type_cylindrical_gear_duty_cycle_rating(self) -> '_413.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _413.CylindricalGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to CylindricalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None

    @property
    def gear_duty_cycle_results_of_type_conical_gear_duty_cycle_rating(self) -> '_486.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _486.ConicalGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to ConicalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None

    @property
    def gear_duty_cycle_results_of_type_concept_gear_duty_cycle_rating(self) -> '_496.ConceptGearDutyCycleRating':
        '''ConceptGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _496.ConceptGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to ConceptGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None

    @property
    def component_analysis_cases(self) -> 'List[_4024.GearParametricStudyTool]':
        '''List[GearParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4024.GearParametricStudyTool))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_4024.GearParametricStudyTool]':
        '''List[GearParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4024.GearParametricStudyTool))
        return value
