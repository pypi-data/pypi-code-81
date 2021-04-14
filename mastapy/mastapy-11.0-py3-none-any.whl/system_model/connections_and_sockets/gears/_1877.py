'''_1877.py

BevelDifferentialGearMesh
'''


from mastapy.gears.gear_designs.bevel import _918
from mastapy._internal import constructor
from mastapy.gears.gear_designs.zerol_bevel import _719
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _728
from mastapy.gears.gear_designs.straight_bevel import _732
from mastapy.gears.gear_designs.spiral_bevel import _736
from mastapy.system_model.connections_and_sockets.gears import _1879
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMesh',)


class BevelDifferentialGearMesh(_1879.BevelGearMesh):
    '''BevelDifferentialGearMesh

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMesh.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def bevel_gear_mesh_design(self) -> '_918.BevelGearMeshDesign':
        '''BevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_918.BevelGearMeshDesign)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None

    @property
    def bevel_gear_mesh_design_of_type_zerol_bevel_gear_mesh_design(self) -> '_719.ZerolBevelGearMeshDesign':
        '''ZerolBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _719.ZerolBevelGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to ZerolBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new(_719.ZerolBevelGearMeshDesign)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None

    @property
    def bevel_gear_mesh_design_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_728.StraightBevelDiffGearMeshDesign':
        '''StraightBevelDiffGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _728.StraightBevelDiffGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new(_728.StraightBevelDiffGearMeshDesign)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None

    @property
    def bevel_gear_mesh_design_of_type_straight_bevel_gear_mesh_design(self) -> '_732.StraightBevelGearMeshDesign':
        '''StraightBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _732.StraightBevelGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to StraightBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new(_732.StraightBevelGearMeshDesign)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None

    @property
    def bevel_gear_mesh_design_of_type_spiral_bevel_gear_mesh_design(self) -> '_736.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _736.SpiralBevelGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to SpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new(_736.SpiralBevelGearMeshDesign)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None
