'''_2401.py

CVTPulleySystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2262
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3738
from mastapy.math_utility.measured_vectors import _1324
from mastapy.system_model.analyses_and_results.system_deflections import _2459
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CVTPulleySystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleySystemDeflection',)


class CVTPulleySystemDeflection(_2459.PulleySystemDeflection):
    '''CVTPulleySystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleySystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2262.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2262.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def power_flow_results(self) -> '_3738.CVTPulleyPowerFlow':
        '''CVTPulleyPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3738.CVTPulleyPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def fixed_sheave_contact_results(self) -> 'List[_1324.NodeResults]':
        '''List[NodeResults]: 'FixedSheaveContactResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FixedSheaveContactResults, constructor.new(_1324.NodeResults))
        return value

    @property
    def moving_sheave_contact_results(self) -> 'List[_1324.NodeResults]':
        '''List[NodeResults]: 'MovingSheaveContactResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MovingSheaveContactResults, constructor.new(_1324.NodeResults))
        return value
