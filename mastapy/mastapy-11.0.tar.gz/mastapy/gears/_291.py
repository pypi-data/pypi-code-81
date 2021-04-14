'''_291.py

GearSetOptimisationResult
'''


from mastapy.gears.gear_designs import _880
from mastapy._internal import constructor
from mastapy.gears.gear_designs.zerol_bevel import _884
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _889
from mastapy.gears.gear_designs.straight_bevel_diff import _893
from mastapy.gears.gear_designs.straight_bevel import _897
from mastapy.gears.gear_designs.spiral_bevel import _901
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _905
from mastapy.gears.gear_designs.klingelnberg_hypoid import _909
from mastapy.gears.gear_designs.klingelnberg_conical import _913
from mastapy.gears.gear_designs.hypoid import _917
from mastapy.gears.gear_designs.face import _925
from mastapy.gears.gear_designs.cylindrical import _956, _967
from mastapy.gears.gear_designs.conical import _1067
from mastapy.gears.gear_designs.concept import _1089
from mastapy.gears.gear_designs.bevel import _1093
from mastapy.gears.gear_designs.agma_gleason_conical import _1106
from mastapy.gears.rating import _316, _323, _324
from mastapy.gears.rating.zerol_bevel import _332
from mastapy.gears.rating.worm import _336, _337
from mastapy.gears.rating.straight_bevel_diff import _358
from mastapy.gears.rating.straight_bevel import _362
from mastapy.gears.rating.spiral_bevel import _365
from mastapy.gears.rating.klingelnberg_spiral_bevel import _368
from mastapy.gears.rating.klingelnberg_hypoid import _371
from mastapy.gears.rating.klingelnberg_conical import _374
from mastapy.gears.rating.hypoid import _401
from mastapy.gears.rating.face import _410, _411
from mastapy.gears.rating.cylindrical import _422, _423
from mastapy.gears.rating.conical import _489, _490
from mastapy.gears.rating.concept import _500, _501
from mastapy.gears.rating.bevel import _504
from mastapy.gears.rating.agma_gleason_conical import _515
from mastapy.math_utility.optimisation import _1305
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_SET_OPTIMISATION_RESULT = python_net_import('SMT.MastaAPI.Gears', 'GearSetOptimisationResult')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetOptimisationResult',)


class GearSetOptimisationResult(_0.APIBase):
    '''GearSetOptimisationResult

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_OPTIMISATION_RESULT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetOptimisationResult.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set(self) -> '_880.GearSetDesign':
        '''GearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _880.GearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to GearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_zerol_bevel_gear_set_design(self) -> '_884.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _884.ZerolBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_worm_gear_set_design(self) -> '_889.WormGearSetDesign':
        '''WormGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _889.WormGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to WormGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_straight_bevel_diff_gear_set_design(self) -> '_893.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _893.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_straight_bevel_gear_set_design(self) -> '_897.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _897.StraightBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_spiral_bevel_gear_set_design(self) -> '_901.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _901.SpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_905.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _905.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_909.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _909.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_conical_gear_set_design(self) -> '_913.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _913.KlingelnbergConicalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_hypoid_gear_set_design(self) -> '_917.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.HypoidGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to HypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_face_gear_set_design(self) -> '_925.FaceGearSetDesign':
        '''FaceGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _925.FaceGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to FaceGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_cylindrical_gear_set_design(self) -> '_956.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _956.CylindricalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_cylindrical_planetary_gear_set_design(self) -> '_967.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _967.CylindricalPlanetaryGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_conical_gear_set_design(self) -> '_1067.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1067.ConicalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to ConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_concept_gear_set_design(self) -> '_1089.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1089.ConceptGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to ConceptGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_bevel_gear_set_design(self) -> '_1093.BevelGearSetDesign':
        '''BevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1093.BevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to BevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_agma_gleason_conical_gear_set_design(self) -> '_1106.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1106.AGMAGleasonConicalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def rating(self) -> '_316.AbstractGearSetRating':
        '''AbstractGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _316.AbstractGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to AbstractGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_gear_set_duty_cycle_rating(self) -> '_323.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _323.GearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to GearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_gear_set_rating(self) -> '_324.GearSetRating':
        '''GearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _324.GearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to GearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_zerol_bevel_gear_set_rating(self) -> '_332.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _332.ZerolBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ZerolBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_worm_gear_set_duty_cycle_rating(self) -> '_336.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _336.WormGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_worm_gear_set_rating(self) -> '_337.WormGearSetRating':
        '''WormGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _337.WormGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to WormGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_diff_gear_set_rating(self) -> '_358.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _358.StraightBevelDiffGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelDiffGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_gear_set_rating(self) -> '_362.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _362.StraightBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_spiral_bevel_gear_set_rating(self) -> '_365.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _365.SpiralBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to SpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(self) -> '_368.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _368.KlingelnbergCycloPalloidSpiralBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidSpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_rating(self) -> '_371.KlingelnbergCycloPalloidHypoidGearSetRating':
        '''KlingelnbergCycloPalloidHypoidGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _371.KlingelnbergCycloPalloidHypoidGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidHypoidGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_conical_gear_set_rating(self) -> '_374.KlingelnbergCycloPalloidConicalGearSetRating':
        '''KlingelnbergCycloPalloidConicalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _374.KlingelnbergCycloPalloidConicalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidConicalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_hypoid_gear_set_rating(self) -> '_401.HypoidGearSetRating':
        '''HypoidGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _401.HypoidGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to HypoidGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_face_gear_set_duty_cycle_rating(self) -> '_410.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _410.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_face_gear_set_rating(self) -> '_411.FaceGearSetRating':
        '''FaceGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _411.FaceGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to FaceGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_422.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _422.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_cylindrical_gear_set_rating(self) -> '_423.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _423.CylindricalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to CylindricalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_conical_gear_set_duty_cycle_rating(self) -> '_489.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _489.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_conical_gear_set_rating(self) -> '_490.ConicalGearSetRating':
        '''ConicalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _490.ConicalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConicalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_concept_gear_set_duty_cycle_rating(self) -> '_500.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _500.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_concept_gear_set_rating(self) -> '_501.ConceptGearSetRating':
        '''ConceptGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _501.ConceptGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConceptGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_bevel_gear_set_rating(self) -> '_504.BevelGearSetRating':
        '''BevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _504.BevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to BevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_agma_gleason_conical_gear_set_rating(self) -> '_515.AGMAGleasonConicalGearSetRating':
        '''AGMAGleasonConicalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _515.AGMAGleasonConicalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to AGMAGleasonConicalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def optimisation_history(self) -> '_1305.OptimisationHistory':
        '''OptimisationHistory: 'OptimisationHistory' is the original name of this property.'''

        return constructor.new(_1305.OptimisationHistory)(self.wrapped.OptimisationHistory) if self.wrapped.OptimisationHistory else None

    @optimisation_history.setter
    def optimisation_history(self, value: '_1305.OptimisationHistory'):
        value = value.wrapped if value else None
        self.wrapped.OptimisationHistory = value

    @property
    def is_optimized(self) -> 'bool':
        '''bool: 'IsOptimized' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsOptimized
