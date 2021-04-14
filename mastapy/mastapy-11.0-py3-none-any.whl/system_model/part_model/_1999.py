'''_1999.py

Assembly
'''


from typing import List, TypeVar, Optional

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _2027, _2008, _2004, _2007,
    _2020, _2034, _2033, _2028,
    _2030, _2000, _2001, _2006,
    _2011, _2012, _2015, _2016,
    _2017, _2024, _2025, _2026,
    _2031, _2036, _2038, _2039,
    _2040
)
from mastapy.system_model.part_model.gears import (
    _2108, _2095, _2104, _2086,
    _2084, _2112, _2097, _2073,
    _2074, _2075, _2076, _2077,
    _2078, _2079, _2080, _2081,
    _2082, _2083, _2085, _2087,
    _2088, _2089, _2090, _2092,
    _2094, _2096, _2098, _2099,
    _2100, _2101, _2102, _2103,
    _2105, _2106, _2107, _2109,
    _2110, _2111, _2113, _2114
)
from mastapy.system_model.part_model.couplings import (
    _2153, _2132, _2134, _2135,
    _2137, _2138, _2139, _2140,
    _2141, _2142, _2143, _2144,
    _2145, _2151, _2152, _2154,
    _2155, _2156, _2158, _2159,
    _2160, _2161, _2162, _2164
)
from mastapy.system_model.part_model.shaft_model import _2043
from mastapy.system_model.part_model.creation_options import (
    _2128, _2130, _2131, _2129
)
from mastapy.gears.gear_designs.creation_options import _883, _886
from mastapy.gears import _135
from mastapy.gears.gear_designs.bevel import _916
from mastapy.nodal_analysis import _1390
from mastapy.bearings import _1513, _1538
from mastapy._internal.python_net import python_net_import

_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')


__docformat__ = 'restructuredtext en'
__all__ = ('Assembly',)


class Assembly(_2000.AbstractAssembly):
    '''Assembly

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Assembly.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def face_width_of_widest_cylindrical_gear(self) -> 'float':
        '''float: 'FaceWidthOfWidestCylindricalGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FaceWidthOfWidestCylindricalGear

    @property
    def mass_of_gears(self) -> 'float':
        '''float: 'MassOfGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfGears

    @property
    def mass_of_bearings(self) -> 'float':
        '''float: 'MassOfBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfBearings

    @property
    def mass_of_shafts(self) -> 'float':
        '''float: 'MassOfShafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfShafts

    @property
    def mass_of_imported_fe_shafts(self) -> 'float':
        '''float: 'MassOfImportedFEShafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfImportedFEShafts

    @property
    def mass_of_imported_fe_housings(self) -> 'float':
        '''float: 'MassOfImportedFEHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfImportedFEHousings

    @property
    def mass_of_other_parts(self) -> 'float':
        '''float: 'MassOfOtherParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfOtherParts

    @property
    def smallest_number_of_teeth(self) -> 'int':
        '''int: 'SmallestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SmallestNumberOfTeeth

    @property
    def largest_number_of_teeth(self) -> 'int':
        '''int: 'LargestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LargestNumberOfTeeth

    @property
    def transverse_and_axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseAndAxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseAndAxialContactRatioRatingForNVH

    @property
    def transverse_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseContactRatioRatingForNVH

    @property
    def axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'AxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialContactRatioRatingForNVH

    @property
    def minimum_tip_thickness(self) -> 'float':
        '''float: 'MinimumTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumTipThickness

    @property
    def oil_level_specification(self) -> '_2027.OilLevelSpecification':
        '''OilLevelSpecification: 'OilLevelSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2027.OilLevelSpecification)(self.wrapped.OilLevelSpecification) if self.wrapped.OilLevelSpecification else None

    @property
    def components_with_unknown_scalar_mass(self) -> 'List[_2008.Component]':
        '''List[Component]: 'ComponentsWithUnknownScalarMass' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentsWithUnknownScalarMass, constructor.new(_2008.Component))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2108.StraightBevelGearSet]':
        '''List[StraightBevelGearSet]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2108.StraightBevelGearSet))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2095.HypoidGearSet]':
        '''List[HypoidGearSet]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2095.HypoidGearSet))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2104.SpiralBevelGearSet]':
        '''List[SpiralBevelGearSet]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2104.SpiralBevelGearSet))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2153.ShaftHubConnection]':
        '''List[ShaftHubConnection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2153.ShaftHubConnection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2086.CylindricalGearSet]':
        '''List[CylindricalGearSet]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2086.CylindricalGearSet))
        return value

    @property
    def conical_gear_sets(self) -> 'List[_2084.ConicalGearSet]':
        '''List[ConicalGearSet]: 'ConicalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConicalGearSets, constructor.new(_2084.ConicalGearSet))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2112.WormGearSet]':
        '''List[WormGearSet]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2112.WormGearSet))
        return value

    @property
    def klingelnberg_cyclo_palloid_gear_sets(self) -> 'List[_2097.KlingelnbergCycloPalloidConicalGearSet]':
        '''List[KlingelnbergCycloPalloidConicalGearSet]: 'KlingelnbergCycloPalloidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidGearSets, constructor.new(_2097.KlingelnbergCycloPalloidConicalGearSet))
        return value

    @property
    def shafts(self) -> 'List[_2043.Shaft]':
        '''List[Shaft]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2043.Shaft))
        return value

    @property
    def bearings(self) -> 'List[_2004.Bearing]':
        '''List[Bearing]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2004.Bearing))
        return value

    @property
    def bolted_joints(self) -> 'List[_2007.BoltedJoint]':
        '''List[BoltedJoint]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2007.BoltedJoint))
        return value

    @property
    def imported_fes(self) -> 'List[_2020.ImportedFEComponent]':
        '''List[ImportedFEComponent]: 'ImportedFEs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEs, constructor.new(_2020.ImportedFEComponent))
        return value

    @property
    def component_details(self) -> 'List[_2008.Component]':
        '''List[Component]: 'ComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDetails, constructor.new(_2008.Component))
        return value

    @property
    def power_loads(self) -> 'List[_2034.PowerLoad]':
        '''List[PowerLoad]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2034.PowerLoad))
        return value

    @property
    def point_loads(self) -> 'List[_2033.PointLoad]':
        '''List[PointLoad]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2033.PointLoad))
        return value

    @property
    def oil_seals(self) -> 'List[_2028.OilSeal]':
        '''List[OilSeal]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2028.OilSeal))
        return value

    def get_part_named(self, name: 'str') -> '_2030.Part':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Part
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2030.Part.TYPE](name if name else None)
        return constructor.new(_2030.Part)(method_result) if method_result else None

    def get_part_named_of_type_assembly(self, name: 'str') -> 'Assembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Assembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[Assembly.TYPE](name if name else None)
        return constructor.new(Assembly)(method_result) if method_result else None

    def get_part_named_of_type_abstract_assembly(self, name: 'str') -> '_2000.AbstractAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.AbstractAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2000.AbstractAssembly.TYPE](name if name else None)
        return constructor.new(_2000.AbstractAssembly)(method_result) if method_result else None

    def get_part_named_of_type_abstract_shaft_or_housing(self, name: 'str') -> '_2001.AbstractShaftOrHousing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.AbstractShaftOrHousing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2001.AbstractShaftOrHousing.TYPE](name if name else None)
        return constructor.new(_2001.AbstractShaftOrHousing)(method_result) if method_result else None

    def get_part_named_of_type_bearing(self, name: 'str') -> '_2004.Bearing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2004.Bearing.TYPE](name if name else None)
        return constructor.new(_2004.Bearing)(method_result) if method_result else None

    def get_part_named_of_type_bolt(self, name: 'str') -> '_2006.Bolt':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bolt
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2006.Bolt.TYPE](name if name else None)
        return constructor.new(_2006.Bolt)(method_result) if method_result else None

    def get_part_named_of_type_bolted_joint(self, name: 'str') -> '_2007.BoltedJoint':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.BoltedJoint
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2007.BoltedJoint.TYPE](name if name else None)
        return constructor.new(_2007.BoltedJoint)(method_result) if method_result else None

    def get_part_named_of_type_component(self, name: 'str') -> '_2008.Component':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Component
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2008.Component.TYPE](name if name else None)
        return constructor.new(_2008.Component)(method_result) if method_result else None

    def get_part_named_of_type_connector(self, name: 'str') -> '_2011.Connector':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Connector
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2011.Connector.TYPE](name if name else None)
        return constructor.new(_2011.Connector)(method_result) if method_result else None

    def get_part_named_of_type_datum(self, name: 'str') -> '_2012.Datum':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Datum
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2012.Datum.TYPE](name if name else None)
        return constructor.new(_2012.Datum)(method_result) if method_result else None

    def get_part_named_of_type_external_cad_model(self, name: 'str') -> '_2015.ExternalCADModel':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.ExternalCADModel
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2015.ExternalCADModel.TYPE](name if name else None)
        return constructor.new(_2015.ExternalCADModel)(method_result) if method_result else None

    def get_part_named_of_type_flexible_pin_assembly(self, name: 'str') -> '_2016.FlexiblePinAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.FlexiblePinAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2016.FlexiblePinAssembly.TYPE](name if name else None)
        return constructor.new(_2016.FlexiblePinAssembly)(method_result) if method_result else None

    def get_part_named_of_type_guide_dxf_model(self, name: 'str') -> '_2017.GuideDxfModel':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.GuideDxfModel
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2017.GuideDxfModel.TYPE](name if name else None)
        return constructor.new(_2017.GuideDxfModel)(method_result) if method_result else None

    def get_part_named_of_type_imported_fe_component(self, name: 'str') -> '_2020.ImportedFEComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.ImportedFEComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2020.ImportedFEComponent.TYPE](name if name else None)
        return constructor.new(_2020.ImportedFEComponent)(method_result) if method_result else None

    def get_part_named_of_type_mass_disc(self, name: 'str') -> '_2024.MassDisc':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MassDisc
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2024.MassDisc.TYPE](name if name else None)
        return constructor.new(_2024.MassDisc)(method_result) if method_result else None

    def get_part_named_of_type_measurement_component(self, name: 'str') -> '_2025.MeasurementComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MeasurementComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2025.MeasurementComponent.TYPE](name if name else None)
        return constructor.new(_2025.MeasurementComponent)(method_result) if method_result else None

    def get_part_named_of_type_mountable_component(self, name: 'str') -> '_2026.MountableComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MountableComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2026.MountableComponent.TYPE](name if name else None)
        return constructor.new(_2026.MountableComponent)(method_result) if method_result else None

    def get_part_named_of_type_oil_seal(self, name: 'str') -> '_2028.OilSeal':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.OilSeal
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2028.OilSeal.TYPE](name if name else None)
        return constructor.new(_2028.OilSeal)(method_result) if method_result else None

    def get_part_named_of_type_planet_carrier(self, name: 'str') -> '_2031.PlanetCarrier':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2031.PlanetCarrier.TYPE](name if name else None)
        return constructor.new(_2031.PlanetCarrier)(method_result) if method_result else None

    def get_part_named_of_type_point_load(self, name: 'str') -> '_2033.PointLoad':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PointLoad
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2033.PointLoad.TYPE](name if name else None)
        return constructor.new(_2033.PointLoad)(method_result) if method_result else None

    def get_part_named_of_type_power_load(self, name: 'str') -> '_2034.PowerLoad':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PowerLoad
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2034.PowerLoad.TYPE](name if name else None)
        return constructor.new(_2034.PowerLoad)(method_result) if method_result else None

    def get_part_named_of_type_root_assembly(self, name: 'str') -> '_2036.RootAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.RootAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2036.RootAssembly.TYPE](name if name else None)
        return constructor.new(_2036.RootAssembly)(method_result) if method_result else None

    def get_part_named_of_type_specialised_assembly(self, name: 'str') -> '_2038.SpecialisedAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.SpecialisedAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2038.SpecialisedAssembly.TYPE](name if name else None)
        return constructor.new(_2038.SpecialisedAssembly)(method_result) if method_result else None

    def get_part_named_of_type_unbalanced_mass(self, name: 'str') -> '_2039.UnbalancedMass':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.UnbalancedMass
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2039.UnbalancedMass.TYPE](name if name else None)
        return constructor.new(_2039.UnbalancedMass)(method_result) if method_result else None

    def get_part_named_of_type_virtual_component(self, name: 'str') -> '_2040.VirtualComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.VirtualComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2040.VirtualComponent.TYPE](name if name else None)
        return constructor.new(_2040.VirtualComponent)(method_result) if method_result else None

    def get_part_named_of_type_shaft(self, name: 'str') -> '_2043.Shaft':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2043.Shaft.TYPE](name if name else None)
        return constructor.new(_2043.Shaft)(method_result) if method_result else None

    def get_part_named_of_type_agma_gleason_conical_gear(self, name: 'str') -> '_2073.AGMAGleasonConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.AGMAGleasonConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2073.AGMAGleasonConicalGear.TYPE](name if name else None)
        return constructor.new(_2073.AGMAGleasonConicalGear)(method_result) if method_result else None

    def get_part_named_of_type_agma_gleason_conical_gear_set(self, name: 'str') -> '_2074.AGMAGleasonConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2074.AGMAGleasonConicalGearSet.TYPE](name if name else None)
        return constructor.new(_2074.AGMAGleasonConicalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_gear(self, name: 'str') -> '_2075.BevelDifferentialGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2075.BevelDifferentialGear.TYPE](name if name else None)
        return constructor.new(_2075.BevelDifferentialGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_gear_set(self, name: 'str') -> '_2076.BevelDifferentialGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2076.BevelDifferentialGearSet.TYPE](name if name else None)
        return constructor.new(_2076.BevelDifferentialGearSet)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_planet_gear(self, name: 'str') -> '_2077.BevelDifferentialPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2077.BevelDifferentialPlanetGear.TYPE](name if name else None)
        return constructor.new(_2077.BevelDifferentialPlanetGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_sun_gear(self, name: 'str') -> '_2078.BevelDifferentialSunGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialSunGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2078.BevelDifferentialSunGear.TYPE](name if name else None)
        return constructor.new(_2078.BevelDifferentialSunGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_gear(self, name: 'str') -> '_2079.BevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2079.BevelGear.TYPE](name if name else None)
        return constructor.new(_2079.BevelGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_gear_set(self, name: 'str') -> '_2080.BevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2080.BevelGearSet.TYPE](name if name else None)
        return constructor.new(_2080.BevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_concept_gear(self, name: 'str') -> '_2081.ConceptGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConceptGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2081.ConceptGear.TYPE](name if name else None)
        return constructor.new(_2081.ConceptGear)(method_result) if method_result else None

    def get_part_named_of_type_concept_gear_set(self, name: 'str') -> '_2082.ConceptGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConceptGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2082.ConceptGearSet.TYPE](name if name else None)
        return constructor.new(_2082.ConceptGearSet)(method_result) if method_result else None

    def get_part_named_of_type_conical_gear(self, name: 'str') -> '_2083.ConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2083.ConicalGear.TYPE](name if name else None)
        return constructor.new(_2083.ConicalGear)(method_result) if method_result else None

    def get_part_named_of_type_conical_gear_set(self, name: 'str') -> '_2084.ConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2084.ConicalGearSet.TYPE](name if name else None)
        return constructor.new(_2084.ConicalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_gear(self, name: 'str') -> '_2085.CylindricalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2085.CylindricalGear.TYPE](name if name else None)
        return constructor.new(_2085.CylindricalGear)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_gear_set(self, name: 'str') -> '_2086.CylindricalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2086.CylindricalGearSet.TYPE](name if name else None)
        return constructor.new(_2086.CylindricalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_planet_gear(self, name: 'str') -> '_2087.CylindricalPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2087.CylindricalPlanetGear.TYPE](name if name else None)
        return constructor.new(_2087.CylindricalPlanetGear)(method_result) if method_result else None

    def get_part_named_of_type_face_gear(self, name: 'str') -> '_2088.FaceGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.FaceGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2088.FaceGear.TYPE](name if name else None)
        return constructor.new(_2088.FaceGear)(method_result) if method_result else None

    def get_part_named_of_type_face_gear_set(self, name: 'str') -> '_2089.FaceGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.FaceGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2089.FaceGearSet.TYPE](name if name else None)
        return constructor.new(_2089.FaceGearSet)(method_result) if method_result else None

    def get_part_named_of_type_gear(self, name: 'str') -> '_2090.Gear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.Gear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2090.Gear.TYPE](name if name else None)
        return constructor.new(_2090.Gear)(method_result) if method_result else None

    def get_part_named_of_type_gear_set(self, name: 'str') -> '_2092.GearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.GearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2092.GearSet.TYPE](name if name else None)
        return constructor.new(_2092.GearSet)(method_result) if method_result else None

    def get_part_named_of_type_hypoid_gear(self, name: 'str') -> '_2094.HypoidGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2094.HypoidGear.TYPE](name if name else None)
        return constructor.new(_2094.HypoidGear)(method_result) if method_result else None

    def get_part_named_of_type_hypoid_gear_set(self, name: 'str') -> '_2095.HypoidGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2095.HypoidGearSet.TYPE](name if name else None)
        return constructor.new(_2095.HypoidGearSet)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_conical_gear(self, name: 'str') -> '_2096.KlingelnbergCycloPalloidConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2096.KlingelnbergCycloPalloidConicalGear.TYPE](name if name else None)
        return constructor.new(_2096.KlingelnbergCycloPalloidConicalGear)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self, name: 'str') -> '_2097.KlingelnbergCycloPalloidConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2097.KlingelnbergCycloPalloidConicalGearSet.TYPE](name if name else None)
        return constructor.new(_2097.KlingelnbergCycloPalloidConicalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self, name: 'str') -> '_2098.KlingelnbergCycloPalloidHypoidGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2098.KlingelnbergCycloPalloidHypoidGear.TYPE](name if name else None)
        return constructor.new(_2098.KlingelnbergCycloPalloidHypoidGear)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self, name: 'str') -> '_2099.KlingelnbergCycloPalloidHypoidGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2099.KlingelnbergCycloPalloidHypoidGearSet.TYPE](name if name else None)
        return constructor.new(_2099.KlingelnbergCycloPalloidHypoidGearSet)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, name: 'str') -> '_2100.KlingelnbergCycloPalloidSpiralBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2100.KlingelnbergCycloPalloidSpiralBevelGear.TYPE](name if name else None)
        return constructor.new(_2100.KlingelnbergCycloPalloidSpiralBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, name: 'str') -> '_2101.KlingelnbergCycloPalloidSpiralBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2101.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE](name if name else None)
        return constructor.new(_2101.KlingelnbergCycloPalloidSpiralBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_planetary_gear_set(self, name: 'str') -> '_2102.PlanetaryGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.PlanetaryGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2102.PlanetaryGearSet.TYPE](name if name else None)
        return constructor.new(_2102.PlanetaryGearSet)(method_result) if method_result else None

    def get_part_named_of_type_spiral_bevel_gear(self, name: 'str') -> '_2103.SpiralBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2103.SpiralBevelGear.TYPE](name if name else None)
        return constructor.new(_2103.SpiralBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_spiral_bevel_gear_set(self, name: 'str') -> '_2104.SpiralBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2104.SpiralBevelGearSet.TYPE](name if name else None)
        return constructor.new(_2104.SpiralBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_diff_gear(self, name: 'str') -> '_2105.StraightBevelDiffGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2105.StraightBevelDiffGear.TYPE](name if name else None)
        return constructor.new(_2105.StraightBevelDiffGear)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_diff_gear_set(self, name: 'str') -> '_2106.StraightBevelDiffGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2106.StraightBevelDiffGearSet.TYPE](name if name else None)
        return constructor.new(_2106.StraightBevelDiffGearSet)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_gear(self, name: 'str') -> '_2107.StraightBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2107.StraightBevelGear.TYPE](name if name else None)
        return constructor.new(_2107.StraightBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_gear_set(self, name: 'str') -> '_2108.StraightBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2108.StraightBevelGearSet.TYPE](name if name else None)
        return constructor.new(_2108.StraightBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_planet_gear(self, name: 'str') -> '_2109.StraightBevelPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2109.StraightBevelPlanetGear.TYPE](name if name else None)
        return constructor.new(_2109.StraightBevelPlanetGear)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_sun_gear(self, name: 'str') -> '_2110.StraightBevelSunGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelSunGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2110.StraightBevelSunGear.TYPE](name if name else None)
        return constructor.new(_2110.StraightBevelSunGear)(method_result) if method_result else None

    def get_part_named_of_type_worm_gear(self, name: 'str') -> '_2111.WormGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.WormGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2111.WormGear.TYPE](name if name else None)
        return constructor.new(_2111.WormGear)(method_result) if method_result else None

    def get_part_named_of_type_worm_gear_set(self, name: 'str') -> '_2112.WormGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.WormGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2112.WormGearSet.TYPE](name if name else None)
        return constructor.new(_2112.WormGearSet)(method_result) if method_result else None

    def get_part_named_of_type_zerol_bevel_gear(self, name: 'str') -> '_2113.ZerolBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2113.ZerolBevelGear.TYPE](name if name else None)
        return constructor.new(_2113.ZerolBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_zerol_bevel_gear_set(self, name: 'str') -> '_2114.ZerolBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2114.ZerolBevelGearSet.TYPE](name if name else None)
        return constructor.new(_2114.ZerolBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_belt_drive(self, name: 'str') -> '_2132.BeltDrive':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2132.BeltDrive.TYPE](name if name else None)
        return constructor.new(_2132.BeltDrive)(method_result) if method_result else None

    def get_part_named_of_type_clutch(self, name: 'str') -> '_2134.Clutch':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Clutch
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2134.Clutch.TYPE](name if name else None)
        return constructor.new(_2134.Clutch)(method_result) if method_result else None

    def get_part_named_of_type_clutch_half(self, name: 'str') -> '_2135.ClutchHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ClutchHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2135.ClutchHalf.TYPE](name if name else None)
        return constructor.new(_2135.ClutchHalf)(method_result) if method_result else None

    def get_part_named_of_type_concept_coupling(self, name: 'str') -> '_2137.ConceptCoupling':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCoupling
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2137.ConceptCoupling.TYPE](name if name else None)
        return constructor.new(_2137.ConceptCoupling)(method_result) if method_result else None

    def get_part_named_of_type_concept_coupling_half(self, name: 'str') -> '_2138.ConceptCouplingHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCouplingHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2138.ConceptCouplingHalf.TYPE](name if name else None)
        return constructor.new(_2138.ConceptCouplingHalf)(method_result) if method_result else None

    def get_part_named_of_type_coupling(self, name: 'str') -> '_2139.Coupling':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Coupling
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2139.Coupling.TYPE](name if name else None)
        return constructor.new(_2139.Coupling)(method_result) if method_result else None

    def get_part_named_of_type_coupling_half(self, name: 'str') -> '_2140.CouplingHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CouplingHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2140.CouplingHalf.TYPE](name if name else None)
        return constructor.new(_2140.CouplingHalf)(method_result) if method_result else None

    def get_part_named_of_type_cvt(self, name: 'str') -> '_2141.CVT':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CVT
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2141.CVT.TYPE](name if name else None)
        return constructor.new(_2141.CVT)(method_result) if method_result else None

    def get_part_named_of_type_cvt_pulley(self, name: 'str') -> '_2142.CVTPulley':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CVTPulley
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2142.CVTPulley.TYPE](name if name else None)
        return constructor.new(_2142.CVTPulley)(method_result) if method_result else None

    def get_part_named_of_type_part_to_part_shear_coupling(self, name: 'str') -> '_2143.PartToPartShearCoupling':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.PartToPartShearCoupling
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2143.PartToPartShearCoupling.TYPE](name if name else None)
        return constructor.new(_2143.PartToPartShearCoupling)(method_result) if method_result else None

    def get_part_named_of_type_part_to_part_shear_coupling_half(self, name: 'str') -> '_2144.PartToPartShearCouplingHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2144.PartToPartShearCouplingHalf.TYPE](name if name else None)
        return constructor.new(_2144.PartToPartShearCouplingHalf)(method_result) if method_result else None

    def get_part_named_of_type_pulley(self, name: 'str') -> '_2145.Pulley':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Pulley
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2145.Pulley.TYPE](name if name else None)
        return constructor.new(_2145.Pulley)(method_result) if method_result else None

    def get_part_named_of_type_rolling_ring(self, name: 'str') -> '_2151.RollingRing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2151.RollingRing.TYPE](name if name else None)
        return constructor.new(_2151.RollingRing)(method_result) if method_result else None

    def get_part_named_of_type_rolling_ring_assembly(self, name: 'str') -> '_2152.RollingRingAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRingAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2152.RollingRingAssembly.TYPE](name if name else None)
        return constructor.new(_2152.RollingRingAssembly)(method_result) if method_result else None

    def get_part_named_of_type_shaft_hub_connection(self, name: 'str') -> '_2153.ShaftHubConnection':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ShaftHubConnection
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2153.ShaftHubConnection.TYPE](name if name else None)
        return constructor.new(_2153.ShaftHubConnection)(method_result) if method_result else None

    def get_part_named_of_type_spring_damper(self, name: 'str') -> '_2154.SpringDamper':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamper
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2154.SpringDamper.TYPE](name if name else None)
        return constructor.new(_2154.SpringDamper)(method_result) if method_result else None

    def get_part_named_of_type_spring_damper_half(self, name: 'str') -> '_2155.SpringDamperHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamperHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2155.SpringDamperHalf.TYPE](name if name else None)
        return constructor.new(_2155.SpringDamperHalf)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser(self, name: 'str') -> '_2156.Synchroniser':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Synchroniser
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2156.Synchroniser.TYPE](name if name else None)
        return constructor.new(_2156.Synchroniser)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_half(self, name: 'str') -> '_2158.SynchroniserHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2158.SynchroniserHalf.TYPE](name if name else None)
        return constructor.new(_2158.SynchroniserHalf)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_part(self, name: 'str') -> '_2159.SynchroniserPart':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserPart
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2159.SynchroniserPart.TYPE](name if name else None)
        return constructor.new(_2159.SynchroniserPart)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_sleeve(self, name: 'str') -> '_2160.SynchroniserSleeve':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserSleeve
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2160.SynchroniserSleeve.TYPE](name if name else None)
        return constructor.new(_2160.SynchroniserSleeve)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter(self, name: 'str') -> '_2161.TorqueConverter':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverter
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2161.TorqueConverter.TYPE](name if name else None)
        return constructor.new(_2161.TorqueConverter)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter_pump(self, name: 'str') -> '_2162.TorqueConverterPump':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverterPump
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2162.TorqueConverterPump.TYPE](name if name else None)
        return constructor.new(_2162.TorqueConverterPump)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter_turbine(self, name: 'str') -> '_2164.TorqueConverterTurbine':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverterTurbine
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2164.TorqueConverterTurbine.TYPE](name if name else None)
        return constructor.new(_2164.TorqueConverterTurbine)(method_result) if method_result else None

    def add_part(self, part_type: 'Assembly.PartType', name: 'str') -> '_2030.Part':
        ''' 'AddPart' is the original name of this method.

        Args:
            part_type (mastapy.system_model.part_model.Assembly.PartType)
            name (str)

        Returns:
            mastapy.system_model.part_model.Part
        '''

        part_type = conversion.mp_to_pn_enum(part_type)
        name = str(name)
        method_result = self.wrapped.AddPart(part_type, name if name else None)
        return constructor.new(_2030.Part)(method_result) if method_result else None

    def add_assembly(self, name: Optional['str'] = 'Assembly') -> 'Assembly':
        ''' 'AddAssembly' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.Assembly
        '''

        name = str(name)
        method_result = self.wrapped.AddAssembly(name if name else None)
        return constructor.new(Assembly)(method_result) if method_result else None

    def add_oil_seal(self, name: Optional['str'] = 'Oil Seal') -> '_2028.OilSeal':
        ''' 'AddOilSeal' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.OilSeal
        '''

        name = str(name)
        method_result = self.wrapped.AddOilSeal(name if name else None)
        return constructor.new(_2028.OilSeal)(method_result) if method_result else None

    def add_power_load(self, name: Optional['str'] = 'Power Load') -> '_2034.PowerLoad':
        ''' 'AddPowerLoad' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.PowerLoad
        '''

        name = str(name)
        method_result = self.wrapped.AddPowerLoad(name if name else None)
        return constructor.new(_2034.PowerLoad)(method_result) if method_result else None

    def add_point_load(self, name: Optional['str'] = 'Point Load') -> '_2033.PointLoad':
        ''' 'AddPointLoad' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.PointLoad
        '''

        name = str(name)
        method_result = self.wrapped.AddPointLoad(name if name else None)
        return constructor.new(_2033.PointLoad)(method_result) if method_result else None

    def add_datum(self, name: Optional['str'] = 'Datum') -> '_2012.Datum':
        ''' 'AddDatum' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.Datum
        '''

        name = str(name)
        method_result = self.wrapped.AddDatum(name if name else None)
        return constructor.new(_2012.Datum)(method_result) if method_result else None

    def add_imported_fe_component(self, name: Optional['str'] = 'Imported FE') -> '_2020.ImportedFEComponent':
        ''' 'AddImportedFEComponent' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.ImportedFEComponent
        '''

        name = str(name)
        method_result = self.wrapped.AddImportedFEComponent(name if name else None)
        return constructor.new(_2020.ImportedFEComponent)(method_result) if method_result else None

    def add_measurement_component(self, name: Optional['str'] = 'Measurement Component') -> '_2025.MeasurementComponent':
        ''' 'AddMeasurementComponent' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.MeasurementComponent
        '''

        name = str(name)
        method_result = self.wrapped.AddMeasurementComponent(name if name else None)
        return constructor.new(_2025.MeasurementComponent)(method_result) if method_result else None

    def add_mass_disc(self, name: Optional['str'] = 'Mass Disc') -> '_2024.MassDisc':
        ''' 'AddMassDisc' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.MassDisc
        '''

        name = str(name)
        method_result = self.wrapped.AddMassDisc(name if name else None)
        return constructor.new(_2024.MassDisc)(method_result) if method_result else None

    def add_unbalanced_mass(self, name: Optional['str'] = 'Unbalanced Mass') -> '_2039.UnbalancedMass':
        ''' 'AddUnbalancedMass' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.UnbalancedMass
        '''

        name = str(name)
        method_result = self.wrapped.AddUnbalancedMass(name if name else None)
        return constructor.new(_2039.UnbalancedMass)(method_result) if method_result else None

    def add_straight_bevel_differential_gear_set(self, name: Optional['str'] = 'Straight Bevel Differential Gear Set') -> '_2106.StraightBevelDiffGearSet':
        ''' 'AddStraightBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddStraightBevelDifferentialGearSet(name if name else None)
        return constructor.new(_2106.StraightBevelDiffGearSet)(method_result) if method_result else None

    def add_spiral_bevel_differential_gear_set(self, name: Optional['str'] = 'Spiral Bevel Differential Gear Set') -> '_2076.BevelDifferentialGearSet':
        ''' 'AddSpiralBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddSpiralBevelDifferentialGearSet(name if name else None)
        return constructor.new(_2076.BevelDifferentialGearSet)(method_result) if method_result else None

    def add_zerol_bevel_differential_gear_set(self, name: Optional['str'] = 'Zerol Bevel Differential Gear Set') -> '_2076.BevelDifferentialGearSet':
        ''' 'AddZerolBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddZerolBevelDifferentialGearSet(name if name else None)
        return constructor.new(_2076.BevelDifferentialGearSet)(method_result) if method_result else None

    def add_planetary_gear_set(self, name: Optional['str'] = 'Planetary Gear Set') -> '_2102.PlanetaryGearSet':
        ''' 'AddPlanetaryGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.PlanetaryGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddPlanetaryGearSet(name if name else None)
        return constructor.new(_2102.PlanetaryGearSet)(method_result) if method_result else None

    def add_spiral_bevel_gear_set(self, name: Optional['str'] = 'Spiral Bevel Gear Set') -> '_2104.SpiralBevelGearSet':
        ''' 'AddSpiralBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddSpiralBevelGearSet(name if name else None)
        return constructor.new(_2104.SpiralBevelGearSet)(method_result) if method_result else None

    def add_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, name: Optional['str'] = 'Klingelnberg Cyclo Palloid Spiral Bevel Gear Set') -> '_2101.KlingelnbergCycloPalloidSpiralBevelGearSet':
        ''' 'AddKlingelnbergCycloPalloidSpiralBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddKlingelnbergCycloPalloidSpiralBevelGearSet(name if name else None)
        return constructor.new(_2101.KlingelnbergCycloPalloidSpiralBevelGearSet)(method_result) if method_result else None

    def add_klingelnberg_cyclo_palloid_hypoid_gear_set(self, name: Optional['str'] = 'Klingelnberg Cyclo Palloid Hypoid Gear Set') -> '_2099.KlingelnbergCycloPalloidHypoidGearSet':
        ''' 'AddKlingelnbergCycloPalloidHypoidGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddKlingelnbergCycloPalloidHypoidGearSet(name if name else None)
        return constructor.new(_2099.KlingelnbergCycloPalloidHypoidGearSet)(method_result) if method_result else None

    def add_straight_bevel_gear_set(self, name: Optional['str'] = 'Straight Bevel Gear Set') -> '_2108.StraightBevelGearSet':
        ''' 'AddStraightBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddStraightBevelGearSet(name if name else None)
        return constructor.new(_2108.StraightBevelGearSet)(method_result) if method_result else None

    def add_hypoid_gear_set(self, name: Optional['str'] = 'Hypoid Gear Set') -> '_2095.HypoidGearSet':
        ''' 'AddHypoidGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddHypoidGearSet(name if name else None)
        return constructor.new(_2095.HypoidGearSet)(method_result) if method_result else None

    def add_worm_gear_set(self, name: Optional['str'] = 'Worm Gear Set') -> '_2112.WormGearSet':
        ''' 'AddWormGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.WormGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddWormGearSet(name if name else None)
        return constructor.new(_2112.WormGearSet)(method_result) if method_result else None

    def add_zerol_bevel_gear_set(self, name: Optional['str'] = 'Zerol Bevel Gear Set') -> '_2114.ZerolBevelGearSet':
        ''' 'AddZerolBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddZerolBevelGearSet(name if name else None)
        return constructor.new(_2114.ZerolBevelGearSet)(method_result) if method_result else None

    def add_clutch(self, name: Optional['str'] = 'Clutch') -> '_2134.Clutch':
        ''' 'AddClutch' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.Clutch
        '''

        name = str(name)
        method_result = self.wrapped.AddClutch(name if name else None)
        return constructor.new(_2134.Clutch)(method_result) if method_result else None

    def add_synchroniser(self, name: Optional['str'] = 'Synchroniser') -> '_2156.Synchroniser':
        ''' 'AddSynchroniser' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.Synchroniser
        '''

        name = str(name)
        method_result = self.wrapped.AddSynchroniser(name if name else None)
        return constructor.new(_2156.Synchroniser)(method_result) if method_result else None

    def add_rolling_ring(self, name: Optional['str'] = 'Rolling Ring') -> '_2151.RollingRing':
        ''' 'AddRollingRing' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRing
        '''

        name = str(name)
        method_result = self.wrapped.AddRollingRing(name if name else None)
        return constructor.new(_2151.RollingRing)(method_result) if method_result else None

    def add_concept_coupling(self, name: Optional['str'] = 'Concept Coupling') -> '_2137.ConceptCoupling':
        ''' 'AddConceptCoupling' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCoupling
        '''

        name = str(name)
        method_result = self.wrapped.AddConceptCoupling(name if name else None)
        return constructor.new(_2137.ConceptCoupling)(method_result) if method_result else None

    def add_cvt(self, name: Optional['str'] = 'CVT') -> '_2141.CVT':
        ''' 'AddCVT' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.CVT
        '''

        name = str(name)
        method_result = self.wrapped.AddCVT(name if name else None)
        return constructor.new(_2141.CVT)(method_result) if method_result else None

    def add_spring_damper(self, name: Optional['str'] = 'Spring Damper') -> '_2154.SpringDamper':
        ''' 'AddSpringDamper' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamper
        '''

        name = str(name)
        method_result = self.wrapped.AddSpringDamper(name if name else None)
        return constructor.new(_2154.SpringDamper)(method_result) if method_result else None

    def add_torque_converter(self, name: Optional['str'] = 'Torque Converter') -> '_2161.TorqueConverter':
        ''' 'AddTorqueConverter' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverter
        '''

        name = str(name)
        method_result = self.wrapped.AddTorqueConverter(name if name else None)
        return constructor.new(_2161.TorqueConverter)(method_result) if method_result else None

    def add_bolted_joint(self, name: Optional['str'] = 'Bolted Joint') -> '_2007.BoltedJoint':
        ''' 'AddBoltedJoint' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.BoltedJoint
        '''

        name = str(name)
        method_result = self.wrapped.AddBoltedJoint(name if name else None)
        return constructor.new(_2007.BoltedJoint)(method_result) if method_result else None

    def add_belt_drive_with_options(self, belt_creation_options: Optional['_2128.BeltCreationOptions'] = None) -> '_2132.BeltDrive':
        ''' 'AddBeltDrive' is the original name of this method.

        Args:
            belt_creation_options (mastapy.system_model.part_model.creation_options.BeltCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        method_result = self.wrapped.AddBeltDrive(belt_creation_options.wrapped if belt_creation_options else None)
        return constructor.new(_2132.BeltDrive)(method_result) if method_result else None

    def add_belt_drive(self, centre_distance: Optional['float'] = 0.1, pulley_a_diameter: Optional['float'] = 0.1, pulley_b_diameter: Optional['float'] = 0.1, name: Optional['str'] = 'Belt Drive') -> '_2132.BeltDrive':
        ''' 'AddBeltDrive' is the original name of this method.

        Args:
            centre_distance (float, optional)
            pulley_a_diameter (float, optional)
            pulley_b_diameter (float, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        centre_distance = float(centre_distance)
        pulley_a_diameter = float(pulley_a_diameter)
        pulley_b_diameter = float(pulley_b_diameter)
        name = str(name)
        method_result = self.wrapped.AddBeltDrive(centre_distance if centre_distance else 0.0, pulley_a_diameter if pulley_a_diameter else 0.0, pulley_b_diameter if pulley_b_diameter else 0.0, name if name else None)
        return constructor.new(_2132.BeltDrive)(method_result) if method_result else None

    def add_planet_carrier_with_options(self, planet_carrier_creation_options: Optional['_2130.PlanetCarrierCreationOptions'] = None) -> '_2031.PlanetCarrier':
        ''' 'AddPlanetCarrier' is the original name of this method.

        Args:
            planet_carrier_creation_options (mastapy.system_model.part_model.creation_options.PlanetCarrierCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        method_result = self.wrapped.AddPlanetCarrier(planet_carrier_creation_options.wrapped if planet_carrier_creation_options else None)
        return constructor.new(_2031.PlanetCarrier)(method_result) if method_result else None

    def add_planet_carrier(self, number_of_planets: Optional['int'] = 3, diameter: Optional['float'] = 0.1) -> '_2031.PlanetCarrier':
        ''' 'AddPlanetCarrier' is the original name of this method.

        Args:
            number_of_planets (int, optional)
            diameter (float, optional)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        number_of_planets = int(number_of_planets)
        diameter = float(diameter)
        method_result = self.wrapped.AddPlanetCarrier(number_of_planets if number_of_planets else 0, diameter if diameter else 0.0)
        return constructor.new(_2031.PlanetCarrier)(method_result) if method_result else None

    def add_shaft_with_options(self, shaft_creation_options: '_2131.ShaftCreationOptions') -> '_2043.Shaft':
        ''' 'AddShaft' is the original name of this method.

        Args:
            shaft_creation_options (mastapy.system_model.part_model.creation_options.ShaftCreationOptions)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        method_result = self.wrapped.AddShaft(shaft_creation_options.wrapped if shaft_creation_options else None)
        return constructor.new(_2043.Shaft)(method_result) if method_result else None

    def add_shaft(self, length: Optional['float'] = 0.1, outer_diameter: Optional['float'] = 0.0, bore: Optional['float'] = 0.0, name: Optional['str'] = 'Shaft') -> '_2043.Shaft':
        ''' 'AddShaft' is the original name of this method.

        Args:
            length (float, optional)
            outer_diameter (float, optional)
            bore (float, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        length = float(length)
        outer_diameter = float(outer_diameter)
        bore = float(bore)
        name = str(name)
        method_result = self.wrapped.AddShaft(length if length else 0.0, outer_diameter if outer_diameter else 0.0, bore if bore else 0.0, name if name else None)
        return constructor.new(_2043.Shaft)(method_result) if method_result else None

    def add_cylindrical_gear_pair_with_options(self, cylindrical_gear_pair_creation_options: Optional['_883.CylindricalGearPairCreationOptions'] = None) -> '_2086.CylindricalGearSet':
        ''' 'AddCylindricalGearPair' is the original name of this method.

        Args:
            cylindrical_gear_pair_creation_options (mastapy.gears.gear_designs.creation_options.CylindricalGearPairCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        method_result = self.wrapped.AddCylindricalGearPair(cylindrical_gear_pair_creation_options.wrapped if cylindrical_gear_pair_creation_options else None)
        return constructor.new(_2086.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_pair(self, centre_distance: 'float') -> '_2086.CylindricalGearSet':
        ''' 'AddCylindricalGearPair' is the original name of this method.

        Args:
            centre_distance (float)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        centre_distance = float(centre_distance)
        method_result = self.wrapped.AddCylindricalGearPair(centre_distance if centre_distance else 0.0)
        return constructor.new(_2086.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_set_with_options(self, cylindrical_gear_linear_train_creation_options: Optional['_2129.CylindricalGearLinearTrainCreationOptions'] = None) -> '_2086.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            cylindrical_gear_linear_train_creation_options (mastapy.system_model.part_model.creation_options.CylindricalGearLinearTrainCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        method_result = self.wrapped.AddCylindricalGearSet(cylindrical_gear_linear_train_creation_options.wrapped if cylindrical_gear_linear_train_creation_options else None)
        return constructor.new(_2086.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_set(self, name: 'str', centre_distances: 'List[float]') -> '_2086.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            name (str)
            centre_distances (List[float])

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        centre_distances = conversion.mp_to_pn_array_float(centre_distances)
        method_result = self.wrapped.AddCylindricalGearSet(name if name else None, centre_distances)
        return constructor.new(_2086.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_set_extended(self, name: 'str', normal_pressure_angle: 'float', helix_angle: 'float', normal_module: 'float', pinion_hand: '_135.Hand', centre_distances: 'List[float]') -> '_2086.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            name (str)
            normal_pressure_angle (float)
            helix_angle (float)
            normal_module (float)
            pinion_hand (mastapy.gears.Hand)
            centre_distances (List[float])

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        normal_pressure_angle = float(normal_pressure_angle)
        helix_angle = float(helix_angle)
        normal_module = float(normal_module)
        pinion_hand = conversion.mp_to_pn_enum(pinion_hand)
        centre_distances = conversion.mp_to_pn_array_float(centre_distances)
        method_result = self.wrapped.AddCylindricalGearSet(name if name else None, normal_pressure_angle if normal_pressure_angle else 0.0, helix_angle if helix_angle else 0.0, normal_module if normal_module else 0.0, pinion_hand, centre_distances)
        return constructor.new(_2086.CylindricalGearSet)(method_result) if method_result else None

    def add_spiral_bevel_gear_set_with_options(self, spiral_bevel_gear_set_creation_options: Optional['_886.SpiralBevelGearSetCreationOptions'] = None) -> '_2104.SpiralBevelGearSet':
        ''' 'AddSpiralBevelGearSet' is the original name of this method.

        Args:
            spiral_bevel_gear_set_creation_options (mastapy.gears.gear_designs.creation_options.SpiralBevelGearSetCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        method_result = self.wrapped.AddSpiralBevelGearSet(spiral_bevel_gear_set_creation_options.wrapped if spiral_bevel_gear_set_creation_options else None)
        return constructor.new(_2104.SpiralBevelGearSet)(method_result) if method_result else None

    def add_spiral_bevel_gear_set_detailed(self, name: Optional['str'] = 'Spiral Bevel Gear Set', outer_transverse_module: Optional['float'] = 0.0, pressure_angle: Optional['float'] = 0.0, mean_spiral_angle: Optional['float'] = 0.5, wheel_number_of_teeth: Optional['int'] = 43, pinion_number_of_teeth: Optional['int'] = 14, wheel_face_width: Optional['float'] = 0.0, pinion_face_width: Optional['float'] = 0.0, pinion_face_width_offset: Optional['float'] = 0.0, shaft_angle: Optional['float'] = 1.6) -> '_2104.SpiralBevelGearSet':
        ''' 'AddSpiralBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)
            outer_transverse_module (float, optional)
            pressure_angle (float, optional)
            mean_spiral_angle (float, optional)
            wheel_number_of_teeth (int, optional)
            pinion_number_of_teeth (int, optional)
            wheel_face_width (float, optional)
            pinion_face_width (float, optional)
            pinion_face_width_offset (float, optional)
            shaft_angle (float, optional)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        name = str(name)
        outer_transverse_module = float(outer_transverse_module)
        pressure_angle = float(pressure_angle)
        mean_spiral_angle = float(mean_spiral_angle)
        wheel_number_of_teeth = int(wheel_number_of_teeth)
        pinion_number_of_teeth = int(pinion_number_of_teeth)
        wheel_face_width = float(wheel_face_width)
        pinion_face_width = float(pinion_face_width)
        pinion_face_width_offset = float(pinion_face_width_offset)
        shaft_angle = float(shaft_angle)
        method_result = self.wrapped.AddSpiralBevelGearSet(name if name else None, outer_transverse_module if outer_transverse_module else 0.0, pressure_angle if pressure_angle else 0.0, mean_spiral_angle if mean_spiral_angle else 0.0, wheel_number_of_teeth if wheel_number_of_teeth else 0, pinion_number_of_teeth if pinion_number_of_teeth else 0, wheel_face_width if wheel_face_width else 0.0, pinion_face_width if pinion_face_width else 0.0, pinion_face_width_offset if pinion_face_width_offset else 0.0, shaft_angle if shaft_angle else 0.0)
        return constructor.new(_2104.SpiralBevelGearSet)(method_result) if method_result else None

    def add_hypoid_gear_set_detailed(self, name: Optional['str'] = 'Hypoid Gear Set', pinion_number_of_teeth: Optional['int'] = 7, wheel_number_of_teeth: Optional['int'] = 41, outer_transverse_module: Optional['float'] = 0.0, wheel_face_width: Optional['float'] = 0.1, offset: Optional['float'] = 0.0, average_pressure_angle: Optional['float'] = 0.4, design_method: Optional['_916.AGMAGleasonConicalGearGeometryMethods'] = _916.AGMAGleasonConicalGearGeometryMethods.GLEASON) -> '_2095.HypoidGearSet':
        ''' 'AddHypoidGearSet' is the original name of this method.

        Args:
            name (str, optional)
            pinion_number_of_teeth (int, optional)
            wheel_number_of_teeth (int, optional)
            outer_transverse_module (float, optional)
            wheel_face_width (float, optional)
            offset (float, optional)
            average_pressure_angle (float, optional)
            design_method (mastapy.gears.gear_designs.bevel.AGMAGleasonConicalGearGeometryMethods, optional)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGearSet
        '''

        name = str(name)
        pinion_number_of_teeth = int(pinion_number_of_teeth)
        wheel_number_of_teeth = int(wheel_number_of_teeth)
        outer_transverse_module = float(outer_transverse_module)
        wheel_face_width = float(wheel_face_width)
        offset = float(offset)
        average_pressure_angle = float(average_pressure_angle)
        design_method = conversion.mp_to_pn_enum(design_method)
        method_result = self.wrapped.AddHypoidGearSet(name if name else None, pinion_number_of_teeth if pinion_number_of_teeth else 0, wheel_number_of_teeth if wheel_number_of_teeth else 0, outer_transverse_module if outer_transverse_module else 0.0, wheel_face_width if wheel_face_width else 0.0, offset if offset else 0.0, average_pressure_angle if average_pressure_angle else 0.0, design_method)
        return constructor.new(_2095.HypoidGearSet)(method_result) if method_result else None

    def add_bearing(self, name: 'str') -> '_2004.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        method_result = self.wrapped.AddBearing(name if name else None)
        return constructor.new(_2004.Bearing)(method_result) if method_result else None

    def import_fe_mesh_from_file(self, file_name: 'str', stiffness_matrix: '_1390.NodalMatrix') -> '_2020.ImportedFEComponent':
        ''' 'ImportFEMeshFromFile' is the original name of this method.

        Args:
            file_name (str)
            stiffness_matrix (mastapy.nodal_analysis.NodalMatrix)

        Returns:
            mastapy.system_model.part_model.ImportedFEComponent
        '''

        file_name = str(file_name)
        method_result = self.wrapped.ImportFEMeshFromFile(file_name if file_name else None, stiffness_matrix.wrapped if stiffness_matrix else None)
        return constructor.new(_2020.ImportedFEComponent)(method_result) if method_result else None

    def all_parts(self) -> 'List[_2030.Part]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Part]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2030.Part.TYPE](), constructor.new(_2030.Part))

    def all_parts_of_type_assembly(self) -> 'List[Assembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Assembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[Assembly.TYPE](), constructor.new(Assembly))

    def all_parts_of_type_abstract_assembly(self) -> 'List[_2000.AbstractAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.AbstractAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2000.AbstractAssembly.TYPE](), constructor.new(_2000.AbstractAssembly))

    def all_parts_of_type_abstract_shaft_or_housing(self) -> 'List[_2001.AbstractShaftOrHousing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.AbstractShaftOrHousing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2001.AbstractShaftOrHousing.TYPE](), constructor.new(_2001.AbstractShaftOrHousing))

    def all_parts_of_type_bearing(self) -> 'List[_2004.Bearing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Bearing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2004.Bearing.TYPE](), constructor.new(_2004.Bearing))

    def all_parts_of_type_bolt(self) -> 'List[_2006.Bolt]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Bolt]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2006.Bolt.TYPE](), constructor.new(_2006.Bolt))

    def all_parts_of_type_bolted_joint(self) -> 'List[_2007.BoltedJoint]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.BoltedJoint]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2007.BoltedJoint.TYPE](), constructor.new(_2007.BoltedJoint))

    def all_parts_of_type_component(self) -> 'List[_2008.Component]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Component]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2008.Component.TYPE](), constructor.new(_2008.Component))

    def all_parts_of_type_connector(self) -> 'List[_2011.Connector]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Connector]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2011.Connector.TYPE](), constructor.new(_2011.Connector))

    def all_parts_of_type_datum(self) -> 'List[_2012.Datum]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Datum]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2012.Datum.TYPE](), constructor.new(_2012.Datum))

    def all_parts_of_type_external_cad_model(self) -> 'List[_2015.ExternalCADModel]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.ExternalCADModel]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2015.ExternalCADModel.TYPE](), constructor.new(_2015.ExternalCADModel))

    def all_parts_of_type_flexible_pin_assembly(self) -> 'List[_2016.FlexiblePinAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.FlexiblePinAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2016.FlexiblePinAssembly.TYPE](), constructor.new(_2016.FlexiblePinAssembly))

    def all_parts_of_type_guide_dxf_model(self) -> 'List[_2017.GuideDxfModel]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.GuideDxfModel]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2017.GuideDxfModel.TYPE](), constructor.new(_2017.GuideDxfModel))

    def all_parts_of_type_imported_fe_component(self) -> 'List[_2020.ImportedFEComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.ImportedFEComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2020.ImportedFEComponent.TYPE](), constructor.new(_2020.ImportedFEComponent))

    def all_parts_of_type_mass_disc(self) -> 'List[_2024.MassDisc]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MassDisc]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2024.MassDisc.TYPE](), constructor.new(_2024.MassDisc))

    def all_parts_of_type_measurement_component(self) -> 'List[_2025.MeasurementComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MeasurementComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2025.MeasurementComponent.TYPE](), constructor.new(_2025.MeasurementComponent))

    def all_parts_of_type_mountable_component(self) -> 'List[_2026.MountableComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MountableComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2026.MountableComponent.TYPE](), constructor.new(_2026.MountableComponent))

    def all_parts_of_type_oil_seal(self) -> 'List[_2028.OilSeal]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.OilSeal]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2028.OilSeal.TYPE](), constructor.new(_2028.OilSeal))

    def all_parts_of_type_planet_carrier(self) -> 'List[_2031.PlanetCarrier]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PlanetCarrier]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2031.PlanetCarrier.TYPE](), constructor.new(_2031.PlanetCarrier))

    def all_parts_of_type_point_load(self) -> 'List[_2033.PointLoad]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PointLoad]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2033.PointLoad.TYPE](), constructor.new(_2033.PointLoad))

    def all_parts_of_type_power_load(self) -> 'List[_2034.PowerLoad]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PowerLoad]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2034.PowerLoad.TYPE](), constructor.new(_2034.PowerLoad))

    def all_parts_of_type_root_assembly(self) -> 'List[_2036.RootAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.RootAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2036.RootAssembly.TYPE](), constructor.new(_2036.RootAssembly))

    def all_parts_of_type_specialised_assembly(self) -> 'List[_2038.SpecialisedAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.SpecialisedAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2038.SpecialisedAssembly.TYPE](), constructor.new(_2038.SpecialisedAssembly))

    def all_parts_of_type_unbalanced_mass(self) -> 'List[_2039.UnbalancedMass]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.UnbalancedMass]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2039.UnbalancedMass.TYPE](), constructor.new(_2039.UnbalancedMass))

    def all_parts_of_type_virtual_component(self) -> 'List[_2040.VirtualComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.VirtualComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2040.VirtualComponent.TYPE](), constructor.new(_2040.VirtualComponent))

    def all_parts_of_type_shaft(self) -> 'List[_2043.Shaft]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.shaft_model.Shaft]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2043.Shaft.TYPE](), constructor.new(_2043.Shaft))

    def all_parts_of_type_agma_gleason_conical_gear(self) -> 'List[_2073.AGMAGleasonConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2073.AGMAGleasonConicalGear.TYPE](), constructor.new(_2073.AGMAGleasonConicalGear))

    def all_parts_of_type_agma_gleason_conical_gear_set(self) -> 'List[_2074.AGMAGleasonConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2074.AGMAGleasonConicalGearSet.TYPE](), constructor.new(_2074.AGMAGleasonConicalGearSet))

    def all_parts_of_type_bevel_differential_gear(self) -> 'List[_2075.BevelDifferentialGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2075.BevelDifferentialGear.TYPE](), constructor.new(_2075.BevelDifferentialGear))

    def all_parts_of_type_bevel_differential_gear_set(self) -> 'List[_2076.BevelDifferentialGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2076.BevelDifferentialGearSet.TYPE](), constructor.new(_2076.BevelDifferentialGearSet))

    def all_parts_of_type_bevel_differential_planet_gear(self) -> 'List[_2077.BevelDifferentialPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2077.BevelDifferentialPlanetGear.TYPE](), constructor.new(_2077.BevelDifferentialPlanetGear))

    def all_parts_of_type_bevel_differential_sun_gear(self) -> 'List[_2078.BevelDifferentialSunGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialSunGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2078.BevelDifferentialSunGear.TYPE](), constructor.new(_2078.BevelDifferentialSunGear))

    def all_parts_of_type_bevel_gear(self) -> 'List[_2079.BevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2079.BevelGear.TYPE](), constructor.new(_2079.BevelGear))

    def all_parts_of_type_bevel_gear_set(self) -> 'List[_2080.BevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2080.BevelGearSet.TYPE](), constructor.new(_2080.BevelGearSet))

    def all_parts_of_type_concept_gear(self) -> 'List[_2081.ConceptGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConceptGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2081.ConceptGear.TYPE](), constructor.new(_2081.ConceptGear))

    def all_parts_of_type_concept_gear_set(self) -> 'List[_2082.ConceptGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConceptGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2082.ConceptGearSet.TYPE](), constructor.new(_2082.ConceptGearSet))

    def all_parts_of_type_conical_gear(self) -> 'List[_2083.ConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2083.ConicalGear.TYPE](), constructor.new(_2083.ConicalGear))

    def all_parts_of_type_conical_gear_set(self) -> 'List[_2084.ConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2084.ConicalGearSet.TYPE](), constructor.new(_2084.ConicalGearSet))

    def all_parts_of_type_cylindrical_gear(self) -> 'List[_2085.CylindricalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2085.CylindricalGear.TYPE](), constructor.new(_2085.CylindricalGear))

    def all_parts_of_type_cylindrical_gear_set(self) -> 'List[_2086.CylindricalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2086.CylindricalGearSet.TYPE](), constructor.new(_2086.CylindricalGearSet))

    def all_parts_of_type_cylindrical_planet_gear(self) -> 'List[_2087.CylindricalPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2087.CylindricalPlanetGear.TYPE](), constructor.new(_2087.CylindricalPlanetGear))

    def all_parts_of_type_face_gear(self) -> 'List[_2088.FaceGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.FaceGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2088.FaceGear.TYPE](), constructor.new(_2088.FaceGear))

    def all_parts_of_type_face_gear_set(self) -> 'List[_2089.FaceGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.FaceGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2089.FaceGearSet.TYPE](), constructor.new(_2089.FaceGearSet))

    def all_parts_of_type_gear(self) -> 'List[_2090.Gear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.Gear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2090.Gear.TYPE](), constructor.new(_2090.Gear))

    def all_parts_of_type_gear_set(self) -> 'List[_2092.GearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.GearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2092.GearSet.TYPE](), constructor.new(_2092.GearSet))

    def all_parts_of_type_hypoid_gear(self) -> 'List[_2094.HypoidGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.HypoidGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2094.HypoidGear.TYPE](), constructor.new(_2094.HypoidGear))

    def all_parts_of_type_hypoid_gear_set(self) -> 'List[_2095.HypoidGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.HypoidGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2095.HypoidGearSet.TYPE](), constructor.new(_2095.HypoidGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> 'List[_2096.KlingelnbergCycloPalloidConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2096.KlingelnbergCycloPalloidConicalGear.TYPE](), constructor.new(_2096.KlingelnbergCycloPalloidConicalGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> 'List[_2097.KlingelnbergCycloPalloidConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2097.KlingelnbergCycloPalloidConicalGearSet.TYPE](), constructor.new(_2097.KlingelnbergCycloPalloidConicalGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> 'List[_2098.KlingelnbergCycloPalloidHypoidGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2098.KlingelnbergCycloPalloidHypoidGear.TYPE](), constructor.new(_2098.KlingelnbergCycloPalloidHypoidGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> 'List[_2099.KlingelnbergCycloPalloidHypoidGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2099.KlingelnbergCycloPalloidHypoidGearSet.TYPE](), constructor.new(_2099.KlingelnbergCycloPalloidHypoidGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> 'List[_2100.KlingelnbergCycloPalloidSpiralBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2100.KlingelnbergCycloPalloidSpiralBevelGear.TYPE](), constructor.new(_2100.KlingelnbergCycloPalloidSpiralBevelGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> 'List[_2101.KlingelnbergCycloPalloidSpiralBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2101.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE](), constructor.new(_2101.KlingelnbergCycloPalloidSpiralBevelGearSet))

    def all_parts_of_type_planetary_gear_set(self) -> 'List[_2102.PlanetaryGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.PlanetaryGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2102.PlanetaryGearSet.TYPE](), constructor.new(_2102.PlanetaryGearSet))

    def all_parts_of_type_spiral_bevel_gear(self) -> 'List[_2103.SpiralBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.SpiralBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2103.SpiralBevelGear.TYPE](), constructor.new(_2103.SpiralBevelGear))

    def all_parts_of_type_spiral_bevel_gear_set(self) -> 'List[_2104.SpiralBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.SpiralBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2104.SpiralBevelGearSet.TYPE](), constructor.new(_2104.SpiralBevelGearSet))

    def all_parts_of_type_straight_bevel_diff_gear(self) -> 'List[_2105.StraightBevelDiffGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelDiffGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2105.StraightBevelDiffGear.TYPE](), constructor.new(_2105.StraightBevelDiffGear))

    def all_parts_of_type_straight_bevel_diff_gear_set(self) -> 'List[_2106.StraightBevelDiffGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelDiffGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2106.StraightBevelDiffGearSet.TYPE](), constructor.new(_2106.StraightBevelDiffGearSet))

    def all_parts_of_type_straight_bevel_gear(self) -> 'List[_2107.StraightBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2107.StraightBevelGear.TYPE](), constructor.new(_2107.StraightBevelGear))

    def all_parts_of_type_straight_bevel_gear_set(self) -> 'List[_2108.StraightBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2108.StraightBevelGearSet.TYPE](), constructor.new(_2108.StraightBevelGearSet))

    def all_parts_of_type_straight_bevel_planet_gear(self) -> 'List[_2109.StraightBevelPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2109.StraightBevelPlanetGear.TYPE](), constructor.new(_2109.StraightBevelPlanetGear))

    def all_parts_of_type_straight_bevel_sun_gear(self) -> 'List[_2110.StraightBevelSunGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelSunGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2110.StraightBevelSunGear.TYPE](), constructor.new(_2110.StraightBevelSunGear))

    def all_parts_of_type_worm_gear(self) -> 'List[_2111.WormGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.WormGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2111.WormGear.TYPE](), constructor.new(_2111.WormGear))

    def all_parts_of_type_worm_gear_set(self) -> 'List[_2112.WormGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.WormGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2112.WormGearSet.TYPE](), constructor.new(_2112.WormGearSet))

    def all_parts_of_type_zerol_bevel_gear(self) -> 'List[_2113.ZerolBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ZerolBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2113.ZerolBevelGear.TYPE](), constructor.new(_2113.ZerolBevelGear))

    def all_parts_of_type_zerol_bevel_gear_set(self) -> 'List[_2114.ZerolBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ZerolBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2114.ZerolBevelGearSet.TYPE](), constructor.new(_2114.ZerolBevelGearSet))

    def all_parts_of_type_belt_drive(self) -> 'List[_2132.BeltDrive]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.BeltDrive]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2132.BeltDrive.TYPE](), constructor.new(_2132.BeltDrive))

    def all_parts_of_type_clutch(self) -> 'List[_2134.Clutch]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Clutch]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2134.Clutch.TYPE](), constructor.new(_2134.Clutch))

    def all_parts_of_type_clutch_half(self) -> 'List[_2135.ClutchHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ClutchHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2135.ClutchHalf.TYPE](), constructor.new(_2135.ClutchHalf))

    def all_parts_of_type_concept_coupling(self) -> 'List[_2137.ConceptCoupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ConceptCoupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2137.ConceptCoupling.TYPE](), constructor.new(_2137.ConceptCoupling))

    def all_parts_of_type_concept_coupling_half(self) -> 'List[_2138.ConceptCouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ConceptCouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2138.ConceptCouplingHalf.TYPE](), constructor.new(_2138.ConceptCouplingHalf))

    def all_parts_of_type_coupling(self) -> 'List[_2139.Coupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Coupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2139.Coupling.TYPE](), constructor.new(_2139.Coupling))

    def all_parts_of_type_coupling_half(self) -> 'List[_2140.CouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2140.CouplingHalf.TYPE](), constructor.new(_2140.CouplingHalf))

    def all_parts_of_type_cvt(self) -> 'List[_2141.CVT]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CVT]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2141.CVT.TYPE](), constructor.new(_2141.CVT))

    def all_parts_of_type_cvt_pulley(self) -> 'List[_2142.CVTPulley]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CVTPulley]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2142.CVTPulley.TYPE](), constructor.new(_2142.CVTPulley))

    def all_parts_of_type_part_to_part_shear_coupling(self) -> 'List[_2143.PartToPartShearCoupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.PartToPartShearCoupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2143.PartToPartShearCoupling.TYPE](), constructor.new(_2143.PartToPartShearCoupling))

    def all_parts_of_type_part_to_part_shear_coupling_half(self) -> 'List[_2144.PartToPartShearCouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2144.PartToPartShearCouplingHalf.TYPE](), constructor.new(_2144.PartToPartShearCouplingHalf))

    def all_parts_of_type_pulley(self) -> 'List[_2145.Pulley]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Pulley]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2145.Pulley.TYPE](), constructor.new(_2145.Pulley))

    def all_parts_of_type_rolling_ring(self) -> 'List[_2151.RollingRing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.RollingRing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2151.RollingRing.TYPE](), constructor.new(_2151.RollingRing))

    def all_parts_of_type_rolling_ring_assembly(self) -> 'List[_2152.RollingRingAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.RollingRingAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2152.RollingRingAssembly.TYPE](), constructor.new(_2152.RollingRingAssembly))

    def all_parts_of_type_shaft_hub_connection(self) -> 'List[_2153.ShaftHubConnection]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ShaftHubConnection]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2153.ShaftHubConnection.TYPE](), constructor.new(_2153.ShaftHubConnection))

    def all_parts_of_type_spring_damper(self) -> 'List[_2154.SpringDamper]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SpringDamper]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2154.SpringDamper.TYPE](), constructor.new(_2154.SpringDamper))

    def all_parts_of_type_spring_damper_half(self) -> 'List[_2155.SpringDamperHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SpringDamperHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2155.SpringDamperHalf.TYPE](), constructor.new(_2155.SpringDamperHalf))

    def all_parts_of_type_synchroniser(self) -> 'List[_2156.Synchroniser]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Synchroniser]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2156.Synchroniser.TYPE](), constructor.new(_2156.Synchroniser))

    def all_parts_of_type_synchroniser_half(self) -> 'List[_2158.SynchroniserHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2158.SynchroniserHalf.TYPE](), constructor.new(_2158.SynchroniserHalf))

    def all_parts_of_type_synchroniser_part(self) -> 'List[_2159.SynchroniserPart]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserPart]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2159.SynchroniserPart.TYPE](), constructor.new(_2159.SynchroniserPart))

    def all_parts_of_type_synchroniser_sleeve(self) -> 'List[_2160.SynchroniserSleeve]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserSleeve]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2160.SynchroniserSleeve.TYPE](), constructor.new(_2160.SynchroniserSleeve))

    def all_parts_of_type_torque_converter(self) -> 'List[_2161.TorqueConverter]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverter]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2161.TorqueConverter.TYPE](), constructor.new(_2161.TorqueConverter))

    def all_parts_of_type_torque_converter_pump(self) -> 'List[_2162.TorqueConverterPump]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverterPump]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2162.TorqueConverterPump.TYPE](), constructor.new(_2162.TorqueConverterPump))

    def all_parts_of_type_torque_converter_turbine(self) -> 'List[_2164.TorqueConverterTurbine]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverterTurbine]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2164.TorqueConverterTurbine.TYPE](), constructor.new(_2164.TorqueConverterTurbine))

    def add_axial_clearance_bearing(self, name: 'str', contact_diameter: 'float') -> '_2004.Bearing':
        ''' 'AddAxialClearanceBearing' is the original name of this method.

        Args:
            name (str)
            contact_diameter (float)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        contact_diameter = float(contact_diameter)
        method_result = self.wrapped.AddAxialClearanceBearing(name if name else None, contact_diameter if contact_diameter else 0.0)
        return constructor.new(_2004.Bearing)(method_result) if method_result else None

    def add_shaft_hub_connection(self, name: 'str') -> '_2153.ShaftHubConnection':
        ''' 'AddShaftHubConnection' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ShaftHubConnection
        '''

        name = str(name)
        method_result = self.wrapped.AddShaftHubConnection(name if name else None)
        return constructor.new(_2153.ShaftHubConnection)(method_result) if method_result else None

    def add_rolling_bearing_from_catalogue(self, catalogue: '_1513.BearingCatalog', designation: 'str', name: 'str') -> '_2004.Bearing':
        ''' 'AddRollingBearingFromCatalogue' is the original name of this method.

        Args:
            catalogue (mastapy.bearings.BearingCatalog)
            designation (str)
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        catalogue = conversion.mp_to_pn_enum(catalogue)
        designation = str(designation)
        name = str(name)
        method_result = self.wrapped.AddRollingBearingFromCatalogue(catalogue, designation if designation else None, name if name else None)
        return constructor.new(_2004.Bearing)(method_result) if method_result else None

    def add_bearing_with_name_and_rolling_bearing_type(self, name: 'str', type_: '_1538.RollingBearingType') -> '_2004.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)
            type_ (mastapy.bearings.RollingBearingType)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        type_ = conversion.mp_to_pn_enum(type_)
        method_result = self.wrapped.AddBearing(name if name else None, type_)
        return constructor.new(_2004.Bearing)(method_result) if method_result else None

    def add_bearing_with_name_rolling_bearing_type_and_designation(self, name: 'str', type_: '_1538.RollingBearingType', designation: 'str') -> '_2004.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)
            type_ (mastapy.bearings.RollingBearingType)
            designation (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        type_ = conversion.mp_to_pn_enum(type_)
        designation = str(designation)
        method_result = self.wrapped.AddBearing(name if name else None, type_, designation if designation else None)
        return constructor.new(_2004.Bearing)(method_result) if method_result else None
