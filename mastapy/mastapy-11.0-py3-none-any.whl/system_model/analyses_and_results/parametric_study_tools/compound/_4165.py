'''_4165.py

GearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.gears.rating import _323
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _336
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _410
from mastapy.gears.rating.cylindrical import _422
from mastapy.gears.rating.conical import _489
from mastapy.gears.rating.concept import _500
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4025
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4203
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'GearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundParametricStudyTool',)


class GearSetCompoundParametricStudyTool(_4203.SpecialisedAssemblyCompoundParametricStudyTool):
    '''GearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_duty_cycle_results(self) -> '_323.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _323.GearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to GearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None

    @property
    def gear_set_duty_cycle_results_of_type_worm_gear_set_duty_cycle_rating(self) -> '_336.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _336.WormGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None

    @property
    def gear_set_duty_cycle_results_of_type_face_gear_set_duty_cycle_rating(self) -> '_410.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _410.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None

    @property
    def gear_set_duty_cycle_results_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_422.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _422.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None

    @property
    def gear_set_duty_cycle_results_of_type_conical_gear_set_duty_cycle_rating(self) -> '_489.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _489.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None

    @property
    def gear_set_duty_cycle_results_of_type_concept_gear_set_duty_cycle_rating(self) -> '_500.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _500.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None

    @property
    def assembly_analysis_cases(self) -> 'List[_4025.GearSetParametricStudyTool]':
        '''List[GearSetParametricStudyTool]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4025.GearSetParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4025.GearSetParametricStudyTool]':
        '''List[GearSetParametricStudyTool]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4025.GearSetParametricStudyTool))
        return value
