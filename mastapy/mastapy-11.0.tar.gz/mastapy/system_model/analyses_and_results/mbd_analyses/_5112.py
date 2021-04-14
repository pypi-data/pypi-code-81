'''_5112.py

KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2214
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6555
from mastapy.system_model.analyses_and_results.mbd_analyses import _5111, _5110, _5109
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis(_5109.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis.TYPE'):
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
    def gears(self) -> 'List[_5111.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5111.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_multibody_dynamics_analysis(self) -> 'List[_5111.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsMultibodyDynamicsAnalysis, constructor.new(_5111.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_multibody_dynamics_analysis(self) -> 'List[_5110.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesMultibodyDynamicsAnalysis, constructor.new(_5110.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis))
        return value
