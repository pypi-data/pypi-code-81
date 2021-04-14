'''_2216.py

KlingelnbergCycloPalloidSpiralBevelGearSet
'''


from typing import List

from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _905
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2215, _2212
from mastapy.system_model.connections_and_sockets.gears import _2000
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSet',)


class KlingelnbergCycloPalloidSpiralBevelGearSet(_2212.KlingelnbergCycloPalloidConicalGearSet):
    '''KlingelnbergCycloPalloidSpiralBevelGearSet

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def klingelnberg_conical_gear_set_design(self) -> '_905.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'KlingelnbergConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_905.KlingelnbergCycloPalloidSpiralBevelGearSetDesign)(self.wrapped.KlingelnbergConicalGearSetDesign) if self.wrapped.KlingelnbergConicalGearSetDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_905.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'KlingelnbergCycloPalloidSpiralBevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_905.KlingelnbergCycloPalloidSpiralBevelGearSetDesign)(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSetDesign) if self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSetDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears(self) -> 'List[_2215.KlingelnbergCycloPalloidSpiralBevelGear]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGear]: 'KlingelnbergCycloPalloidSpiralBevelGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGears, constructor.new(_2215.KlingelnbergCycloPalloidSpiralBevelGear))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes(self) -> 'List[_2000.KlingelnbergCycloPalloidSpiralBevelGearMesh]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMesh]: 'KlingelnbergCycloPalloidSpiralBevelMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshes, constructor.new(_2000.KlingelnbergCycloPalloidSpiralBevelGearMesh))
        return value
