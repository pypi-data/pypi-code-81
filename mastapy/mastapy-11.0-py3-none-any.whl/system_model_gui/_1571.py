'''_1571.py

MASTAGUI
'''


from typing import List, Dict

from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy.system_model import _1891, _1887
from mastapy.system_model.connections_and_sockets import (
    _1945, _1948, _1949, _1952,
    _1953, _1961, _1967, _1972,
    _1975
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1979, _1981, _1983, _1985,
    _1987, _1989, _1991, _1993,
    _1995, _1998, _1999, _2000,
    _2003, _2005, _2007, _2009,
    _2011
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2015, _2018, _2021
from mastapy.system_model.connections_and_sockets.couplings import (
    _2022, _2024, _2026, _2028,
    _2030, _2032
)
from mastapy.system_model.part_model import (
    _2112, _2113, _2114, _2115,
    _2118, _2120, _2121, _2122,
    _2125, _2126, _2129, _2130,
    _2131, _2132, _2139, _2140,
    _2141, _2143, _2145, _2146,
    _2148, _2149, _2151, _2153,
    _2154, _2155
)
from mastapy.system_model.part_model.shaft_model import _2158
from mastapy.system_model.part_model.gears import (
    _2188, _2189, _2190, _2191,
    _2192, _2193, _2194, _2195,
    _2196, _2197, _2198, _2199,
    _2200, _2201, _2202, _2203,
    _2204, _2205, _2207, _2209,
    _2210, _2211, _2212, _2213,
    _2214, _2215, _2216, _2217,
    _2218, _2219, _2220, _2221,
    _2222, _2223, _2224, _2225,
    _2226, _2227, _2228, _2229
)
from mastapy.system_model.part_model.cycloidal import _2243, _2244, _2245
from mastapy.system_model.part_model.couplings import (
    _2251, _2253, _2254, _2256,
    _2257, _2258, _2259, _2261,
    _2262, _2263, _2264, _2265,
    _2271, _2272, _2273, _2275,
    _2276, _2277, _2279, _2280,
    _2281, _2282, _2283, _2285
)
from mastapy._math.color import Color
from mastapy._math.vector_3d import Vector3D
from mastapy.utility.operation_modes import _1521
from mastapy.math_utility import _1255, _1274
from mastapy.nodal_analysis.space_claim_link import _118
from mastapy._internal.python_net import python_net_import
from mastapy import _0

_FACETED_BODY = python_net_import('SMT.MastaAPI.MathUtility', 'FacetedBody')
_STRING = python_net_import('System', 'String')
_MASTAGUI = python_net_import('SMT.MastaAPI.SystemModelGUI', 'MASTAGUI')


__docformat__ = 'restructuredtext en'
__all__ = ('MASTAGUI',)


class MASTAGUI(_0.APIBase):
    '''MASTAGUI

    This is a mastapy class.
    '''

    TYPE = _MASTAGUI

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MASTAGUI.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_paused(self) -> 'bool':
        '''bool: 'IsPaused' is the original name of this property.'''

        return self.wrapped.IsPaused

    @is_paused.setter
    def is_paused(self, value: 'bool'):
        self.wrapped.IsPaused = bool(value) if value else False

    @property
    def is_initialised(self) -> 'bool':
        '''bool: 'IsInitialised' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsInitialised

    @property
    def is_remoting(self) -> 'bool':
        '''bool: 'IsRemoting' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsRemoting

    @property
    def selected_design_entity(self) -> '_1891.DesignEntity':
        '''DesignEntity: 'SelectedDesignEntity' is the original name of this property.'''

        if _1891.DesignEntity.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to DesignEntity. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity.setter
    def selected_design_entity(self, value: '_1891.DesignEntity'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1945.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1945.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection.setter
    def selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection(self, value: '_1945.AbstractShaftToMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_belt_connection(self) -> '_1948.BeltConnection':
        '''BeltConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1948.BeltConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BeltConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_belt_connection.setter
    def selected_design_entity_of_type_belt_connection(self, value: '_1948.BeltConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coaxial_connection(self) -> '_1949.CoaxialConnection':
        '''CoaxialConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1949.CoaxialConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CoaxialConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_coaxial_connection.setter
    def selected_design_entity_of_type_coaxial_connection(self, value: '_1949.CoaxialConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_connection(self) -> '_1952.Connection':
        '''Connection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1952.Connection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Connection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_connection.setter
    def selected_design_entity_of_type_connection(self, value: '_1952.Connection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt_belt_connection(self) -> '_1953.CVTBeltConnection':
        '''CVTBeltConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1953.CVTBeltConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVTBeltConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cvt_belt_connection.setter
    def selected_design_entity_of_type_cvt_belt_connection(self, value: '_1953.CVTBeltConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_inter_mountable_component_connection(self) -> '_1961.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1961.InterMountableComponentConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_inter_mountable_component_connection.setter
    def selected_design_entity_of_type_inter_mountable_component_connection(self, value: '_1961.InterMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planetary_connection(self) -> '_1967.PlanetaryConnection':
        '''PlanetaryConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1967.PlanetaryConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetaryConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_planetary_connection.setter
    def selected_design_entity_of_type_planetary_connection(self, value: '_1967.PlanetaryConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring_connection(self) -> '_1972.RollingRingConnection':
        '''RollingRingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1972.RollingRingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_rolling_ring_connection.setter
    def selected_design_entity_of_type_rolling_ring_connection(self, value: '_1972.RollingRingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft_to_mountable_component_connection(self) -> '_1975.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1975.ShaftToMountableComponentConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_shaft_to_mountable_component_connection.setter
    def selected_design_entity_of_type_shaft_to_mountable_component_connection(self, value: '_1975.ShaftToMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear_mesh(self) -> '_1979.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1979.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_agma_gleason_conical_gear_mesh.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear_mesh(self, value: '_1979.AGMAGleasonConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear_mesh(self) -> '_1981.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1981.BevelDifferentialGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_differential_gear_mesh.setter
    def selected_design_entity_of_type_bevel_differential_gear_mesh(self, value: '_1981.BevelDifferentialGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear_mesh(self) -> '_1983.BevelGearMesh':
        '''BevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1983.BevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_gear_mesh.setter
    def selected_design_entity_of_type_bevel_gear_mesh(self, value: '_1983.BevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear_mesh(self) -> '_1985.ConceptGearMesh':
        '''ConceptGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1985.ConceptGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_gear_mesh.setter
    def selected_design_entity_of_type_concept_gear_mesh(self, value: '_1985.ConceptGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear_mesh(self) -> '_1987.ConicalGearMesh':
        '''ConicalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1987.ConicalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_conical_gear_mesh.setter
    def selected_design_entity_of_type_conical_gear_mesh(self, value: '_1987.ConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear_mesh(self) -> '_1989.CylindricalGearMesh':
        '''CylindricalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1989.CylindricalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cylindrical_gear_mesh.setter
    def selected_design_entity_of_type_cylindrical_gear_mesh(self, value: '_1989.CylindricalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear_mesh(self) -> '_1991.FaceGearMesh':
        '''FaceGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1991.FaceGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_face_gear_mesh.setter
    def selected_design_entity_of_type_face_gear_mesh(self, value: '_1991.FaceGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear_mesh(self) -> '_1993.GearMesh':
        '''GearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1993.GearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_gear_mesh.setter
    def selected_design_entity_of_type_gear_mesh(self, value: '_1993.GearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear_mesh(self) -> '_1995.HypoidGearMesh':
        '''HypoidGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1995.HypoidGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_hypoid_gear_mesh.setter
    def selected_design_entity_of_type_hypoid_gear_mesh(self, value: '_1995.HypoidGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1998.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1998.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self, value: '_1998.KlingelnbergCycloPalloidConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1999.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1999.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, value: '_1999.KlingelnbergCycloPalloidHypoidGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2000.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2000.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, value: '_2000.KlingelnbergCycloPalloidSpiralBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear_mesh(self) -> '_2003.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2003.SpiralBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spiral_bevel_gear_mesh.setter
    def selected_design_entity_of_type_spiral_bevel_gear_mesh(self, value: '_2003.SpiralBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear_mesh(self) -> '_2005.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2005.StraightBevelDiffGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_diff_gear_mesh.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear_mesh(self, value: '_2005.StraightBevelDiffGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear_mesh(self) -> '_2007.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2007.StraightBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_gear_mesh.setter
    def selected_design_entity_of_type_straight_bevel_gear_mesh(self, value: '_2007.StraightBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear_mesh(self) -> '_2009.WormGearMesh':
        '''WormGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2009.WormGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_worm_gear_mesh.setter
    def selected_design_entity_of_type_worm_gear_mesh(self, value: '_2009.WormGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear_mesh(self) -> '_2011.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2011.ZerolBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_zerol_bevel_gear_mesh.setter
    def selected_design_entity_of_type_zerol_bevel_gear_mesh(self, value: '_2011.ZerolBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2015.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2015.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cycloidal_disc_central_bearing_connection.setter
    def selected_design_entity_of_type_cycloidal_disc_central_bearing_connection(self, value: '_2015.CycloidalDiscCentralBearingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2018.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2018.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection.setter
    def selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection(self, value: '_2018.CycloidalDiscPlanetaryBearingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_ring_pins_to_disc_connection(self) -> '_2021.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2021.RingPinsToDiscConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_ring_pins_to_disc_connection.setter
    def selected_design_entity_of_type_ring_pins_to_disc_connection(self, value: '_2021.RingPinsToDiscConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch_connection(self) -> '_2022.ClutchConnection':
        '''ClutchConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2022.ClutchConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ClutchConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_clutch_connection.setter
    def selected_design_entity_of_type_clutch_connection(self, value: '_2022.ClutchConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling_connection(self) -> '_2024.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2024.ConceptCouplingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_coupling_connection.setter
    def selected_design_entity_of_type_concept_coupling_connection(self, value: '_2024.ConceptCouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling_connection(self) -> '_2026.CouplingConnection':
        '''CouplingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2026.CouplingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CouplingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_coupling_connection.setter
    def selected_design_entity_of_type_coupling_connection(self, value: '_2026.CouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling_connection(self) -> '_2028.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2028.PartToPartShearCouplingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_part_to_part_shear_coupling_connection.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling_connection(self, value: '_2028.PartToPartShearCouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper_connection(self) -> '_2030.SpringDamperConnection':
        '''SpringDamperConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2030.SpringDamperConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamperConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spring_damper_connection.setter
    def selected_design_entity_of_type_spring_damper_connection(self, value: '_2030.SpringDamperConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_connection(self) -> '_2032.TorqueConverterConnection':
        '''TorqueConverterConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2032.TorqueConverterConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_torque_converter_connection.setter
    def selected_design_entity_of_type_torque_converter_connection(self, value: '_2032.TorqueConverterConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_assembly(self) -> '_2112.Assembly':
        '''Assembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2112.Assembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Assembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_assembly.setter
    def selected_design_entity_of_type_assembly(self, value: '_2112.Assembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_assembly(self) -> '_2113.AbstractAssembly':
        '''AbstractAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2113.AbstractAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_abstract_assembly.setter
    def selected_design_entity_of_type_abstract_assembly(self, value: '_2113.AbstractAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft(self) -> '_2114.AbstractShaft':
        '''AbstractShaft: 'SelectedDesignEntity' is the original name of this property.'''

        if _2114.AbstractShaft.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaft. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_abstract_shaft.setter
    def selected_design_entity_of_type_abstract_shaft(self, value: '_2114.AbstractShaft'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft_or_housing(self) -> '_2115.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'SelectedDesignEntity' is the original name of this property.'''

        if _2115.AbstractShaftOrHousing.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_abstract_shaft_or_housing.setter
    def selected_design_entity_of_type_abstract_shaft_or_housing(self, value: '_2115.AbstractShaftOrHousing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bearing(self) -> '_2118.Bearing':
        '''Bearing: 'SelectedDesignEntity' is the original name of this property.'''

        if _2118.Bearing.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Bearing. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bearing.setter
    def selected_design_entity_of_type_bearing(self, value: '_2118.Bearing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bolt(self) -> '_2120.Bolt':
        '''Bolt: 'SelectedDesignEntity' is the original name of this property.'''

        if _2120.Bolt.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Bolt. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bolt.setter
    def selected_design_entity_of_type_bolt(self, value: '_2120.Bolt'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bolted_joint(self) -> '_2121.BoltedJoint':
        '''BoltedJoint: 'SelectedDesignEntity' is the original name of this property.'''

        if _2121.BoltedJoint.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BoltedJoint. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bolted_joint.setter
    def selected_design_entity_of_type_bolted_joint(self, value: '_2121.BoltedJoint'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_component(self) -> '_2122.Component':
        '''Component: 'SelectedDesignEntity' is the original name of this property.'''

        if _2122.Component.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Component. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_component.setter
    def selected_design_entity_of_type_component(self, value: '_2122.Component'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_connector(self) -> '_2125.Connector':
        '''Connector: 'SelectedDesignEntity' is the original name of this property.'''

        if _2125.Connector.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Connector. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_connector.setter
    def selected_design_entity_of_type_connector(self, value: '_2125.Connector'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_datum(self) -> '_2126.Datum':
        '''Datum: 'SelectedDesignEntity' is the original name of this property.'''

        if _2126.Datum.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Datum. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_datum.setter
    def selected_design_entity_of_type_datum(self, value: '_2126.Datum'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_external_cad_model(self) -> '_2129.ExternalCADModel':
        '''ExternalCADModel: 'SelectedDesignEntity' is the original name of this property.'''

        if _2129.ExternalCADModel.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ExternalCADModel. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_external_cad_model.setter
    def selected_design_entity_of_type_external_cad_model(self, value: '_2129.ExternalCADModel'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_fe_part(self) -> '_2130.FEPart':
        '''FEPart: 'SelectedDesignEntity' is the original name of this property.'''

        if _2130.FEPart.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FEPart. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_fe_part.setter
    def selected_design_entity_of_type_fe_part(self, value: '_2130.FEPart'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_flexible_pin_assembly(self) -> '_2131.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2131.FlexiblePinAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FlexiblePinAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_flexible_pin_assembly.setter
    def selected_design_entity_of_type_flexible_pin_assembly(self, value: '_2131.FlexiblePinAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_guide_dxf_model(self) -> '_2132.GuideDxfModel':
        '''GuideDxfModel: 'SelectedDesignEntity' is the original name of this property.'''

        if _2132.GuideDxfModel.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GuideDxfModel. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_guide_dxf_model.setter
    def selected_design_entity_of_type_guide_dxf_model(self, value: '_2132.GuideDxfModel'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_mass_disc(self) -> '_2139.MassDisc':
        '''MassDisc: 'SelectedDesignEntity' is the original name of this property.'''

        if _2139.MassDisc.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MassDisc. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_mass_disc.setter
    def selected_design_entity_of_type_mass_disc(self, value: '_2139.MassDisc'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_measurement_component(self) -> '_2140.MeasurementComponent':
        '''MeasurementComponent: 'SelectedDesignEntity' is the original name of this property.'''

        if _2140.MeasurementComponent.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MeasurementComponent. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_measurement_component.setter
    def selected_design_entity_of_type_measurement_component(self, value: '_2140.MeasurementComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_mountable_component(self) -> '_2141.MountableComponent':
        '''MountableComponent: 'SelectedDesignEntity' is the original name of this property.'''

        if _2141.MountableComponent.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MountableComponent. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_mountable_component.setter
    def selected_design_entity_of_type_mountable_component(self, value: '_2141.MountableComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_oil_seal(self) -> '_2143.OilSeal':
        '''OilSeal: 'SelectedDesignEntity' is the original name of this property.'''

        if _2143.OilSeal.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to OilSeal. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_oil_seal.setter
    def selected_design_entity_of_type_oil_seal(self, value: '_2143.OilSeal'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part(self) -> '_2145.Part':
        '''Part: 'SelectedDesignEntity' is the original name of this property.'''

        if _2145.Part.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Part. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_part.setter
    def selected_design_entity_of_type_part(self, value: '_2145.Part'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planet_carrier(self) -> '_2146.PlanetCarrier':
        '''PlanetCarrier: 'SelectedDesignEntity' is the original name of this property.'''

        if _2146.PlanetCarrier.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetCarrier. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_planet_carrier.setter
    def selected_design_entity_of_type_planet_carrier(self, value: '_2146.PlanetCarrier'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_point_load(self) -> '_2148.PointLoad':
        '''PointLoad: 'SelectedDesignEntity' is the original name of this property.'''

        if _2148.PointLoad.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PointLoad. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_point_load.setter
    def selected_design_entity_of_type_point_load(self, value: '_2148.PointLoad'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_power_load(self) -> '_2149.PowerLoad':
        '''PowerLoad: 'SelectedDesignEntity' is the original name of this property.'''

        if _2149.PowerLoad.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PowerLoad. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_power_load.setter
    def selected_design_entity_of_type_power_load(self, value: '_2149.PowerLoad'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_root_assembly(self) -> '_2151.RootAssembly':
        '''RootAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2151.RootAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RootAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_root_assembly.setter
    def selected_design_entity_of_type_root_assembly(self, value: '_2151.RootAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_specialised_assembly(self) -> '_2153.SpecialisedAssembly':
        '''SpecialisedAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2153.SpecialisedAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpecialisedAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_specialised_assembly.setter
    def selected_design_entity_of_type_specialised_assembly(self, value: '_2153.SpecialisedAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_unbalanced_mass(self) -> '_2154.UnbalancedMass':
        '''UnbalancedMass: 'SelectedDesignEntity' is the original name of this property.'''

        if _2154.UnbalancedMass.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to UnbalancedMass. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_unbalanced_mass.setter
    def selected_design_entity_of_type_unbalanced_mass(self, value: '_2154.UnbalancedMass'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_virtual_component(self) -> '_2155.VirtualComponent':
        '''VirtualComponent: 'SelectedDesignEntity' is the original name of this property.'''

        if _2155.VirtualComponent.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to VirtualComponent. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_virtual_component.setter
    def selected_design_entity_of_type_virtual_component(self, value: '_2155.VirtualComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft(self) -> '_2158.Shaft':
        '''Shaft: 'SelectedDesignEntity' is the original name of this property.'''

        if _2158.Shaft.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Shaft. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_shaft.setter
    def selected_design_entity_of_type_shaft(self, value: '_2158.Shaft'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear(self) -> '_2188.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2188.AGMAGleasonConicalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_agma_gleason_conical_gear.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear(self, value: '_2188.AGMAGleasonConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear_set(self) -> '_2189.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2189.AGMAGleasonConicalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_agma_gleason_conical_gear_set.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear_set(self, value: '_2189.AGMAGleasonConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear(self) -> '_2190.BevelDifferentialGear':
        '''BevelDifferentialGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2190.BevelDifferentialGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_differential_gear.setter
    def selected_design_entity_of_type_bevel_differential_gear(self, value: '_2190.BevelDifferentialGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear_set(self) -> '_2191.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2191.BevelDifferentialGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_differential_gear_set.setter
    def selected_design_entity_of_type_bevel_differential_gear_set(self, value: '_2191.BevelDifferentialGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_planet_gear(self) -> '_2192.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2192.BevelDifferentialPlanetGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_differential_planet_gear.setter
    def selected_design_entity_of_type_bevel_differential_planet_gear(self, value: '_2192.BevelDifferentialPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_sun_gear(self) -> '_2193.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2193.BevelDifferentialSunGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_differential_sun_gear.setter
    def selected_design_entity_of_type_bevel_differential_sun_gear(self, value: '_2193.BevelDifferentialSunGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear(self) -> '_2194.BevelGear':
        '''BevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2194.BevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_gear.setter
    def selected_design_entity_of_type_bevel_gear(self, value: '_2194.BevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear_set(self) -> '_2195.BevelGearSet':
        '''BevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2195.BevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_gear_set.setter
    def selected_design_entity_of_type_bevel_gear_set(self, value: '_2195.BevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear(self) -> '_2196.ConceptGear':
        '''ConceptGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2196.ConceptGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_gear.setter
    def selected_design_entity_of_type_concept_gear(self, value: '_2196.ConceptGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear_set(self) -> '_2197.ConceptGearSet':
        '''ConceptGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2197.ConceptGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_gear_set.setter
    def selected_design_entity_of_type_concept_gear_set(self, value: '_2197.ConceptGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear(self) -> '_2198.ConicalGear':
        '''ConicalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2198.ConicalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_conical_gear.setter
    def selected_design_entity_of_type_conical_gear(self, value: '_2198.ConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear_set(self) -> '_2199.ConicalGearSet':
        '''ConicalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2199.ConicalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_conical_gear_set.setter
    def selected_design_entity_of_type_conical_gear_set(self, value: '_2199.ConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear(self) -> '_2200.CylindricalGear':
        '''CylindricalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2200.CylindricalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cylindrical_gear.setter
    def selected_design_entity_of_type_cylindrical_gear(self, value: '_2200.CylindricalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear_set(self) -> '_2201.CylindricalGearSet':
        '''CylindricalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2201.CylindricalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cylindrical_gear_set.setter
    def selected_design_entity_of_type_cylindrical_gear_set(self, value: '_2201.CylindricalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_planet_gear(self) -> '_2202.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2202.CylindricalPlanetGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cylindrical_planet_gear.setter
    def selected_design_entity_of_type_cylindrical_planet_gear(self, value: '_2202.CylindricalPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear(self) -> '_2203.FaceGear':
        '''FaceGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2203.FaceGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_face_gear.setter
    def selected_design_entity_of_type_face_gear(self, value: '_2203.FaceGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear_set(self) -> '_2204.FaceGearSet':
        '''FaceGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2204.FaceGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_face_gear_set.setter
    def selected_design_entity_of_type_face_gear_set(self, value: '_2204.FaceGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear(self) -> '_2205.Gear':
        '''Gear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2205.Gear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Gear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_gear.setter
    def selected_design_entity_of_type_gear(self, value: '_2205.Gear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear_set(self) -> '_2207.GearSet':
        '''GearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2207.GearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_gear_set.setter
    def selected_design_entity_of_type_gear_set(self, value: '_2207.GearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear(self) -> '_2209.HypoidGear':
        '''HypoidGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2209.HypoidGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_hypoid_gear.setter
    def selected_design_entity_of_type_hypoid_gear(self, value: '_2209.HypoidGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear_set(self) -> '_2210.HypoidGearSet':
        '''HypoidGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2210.HypoidGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_hypoid_gear_set.setter
    def selected_design_entity_of_type_hypoid_gear_set(self, value: '_2210.HypoidGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2211.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2211.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear(self, value: '_2211.KlingelnbergCycloPalloidConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2212.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2212.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self, value: '_2212.KlingelnbergCycloPalloidConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2213.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2213.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self, value: '_2213.KlingelnbergCycloPalloidHypoidGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2214.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2214.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self, value: '_2214.KlingelnbergCycloPalloidHypoidGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2215.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2215.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, value: '_2215.KlingelnbergCycloPalloidSpiralBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2216.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2216.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, value: '_2216.KlingelnbergCycloPalloidSpiralBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planetary_gear_set(self) -> '_2217.PlanetaryGearSet':
        '''PlanetaryGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2217.PlanetaryGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetaryGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_planetary_gear_set.setter
    def selected_design_entity_of_type_planetary_gear_set(self, value: '_2217.PlanetaryGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear(self) -> '_2218.SpiralBevelGear':
        '''SpiralBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2218.SpiralBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spiral_bevel_gear.setter
    def selected_design_entity_of_type_spiral_bevel_gear(self, value: '_2218.SpiralBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear_set(self) -> '_2219.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2219.SpiralBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spiral_bevel_gear_set.setter
    def selected_design_entity_of_type_spiral_bevel_gear_set(self, value: '_2219.SpiralBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear(self) -> '_2220.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2220.StraightBevelDiffGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_diff_gear.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear(self, value: '_2220.StraightBevelDiffGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear_set(self) -> '_2221.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2221.StraightBevelDiffGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_diff_gear_set.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear_set(self, value: '_2221.StraightBevelDiffGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear(self) -> '_2222.StraightBevelGear':
        '''StraightBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2222.StraightBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_gear.setter
    def selected_design_entity_of_type_straight_bevel_gear(self, value: '_2222.StraightBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear_set(self) -> '_2223.StraightBevelGearSet':
        '''StraightBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2223.StraightBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_gear_set.setter
    def selected_design_entity_of_type_straight_bevel_gear_set(self, value: '_2223.StraightBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_planet_gear(self) -> '_2224.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2224.StraightBevelPlanetGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_planet_gear.setter
    def selected_design_entity_of_type_straight_bevel_planet_gear(self, value: '_2224.StraightBevelPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_sun_gear(self) -> '_2225.StraightBevelSunGear':
        '''StraightBevelSunGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2225.StraightBevelSunGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_sun_gear.setter
    def selected_design_entity_of_type_straight_bevel_sun_gear(self, value: '_2225.StraightBevelSunGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear(self) -> '_2226.WormGear':
        '''WormGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2226.WormGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_worm_gear.setter
    def selected_design_entity_of_type_worm_gear(self, value: '_2226.WormGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear_set(self) -> '_2227.WormGearSet':
        '''WormGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2227.WormGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_worm_gear_set.setter
    def selected_design_entity_of_type_worm_gear_set(self, value: '_2227.WormGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear(self) -> '_2228.ZerolBevelGear':
        '''ZerolBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2228.ZerolBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_zerol_bevel_gear.setter
    def selected_design_entity_of_type_zerol_bevel_gear(self, value: '_2228.ZerolBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear_set(self) -> '_2229.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2229.ZerolBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_zerol_bevel_gear_set.setter
    def selected_design_entity_of_type_zerol_bevel_gear_set(self, value: '_2229.ZerolBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_assembly(self) -> '_2243.CycloidalAssembly':
        '''CycloidalAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2243.CycloidalAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cycloidal_assembly.setter
    def selected_design_entity_of_type_cycloidal_assembly(self, value: '_2243.CycloidalAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc(self) -> '_2244.CycloidalDisc':
        '''CycloidalDisc: 'SelectedDesignEntity' is the original name of this property.'''

        if _2244.CycloidalDisc.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDisc. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cycloidal_disc.setter
    def selected_design_entity_of_type_cycloidal_disc(self, value: '_2244.CycloidalDisc'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_ring_pins(self) -> '_2245.RingPins':
        '''RingPins: 'SelectedDesignEntity' is the original name of this property.'''

        if _2245.RingPins.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RingPins. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_ring_pins.setter
    def selected_design_entity_of_type_ring_pins(self, value: '_2245.RingPins'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_belt_drive(self) -> '_2251.BeltDrive':
        '''BeltDrive: 'SelectedDesignEntity' is the original name of this property.'''

        if _2251.BeltDrive.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BeltDrive. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_belt_drive.setter
    def selected_design_entity_of_type_belt_drive(self, value: '_2251.BeltDrive'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch(self) -> '_2253.Clutch':
        '''Clutch: 'SelectedDesignEntity' is the original name of this property.'''

        if _2253.Clutch.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Clutch. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_clutch.setter
    def selected_design_entity_of_type_clutch(self, value: '_2253.Clutch'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch_half(self) -> '_2254.ClutchHalf':
        '''ClutchHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2254.ClutchHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ClutchHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_clutch_half.setter
    def selected_design_entity_of_type_clutch_half(self, value: '_2254.ClutchHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling(self) -> '_2256.ConceptCoupling':
        '''ConceptCoupling: 'SelectedDesignEntity' is the original name of this property.'''

        if _2256.ConceptCoupling.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCoupling. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_coupling.setter
    def selected_design_entity_of_type_concept_coupling(self, value: '_2256.ConceptCoupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling_half(self) -> '_2257.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2257.ConceptCouplingHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_coupling_half.setter
    def selected_design_entity_of_type_concept_coupling_half(self, value: '_2257.ConceptCouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling(self) -> '_2258.Coupling':
        '''Coupling: 'SelectedDesignEntity' is the original name of this property.'''

        if _2258.Coupling.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Coupling. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_coupling.setter
    def selected_design_entity_of_type_coupling(self, value: '_2258.Coupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling_half(self) -> '_2259.CouplingHalf':
        '''CouplingHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2259.CouplingHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CouplingHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_coupling_half.setter
    def selected_design_entity_of_type_coupling_half(self, value: '_2259.CouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt(self) -> '_2261.CVT':
        '''CVT: 'SelectedDesignEntity' is the original name of this property.'''

        if _2261.CVT.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVT. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cvt.setter
    def selected_design_entity_of_type_cvt(self, value: '_2261.CVT'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt_pulley(self) -> '_2262.CVTPulley':
        '''CVTPulley: 'SelectedDesignEntity' is the original name of this property.'''

        if _2262.CVTPulley.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVTPulley. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cvt_pulley.setter
    def selected_design_entity_of_type_cvt_pulley(self, value: '_2262.CVTPulley'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling(self) -> '_2263.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'SelectedDesignEntity' is the original name of this property.'''

        if _2263.PartToPartShearCoupling.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCoupling. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_part_to_part_shear_coupling.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling(self, value: '_2263.PartToPartShearCoupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling_half(self) -> '_2264.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2264.PartToPartShearCouplingHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_part_to_part_shear_coupling_half.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling_half(self, value: '_2264.PartToPartShearCouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_pulley(self) -> '_2265.Pulley':
        '''Pulley: 'SelectedDesignEntity' is the original name of this property.'''

        if _2265.Pulley.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Pulley. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_pulley.setter
    def selected_design_entity_of_type_pulley(self, value: '_2265.Pulley'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring(self) -> '_2271.RollingRing':
        '''RollingRing: 'SelectedDesignEntity' is the original name of this property.'''

        if _2271.RollingRing.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRing. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_rolling_ring.setter
    def selected_design_entity_of_type_rolling_ring(self, value: '_2271.RollingRing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring_assembly(self) -> '_2272.RollingRingAssembly':
        '''RollingRingAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2272.RollingRingAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRingAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_rolling_ring_assembly.setter
    def selected_design_entity_of_type_rolling_ring_assembly(self, value: '_2272.RollingRingAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft_hub_connection(self) -> '_2273.ShaftHubConnection':
        '''ShaftHubConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2273.ShaftHubConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ShaftHubConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_shaft_hub_connection.setter
    def selected_design_entity_of_type_shaft_hub_connection(self, value: '_2273.ShaftHubConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper(self) -> '_2275.SpringDamper':
        '''SpringDamper: 'SelectedDesignEntity' is the original name of this property.'''

        if _2275.SpringDamper.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamper. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spring_damper.setter
    def selected_design_entity_of_type_spring_damper(self, value: '_2275.SpringDamper'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper_half(self) -> '_2276.SpringDamperHalf':
        '''SpringDamperHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2276.SpringDamperHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamperHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spring_damper_half.setter
    def selected_design_entity_of_type_spring_damper_half(self, value: '_2276.SpringDamperHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser(self) -> '_2277.Synchroniser':
        '''Synchroniser: 'SelectedDesignEntity' is the original name of this property.'''

        if _2277.Synchroniser.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Synchroniser. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_synchroniser.setter
    def selected_design_entity_of_type_synchroniser(self, value: '_2277.Synchroniser'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_half(self) -> '_2279.SynchroniserHalf':
        '''SynchroniserHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2279.SynchroniserHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_synchroniser_half.setter
    def selected_design_entity_of_type_synchroniser_half(self, value: '_2279.SynchroniserHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_part(self) -> '_2280.SynchroniserPart':
        '''SynchroniserPart: 'SelectedDesignEntity' is the original name of this property.'''

        if _2280.SynchroniserPart.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserPart. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_synchroniser_part.setter
    def selected_design_entity_of_type_synchroniser_part(self, value: '_2280.SynchroniserPart'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_sleeve(self) -> '_2281.SynchroniserSleeve':
        '''SynchroniserSleeve: 'SelectedDesignEntity' is the original name of this property.'''

        if _2281.SynchroniserSleeve.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_synchroniser_sleeve.setter
    def selected_design_entity_of_type_synchroniser_sleeve(self, value: '_2281.SynchroniserSleeve'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter(self) -> '_2282.TorqueConverter':
        '''TorqueConverter: 'SelectedDesignEntity' is the original name of this property.'''

        if _2282.TorqueConverter.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverter. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_torque_converter.setter
    def selected_design_entity_of_type_torque_converter(self, value: '_2282.TorqueConverter'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_pump(self) -> '_2283.TorqueConverterPump':
        '''TorqueConverterPump: 'SelectedDesignEntity' is the original name of this property.'''

        if _2283.TorqueConverterPump.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterPump. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_torque_converter_pump.setter
    def selected_design_entity_of_type_torque_converter_pump(self, value: '_2283.TorqueConverterPump'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_turbine(self) -> '_2285.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'SelectedDesignEntity' is the original name of this property.'''

        if _2285.TorqueConverterTurbine.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_torque_converter_turbine.setter
    def selected_design_entity_of_type_torque_converter_turbine(self, value: '_2285.TorqueConverterTurbine'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def active_design(self) -> '_1887.Design':
        '''Design: 'ActiveDesign' is the original name of this property.'''

        return constructor.new(_1887.Design)(self.wrapped.ActiveDesign) if self.wrapped.ActiveDesign else None

    @active_design.setter
    def active_design(self, value: '_1887.Design'):
        value = value.wrapped if value else None
        self.wrapped.ActiveDesign = value

    @property
    def restart_space_claim_flag(self) -> 'bool':
        '''bool: 'RestartSpaceClaimFlag' is the original name of this property.'''

        return self.wrapped.RestartSpaceClaimFlag

    @restart_space_claim_flag.setter
    def restart_space_claim_flag(self, value: 'bool'):
        self.wrapped.RestartSpaceClaimFlag = bool(value) if value else False

    @property
    def space_claim_process_id(self) -> 'int':
        '''int: 'SpaceClaimProcessID' is the original name of this property.'''

        return self.wrapped.SpaceClaimProcessID

    @space_claim_process_id.setter
    def space_claim_process_id(self, value: 'int'):
        self.wrapped.SpaceClaimProcessID = int(value) if value else 0

    @property
    def restart_space_claim_save_file(self) -> 'str':
        '''str: 'RestartSpaceClaimSaveFile' is the original name of this property.'''

        return self.wrapped.RestartSpaceClaimSaveFile

    @restart_space_claim_save_file.setter
    def restart_space_claim_save_file(self, value: 'str'):
        self.wrapped.RestartSpaceClaimSaveFile = str(value) if value else None

    @property
    def color_of_new_problem_node_group(self) -> 'Color':
        '''Color: 'ColorOfNewProblemNodeGroup' is the original name of this property.'''

        value = conversion.pn_to_mp_color(self.wrapped.ColorOfNewProblemNodeGroup)
        return value

    @color_of_new_problem_node_group.setter
    def color_of_new_problem_node_group(self, value: 'Color'):
        value = value if value else None
        value = conversion.mp_to_pn_color(value)
        self.wrapped.ColorOfNewProblemNodeGroup = value

    @property
    def name_of_new_problem_node_group(self) -> 'str':
        '''str: 'NameOfNewProblemNodeGroup' is the original name of this property.'''

        return self.wrapped.NameOfNewProblemNodeGroup

    @name_of_new_problem_node_group.setter
    def name_of_new_problem_node_group(self, value: 'str'):
        self.wrapped.NameOfNewProblemNodeGroup = str(value) if value else None

    @property
    def positions_of_problem_node_group(self) -> 'List[Vector3D]':
        '''List[Vector3D]: 'PositionsOfProblemNodeGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PositionsOfProblemNodeGroup, Vector3D)
        return value

    @property
    def operation_mode(self) -> '_1521.OperationMode':
        '''OperationMode: 'OperationMode' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.OperationMode)
        return constructor.new(_1521.OperationMode)(value) if value else None

    @operation_mode.setter
    def operation_mode(self, value: '_1521.OperationMode'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OperationMode = value

    @property
    def is_connected_to_space_claim(self) -> 'bool':
        '''bool: 'IsConnectedToSpaceClaim' is the original name of this property.'''

        return self.wrapped.IsConnectedToSpaceClaim

    @is_connected_to_space_claim.setter
    def is_connected_to_space_claim(self, value: 'bool'):
        self.wrapped.IsConnectedToSpaceClaim = bool(value) if value else False

    @property
    def process_id(self) -> 'int':
        '''int: 'ProcessId' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ProcessId

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    @staticmethod
    def get_mastagui(process_id: 'int') -> 'MASTAGUI':
        ''' 'GetMASTAGUI' is the original name of this method.

        Args:
            process_id (int)

        Returns:
            mastapy.system_model_gui.MASTAGUI
        '''

        process_id = int(process_id)
        method_result = MASTAGUI.TYPE.GetMASTAGUI(process_id if process_id else 0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def resume(self):
        ''' 'Resume' is the original name of this method.'''

        self.wrapped.Resume()

    def pause(self):
        ''' 'Pause' is the original name of this method.'''

        self.wrapped.Pause()

    def start_remoting(self):
        ''' 'StartRemoting' is the original name of this method.'''

        self.wrapped.StartRemoting()

    def stop_remoting(self):
        ''' 'StopRemoting' is the original name of this method.'''

        self.wrapped.StopRemoting()

    def open_design_in_new_tab(self, design: '_1887.Design'):
        ''' 'OpenDesignInNewTab' is the original name of this method.

        Args:
            design (mastapy.system_model.Design)
        '''

        self.wrapped.OpenDesignInNewTab(design.wrapped if design else None)

    def select_tab(self, tab_text: 'str'):
        ''' 'SelectTab' is the original name of this method.

        Args:
            tab_text (str)
        '''

        tab_text = str(tab_text)
        self.wrapped.SelectTab(tab_text if tab_text else None)

    def move_selected_component(self, origin: 'Vector3D', axis: 'Vector3D'):
        ''' 'MoveSelectedComponent' is the original name of this method.

        Args:
            origin (Vector3D)
            axis (Vector3D)
        '''

        origin = conversion.mp_to_pn_vector3d(origin)
        axis = conversion.mp_to_pn_vector3d(axis)
        self.wrapped.MoveSelectedComponent(origin, axis)

    def run_command(self, command: 'str'):
        ''' 'RunCommand' is the original name of this method.

        Args:
            command (str)
        '''

        command = str(command)
        self.wrapped.RunCommand(command if command else None)

    def add_line_from_space_claim(self, circles_on_axis: '_1255.CirclesOnAxis'):
        ''' 'AddLineFromSpaceClaim' is the original name of this method.

        Args:
            circles_on_axis (mastapy.math_utility.CirclesOnAxis)
        '''

        self.wrapped.AddLineFromSpaceClaim(circles_on_axis.wrapped if circles_on_axis else None)

    def show_boxes(self, small_box: 'List[Vector3D]', big_box: 'List[Vector3D]'):
        ''' 'ShowBoxes' is the original name of this method.

        Args:
            small_box (List[Vector3D])
            big_box (List[Vector3D])
        '''

        small_box = conversion.mp_to_pn_objects_in_list(small_box)
        big_box = conversion.mp_to_pn_objects_in_list(big_box)
        self.wrapped.ShowBoxes(small_box, big_box)

    def circle_pairs_from_space_claim(self, preselection_circles: '_1255.CirclesOnAxis', selected_circles: 'List[_1255.CirclesOnAxis]'):
        ''' 'CirclePairsFromSpaceClaim' is the original name of this method.

        Args:
            preselection_circles (mastapy.math_utility.CirclesOnAxis)
            selected_circles (List[mastapy.math_utility.CirclesOnAxis])
        '''

        selected_circles = conversion.mp_to_pn_objects_in_list(selected_circles)
        self.wrapped.CirclePairsFromSpaceClaim(preselection_circles.wrapped if preselection_circles else None, selected_circles)

    def add_fe_substructure_from_data(self, vertices_and_facets: '_1274.FacetedBody', dimensions: 'Dict[str, _118.SpaceClaimDimension]', moniker: 'str'):
        ''' 'AddFESubstructureFromData' is the original name of this method.

        Args:
            vertices_and_facets (mastapy.math_utility.FacetedBody)
            dimensions (Dict[str, mastapy.nodal_analysis.space_claim_link.SpaceClaimDimension])
            moniker (str)
        '''

        moniker = str(moniker)
        self.wrapped.AddFESubstructureFromData(vertices_and_facets.wrapped if vertices_and_facets else None, dimensions, moniker if moniker else None)

    def add_fe_substructure_from_file(self, length_scale: 'float', stl_file_name: 'str', dimensions: 'Dict[str, _118.SpaceClaimDimension]'):
        ''' 'AddFESubstructureFromFile' is the original name of this method.

        Args:
            length_scale (float)
            stl_file_name (str)
            dimensions (Dict[str, mastapy.nodal_analysis.space_claim_link.SpaceClaimDimension])
        '''

        length_scale = float(length_scale)
        stl_file_name = str(stl_file_name)
        self.wrapped.AddFESubstructureFromFile(length_scale if length_scale else 0.0, stl_file_name if stl_file_name else None, dimensions)

    def flag_message_received(self):
        ''' 'FlagMessageReceived' is the original name of this method.'''

        self.wrapped.FlagMessageReceived()

    def space_claim_document_loaded(self):
        ''' 'SpaceClaimDocumentLoaded' is the original name of this method.'''

        self.wrapped.SpaceClaimDocumentLoaded()

    def set_error(self, error: 'str'):
        ''' 'SetError' is the original name of this method.

        Args:
            error (str)
        '''

        error = str(error)
        self.wrapped.SetError(error if error else None)

    def new_dimensions(self, dimensions: 'Dict[str, _118.SpaceClaimDimension]'):
        ''' 'NewDimensions' is the original name of this method.

        Args:
            dimensions (Dict[str, mastapy.nodal_analysis.space_claim_link.SpaceClaimDimension])
        '''

        self.wrapped.NewDimensions(dimensions)

    def create_space_claim_dimension(self) -> '_118.SpaceClaimDimension':
        ''' 'CreateSpaceClaimDimension' is the original name of this method.

        Returns:
            mastapy.nodal_analysis.space_claim_link.SpaceClaimDimension
        '''

        method_result = self.wrapped.CreateSpaceClaimDimension()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def new_mesh_data(self, vertices_and_facets: '_1274.FacetedBody'):
        ''' 'NewMeshData' is the original name of this method.

        Args:
            vertices_and_facets (mastapy.math_utility.FacetedBody)
        '''

        self.wrapped.NewMeshData.Overloads[_FACETED_BODY](vertices_and_facets.wrapped if vertices_and_facets else None)

    def new_mesh_data_from_file(self, stl_file_name: 'str'):
        ''' 'NewMeshData' is the original name of this method.

        Args:
            stl_file_name (str)
        '''

        stl_file_name = str(stl_file_name)
        self.wrapped.NewMeshData.Overloads[_STRING](stl_file_name if stl_file_name else None)

    def create_new_circles_on_axis(self) -> '_1255.CirclesOnAxis':
        ''' 'CreateNewCirclesOnAxis' is the original name of this method.

        Returns:
            mastapy.math_utility.CirclesOnAxis
        '''

        method_result = self.wrapped.CreateNewCirclesOnAxis()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def create_new_faceted_body(self) -> '_1274.FacetedBody':
        ''' 'CreateNewFacetedBody' is the original name of this method.

        Returns:
            mastapy.math_utility.FacetedBody
        '''

        method_result = self.wrapped.CreateNewFacetedBody()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
