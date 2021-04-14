'''_2538.py

ClutchCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2253
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2381
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2554
from mastapy._internal.python_net import python_net_import

_CLUTCH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ClutchCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchCompoundSystemDeflection',)


class ClutchCompoundSystemDeflection(_2554.CouplingCompoundSystemDeflection):
    '''ClutchCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2253.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.Clutch)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2253.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2381.ClutchSystemDeflection]':
        '''List[ClutchSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2381.ClutchSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2381.ClutchSystemDeflection]':
        '''List[ClutchSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2381.ClutchSystemDeflection))
        return value
