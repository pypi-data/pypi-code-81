'''_2564.py

CylindricalGearCompoundSystemDeflection
'''


from typing import List

from mastapy.gears.rating.cylindrical import _413
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2200, _2202
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.system_deflections import _2413
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2576
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CylindricalGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearCompoundSystemDeflection',)


class CylindricalGearCompoundSystemDeflection(_2576.GearCompoundSystemDeflection):
    '''CylindricalGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_rating(self) -> '_413.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_413.CylindricalGearDutyCycleRating)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def cylindrical_duty_cycle_rating(self) -> '_413.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'CylindricalDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_413.CylindricalGearDutyCycleRating)(self.wrapped.CylindricalDutyCycleRating) if self.wrapped.CylindricalDutyCycleRating else None

    @property
    def component_design(self) -> '_2200.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.CylindricalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2413.CylindricalGearSystemDeflection]':
        '''List[CylindricalGearSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2413.CylindricalGearSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearCompoundSystemDeflection]':
        '''List[CylindricalGearCompoundSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearCompoundSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2413.CylindricalGearSystemDeflection]':
        '''List[CylindricalGearSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2413.CylindricalGearSystemDeflection))
        return value
