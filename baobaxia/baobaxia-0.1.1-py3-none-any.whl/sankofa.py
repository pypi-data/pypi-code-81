from datetime import datetime
from typing import Optional

from .root import Mocambola, Baobaxia
from .saberes import Saber, SaberesConfig, SaberesDataSet

from datalad.api import Dataset, create
from datalad.config import ConfigManager

from pathlib import Path

from datetime import datetime

import glob, os

    
class SankofaInfo():
    """Context manager for setting commit info on datalad operations that use it."""

    def __init__(self, balaio, name=None, email=None, where='local'):
        self.config_manager = ConfigManager(balaio)
        self.email = email if email else 'exu@mocambos.net'
        self.name = name if name else 'exu'
        self.where = where

    def __enter__(self):
        self.config_manager.set('user.email', self.email, self.where)
        self.config_manager.set('user.name', self.name, self.where)

    def __exit__(self, exception_type, exception_value, traceback):
        self.config_manager.set('user.email', 'exu@mocambos.net', self.where)
        self.config_manager.set('user.name', 'exu', self.where)


class Sankofa():

    @staticmethod
    def _prepare_paths(saberes: [Saber], config: SaberesConfig):
        print(repr(saberes))
        sankofa_data = {}
        balaios = {b.balaio for b in saberes if not b.balaio == None}
        for balaio in balaios:
            saberes_paths = []
            for saber in saberes:
                if saber.balaio == balaio:
                    if saber.mucua == None:
                        saberpath = saber.path 
                    else:
                        saberpath = saber.mucua / saber.path
                        saberes_paths.append(saberpath)
                    if str(saberpath).endswith(config.saber_file_ext):
                        saberpathfile = saberpath.removesuffix(
                            config.saber_file_ext)
                        if saberpathfile.is_file():
                            saberes_paths.append(saberpathfile)
                    else:
                        saberfilewithext = Path(
                            str(saberpath) + config.saber_file_ext)
                        saberes_paths.append(saberfilewithext)
            sankofa_data[balaio] = saberes_paths
            
        return sankofa_data
    
    @classmethod
    def create_balaio(cls, *, balaio: str, description: str,
                      config: SaberesConfig):
        balaio_path = Path(balaio)
        balaio_fullpath = config.data_path / balaio_path 
        dataset = create(path=balaio_fullpath,
                         force=True,
                         annex=True,
                         cfg_proc='text2git',
                         description=description)
        dataset.save() 

    @classmethod
    def add(cls, *,
            saberes: [Saber], mocambola=Mocambola,
            config: SaberesConfig):

        sankofa_data = Sankofa._prepare_paths(saberes, config)
                 
        for balaio, saberes_paths in sankofa_data.items():
            repopath = config.data_path
            balaiopath = repopath / balaio
            dataset = Dataset(balaiopath)
            
            with SankofaInfo(balaio=dataset,
                             name=mocambola.username,
                             email=mocambola.email):
                dataset.save(path=saberes_paths)
                
    @classmethod
    def remove(cls, *,
            saberes: [Saber], mocambola=Mocambola,
            config: SaberesConfig):

        sankofa_data = Sankofa._prepare_paths(saberes, config)

        for balaio, saberes_paths in sankofa_data.items():
            repopath = config.data_path
            balaiopath = repopath / balaio
            dataset = Dataset(balaiopath)

            with SankofaInfo(balaio=dataset,
                             name=mocambola.username,
                             email=mocambola.email):
                dataset.remove(path=saberes_paths, check=False)

    @classmethod
    def sync(cls, *, balaio_slug: Optional[str] = None,
             mucua_slug: Optional[str] = None,
             config: SaberesConfig, **kwargs):

        repopath = config.data_path
        balaiopath = repopath / balaio_slug
        dataset = Dataset(balaiopath)
        
        with SankofaInfo(balaio=dataset):
            dataset.update(**kwargs)       

    @classmethod
    def lookback(cls, *,
                 when: Optional[datetime] = None,
                 commit: Optional[str] = None
    ):
        pass

    @classmethod
    def goback(cls, *,
               when: Optional[datetime] = None,
               commit: Optional[str] = None
    ):
        pass
                
    @classmethod
    def rollback(cls):
        pass

    @classmethod
    def create(cls):
        pass

    @classmethod
    def update(cls):
        pass

    @classmethod
    def copy(cls):
        pass

    @classmethod
    def get(cls):
        pass


