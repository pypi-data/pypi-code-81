'''_121.py

SpaceClaimSettings
'''


from mastapy._internal import constructor
from mastapy.utility import _1349
from mastapy._internal.python_net import python_net_import

_SPACE_CLAIM_SETTINGS = python_net_import('SMT.MastaAPI.NodalAnalysis.SpaceClaimLink', 'SpaceClaimSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('SpaceClaimSettings',)


class SpaceClaimSettings(_1349.PerMachineSettings):
    '''SpaceClaimSettings

    This is a mastapy class.
    '''

    TYPE = _SPACE_CLAIM_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpaceClaimSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def folder_path(self) -> 'str':
        '''str: 'FolderPath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FolderPath

    @property
    def licence(self) -> 'str':
        '''str: 'Licence' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Licence

    def edit_folder_path(self):
        ''' 'EditFolderPath' is the original name of this method.'''

        self.wrapped.EditFolderPath()
