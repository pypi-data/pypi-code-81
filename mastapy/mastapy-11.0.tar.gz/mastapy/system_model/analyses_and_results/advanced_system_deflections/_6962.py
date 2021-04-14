'''_6962.py

CylindricalGearSetAdvancedSystemDeflection
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical import _956, _967
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1028
from mastapy.system_model.part_model.gears import _2201, _2217
from mastapy.system_model.analyses_and_results.static_loads import _6500, _6571
from mastapy.gears.rating.cylindrical import _423
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6960, _6961, _6974
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CylindricalGearSetAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetAdvancedSystemDeflection',)


class CylindricalGearSetAdvancedSystemDeflection(_6974.GearSetAdvancedSystemDeflection):
    '''CylindricalGearSetAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_design(self) -> '_956.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _956.CylindricalGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def micro_geometry(self) -> '_1028.CylindricalGearSetMicroGeometry':
        '''CylindricalGearSetMicroGeometry: 'MicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1028.CylindricalGearSetMicroGeometry)(self.wrapped.MicroGeometry) if self.wrapped.MicroGeometry else None

    @property
    def assembly_design(self) -> '_2201.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2201.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6500.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6500.CylindricalGearSetLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to CylindricalGearSetLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_423.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_423.CylindricalGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_423.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_423.CylindricalGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def cylindrical_gears_advanced_system_deflection(self) -> 'List[_6960.CylindricalGearAdvancedSystemDeflection]':
        '''List[CylindricalGearAdvancedSystemDeflection]: 'CylindricalGearsAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsAdvancedSystemDeflection, constructor.new(_6960.CylindricalGearAdvancedSystemDeflection))
        return value

    @property
    def cylindrical_meshes_advanced_system_deflection(self) -> 'List[_6961.CylindricalGearMeshAdvancedSystemDeflection]':
        '''List[CylindricalGearMeshAdvancedSystemDeflection]: 'CylindricalMeshesAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesAdvancedSystemDeflection, constructor.new(_6961.CylindricalGearMeshAdvancedSystemDeflection))
        return value
