'''_4176.py

KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2214
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4174, _4175, _4173
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4036
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool(_4173.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2214.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2214.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2214.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2214.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_parametric_study_tool(self) -> 'List[_4174.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundParametricStudyTool, constructor.new(_4174.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_parametric_study_tool(self) -> 'List[_4175.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundParametricStudyTool, constructor.new(_4175.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4036.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4036.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4036.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4036.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool))
        return value
