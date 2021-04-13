import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Union, List, Optional, Any

import shortuuid
from slugify import slugify

from pydantic import BaseModel, EmailStr, ValidationError

from .util import GeoLocation

class SaberesConfig(BaseModel):
    """
    Modelo de configuração do Saber. 
    Essa classe é usada para armazenar algumas configurações de base do Baobáxia.

    TODO: Colocar variaveis em arquivo de configuração
    """

    data_path: Path
    saber_file_ext: str = '.baobaxia'
    
    balaio_local: str
    mucua_local: str

    smid_len: int = 13
    slug_smid_len: int = 7
    slug_name_len: int = 7
    slug_sep: str = '_'


class Mucua(BaseModel):
    """
    Modelo da classe Mucua. 
    
    
    """
    pass

class Balaio(BaseModel):

    """
    Modelo da classe Balaio. 
    
    """
    pass

class Mocambola(BaseModel):
    """
    Modelo da classe Mocambola.
    
    :param email: Email do mocambola
    :type email: emailStr, optional
    :param mocambo: Mocambo de base (SMID) 
    :type mocambo: str, optional
    :param username: Username do mocambola
    :type username: str
    :param name: Nome do mocambola
    :type name: str, optional
    :param is_native: Nativo por padrã não (False)
    :type is_native: str, false
    :param family: Familia do mocambola
    :type family: str, optional
    
    :param password_hash: Hash da senha
    :type password_hash: str
    :param validation_code: Codigo de validação
    :type validation_code: str
    
    """
    
    email: Optional[EmailStr] = None
    mocambo: Optional[str] = None
    username: str
    name: Optional[str] = None    

    is_native: bool = False
    family: Optional[str] = None

    password_hash: Optional[str] = None
    validation_code: Optional[str] = None

class Mocambo(BaseModel):
    location: Optional[GeoLocation] = None
    mocambolas: List[Mocambola] = []

class Territorio(BaseModel):
    pass

class Saber(BaseModel):
    """
    Modelo da classe Saber
    
    :param path: Caminho do Saber (Path)
    :type path: str
    :param smid: Id do Saber (SmallID)
    :type smid: str
    :param name: Nome do saber
    :type name: str
    :param slug: Identificativo do Saber, gerado pelo nome e id (Name + Smid)
    :type slug: str, optional
    :param balaio: Balaio de base do Saber (SLUG)
    :type balaio: str, optional
    :param mucua: Mucua de base do Saber (SLUG)
    :type mucua: str, optional
    :param created: Data de gravação
    :type created: datetime
    :param creator: Mocambola gravador
    :type creator: str
    :param last_update: Data do ultimo manejo
    :type last_update: datetime
    :param data: Modelo de dados especifico do Saber (BaseModel). 
    :type data: BaseModel, optional

    """

    path: Path

    smid: str
    name: str
    slug: Optional[str] = None

    balaio: Optional[str] = None
    mucua: Optional[str] = None

    created: datetime
    creator: Mocambola

    last_update: datetime

    data: Any = None

class SaberesDataStore():
    """
    Classe para criar e manejar os Saberes.

    :param config: Objeto de configuração SaberConfig
    :type config: SaberConfig
    
    """
    EMPTY_BALAIO = "!balaio!"
    EMPTY_MUCUA = "!mucua!"

    def __init__(self, config: SaberesConfig):
        """Metodo construtor
        """
        super().__init__()
        self.config = config
        self.clear_cache()
    
    def clear_cache(self):
        """Limpa a cache
        """
        self._saberes_by_path = {}
        self._saberes_by_smid = {}

    def cache_saber(self, saber: Saber):
        """Coloca o Saber na cache
        
        :param saber: Objeto Saber a ser memorizado na cache
        :type saber: Saber

        """
        self._saberes_by_smid[saber.smid] = saber
        
        balaio_slug = saber.balaio
        if balaio_slug is None:
            balaio_slug = self.__class__.EMPTY_BALAIO
        if balaio_slug not in self._saberes_by_path:
            self._saberes_by_path[balaio_slug] = {}

        mucua_slug = saber.mucua
        if mucua_slug is None:
            mucua_slug = self.__class__.EMPTY_MUCUA
        if mucua_slug not in self._saberes_by_path[balaio_slug]:
            self._saberes_by_path[balaio_slug][mucua_slug] = {}

        self._saberes_by_path[balaio_slug][mucua_slug][saber.path] = saber

    def uncache_saber(self, saber: Saber):
        """Remove o objeto do cache

        :param saber: Objeto Saber a ser removido da cache
        :type saber: Saber

        """
        del self._saberes_by_smid[saber.smid]

        balaio_slug = saber.balaio
        if balaio_slug is None:
            balaio_slug = self.__class__.EMPTY_BALAIO

        mucua_slug = saber.mucua
        if mucua_slug is None:
            mucua_slug = self.__class__.EMPTY_MUCUA

        del self._saberes_by_path[balaio_slug][mucua_slug][saber.path]

    def get_cached_saber_by_smid(self, smid: str):
        """Retorna o objeto Saber a partir de um SMID

        TODO: Continue aqui.. 
        
        """
        return self._saberes_by_smid[smid]

    def get_cached_saber_by_path(self, path: Path,
                          balaio_slug: Optional[str]=None,
                          mucua_slug: Optional[str]=None
    ):
        if balaio_slug is None:
            balaio_slug = self.__class__.EMPTY_BALAIO
        if mucua_slug is None:
            mucua_slug = self.__class__.EMPTY_MUCUA
        return self._saberes_by_path[balaio_slug][mucua_slug][path]

    def is_smid_cached(self, smid: str):
        return smid in self._saberes_by_smid

    def is_path_cached(self, path: Path,
                       balaio_slug: Optional[str]=None,
                       mucua_slug: Optional[str]=None
    ):
        if balaio_slug is None:
            balaio_slug = self.__class__.EMPTY_BALAIO
        if balaio_slug not in self._saberes_by_path:
            return False

        if mucua_slug is None:
            mucua_slug = self.__class__.EMPTY_MUCUA
        if mucua_slug not in self._saberes_by_path[balaio_slug]:
            return False

        return path in self._saberes_by_path[balaio_slug][mucua_slug]

    def create_dataset(self, *,
                       mocambola: Optional[str] = None,
                       model: Optional[type] = None,
                       balaio: Optional[str] = None,
                       mucua: Optional[str] = None,
    ):
        return SaberesDataSet(
            datastore=self,
            model=model,
            mocambola=mocambola,
            balaio=balaio,
            mucua=mucua)


class SaberesDataSet():

    def __init__(self, *,
                 datastore: SaberesDataStore,
                 mocambola: Optional[str] = None,
                 model: Optional[type] = None,
                 balaio: Optional[str] = None,
                 mucua: Optional[str] = None
    ):
        super().__init__()
        self.datastore = datastore
        self.mocambola = mocambola

        self.model = model
        self.balaio = balaio
        self.mucua = mucua

    def _prepare_path(self):
        path = self.datastore.config.data_path
        if self.balaio is not None:
            path = path / self.balaio
            if self.mucua is not None:
                path = path / self.mucua
        return path

    def _prepare_file_path(self, path):
        file_path = self._prepare_path() / path
        file_ext = self.datastore.config.saber_file_ext
        if file_path.exists() and file_path.is_dir():
            file_path = file_path / file_ext
        else:
            file_path = file_path.parent / (file_path.name + file_ext)
        return file_path

    def create_smid(self):
        return shortuuid.ShortUUID().random(
            length=self.datastore.config.smid_len)

    def create_slug(self, smid: str, name: str):
        result = slugify(name)
        if len(result) > self.datastore.config.slug_name_len:
            result = result[:self.datastore.config.slug_name_len]
        result += self.datastore.config.slug_sep
        if len(smid) > self.datastore.config.slug_smid_len:
            result += smid[:self.datastore.config.slug_smid_len]
        else:
            result += smid
        return result

    def collect_saberes(self, pattern: str):
        result = []
        baobaxia_files = self._prepare_path().glob(
            pattern+self.datastore.config.saber_file_ext)
        for bf in baobaxia_files:
            saber = self.collect_saber(path=bf, is_full_path=True)
            result.append(saber)
        return result

    def collect_saber(self, path: Path, is_full_path=False):
        if not is_full_path:
            path = self._prepare_file_path(path)
        
        result = Saber.parse_file(path)
        if self.model is not None and self.model != result.data.__class__:
            try:
                result.data = self.model.parse_obj(result.data)
            except ValidationError as ex:
                raise ex

        self.datastore.cache_saber(result)

        return result.copy()

    def settle_saber(self, *,
                     path: Path,
                     name: Optional[str] = None,
                     data: BaseModel,
                     slug_dir: bool = False,
    ):
        if not slug_dir and not self.datastore.is_path_cached(
                path, self.balaio, self.mucua) and \
                self._prepare_file_path(path).exists():
            self.collect_saber(path)

        if slug_dir:
            smid = self.create_smid()
            slug = self.create_slug(smid, name)
            path = path / slug
            full_path = self._prepare_path() / path
            full_path.mkdir()
            saber = Saber(
                path = path,
                smid = smid,
                name = name,
                slug = slug,
                balaio = self.balaio,
                mucua = self.mucua,
                created = datetime.now(),
                creator = self.mocambola,
                last_update = datetime.now(),
                data = data)
        elif self.datastore.is_path_cached(
                path, self.balaio, self.mucua):
            saber = self.datastore.get_cached_saber_by_path(
                path, self.balaio, self.mucua)
            if name is not None:
                saber.name = name
            if data is not None:
                saber.data = data
            saber.last_update = datetime.now()
        elif slug_dir:
            smid = self.create_smid()
            slug = self.create_slug(smid, name)
            path = path / slug
            full_path = self._prepare_path() / path
            full_path.mkdir()
            saber = Saber(
                path = path,
                smid = smid,
                name = name,
                slug = slug,
                balaio = self.balaio,
                mucua = self.mucua,
                created = datetime.now(),
                creator = self.mocambola,
                last_update = datetime.now(),
                data = data)
        else:
            smid = self.create_smid()
            saber = Saber(
                path = path,
                smid = smid,
                name = name,
                slug = self.create_slug(smid, name),
                balaio = self.balaio,
                mucua = self.mucua,
                created = datetime.now(),
                creator = self.mocambola,
                last_update = datetime.now(),
                data = data)

        filepath = self._prepare_file_path(path)
        if not filepath.exists():
            filepath.touch()
        filepath.open('w').write(saber.json())

        self.datastore.cache_saber(saber)
        return saber.copy()

    def drop_saber(self, path: Path):
        saber = self.datastore.get_cached_saber_by_path(
            path, self.balaio, self.mucua)
        self.datastore.uncache_saber(saber)
        self._prepare_file_path(path).unlink()

