'''_4036.py

KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2214
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6555
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4035, _4034, _4033
from mastapy.system_model.analyses_and_results.system_deflections import _2438
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool',)


class KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool(_4033.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool):
    '''KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2214.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2214.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6555.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6555.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_parametric_study_tool(self) -> 'List[_4035.KlingelnbergCycloPalloidHypoidGearParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidGearsParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsParametricStudyTool, constructor.new(_4035.KlingelnbergCycloPalloidHypoidGearParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_parametric_study_tool(self) -> 'List[_4034.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidMeshesParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesParametricStudyTool, constructor.new(_4034.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2438.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2438.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection))
        return value
