'''_518.py

FlankMicroGeometry
'''


from mastapy.gears import _297
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.utility.scripting import _1477
from mastapy.gears.gear_designs import _877
from mastapy.gears.gear_designs.zerol_bevel import _882
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _886, _887, _890
from mastapy.gears.gear_designs.straight_bevel_diff import _891
from mastapy.gears.gear_designs.straight_bevel import _895
from mastapy.gears.gear_designs.spiral_bevel import _899
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _903
from mastapy.gears.gear_designs.klingelnberg_hypoid import _907
from mastapy.gears.gear_designs.klingelnberg_conical import _911
from mastapy.gears.gear_designs.hypoid import _915
from mastapy.gears.gear_designs.face import _919, _924, _927
from mastapy.gears.gear_designs.cylindrical import _942, _968
from mastapy.gears.gear_designs.conical import _1065
from mastapy.gears.gear_designs.concept import _1087
from mastapy.gears.gear_designs.bevel import _1091
from mastapy.gears.gear_designs.agma_gleason_conical import _1104
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FLANK_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.MicroGeometry', 'FlankMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('FlankMicroGeometry',)


class FlankMicroGeometry(_0.APIBase):
    '''FlankMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _FLANK_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlankMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def micro_geometry_input_type(self) -> '_297.MicroGeometryInputTypes':
        '''MicroGeometryInputTypes: 'MicroGeometryInputType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MicroGeometryInputType)
        return constructor.new(_297.MicroGeometryInputTypes)(value) if value else None

    @micro_geometry_input_type.setter
    def micro_geometry_input_type(self, value: '_297.MicroGeometryInputTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MicroGeometryInputType = value

    @property
    def user_specified_data(self) -> '_1477.UserSpecifiedData':
        '''UserSpecifiedData: 'UserSpecifiedData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1477.UserSpecifiedData)(self.wrapped.UserSpecifiedData) if self.wrapped.UserSpecifiedData else None

    @property
    def gear_design(self) -> '_877.GearDesign':
        '''GearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _877.GearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to GearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_zerol_bevel_gear_design(self) -> '_882.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _882.ZerolBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_worm_design(self) -> '_886.WormDesign':
        '''WormDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _886.WormDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to WormDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_worm_gear_design(self) -> '_887.WormGearDesign':
        '''WormGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _887.WormGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to WormGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_worm_wheel_design(self) -> '_890.WormWheelDesign':
        '''WormWheelDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _890.WormWheelDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to WormWheelDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_straight_bevel_diff_gear_design(self) -> '_891.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _891.StraightBevelDiffGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_straight_bevel_gear_design(self) -> '_895.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _895.StraightBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_spiral_bevel_gear_design(self) -> '_899.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _899.SpiralBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_design(self) -> '_903.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _903.KlingelnbergCycloPalloidSpiralBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergCycloPalloidSpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_design(self) -> '_907.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _907.KlingelnbergCycloPalloidHypoidGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergCycloPalloidHypoidGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_klingelnberg_conical_gear_design(self) -> '_911.KlingelnbergConicalGearDesign':
        '''KlingelnbergConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _911.KlingelnbergConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_hypoid_gear_design(self) -> '_915.HypoidGearDesign':
        '''HypoidGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _915.HypoidGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to HypoidGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_face_gear_design(self) -> '_919.FaceGearDesign':
        '''FaceGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _919.FaceGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to FaceGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_face_gear_pinion_design(self) -> '_924.FaceGearPinionDesign':
        '''FaceGearPinionDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _924.FaceGearPinionDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to FaceGearPinionDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_face_gear_wheel_design(self) -> '_927.FaceGearWheelDesign':
        '''FaceGearWheelDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _927.FaceGearWheelDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to FaceGearWheelDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_cylindrical_gear_design(self) -> '_942.CylindricalGearDesign':
        '''CylindricalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _942.CylindricalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to CylindricalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_cylindrical_planet_gear_design(self) -> '_968.CylindricalPlanetGearDesign':
        '''CylindricalPlanetGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _968.CylindricalPlanetGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to CylindricalPlanetGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_conical_gear_design(self) -> '_1065.ConicalGearDesign':
        '''ConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1065.ConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to ConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_concept_gear_design(self) -> '_1087.ConceptGearDesign':
        '''ConceptGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1087.ConceptGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to ConceptGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_bevel_gear_design(self) -> '_1091.BevelGearDesign':
        '''BevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1091.BevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to BevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_agma_gleason_conical_gear_design(self) -> '_1104.AGMAGleasonConicalGearDesign':
        '''AGMAGleasonConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1104.AGMAGleasonConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to AGMAGleasonConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None
