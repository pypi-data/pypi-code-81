"""
originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation
"""
# pylint: disable=C0103,C0301
from .config import po, oext
from .utils import LTTMPOUTSTR, active_obj
from .base import BaseObject
from .project import _PO_PAGE_TYPES, _PAGE_CLS

def search(name='', kind=0):
    """
    Get current Project Explorer path or path of specified window
    Parameters:
        name (str): Name of the page/folder to be searched for
        kind (int): Page Short Name if 0, Subfolder Name if 1
    Returns:
        Current path if page/folder is empty, or path where page/folder is located
    """
    with LTTMPOUTSTR() as pp:
        po.LT_execute(f'pe_path page:="{name}" path:={pp.name}$ type:={kind};')
        return pp.get()

def cd(path=None):
    """
    Change Project Explorer directory
    Parameters:
        path (str): Path of the directory to move into
    Returns:
        Current path
    """
    if path is not None:
        po.LT_execute(f'pe_cd path:={path}')
    return search()

def mkdir(path, chk=False):
    """
    Create new folder in Project Explorer
    Parameters:
        path (str): Name of the path to be created; if folder already exists and chk is False, then it is enumerated, but if chk is True, then will not create new
        chk (bool): Specify if check folder exists or not. If set to True, then will not force create enumerated new one if already existed
    Returns:
        Path created
    """
    with LTTMPOUTSTR() as pp:
        po.LT_execute(f'pe_mkdir folder:="{path}" chk:={int(chk)} path:={pp.name}$;')
        return pp.get()

def move(name, path):
    """
    Move page or folder to specified folder in Project Explorer
    Parameters:
        name (str): Name of the existing page or folder
        path (str): path of the location where the page should be moved to
    Returns:
        None
    """
    po.LT_execute(f'pe_move move:="{name}" path:={path};')

class Folder(BaseObject):
    ''' Origin Folder in Project Explorer'''
    def __repr__(self):
        return self.path

    @property
    def path(self):
        '''Full path of folder'''
        path = self.obj.Path
        return path if oext else path()

    def pages(self, type_=''):
        """
        All pages in folder.
        Parameters:
            type_ (str): Page type, can be 'w', 'm', 'g'
        Returns:
            Page Objects
        """
        for page in self.obj.PageBases():
            try:
                ptype = _PO_PAGE_TYPES[page.GetType()]
            except KeyError:
                continue
            if not type_ or type_ == ptype:
                yield _PAGE_CLS[ptype](page)

def active_folder():
    '''Active Folder in Project Explorer'''
    return Folder(active_obj('Folder'))

def root_folder():
    '''Root Folder in Project Explorer'''
    return Folder(po.GetRootFolder())
