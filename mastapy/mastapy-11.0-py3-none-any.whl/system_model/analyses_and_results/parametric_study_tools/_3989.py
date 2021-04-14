'''_3989.py

ConceptGearSetParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2197
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6478
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3988, _3987, _4025
from mastapy.system_model.analyses_and_results.system_deflections import _2389
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ConceptGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetParametricStudyTool',)


class ConceptGearSetParametricStudyTool(_4025.GearSetParametricStudyTool):
    '''ConceptGearSetParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2197.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2197.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6478.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6478.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def concept_gears_parametric_study_tool(self) -> 'List[_3988.ConceptGearParametricStudyTool]':
        '''List[ConceptGearParametricStudyTool]: 'ConceptGearsParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsParametricStudyTool, constructor.new(_3988.ConceptGearParametricStudyTool))
        return value

    @property
    def concept_meshes_parametric_study_tool(self) -> 'List[_3987.ConceptGearMeshParametricStudyTool]':
        '''List[ConceptGearMeshParametricStudyTool]: 'ConceptMeshesParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesParametricStudyTool, constructor.new(_3987.ConceptGearMeshParametricStudyTool))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2389.ConceptGearSetSystemDeflection]':
        '''List[ConceptGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2389.ConceptGearSetSystemDeflection))
        return value
