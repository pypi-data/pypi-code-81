'''_400.py

HypoidGearRating
'''


from mastapy.gears.gear_designs.hypoid import _915
from mastapy._internal import constructor
from mastapy.gears.rating.agma_gleason_conical import _514
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Hypoid', 'HypoidGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearRating',)


class HypoidGearRating(_514.AGMAGleasonConicalGearRating):
    '''HypoidGearRating

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hypoid_gear(self) -> '_915.HypoidGearDesign':
        '''HypoidGearDesign: 'HypoidGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_915.HypoidGearDesign)(self.wrapped.HypoidGear) if self.wrapped.HypoidGear else None
