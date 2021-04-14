'''_750.py

PinionConcave
'''


from mastapy.gears.manufacturing.bevel import (
    _753, _748, _749, _751,
    _754, _755, _756
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel.basic_machine_settings import _770
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PINION_CONCAVE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'PinionConcave')


__docformat__ = 'restructuredtext en'
__all__ = ('PinionConcave',)


class PinionConcave(_0.APIBase):
    '''PinionConcave

    This is a mastapy class.
    '''

    TYPE = _PINION_CONCAVE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PinionConcave.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pinion_cutter_parameters_concave(self) -> '_753.PinionFinishMachineSettings':
        '''PinionFinishMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _753.PinionFinishMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionFinishMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConcave.__class__)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_bevel_generating_modified_roll_machine_settings(self) -> '_748.PinionBevelGeneratingModifiedRollMachineSettings':
        '''PinionBevelGeneratingModifiedRollMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _748.PinionBevelGeneratingModifiedRollMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionBevelGeneratingModifiedRollMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConcave.__class__)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_bevel_generating_tilt_machine_settings(self) -> '_749.PinionBevelGeneratingTiltMachineSettings':
        '''PinionBevelGeneratingTiltMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _749.PinionBevelGeneratingTiltMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionBevelGeneratingTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConcave.__class__)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_conical_machine_settings_specified(self) -> '_751.PinionConicalMachineSettingsSpecified':
        '''PinionConicalMachineSettingsSpecified: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _751.PinionConicalMachineSettingsSpecified.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionConicalMachineSettingsSpecified. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConcave.__class__)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_hypoid_formate_tilt_machine_settings(self) -> '_754.PinionHypoidFormateTiltMachineSettings':
        '''PinionHypoidFormateTiltMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _754.PinionHypoidFormateTiltMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionHypoidFormateTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConcave.__class__)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_hypoid_generating_tilt_machine_settings(self) -> '_755.PinionHypoidGeneratingTiltMachineSettings':
        '''PinionHypoidGeneratingTiltMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _755.PinionHypoidGeneratingTiltMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionHypoidGeneratingTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConcave.__class__)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_machine_settings_smt(self) -> '_756.PinionMachineSettingsSMT':
        '''PinionMachineSettingsSMT: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _756.PinionMachineSettingsSMT.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionMachineSettingsSMT. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConcave.__class__)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_concave_ob_configuration(self) -> '_770.BasicConicalGearMachineSettingsGenerated':
        '''BasicConicalGearMachineSettingsGenerated: 'PinionConcaveOBConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_770.BasicConicalGearMachineSettingsGenerated)(self.wrapped.PinionConcaveOBConfiguration) if self.wrapped.PinionConcaveOBConfiguration else None
