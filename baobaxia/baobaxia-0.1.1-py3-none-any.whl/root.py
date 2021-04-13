from pathlib import Path
from datetime import date, datetime, time
import os, hashlib

from .saberes import (
    Saber,
    Balaio,
    Mucua,
    Mocambola,
    Mocambo,
    SaberesConfig,
    SaberesDataStore
)

from typing import Optional, List

from pydantic import BaseModel

from configparser import ConfigParser 

def str_to_hash(base: str):
    return hashlib.md5(base.encode()).hexdigest()

class BaobaxiaError(RuntimeError):
    pass

class BaobaxiaSession():

    timeout = 900 # 15 minutos

    def __init__(self, mocambola: Mocambola):
        super().__init__()
        self.mocambola = mocambola
        self.started = datetime.now()
        self.alive_at = datetime.now()
        self.token = str_to_hash(
            str(round(time.time() * 1000)))

    def keep_alive(self):
        delta = datetime.now() - self.alive_at
        if self.__class__.timeout < delta:
            raise Baobaxia('Sessão expirou')
        self.alive_at = datetime.now()
        return self

class Baobaxia():

    _MOCAMBOLA = Mocambola(username='exu', email='exu@mocambos.net')

    def __init__(self, config: Optional[SaberesConfig] = None):
        if config == None:
            config_file = ConfigParser()
            config_file.read(os.path.join(os.path.expanduser("~"), '.baobaxia.conf'))
            config = SaberesConfig(
                data_path = Path(config_file['default']['data_path']),
                saber_file_ext = config_file['default']['saber_file_ext'],
                balaio_local = config_file['default']['balaio_local'],
                mucua_local = config_file['default']['mucua_local'],
                smid_len = config_file['default'].getint('smid_len'),
                slug_smid_len = config_file['default'].getint('slug_smid_len'),
                slug_name_len = config_file['default'].getint('slug_name_len'),
                slug_sep = config_file['default']['slug_sep']
                )
        self.config = config
        self.datastore = SaberesDataStore(self.config)
        self.reload_balaios()
        self._sessions = {}

    def reload_balaios(self):
        balaios_list = self.datastore.create_dataset(
            model=Balaio).collect_saberes('*/')
        self._balaios = {}
        self._mocambolas = {}
        self._mucuas_por_balaio = {}
        self._mocambos_por_mucua = {}
        for balaio in balaios_list:
            self._balaios[balaio.slug] = balaio
            self._mucuas_por_balaio[balaio.slug] = {}
            self._mocambos_por_mucua[balaio.slug] = {}
            mucuas = self.datastore.create_dataset(
                model=Mucua, balaio=balaio.slug).collect_saberes('*/')
            for mucua in mucuas:
                self._mucuas_por_balaio[balaio.slug][mucua.slug] = mucua
                self._mocambos_por_mucua[balaio.slug][mucua.slug] = {}
                mocambos = self.datastore.create_dataset(
                    model=Mocambo, balaio=balaio.slug,
                    mucua=mucua.slug).collect_saberes('mocambos/*')
                for mocambo in mocambos:
                    self._mocambos_por_mucua[balaio.slug][mucua.slug][
                        mocambo.slug] = mocambo

        self._balaio_local = self._balaios[
            self.config.balaio_local]
        self._mucua_local = self._mucuas_por_balaio[
            self.config.balaio_local][self.config.mucua_local]
        for mocambo in self._mocambos_por_mucua[self.config.balaio_local][
                self.config.mucua_local]:
            for mocambola in mocambo.mocambolas:
                self._mocambolas[mocambola.username] = mocambola

    def list_balaios(self,
                     mocambola: Optional[Mocambola] = None
    ):
        mocambola = self._MOCAMBOLA if mocambola is None else mocambola
        result = []
        for key, value in self._balaios.items():
            result.append(value.copy())
        return result

    def get_balaio(self,
                   slug: str,
                   mocambola: Optional[Mocambola] = None
    ):
        mocambola = self._MOCAMBOLA if mocambola is None else mocambola
        return self._balaios[slug].copy()

    def put_balaio(self, *,
                   slug: Optional[str] = None,
                   name: str,
                   mocambola: Optional[Mocambola] = None
    ):
        mocambola = self._MOCAMBOLA if mocambola is None else mocambola
        dataset = self.datastore.create_dataset(
            mocambola=mocambola,
            model=Balaio)
        if slug is None:
            balaio = dataset.settle_saber(
                path = Path('.'),
                name = name,
                data = Balaio(),
                slug_dir = True
            )
            self._balaios[balaio.slug] = balaio
            self._mucuas_por_balaio[balaio.slug] = {}
            self._mocambos_por_mucua[balaio.slug] = {}
        else:
            balaio = self._balaios[slug]
            balaio.name = name
            dataset.settle_saber(
                path=balaio.path, name=name, data=balaio.data)
        return balaio.copy()

    def del_balaio(self,
                   slug: str,
                   mocambola: Optional[Mocambola] = None
    ):
        mocambola = self._MOCAMBOLA if mocambola is None else mocambola
        if slug == self._balaio_local.slug:
            # Baobaxia não pode deixar para trás o balaio de seus próprios saberes.
            raise RuntimeError('Cannot delete balaio local.')
        self.datastore.create_dataset(
            mocambola = mocambola,
            model = Balaio).drop_saber(Path(slug))
        del self._balaios[slug]
        del self._mucuas_por_balaio[slug]
        del self._mocambos_por_mucua[slug]

    def list_mucuas(self,
                    balaio_slug: str,
                    mocambola: Optional[Mocambola] = None
    ):
        mocambola = self._MOCAMBOLA if mocambola is None else mocambola
        result = []
        for key, value in self._mucuas_por_balaio[balaio_slug].items():
            result.append(value.copy())
        return result

    def get_mucua(self,
                  balaio_slug: str,
                  mucua_slug: str,
                  mocambola: Optional[Mocambola] = None
    ):
        mocambola = self._MOCAMBOLA if mocambola is None else mocambola
        return self._mucuas_por_balaio[balaio_slug][mucua_slug].copy()

    def put_mucua(self,
                  balaio_slug: str,
                  name: str,
                  mocambola: Optional[Mocambola] = None,
                  mucua_slug: Optional[str] = None
    ):
        mocambola = self._MOCAMBOLA if mocambola is None else mocambola
        dataset = self.datastore.create_dataset(
            mocambola=mocambola,
            model=Mucua,
            balaio=balaio_slug
        )
        if mucua_slug is None:
            mucua = dataset.settle_saber(
                path=Path('.'),
                name=name,
                data=Mucua(),
                slug_dir=True
            )
            self._mucuas_por_balaio[balaio_slug][mucua.slug] = mucua
            self._mocambos_por_mucua[balaio_slug][mucua.slug] = {}
        else:
            mucua = self._mucuas_por_balaio[balaio_slug][mucua_slug]
            mucua.name = name
            dataset.settle_saber(
                path=mucua.path, name=name, data=mucua.data)
        return mucua.copy()

    def del_mucua(self,
                  balaio_slug: str,
                  mucua_slug: str,
                  mocambola: Optional[Mocambola] = None):
        mocambola = self._MOCAMBOLA if mocambola is None else mocambola
        if balaio_slug == self._balaio_local.slug and \
           mucua_slug == self._mucua_local.slug:
            # Baobaxia não pode deixar para trás a mucua de seus próprios saberes.
            raise RuntimeError('Cannot delete mucua local.')
            
        self.datastore.create_dataset(
            mocambola=mocambola,
            model=Mucua,
            balaio=balaio_slug).drop_saber(Path(mucua_slug))
        del self._mucuas_por_balaio[balaio_slug][mucua_slug]
        del self._mocambos_por_mucua[balaio_slug][mucua_slug]

    def list_mocambos(self, *,
                      balaio_slug: str,
                      mucua_slug: str,
                      token: str):
        result = []
        for mocambo in self._mocambos_por_mucua[
                balaio_slug][mucua_slug]:
            result.append(mocambo.copy(exclude={'mocambolas'}))
        return result
    def get_mocambo(self, *,
                    balaio_slug: str,
                    mucua_slug: str,
                    mocambo_slug: str,
                    token: str):
        return self._mocambos_por_mucua[balaio_slug][mucua_slug][
            mocambo_slug].copy(exclude={'mocambolas'})
    def put_mocambo(self, *,
                    balaio_slug: str,
                    mucua_slug: str,
                    mocambo: Saber,
                    token: str):
        raise NotImplementedError()
    def del_mocambo(self, *,
                    balaio_slug: str,
                    mucua_slug: str,
                    mocambo_slug: str,
                    token, str):
        raise NotImplementedError()

    def list_mocambolas(self, *,
                        balaio_slug: str,
                        mucua_slug: str,
                        mocambo_slug: str,
                        token: str):
        result = []
        mocambo = self._mocambos_por_mucua[balaio_slug][
            mucua_slug][mocambo_slug]
        for mocambola in mocambo.mocambolas:
            result.append(mocambola.copy(exclude={
                'password_hash', 'validation_code'}))
        return result
    def get_mocambola(self, *,
                      balaio_slug: str,
                      mucua_slug: str,
                      mocambo_slug: str,
                      username: str,
                      token: str):
        mocambo = self._mocambos_por_mucua[balaio_slug][
            mucua_slug][mocambo_slug]
        for mocambola in mocambo.mocambolas:
            if mocambola.username == username:
                return mocambola.copy(exclude={
                    'password_hash', 'validation_code'})
        return None
    def put_mocambola(self, *,
                      balaio_slug: str,
                      mucua_slug: str,
                      mocambo_slug: str,
                      mocambola: Mocambola,
                      token: str):
        raise NotImplementedError()
    def del_mocambola(self, *,
                      balaio_slug: str,
                      mucua_slug: str,
                      mocambo_slug: str,
                      username: str,
                      token: str):
        raise NotImplementedError

    def discover_saberes(self, *,
                         balaio_slug: str,
                         mucua_slug: str,
                         mocambola: Mocambola,
                         model: type,
                         patterns: List[str],
                         field_name: Optional[str] = None,
                         list_field_name: Optional[str] = None,
    ):
        if field_name is None:
            field_name = model.__name__.lower()
        if list_field_name is None:
            list_field_name = field_name + 's'

        if not hasattr(self, 'saberes'):
            self.saberes = {}
        if balaio_slug not in self.saberes:
            self.saberes[balaio_slug] = {}
        if mucua_slug not in self.saberes[balaio_slug]:
            self.saberes[balaio_slug][mucua_slug] = {}
        self.saberes[balaio_slug][mucua_slug][field_name] = {}

        dataset = self.datastore.create_dataset(
            balaio = balaio_slug,
            mucua = mucua_slug,
            model = model,
            mocambola = mocambola)

        for pattern in patterns:
            saberes = dataset.collect_saberes(pattern)
            for saber in saberes:
                self.saberes[balaio_slug][mucua_slug][
                    field_name][saber.path] = saber

        def list_method_template(mocambola: Optional[Mocambola] = None):
            mocambola = self._MOCAMBOLA if mocambola is None else mocambola
            result = []
            for key, saber in self.saberes[balaio_slug][mucua_slug][
                    field_name].items():
                result.append(saber)
            return result
        setattr(self, 'list_'+list_field_name, list_method_template)

        def get_method_template(path: Path, mocambola: Optional[Mocambola] = None):
            mocambola = self._MOCAMBOLA if mocambola is None else mocambola
            print(self.saberes[balaio_slug][mucua_slug][field_name])
            return self.saberes[balaio_slug][mucua_slug][
                field_name][path]
        setattr(self, 'get_'+field_name, get_method_template)

        def put_method_template(*, path: Path,
                                name: Optional[str] = None,
                                data: Optional[BaseModel] = None,
                                mocambola: Optional[Mocambola] = None,
                                slug_dir: bool = False):
            mocambola = self._MOCAMBOLA if mocambola is None else mocambola
            saber = self.datastore.create_dataset(
                    balaio = balaio_slug,
                    mucua = mucua_slug,
                    model = model,
                    mocambola = mocambola).settle_saber(
                        path = path, name = name,
                        data = data, slug_dir = slug_dir)
            path = path / saber.slug if slug_dir else path
            self.saberes[balaio_slug][mucua_slug][
                field_name][path] = saber
            return self.saberes[balaio_slug][mucua_slug][
                field_name][path]
        setattr(self, 'put_'+field_name, put_method_template)

        def del_method_template(path: Path, mocambola: Optional[Mocambola] = None):
            mocambola = self._MOCAMBOLA if mocambola is None else mocambola
            self.datastore.create_dataset(
                balaio = balaio_slug,
                mucua = mucua_slug,
                model = model,
                mocambola = mocambola).drop_saber(path)
            del self.saberes[balaio_slug][mucua_slug][
                field_name][path]
        setattr(self, 'del_'+field_name, del_method_template)

    def authenticate(self, username: str, password: str):
        errmsg = 'Erro de autenticação'
        if username not in self._mocambolas:
            raise BaobaxiaError(errmsg)
        mocambola = self._mocambolas[username]
        if str_to_hash(password) != mocambola.password_hash:
            raise BaobaxiaError(errmsg)
        session = BaobaxiaSession(mocambola)
        self._sessions[session.token] = session
        return session.token

    def check_validation_code(self, validation_code: str):
        for mocambola in self._mocambolas:
            if validation_code == mocambola.validation_code:
                return
        raise BaobaxiaError('Código inválido')

    def set_password_by_validation_code(
            self,
            validation_code: str,
            password: str):
        mocambola = None
        for a_mocambola in self._mocambolas:
            if validation_code == a_mocambola.validation_code:
                mocambola = a_mocambola
                break
        if mocambola is None:
            raise BaobaxiaError('Código inválido')
        mocambola.password_hash = str_to_hash(password)
        # PERSIST #######################################################################

    def set_password(
            self,
            old_password: str,
            new_password: str,
            token: str):
        session = self._sessions[token].keep_alive()
        mocambola = session.mocambola
        if mocambola.password_hash != str_to_hash(old_password):
            raise BaobaxiaError('Password antigo está incorreto')
        mocambola.password_hash = str_to_hash(new_password)
        # PERSIST #######################################################################

