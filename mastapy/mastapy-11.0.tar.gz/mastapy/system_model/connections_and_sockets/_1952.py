'''_1952.py

Connection
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _1976, _1946, _1947, _1954,
    _1956, _1958, _1959, _1960,
    _1962, _1963, _1964, _1965,
    _1966, _1968, _1969, _1970,
    _1973, _1974
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1980, _1982, _1984, _1986,
    _1988, _1990, _1992, _1994,
    _1996, _1997, _2001, _2002,
    _2004, _2006, _2008, _2010,
    _2012
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2013, _2014, _2016, _2017,
    _2019, _2020
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2023, _2025, _2027, _2029,
    _2031, _2033, _2034
)
from mastapy.system_model.part_model import (
    _2122, _2114, _2115, _2118,
    _2120, _2125, _2126, _2129,
    _2130, _2132, _2139, _2140,
    _2141, _2143, _2146, _2148,
    _2149, _2154, _2155
)
from mastapy.system_model.part_model.shaft_model import _2158
from mastapy.system_model.part_model.gears import (
    _2188, _2190, _2192, _2193,
    _2194, _2196, _2198, _2200,
    _2202, _2203, _2205, _2209,
    _2211, _2213, _2215, _2218,
    _2220, _2222, _2224, _2225,
    _2226, _2228
)
from mastapy.system_model.part_model.cycloidal import _2244, _2245
from mastapy.system_model.part_model.couplings import (
    _2254, _2257, _2259, _2262,
    _2264, _2265, _2271, _2273,
    _2276, _2279, _2280, _2281,
    _2283, _2285
)
from mastapy._internal.python_net import python_net_import
from mastapy.system_model import _1891

_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Socket')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')


__docformat__ = 'restructuredtext en'
__all__ = ('Connection',)


class Connection(_1891.DesignEntity):
    '''Connection

    This is a mastapy class.
    '''

    TYPE = _CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Connection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def drawing_position(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'DrawingPosition' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.DrawingPosition) if self.wrapped.DrawingPosition else None

    @drawing_position.setter
    def drawing_position(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.DrawingPosition = value

    @property
    def speed_ratio_from_a_to_b(self) -> 'float':
        '''float: 'SpeedRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedRatioFromAToB

    @property
    def torque_ratio_from_a_to_b(self) -> 'float':
        '''float: 'TorqueRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueRatioFromAToB

    @property
    def unique_name(self) -> 'str':
        '''str: 'UniqueName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UniqueName

    @property
    def connection_id(self) -> 'str':
        '''str: 'ConnectionID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ConnectionID

    @property
    def socket_a(self) -> '_1976.Socket':
        '''Socket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1976.Socket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to Socket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_bearing_inner_socket(self) -> '_1946.BearingInnerSocket':
        '''BearingInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1946.BearingInnerSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BearingInnerSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_bearing_outer_socket(self) -> '_1947.BearingOuterSocket':
        '''BearingOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1947.BearingOuterSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BearingOuterSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cvt_pulley_socket(self) -> '_1954.CVTPulleySocket':
        '''CVTPulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1954.CVTPulleySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CVTPulleySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cylindrical_socket(self) -> '_1956.CylindricalSocket':
        '''CylindricalSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1956.CylindricalSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_electric_machine_stator_socket(self) -> '_1958.ElectricMachineStatorSocket':
        '''ElectricMachineStatorSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1958.ElectricMachineStatorSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ElectricMachineStatorSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_inner_shaft_socket(self) -> '_1959.InnerShaftSocket':
        '''InnerShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.InnerShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_inner_shaft_socket_base(self) -> '_1960.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1960.InnerShaftSocketBase.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_mountable_component_inner_socket(self) -> '_1962.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.MountableComponentInnerSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_mountable_component_outer_socket(self) -> '_1963.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1963.MountableComponentOuterSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_mountable_component_socket(self) -> '_1964.MountableComponentSocket':
        '''MountableComponentSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.MountableComponentSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_outer_shaft_socket(self) -> '_1965.OuterShaftSocket':
        '''OuterShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1965.OuterShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_outer_shaft_socket_base(self) -> '_1966.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1966.OuterShaftSocketBase.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_planetary_socket(self) -> '_1968.PlanetarySocket':
        '''PlanetarySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1968.PlanetarySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PlanetarySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_planetary_socket_base(self) -> '_1969.PlanetarySocketBase':
        '''PlanetarySocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.PlanetarySocketBase.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_pulley_socket(self) -> '_1970.PulleySocket':
        '''PulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1970.PulleySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PulleySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_rolling_ring_socket(self) -> '_1973.RollingRingSocket':
        '''RollingRingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.RollingRingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to RollingRingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_shaft_socket(self) -> '_1974.ShaftSocket':
        '''ShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1974.ShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_1980.AGMAGleasonConicalGearTeethSocket':
        '''AGMAGleasonConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1980.AGMAGleasonConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_bevel_differential_gear_teeth_socket(self) -> '_1982.BevelDifferentialGearTeethSocket':
        '''BevelDifferentialGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.BevelDifferentialGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelDifferentialGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_bevel_gear_teeth_socket(self) -> '_1984.BevelGearTeethSocket':
        '''BevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1984.BevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_concept_gear_teeth_socket(self) -> '_1986.ConceptGearTeethSocket':
        '''ConceptGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1986.ConceptGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_conical_gear_teeth_socket(self) -> '_1988.ConicalGearTeethSocket':
        '''ConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.ConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cylindrical_gear_teeth_socket(self) -> '_1990.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.CylindricalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_face_gear_teeth_socket(self) -> '_1992.FaceGearTeethSocket':
        '''FaceGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.FaceGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to FaceGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_gear_teeth_socket(self) -> '_1994.GearTeethSocket':
        '''GearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.GearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to GearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_hypoid_gear_teeth_socket(self) -> '_1996.HypoidGearTeethSocket':
        '''HypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.HypoidGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to HypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_1997.KlingelnbergConicalGearTeethSocket':
        '''KlingelnbergConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1997.KlingelnbergConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_2001.KlingelnbergHypoidGearTeethSocket':
        '''KlingelnbergHypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.KlingelnbergHypoidGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_2002.KlingelnbergSpiralBevelGearTeethSocket':
        '''KlingelnbergSpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_spiral_bevel_gear_teeth_socket(self) -> '_2004.SpiralBevelGearTeethSocket':
        '''SpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.SpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_2006.StraightBevelDiffGearTeethSocket':
        '''StraightBevelDiffGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.StraightBevelDiffGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_straight_bevel_gear_teeth_socket(self) -> '_2008.StraightBevelGearTeethSocket':
        '''StraightBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2008.StraightBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_worm_gear_teeth_socket(self) -> '_2010.WormGearTeethSocket':
        '''WormGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.WormGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to WormGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_zerol_bevel_gear_teeth_socket(self) -> '_2012.ZerolBevelGearTeethSocket':
        '''ZerolBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.ZerolBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ZerolBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cycloidal_disc_axial_left_socket(self) -> '_2013.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cycloidal_disc_axial_right_socket(self) -> '_2014.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2014.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cycloidal_disc_inner_socket(self) -> '_2016.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.CycloidalDiscInnerSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cycloidal_disc_outer_socket(self) -> '_2017.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.CycloidalDiscOuterSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2019.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_ring_pins_socket(self) -> '_2020.RingPinsSocket':
        '''RingPinsSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.RingPinsSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to RingPinsSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_clutch_socket(self) -> '_2023.ClutchSocket':
        '''ClutchSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.ClutchSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ClutchSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_concept_coupling_socket(self) -> '_2025.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.ConceptCouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_coupling_socket(self) -> '_2027.CouplingSocket':
        '''CouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.CouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_part_to_part_shear_coupling_socket(self) -> '_2029.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.PartToPartShearCouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_spring_damper_socket(self) -> '_2031.SpringDamperSocket':
        '''SpringDamperSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.SpringDamperSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpringDamperSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_torque_converter_pump_socket(self) -> '_2033.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.TorqueConverterPumpSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_torque_converter_turbine_socket(self) -> '_2034.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.TorqueConverterTurbineSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_b(self) -> '_1976.Socket':
        '''Socket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1976.Socket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to Socket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_bearing_inner_socket(self) -> '_1946.BearingInnerSocket':
        '''BearingInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1946.BearingInnerSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BearingInnerSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_bearing_outer_socket(self) -> '_1947.BearingOuterSocket':
        '''BearingOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1947.BearingOuterSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BearingOuterSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cvt_pulley_socket(self) -> '_1954.CVTPulleySocket':
        '''CVTPulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1954.CVTPulleySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CVTPulleySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cylindrical_socket(self) -> '_1956.CylindricalSocket':
        '''CylindricalSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1956.CylindricalSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_electric_machine_stator_socket(self) -> '_1958.ElectricMachineStatorSocket':
        '''ElectricMachineStatorSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1958.ElectricMachineStatorSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ElectricMachineStatorSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_inner_shaft_socket(self) -> '_1959.InnerShaftSocket':
        '''InnerShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.InnerShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_inner_shaft_socket_base(self) -> '_1960.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1960.InnerShaftSocketBase.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_mountable_component_inner_socket(self) -> '_1962.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.MountableComponentInnerSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_mountable_component_outer_socket(self) -> '_1963.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1963.MountableComponentOuterSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_mountable_component_socket(self) -> '_1964.MountableComponentSocket':
        '''MountableComponentSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.MountableComponentSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_outer_shaft_socket(self) -> '_1965.OuterShaftSocket':
        '''OuterShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1965.OuterShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_outer_shaft_socket_base(self) -> '_1966.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1966.OuterShaftSocketBase.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_planetary_socket(self) -> '_1968.PlanetarySocket':
        '''PlanetarySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1968.PlanetarySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PlanetarySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_planetary_socket_base(self) -> '_1969.PlanetarySocketBase':
        '''PlanetarySocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.PlanetarySocketBase.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_pulley_socket(self) -> '_1970.PulleySocket':
        '''PulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1970.PulleySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PulleySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_rolling_ring_socket(self) -> '_1973.RollingRingSocket':
        '''RollingRingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.RollingRingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to RollingRingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_shaft_socket(self) -> '_1974.ShaftSocket':
        '''ShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1974.ShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_1980.AGMAGleasonConicalGearTeethSocket':
        '''AGMAGleasonConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1980.AGMAGleasonConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_bevel_differential_gear_teeth_socket(self) -> '_1982.BevelDifferentialGearTeethSocket':
        '''BevelDifferentialGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.BevelDifferentialGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelDifferentialGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_bevel_gear_teeth_socket(self) -> '_1984.BevelGearTeethSocket':
        '''BevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1984.BevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_concept_gear_teeth_socket(self) -> '_1986.ConceptGearTeethSocket':
        '''ConceptGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1986.ConceptGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_conical_gear_teeth_socket(self) -> '_1988.ConicalGearTeethSocket':
        '''ConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.ConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cylindrical_gear_teeth_socket(self) -> '_1990.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.CylindricalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_face_gear_teeth_socket(self) -> '_1992.FaceGearTeethSocket':
        '''FaceGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.FaceGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to FaceGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_gear_teeth_socket(self) -> '_1994.GearTeethSocket':
        '''GearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.GearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to GearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_hypoid_gear_teeth_socket(self) -> '_1996.HypoidGearTeethSocket':
        '''HypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.HypoidGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to HypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_1997.KlingelnbergConicalGearTeethSocket':
        '''KlingelnbergConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1997.KlingelnbergConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_2001.KlingelnbergHypoidGearTeethSocket':
        '''KlingelnbergHypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.KlingelnbergHypoidGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_2002.KlingelnbergSpiralBevelGearTeethSocket':
        '''KlingelnbergSpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_spiral_bevel_gear_teeth_socket(self) -> '_2004.SpiralBevelGearTeethSocket':
        '''SpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.SpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_2006.StraightBevelDiffGearTeethSocket':
        '''StraightBevelDiffGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.StraightBevelDiffGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_straight_bevel_gear_teeth_socket(self) -> '_2008.StraightBevelGearTeethSocket':
        '''StraightBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2008.StraightBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_worm_gear_teeth_socket(self) -> '_2010.WormGearTeethSocket':
        '''WormGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.WormGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to WormGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_zerol_bevel_gear_teeth_socket(self) -> '_2012.ZerolBevelGearTeethSocket':
        '''ZerolBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.ZerolBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ZerolBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cycloidal_disc_axial_left_socket(self) -> '_2013.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cycloidal_disc_axial_right_socket(self) -> '_2014.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2014.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cycloidal_disc_inner_socket(self) -> '_2016.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.CycloidalDiscInnerSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cycloidal_disc_outer_socket(self) -> '_2017.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.CycloidalDiscOuterSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2019.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_ring_pins_socket(self) -> '_2020.RingPinsSocket':
        '''RingPinsSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.RingPinsSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to RingPinsSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_clutch_socket(self) -> '_2023.ClutchSocket':
        '''ClutchSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.ClutchSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ClutchSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_concept_coupling_socket(self) -> '_2025.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.ConceptCouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_coupling_socket(self) -> '_2027.CouplingSocket':
        '''CouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.CouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_part_to_part_shear_coupling_socket(self) -> '_2029.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.PartToPartShearCouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_spring_damper_socket(self) -> '_2031.SpringDamperSocket':
        '''SpringDamperSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.SpringDamperSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpringDamperSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_torque_converter_pump_socket(self) -> '_2033.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.TorqueConverterPumpSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_torque_converter_turbine_socket(self) -> '_2034.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.TorqueConverterTurbineSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def owner_a(self) -> '_2122.Component':
        '''Component: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2122.Component.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Component. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_abstract_shaft(self) -> '_2114.AbstractShaft':
        '''AbstractShaft: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.AbstractShaft.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AbstractShaft. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_abstract_shaft_or_housing(self) -> '_2115.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2115.AbstractShaftOrHousing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bearing(self) -> '_2118.Bearing':
        '''Bearing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2118.Bearing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bearing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bolt(self) -> '_2120.Bolt':
        '''Bolt: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.Bolt.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bolt. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_connector(self) -> '_2125.Connector':
        '''Connector: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2125.Connector.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Connector. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_datum(self) -> '_2126.Datum':
        '''Datum: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2126.Datum.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Datum. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_external_cad_model(self) -> '_2129.ExternalCADModel':
        '''ExternalCADModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2129.ExternalCADModel.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ExternalCADModel. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_fe_part(self) -> '_2130.FEPart':
        '''FEPart: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2130.FEPart.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to FEPart. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_guide_dxf_model(self) -> '_2132.GuideDxfModel':
        '''GuideDxfModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2132.GuideDxfModel.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to GuideDxfModel. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_mass_disc(self) -> '_2139.MassDisc':
        '''MassDisc: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2139.MassDisc.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MassDisc. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_measurement_component(self) -> '_2140.MeasurementComponent':
        '''MeasurementComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2140.MeasurementComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MeasurementComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_mountable_component(self) -> '_2141.MountableComponent':
        '''MountableComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2141.MountableComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MountableComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_oil_seal(self) -> '_2143.OilSeal':
        '''OilSeal: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.OilSeal.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to OilSeal. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_planet_carrier(self) -> '_2146.PlanetCarrier':
        '''PlanetCarrier: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2146.PlanetCarrier.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PlanetCarrier. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_point_load(self) -> '_2148.PointLoad':
        '''PointLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2148.PointLoad.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PointLoad. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_power_load(self) -> '_2149.PowerLoad':
        '''PowerLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.PowerLoad.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PowerLoad. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_unbalanced_mass(self) -> '_2154.UnbalancedMass':
        '''UnbalancedMass: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2154.UnbalancedMass.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to UnbalancedMass. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_virtual_component(self) -> '_2155.VirtualComponent':
        '''VirtualComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2155.VirtualComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to VirtualComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_shaft(self) -> '_2158.Shaft':
        '''Shaft: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2158.Shaft.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Shaft. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_agma_gleason_conical_gear(self) -> '_2188.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2188.AGMAGleasonConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_differential_gear(self) -> '_2190.BevelDifferentialGear':
        '''BevelDifferentialGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2190.BevelDifferentialGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_differential_planet_gear(self) -> '_2192.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2192.BevelDifferentialPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_differential_sun_gear(self) -> '_2193.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2193.BevelDifferentialSunGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_gear(self) -> '_2194.BevelGear':
        '''BevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2194.BevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_concept_gear(self) -> '_2196.ConceptGear':
        '''ConceptGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.ConceptGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_conical_gear(self) -> '_2198.ConicalGear':
        '''ConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2198.ConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_cylindrical_gear(self) -> '_2200.CylindricalGear':
        '''CylindricalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.CylindricalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_cylindrical_planet_gear(self) -> '_2202.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2202.CylindricalPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_face_gear(self) -> '_2203.FaceGear':
        '''FaceGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2203.FaceGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to FaceGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_gear(self) -> '_2205.Gear':
        '''Gear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2205.Gear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Gear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_hypoid_gear(self) -> '_2209.HypoidGear':
        '''HypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2209.HypoidGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to HypoidGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2211.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2211.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2213.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2213.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2215.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2215.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_spiral_bevel_gear(self) -> '_2218.SpiralBevelGear':
        '''SpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2218.SpiralBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_diff_gear(self) -> '_2220.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2220.StraightBevelDiffGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_gear(self) -> '_2222.StraightBevelGear':
        '''StraightBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2222.StraightBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_planet_gear(self) -> '_2224.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2224.StraightBevelPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_sun_gear(self) -> '_2225.StraightBevelSunGear':
        '''StraightBevelSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2225.StraightBevelSunGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_worm_gear(self) -> '_2226.WormGear':
        '''WormGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.WormGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to WormGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_zerol_bevel_gear(self) -> '_2228.ZerolBevelGear':
        '''ZerolBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2228.ZerolBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ZerolBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_cycloidal_disc(self) -> '_2244.CycloidalDisc':
        '''CycloidalDisc: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2244.CycloidalDisc.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CycloidalDisc. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_ring_pins(self) -> '_2245.RingPins':
        '''RingPins: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2245.RingPins.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to RingPins. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_clutch_half(self) -> '_2254.ClutchHalf':
        '''ClutchHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2254.ClutchHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ClutchHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_concept_coupling_half(self) -> '_2257.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2257.ConceptCouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_coupling_half(self) -> '_2259.CouplingHalf':
        '''CouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2259.CouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_cvt_pulley(self) -> '_2262.CVTPulley':
        '''CVTPulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.CVTPulley.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CVTPulley. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_part_to_part_shear_coupling_half(self) -> '_2264.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.PartToPartShearCouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_pulley(self) -> '_2265.Pulley':
        '''Pulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2265.Pulley.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Pulley. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_rolling_ring(self) -> '_2271.RollingRing':
        '''RollingRing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2271.RollingRing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to RollingRing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_shaft_hub_connection(self) -> '_2273.ShaftHubConnection':
        '''ShaftHubConnection: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2273.ShaftHubConnection.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ShaftHubConnection. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_spring_damper_half(self) -> '_2276.SpringDamperHalf':
        '''SpringDamperHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2276.SpringDamperHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpringDamperHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_synchroniser_half(self) -> '_2279.SynchroniserHalf':
        '''SynchroniserHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2279.SynchroniserHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_synchroniser_part(self) -> '_2280.SynchroniserPart':
        '''SynchroniserPart: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2280.SynchroniserPart.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserPart. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_synchroniser_sleeve(self) -> '_2281.SynchroniserSleeve':
        '''SynchroniserSleeve: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2281.SynchroniserSleeve.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_torque_converter_pump(self) -> '_2283.TorqueConverterPump':
        '''TorqueConverterPump: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2283.TorqueConverterPump.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterPump. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_torque_converter_turbine(self) -> '_2285.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2285.TorqueConverterTurbine.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_b(self) -> '_2122.Component':
        '''Component: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2122.Component.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Component. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_abstract_shaft(self) -> '_2114.AbstractShaft':
        '''AbstractShaft: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.AbstractShaft.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AbstractShaft. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_abstract_shaft_or_housing(self) -> '_2115.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2115.AbstractShaftOrHousing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bearing(self) -> '_2118.Bearing':
        '''Bearing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2118.Bearing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bearing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bolt(self) -> '_2120.Bolt':
        '''Bolt: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.Bolt.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bolt. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_connector(self) -> '_2125.Connector':
        '''Connector: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2125.Connector.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Connector. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_datum(self) -> '_2126.Datum':
        '''Datum: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2126.Datum.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Datum. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_external_cad_model(self) -> '_2129.ExternalCADModel':
        '''ExternalCADModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2129.ExternalCADModel.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ExternalCADModel. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_fe_part(self) -> '_2130.FEPart':
        '''FEPart: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2130.FEPart.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to FEPart. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_guide_dxf_model(self) -> '_2132.GuideDxfModel':
        '''GuideDxfModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2132.GuideDxfModel.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to GuideDxfModel. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_mass_disc(self) -> '_2139.MassDisc':
        '''MassDisc: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2139.MassDisc.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MassDisc. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_measurement_component(self) -> '_2140.MeasurementComponent':
        '''MeasurementComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2140.MeasurementComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MeasurementComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_mountable_component(self) -> '_2141.MountableComponent':
        '''MountableComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2141.MountableComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MountableComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_oil_seal(self) -> '_2143.OilSeal':
        '''OilSeal: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.OilSeal.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to OilSeal. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_planet_carrier(self) -> '_2146.PlanetCarrier':
        '''PlanetCarrier: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2146.PlanetCarrier.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PlanetCarrier. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_point_load(self) -> '_2148.PointLoad':
        '''PointLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2148.PointLoad.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PointLoad. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_power_load(self) -> '_2149.PowerLoad':
        '''PowerLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.PowerLoad.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PowerLoad. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_unbalanced_mass(self) -> '_2154.UnbalancedMass':
        '''UnbalancedMass: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2154.UnbalancedMass.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to UnbalancedMass. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_virtual_component(self) -> '_2155.VirtualComponent':
        '''VirtualComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2155.VirtualComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to VirtualComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_shaft(self) -> '_2158.Shaft':
        '''Shaft: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2158.Shaft.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Shaft. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_agma_gleason_conical_gear(self) -> '_2188.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2188.AGMAGleasonConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_differential_gear(self) -> '_2190.BevelDifferentialGear':
        '''BevelDifferentialGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2190.BevelDifferentialGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_differential_planet_gear(self) -> '_2192.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2192.BevelDifferentialPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_differential_sun_gear(self) -> '_2193.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2193.BevelDifferentialSunGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_gear(self) -> '_2194.BevelGear':
        '''BevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2194.BevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_concept_gear(self) -> '_2196.ConceptGear':
        '''ConceptGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.ConceptGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_conical_gear(self) -> '_2198.ConicalGear':
        '''ConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2198.ConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_cylindrical_gear(self) -> '_2200.CylindricalGear':
        '''CylindricalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.CylindricalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_cylindrical_planet_gear(self) -> '_2202.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2202.CylindricalPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_face_gear(self) -> '_2203.FaceGear':
        '''FaceGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2203.FaceGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to FaceGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_gear(self) -> '_2205.Gear':
        '''Gear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2205.Gear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Gear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_hypoid_gear(self) -> '_2209.HypoidGear':
        '''HypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2209.HypoidGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to HypoidGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2211.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2211.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2213.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2213.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2215.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2215.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_spiral_bevel_gear(self) -> '_2218.SpiralBevelGear':
        '''SpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2218.SpiralBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_diff_gear(self) -> '_2220.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2220.StraightBevelDiffGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_gear(self) -> '_2222.StraightBevelGear':
        '''StraightBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2222.StraightBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_planet_gear(self) -> '_2224.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2224.StraightBevelPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_sun_gear(self) -> '_2225.StraightBevelSunGear':
        '''StraightBevelSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2225.StraightBevelSunGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_worm_gear(self) -> '_2226.WormGear':
        '''WormGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.WormGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to WormGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_zerol_bevel_gear(self) -> '_2228.ZerolBevelGear':
        '''ZerolBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2228.ZerolBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ZerolBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_cycloidal_disc(self) -> '_2244.CycloidalDisc':
        '''CycloidalDisc: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2244.CycloidalDisc.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CycloidalDisc. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_ring_pins(self) -> '_2245.RingPins':
        '''RingPins: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2245.RingPins.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to RingPins. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_clutch_half(self) -> '_2254.ClutchHalf':
        '''ClutchHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2254.ClutchHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ClutchHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_concept_coupling_half(self) -> '_2257.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2257.ConceptCouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_coupling_half(self) -> '_2259.CouplingHalf':
        '''CouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2259.CouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_cvt_pulley(self) -> '_2262.CVTPulley':
        '''CVTPulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.CVTPulley.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CVTPulley. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_part_to_part_shear_coupling_half(self) -> '_2264.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.PartToPartShearCouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_pulley(self) -> '_2265.Pulley':
        '''Pulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2265.Pulley.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Pulley. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_rolling_ring(self) -> '_2271.RollingRing':
        '''RollingRing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2271.RollingRing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to RollingRing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_shaft_hub_connection(self) -> '_2273.ShaftHubConnection':
        '''ShaftHubConnection: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2273.ShaftHubConnection.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ShaftHubConnection. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_spring_damper_half(self) -> '_2276.SpringDamperHalf':
        '''SpringDamperHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2276.SpringDamperHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpringDamperHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_synchroniser_half(self) -> '_2279.SynchroniserHalf':
        '''SynchroniserHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2279.SynchroniserHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_synchroniser_part(self) -> '_2280.SynchroniserPart':
        '''SynchroniserPart: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2280.SynchroniserPart.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserPart. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_synchroniser_sleeve(self) -> '_2281.SynchroniserSleeve':
        '''SynchroniserSleeve: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2281.SynchroniserSleeve.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_torque_converter_pump(self) -> '_2283.TorqueConverterPump':
        '''TorqueConverterPump: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2283.TorqueConverterPump.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterPump. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_torque_converter_turbine(self) -> '_2285.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2285.TorqueConverterTurbine.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    def socket_for(self, component: '_2122.Component') -> '_1976.Socket':
        ''' 'SocketFor' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.SocketFor(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def other_owner(self, component: '_2122.Component') -> '_2122.Component':
        ''' 'OtherOwner' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.Component
        '''

        method_result = self.wrapped.OtherOwner(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def other_socket_for_component(self, component: '_2122.Component') -> '_1976.Socket':
        ''' 'OtherSocket' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.OtherSocket.Overloads[_COMPONENT](component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def other_socket(self, socket: '_1976.Socket') -> '_1976.Socket':
        ''' 'OtherSocket' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.OtherSocket.Overloads[_SOCKET](socket.wrapped if socket else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
