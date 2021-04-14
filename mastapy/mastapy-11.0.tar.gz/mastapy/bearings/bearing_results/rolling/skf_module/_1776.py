'''_1776.py

DynamicAxialLoadCarryingCapacity
'''


from mastapy.bearings.bearing_results.rolling.skf_module import _1789, _1791
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_DYNAMIC_AXIAL_LOAD_CARRYING_CAPACITY = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'DynamicAxialLoadCarryingCapacity')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicAxialLoadCarryingCapacity',)


class DynamicAxialLoadCarryingCapacity(_1791.SKFCalculationResult):
    '''DynamicAxialLoadCarryingCapacity

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_AXIAL_LOAD_CARRYING_CAPACITY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicAxialLoadCarryingCapacity.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def permissible_axial_load(self) -> '_1789.PermissibleAxialLoad':
        '''PermissibleAxialLoad: 'PermissibleAxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1789.PermissibleAxialLoad)(self.wrapped.PermissibleAxialLoad) if self.wrapped.PermissibleAxialLoad else None
