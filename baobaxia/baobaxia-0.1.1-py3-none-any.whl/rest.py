from pathlib import Path
from typing import Optional, List, Any

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel

from .saberes import Saber, SaberesConfig, Balaio
from .root import Baobaxia

from configparser import ConfigParser

class BaobaxiaAPI(FastAPI):

    def __init__(
            self,
            config: Optional[SaberesConfig] = None,
            prefix: Optional[str] = None,
            tags: Optional[List[str]] = None,
            **kwargs: Any) -> None:
        super().__init__(prefix=prefix, tags=tags, **kwargs)
        self.baobaxia = Baobaxia()

        super().add_api_route(
            '/balaio',
            self.list_balaios,
            methods=['GET'],
            response_model=List[Saber],
            summary='Listar balaios')
        super().add_api_route(
            '/balaio',
            self.post_balaio,
            methods=['POST'],
            response_model=Saber,
            summary='Criar um novo balaio')
        super().add_api_route(
            '/balaio/{balaio_slug}',
            self.get_balaio,
            methods=['GET'],
            response_model=Saber,
            summary='Retornar um balaio')
        super().add_api_route(
            '/balaio/{balaio_slug}',
            self.put_balaio,
            methods=['PUT'],
            response_model=Any,
            summary='Atualizar um balaio')
        super().add_api_route(
            '/balaio/{balaio_slug}',
            self.del_balaio,
            methods=['DELETE'],
            summary='Deletar um balaio')
        super().add_api_route(
            '/mucua/{balaio_slug}',
            self.list_mucuas,
            methods=['GET'],
            response_model=List[Saber],
            summary='Listar mucuas')
        super().add_api_route(
            '/mucua/{balaio_slug}',
            self.post_mucua,
            methods=['POST'],
            response_model=Saber,
            summary='Criar uma nova mucua')
        super().add_api_route(
            '/mucua/{balaio_slug}/{mucua_slug}',
            self.get_mucua,
            methods=['GET'],
            response_model=Saber,
            summary='Retornar uma mucua')
        super().add_api_route(
            '/mucua/{balaio_slug}/{mucua_slug}',
            self.put_mucua,
            methods=['PUT'],
            response_model=Saber,
            summary='Atualizar uma mucua')
        super().add_api_route(
            '/mucua/{balaio_slug}/{mucua_slug}',
            self.del_mucua,
            methods=['DELETE'],
            summary='Deletar uma mucua')
        return

    def add_saberes_api(self, model: type, **kwargs):
        if 'field_name' in kwargs and kwargs['field_name'] is not None:
            field_name = kwargs['field_name']
        else:
            field_name = model.__name__.lower()
        if 'list_field_name' in kwargs and kwargs['list_field_name'] is not None:
            list_field_name = kwargs['list_field_name']
        else:
            list_field_name = field_name + 's'

        if 'url_path' in kwargs:
            url_path = kwargs['url_path']
        else:
            url_path = '/'+field_name

        if 'list_summary' in kwargs:
            summary = kwargs['list_summary']
        else:
            summary = 'Listar '+list_field_name
        if 'list_url' in kwargs:
            list_url = kwargs['list_url']
        else:
            list_url = url_path
        if 'list_method' in kwargs and callable(kwargs['list_method']):
            super().add_api_route(
                list_url,
                kwargs['list_method'],
                response_model=List[Saber],
                methods=['GET'],
                summary=summary)
        elif 'skip_list_method' not in kwargs:
            def list_rest_template():
                return getattr(self.baobaxia, 'list_'+list_field_name)()
            super().add_api_route(
                list_url,
                list_rest_template,
                response_model=List[Saber],
                methods=['GET'],
                summary=summary)

        if 'post_summary' in kwargs:
            summary = kwargs['post_summary']
        else:
            summary = 'Criar '+field_name
        if 'post_url' in kwargs:
            post_url = kwargs['post_url']
        else:
            post_url = url_path+'/{path:path}'
        if 'post_method' in kwargs and callable(kwargs['post_method']):
            super().add_api_route(
                post_url,
                kwargs['post_method'],
                response_model=Saber,
                methods=['POST'],
                summary=summary)
        elif 'skip_post_method' not in kwargs:
            def post_rest_template(path: Path, name: str, data: model):
                return getattr(self.baobaxia, 'put_'+field_name)(
                    path=path,
                    name=name,
                    data=data,
                    slug_dir=True)
            super().add_api_route(
                post_url,
                post_rest_template,
                response_model=Saber,
                methods=['POST'],
                summary=summary)

        if 'get_summary' in kwargs:
            summary = kwargs['get_summary']
        else:
            summary = 'Retornar '+field_name
        if 'get_url' in kwargs:
            get_url = kwargs['get_url']
        else:
            get_url = url_path+'/{path:path}'
        if 'get_method' in kwargs and callable(kwargs['get_method']):
            super().add_api_route(
                get_url,
                kwargs['get_method'],
                response_model=Saber,
                methods=['GET'],
                summary=summary)
        elif 'skip_get_method' not in kwargs:
            def get_rest_template(path: Path):
                return getattr(self.baobaxia, 'get_'+field_name)(
                    path)
            super().add_api_route(
                get_url,
                get_rest_template,
                response_model=Saber,
                methods=['GET'],
                summary=summary)

        if 'put_summary' in kwargs:
            summary = kwargs['put_summary']
        else:
            summary = 'Atualizar '+field_name
        if 'put_url' in kwargs:
            put_url = kwargs['put_url']
        else:
            put_url = url_path+'/{path:path}'
        if 'put_method' in kwargs and callable(kwargs['put_method']):
            super().add_api_route(
                put_url,
                kwargs['put_method'],
                response_model=Saber,
                methods=['PUT'],
                summary=summary)
        elif 'skip_put_method' not in kwargs:
            def put_rest_template(path: Path,
                                  name: Optional[str] = None,
                                  data: Optional[model] = None):
                return getattr(self.baobaxia, 'put_'+field_name)(
                    path=path,
                    name=name,
                    data=data)
            super().add_api_route(
                put_url,
                put_rest_template,
                response_model=Saber,
                methods=['PUT'],
                summary=summary)

        if 'del_summary' in kwargs:
            summary = kwargs['del_summary']
        else:
            summary = 'Deletar '+field_name
        if 'del_url' in kwargs:
            del_url = kwargs['del_url']
        else:
            del_url = url_path+'/{path:path}'
        if 'del_method' in kwargs and callable(kwargs['del_method']):
            super().add_api_route(
                del_url,
                kwargs['del_method'],
                methods['DELETE'],
                summary=summary)
        elif 'skip_del_method' not in kwargs:
            def del_rest_template(path: Path):
                getattr(self.baobaxia, 'del_'+field_name)(
                    path)
                return
            super().add_api_route(
                del_url,
                del_rest_template,
                methods=['DELETE'],
                summary=summary)


    async def list_balaios(self):
        return self.baobaxia.list_balaios()
    async def post_balaio(self, name: str):
        return self.baobaxia.put_balaio(name=name)
    async def get_balaio(self, balaio_slug: str):
        return self.baobaxia.get_balaio(balaio_slug)
    async def put_balaio(self, balaio_slug: str, name: str):
        return self.baobaxia.put_balaio(slug=balaio_slug, name=name)
    async def del_balaio(self, balaio_slug: str):
        self.baobaxia.del_balaio(balaio_slug)
        return
    async def list_mucuas(self, balaio_slug: str):
        return self.baobaxia.list_mucuas(balaio_slug)
    async def post_mucua(self, balaio_slug: str, name: str):
        return self.baobaxia.put_mucua(balaio_slug, name)
    async def get_mucua(self, balaio_slug: str, mucua_slug: str):
        return self.baobaxia.get_mucua(balaio_slug, mucua_slug)
    async def put_mucua(self, balaio_slug: str, mucua_slug: str, name: str):
        return self.baobaxia.put_mucua(
            balaio_slug=balaio_slug,
            mucua_slug=mucua_slug,
            name=name)
    async def del_mucua(self, balaio_slug: str, mucua_slug: str):
        self.baobaxia.del_mucua(balaio_slug, mucua_slug)
        return

 
#path = config.data_path / config.balaio_local / config.mucua_local
api = BaobaxiaAPI()

'''
class Brilho(BaseModel):
    cor: str
    intensidade: int

app.baobaxia.discover_saberes(
    balaio_slug=config.balaio_local,
    mucua_slug=config.mucua_local,
    mocambola=app.baobaxia._MOCAMBOLA,
    model=Brilho,
    patterns=['brilhos/*/'])
app.add_saberes_api(Brilho)
'''
