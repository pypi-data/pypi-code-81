'''_3448.py

BoltedJointStabilityAnalysis
'''


from mastapy.system_model.part_model import _2121
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6466
from mastapy.system_model.analyses_and_results.stability_analyses import _3528
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'BoltedJointStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointStabilityAnalysis',)


class BoltedJointStabilityAnalysis(_3528.SpecialisedAssemblyStabilityAnalysis):
    '''BoltedJointStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2121.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6466.BoltedJointLoadCase':
        '''BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6466.BoltedJointLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
