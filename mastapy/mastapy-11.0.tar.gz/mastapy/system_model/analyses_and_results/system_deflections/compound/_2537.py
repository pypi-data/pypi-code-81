'''_2537.py

BoltedJointCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2121
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2377
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2617
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'BoltedJointCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointCompoundSystemDeflection',)


class BoltedJointCompoundSystemDeflection(_2617.SpecialisedAssemblyCompoundSystemDeflection):
    '''BoltedJointCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2121.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2121.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2377.BoltedJointSystemDeflection]':
        '''List[BoltedJointSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2377.BoltedJointSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2377.BoltedJointSystemDeflection]':
        '''List[BoltedJointSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2377.BoltedJointSystemDeflection))
        return value
