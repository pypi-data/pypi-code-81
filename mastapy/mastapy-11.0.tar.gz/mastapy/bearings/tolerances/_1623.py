'''_1623.py

RoundnessSpecification
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.tolerances import _1624, _1629, _1620
from mastapy.utility import _1344
from mastapy._internal.python_net import python_net_import

_ROUNDNESS_SPECIFICATION = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'RoundnessSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('RoundnessSpecification',)


class RoundnessSpecification(_1344.IndependentReportablePropertiesBase['RoundnessSpecification']):
    '''RoundnessSpecification

    This is a mastapy class.
    '''

    TYPE = _ROUNDNESS_SPECIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RoundnessSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_deviation_from_round(self) -> 'float':
        '''float: 'MaximumDeviationFromRound' is the original name of this property.'''

        return self.wrapped.MaximumDeviationFromRound

    @maximum_deviation_from_round.setter
    def maximum_deviation_from_round(self, value: 'float'):
        self.wrapped.MaximumDeviationFromRound = float(value) if value else 0.0

    @property
    def angle_of_first_max_deviation_from_round(self) -> 'float':
        '''float: 'AngleOfFirstMaxDeviationFromRound' is the original name of this property.'''

        return self.wrapped.AngleOfFirstMaxDeviationFromRound

    @angle_of_first_max_deviation_from_round.setter
    def angle_of_first_max_deviation_from_round(self, value: 'float'):
        self.wrapped.AngleOfFirstMaxDeviationFromRound = float(value) if value else 0.0

    @property
    def number_of_lobes(self) -> 'int':
        '''int: 'NumberOfLobes' is the original name of this property.'''

        return self.wrapped.NumberOfLobes

    @number_of_lobes.setter
    def number_of_lobes(self, value: 'int'):
        self.wrapped.NumberOfLobes = int(value) if value else 0

    @property
    def specification_type(self) -> '_1624.RoundnessSpecificationType':
        '''RoundnessSpecificationType: 'SpecificationType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SpecificationType)
        return constructor.new(_1624.RoundnessSpecificationType)(value) if value else None

    @specification_type.setter
    def specification_type(self, value: '_1624.RoundnessSpecificationType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SpecificationType = value

    @property
    def type_of_fit(self) -> '_1629.TypeOfFit':
        '''TypeOfFit: 'TypeOfFit' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.TypeOfFit)
        return constructor.new(_1629.TypeOfFit)(value) if value else None

    @type_of_fit.setter
    def type_of_fit(self, value: '_1629.TypeOfFit'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TypeOfFit = value

    @property
    def roundness_distribution(self) -> 'List[_1620.RaceRoundnessAtAngle]':
        '''List[RaceRoundnessAtAngle]: 'RoundnessDistribution' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RoundnessDistribution, constructor.new(_1620.RaceRoundnessAtAngle))
        return value
