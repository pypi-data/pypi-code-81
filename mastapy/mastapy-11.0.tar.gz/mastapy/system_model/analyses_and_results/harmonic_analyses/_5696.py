'''_5696.py

OilSealHarmonicAnalysis
'''


from mastapy.system_model.part_model import _2143
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6564
from mastapy.system_model.analyses_and_results.system_deflections import _2450
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5631
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'OilSealHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealHarmonicAnalysis',)


class OilSealHarmonicAnalysis(_5631.ConnectorHarmonicAnalysis):
    '''OilSealHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2143.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2143.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6564.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6564.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2450.OilSealSystemDeflection':
        '''OilSealSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2450.OilSealSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
