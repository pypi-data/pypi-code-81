'''_2045.py

ConcentricPartGroupParallelToThis
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model.part_groups import _2043, _2044, _2047
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CONCENTRIC_PART_GROUP_PARALLEL_TO_THIS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.PartGroups', 'ConcentricPartGroupParallelToThis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConcentricPartGroupParallelToThis',)


class ConcentricPartGroupParallelToThis(_0.APIBase):
    '''ConcentricPartGroupParallelToThis

    This is a mastapy class.
    '''

    TYPE = _CONCENTRIC_PART_GROUP_PARALLEL_TO_THIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConcentricPartGroupParallelToThis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def centre_distance(self) -> 'float':
        '''float: 'CentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CentreDistance

    @property
    def parallel_group(self) -> '_2043.ConcentricOrParallelPartGroup':
        '''ConcentricOrParallelPartGroup: 'ParallelGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2043.ConcentricOrParallelPartGroup)(self.wrapped.ParallelGroup) if self.wrapped.ParallelGroup else None

    @property
    def parallel_group_of_type_concentric_part_group(self) -> '_2044.ConcentricPartGroup':
        '''ConcentricPartGroup: 'ParallelGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.ConcentricPartGroup.TYPE not in self.wrapped.ParallelGroup.__class__.__mro__:
            raise CastException('Failed to cast parallel_group to ConcentricPartGroup. Expected: {}.'.format(self.wrapped.ParallelGroup.__class__.__qualname__))

        return constructor.new(_2044.ConcentricPartGroup)(self.wrapped.ParallelGroup) if self.wrapped.ParallelGroup else None

    @property
    def parallel_group_of_type_parallel_part_group(self) -> '_2047.ParallelPartGroup':
        '''ParallelPartGroup: 'ParallelGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2047.ParallelPartGroup.TYPE not in self.wrapped.ParallelGroup.__class__.__mro__:
            raise CastException('Failed to cast parallel_group to ParallelPartGroup. Expected: {}.'.format(self.wrapped.ParallelGroup.__class__.__qualname__))

        return constructor.new(_2047.ParallelPartGroup)(self.wrapped.ParallelGroup) if self.wrapped.ParallelGroup else None
