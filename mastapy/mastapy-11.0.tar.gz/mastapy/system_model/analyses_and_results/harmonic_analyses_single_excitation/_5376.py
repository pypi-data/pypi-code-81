'''_5376.py

CVTPulleyHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.couplings import _2262
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5423
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'CVTPulleyHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyHarmonicAnalysisOfSingleExcitation',)


class CVTPulleyHarmonicAnalysisOfSingleExcitation(_5423.PulleyHarmonicAnalysisOfSingleExcitation):
    '''CVTPulleyHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2262.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2262.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
