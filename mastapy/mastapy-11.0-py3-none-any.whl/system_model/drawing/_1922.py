'''_1922.py

AbstractSystemDeflectionViewable
'''


from mastapy.system_model.drawing import _1925, _1932
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2492
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3274
from mastapy.system_model.analyses_and_results.stability_analyses import _3535
from mastapy.system_model.analyses_and_results.rotor_dynamics import _3690
from mastapy.system_model.analyses_and_results.modal_analyses import _4831
from mastapy.system_model.analyses_and_results.mbd_analyses import _5117
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5674
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5968
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6221
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SYSTEM_DEFLECTION_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'AbstractSystemDeflectionViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractSystemDeflectionViewable',)


class AbstractSystemDeflectionViewable(_1932.PartAnalysisCaseWithContourViewable):
    '''AbstractSystemDeflectionViewable

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SYSTEM_DEFLECTION_VIEWABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractSystemDeflectionViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contour_draw_style(self) -> '_1925.ContourDrawStyle':
        '''ContourDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1925.ContourDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to ContourDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_system_deflection_draw_style(self) -> '_2492.SystemDeflectionDrawStyle':
        '''SystemDeflectionDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2492.SystemDeflectionDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to SystemDeflectionDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_steady_state_synchronous_response_draw_style(self) -> '_3274.SteadyStateSynchronousResponseDrawStyle':
        '''SteadyStateSynchronousResponseDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3274.SteadyStateSynchronousResponseDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to SteadyStateSynchronousResponseDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_stability_analysis_draw_style(self) -> '_3535.StabilityAnalysisDrawStyle':
        '''StabilityAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3535.StabilityAnalysisDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to StabilityAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_rotor_dynamics_draw_style(self) -> '_3690.RotorDynamicsDrawStyle':
        '''RotorDynamicsDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3690.RotorDynamicsDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to RotorDynamicsDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_modal_analysis_draw_style(self) -> '_4831.ModalAnalysisDrawStyle':
        '''ModalAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4831.ModalAnalysisDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to ModalAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_mbd_analysis_draw_style(self) -> '_5117.MBDAnalysisDrawStyle':
        '''MBDAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5117.MBDAnalysisDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to MBDAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_harmonic_analysis_draw_style(self) -> '_5674.HarmonicAnalysisDrawStyle':
        '''HarmonicAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5674.HarmonicAnalysisDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to HarmonicAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_dynamic_analysis_draw_style(self) -> '_5968.DynamicAnalysisDrawStyle':
        '''DynamicAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5968.DynamicAnalysisDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to DynamicAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_critical_speed_analysis_draw_style(self) -> '_6221.CriticalSpeedAnalysisDrawStyle':
        '''CriticalSpeedAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6221.CriticalSpeedAnalysisDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to CriticalSpeedAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def system_deflection_draw_style(self) -> '_2492.SystemDeflectionDrawStyle':
        '''SystemDeflectionDrawStyle: 'SystemDeflectionDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2492.SystemDeflectionDrawStyle)(self.wrapped.SystemDeflectionDrawStyle) if self.wrapped.SystemDeflectionDrawStyle else None

    def fe_results(self):
        ''' 'FEResults' is the original name of this method.'''

        self.wrapped.FEResults()
