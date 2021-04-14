'''_5945.py

ConceptGearDynamicAnalysis
'''


from mastapy.system_model.part_model.gears import _2196
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6476
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5975
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ConceptGearDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearDynamicAnalysis',)


class ConceptGearDynamicAnalysis(_5975.GearDynamicAnalysis):
    '''ConceptGearDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2196.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6476.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6476.ConceptGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
