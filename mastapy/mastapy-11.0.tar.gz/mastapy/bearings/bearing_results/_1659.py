'''_1659.py

LoadedNonLinearBearingResults
'''


from mastapy.materials.efficiency import (
    _265, _259, _261, _266,
    _257, _260
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_results import _1651
from mastapy._internal.python_net import python_net_import

_LOADED_NON_LINEAR_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedNonLinearBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedNonLinearBearingResults',)


class LoadedNonLinearBearingResults(_1651.LoadedBearingResults):
    '''LoadedNonLinearBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_NON_LINEAR_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedNonLinearBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def power_loss(self) -> '_265.PowerLoss':
        '''PowerLoss: 'PowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _265.PowerLoss.TYPE not in self.wrapped.PowerLoss.__class__.__mro__:
            raise CastException('Failed to cast power_loss to PowerLoss. Expected: {}.'.format(self.wrapped.PowerLoss.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerLoss.__class__)(self.wrapped.PowerLoss) if self.wrapped.PowerLoss else None

    @property
    def power_loss_of_type_independent_power_loss(self) -> '_259.IndependentPowerLoss':
        '''IndependentPowerLoss: 'PowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _259.IndependentPowerLoss.TYPE not in self.wrapped.PowerLoss.__class__.__mro__:
            raise CastException('Failed to cast power_loss to IndependentPowerLoss. Expected: {}.'.format(self.wrapped.PowerLoss.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerLoss.__class__)(self.wrapped.PowerLoss) if self.wrapped.PowerLoss else None

    @property
    def power_loss_of_type_load_and_speed_combined_power_loss(self) -> '_261.LoadAndSpeedCombinedPowerLoss':
        '''LoadAndSpeedCombinedPowerLoss: 'PowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _261.LoadAndSpeedCombinedPowerLoss.TYPE not in self.wrapped.PowerLoss.__class__.__mro__:
            raise CastException('Failed to cast power_loss to LoadAndSpeedCombinedPowerLoss. Expected: {}.'.format(self.wrapped.PowerLoss.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerLoss.__class__)(self.wrapped.PowerLoss) if self.wrapped.PowerLoss else None

    @property
    def resistive_torque(self) -> '_266.ResistiveTorque':
        '''ResistiveTorque: 'ResistiveTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _266.ResistiveTorque.TYPE not in self.wrapped.ResistiveTorque.__class__.__mro__:
            raise CastException('Failed to cast resistive_torque to ResistiveTorque. Expected: {}.'.format(self.wrapped.ResistiveTorque.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ResistiveTorque.__class__)(self.wrapped.ResistiveTorque) if self.wrapped.ResistiveTorque else None

    @property
    def resistive_torque_of_type_combined_resistive_torque(self) -> '_257.CombinedResistiveTorque':
        '''CombinedResistiveTorque: 'ResistiveTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _257.CombinedResistiveTorque.TYPE not in self.wrapped.ResistiveTorque.__class__.__mro__:
            raise CastException('Failed to cast resistive_torque to CombinedResistiveTorque. Expected: {}.'.format(self.wrapped.ResistiveTorque.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ResistiveTorque.__class__)(self.wrapped.ResistiveTorque) if self.wrapped.ResistiveTorque else None

    @property
    def resistive_torque_of_type_independent_resistive_torque(self) -> '_260.IndependentResistiveTorque':
        '''IndependentResistiveTorque: 'ResistiveTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _260.IndependentResistiveTorque.TYPE not in self.wrapped.ResistiveTorque.__class__.__mro__:
            raise CastException('Failed to cast resistive_torque to IndependentResistiveTorque. Expected: {}.'.format(self.wrapped.ResistiveTorque.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ResistiveTorque.__class__)(self.wrapped.ResistiveTorque) if self.wrapped.ResistiveTorque else None
