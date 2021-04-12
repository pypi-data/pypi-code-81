import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from time import time
from typing import Optional
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .model import *
from .endpoints import MucuaContext, RepositoryEndpoint
from .mock_data import MOCKED_MUCUA, MOCKED_REPOS, MOCKED_MOCAMBOLA, MOCKED_TMP_FILES

from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

DEFAULT_RESPONSE = {'detail': 'success'}

MOCKED_MUCUA_CONTEXT = MucuaContext()
MOCKED_MUCUA_CONTEXT._mocambola = MOCKED_MOCAMBOLA

@app.get("/")
async def get_mucua(token: str = Depends(oauth2_scheme)):
    '''Retorna os dados da mucua local.'''
    return MOCKED_MUCUA.copy(exclude={'territory', 'connections', 'mocambolas'})

@app.put("/")
async def put_mucua(mucua: BaseBaobaxiaModel, token: str = Depends(oauth2_scheme)):
    '''Atualiza os dados da mucua local.'''
    MOCKED_MUCUA.update(mucua)
    return DEFAULT_RESPONSE

@app.get("/connection")
async def list_connections(token: str = Depends(oauth2_scheme)):
    '''Retorna a lista de mucuas remotas conectadas à mucua local.'''
    return MOCKED_MUCUA.connections

@app.put("/connection")
async def connect_or_update(mucua: MucuaRemote, token: str = Depends(oauth2_scheme)):
    '''Conecta a mucua local a uma mucua remota ou atualiza os dados da mucua remota para a mucua local.'''
    MOCKED_MUCUA.connections[mucua.uuid] = mucua
    return DEFAULT_RESPONSE

@app.delete("/connection/{mucua_uuid}")
async def disconnect(mucua_uuid: UUID, token: str = Depends(oauth2_scheme)):
    '''Desconecta a mucua local de uma mucua remota.'''
    try:
        del MOCKED_MUCUA.connections[mucua_uuid]
    except KeyError:
        raise HTTPException(status_code=404, detail='Item not found.')
    return DEFAULT_RESPONSE

@app.get("/territory")
async def get_territory(token: str = Depends(oauth2_scheme)):
    '''Retorna os dados do território no qual a mucua local se localiza.'''
    return MOCKED_MUCUA.territory.copy(exclude={'routes', 'mucuas'})

@app.put("/territory")
async def update_territory(territory: BaseTerritory, token: str = Depends(oauth2_scheme)):
    '''Atualiza os dados do território.'''
    MOCKED_MUCUA.territory.update(territory)
    return DEFAULT_RESPONSE

@app.get("/territory/mucua")
async def list_territory_mucuas(token: str = Depends(oauth2_scheme)):
    '''Retorna a lista de mucuas remotas localizadas no mesmo território.'''
    return MOCKED_MUCUA.territory.mucuas

@app.put("/territory/mucua")
async def add_or_update_territory_mucua(mucua: MucuaRemote, token: str = Depends(oauth2_scheme)):
    '''Adiciona uma mucua remota ao território ou atualiza os dados da mucua remota para o território.'''
    MOCKED_MUCUA.territory.mucuas[mucua.uuid] = mucua
    return DEFAULT_RESPONSE

@app.delete("/territory/mucua/{mucua_uuid}")
async def remove_territory_mucua(mucua_uuid: UUID, token: str = Depends(oauth2_scheme)):
    '''Remove uma mucua remota do território.'''
    try:
        del MOCKED_MUCUA.territory.mucuas[mucua_uuid]
    except KeyError:
        raise HTTPException(status_code=404, detail='Item not found.')
    return DEFAULT_RESPONSE

@app.get("/territory/route")
async def list_routes(token: str = Depends(oauth2_scheme)):
    '''Retorna as rotas das quais o território participa.'''
    result = {}
    for item, value in MOCKED_MUCUA.territory.routes.items():
        result[item] = value.copy(exclude={'mucuas'})
    return result

@app.put("/territory/route")
async def join_or_update_route(route: BaseBaobaxiaModel, token: str = Depends(oauth2_scheme)):
    '''Ingressa em uma rota ou atualiza os dados da rota.'''
    if route.uuid in MOCKED_MUCUA.territory.routes:
        MOCKED_MUCUA.territory.routes[route.uuid].update(route)
    else:
        MOCKED_MUCUA.territory.routes[route.uuid] = Route(uuid=route.uuid, name=route.name, description=route.description)
    return DEFAULT_RESPONSE

@app.delete("/territory/route/{route_uuid}")
async def leave_route(route_uuid: UUID, token: str = Depends(oauth2_scheme)):
    '''Deixa uma rota.'''
    try:
        del MOCKED_MUCUA.territory.routes[route_uuid]
    except KeyError:
        raise HTTPException(status_code=404, detail='Item not found.')
    return DEFAULT_RESPONSE

@app.get("/territory/route/{route_uuid}/mucua")
async def list_route_mucuas(route_uuid: UUID, token: str = Depends(oauth2_scheme)):
    '''Retorna a lista de mucuas remotas que participam de uma rota.'''
    return MOCKED_MUCUA.territory.routes[route_uuid].mucuas

@app.put("/territory/route/{route_uuid}/mucua")
async def add_or_update_route_mucua(route_uuid: UUID, mucua: MucuaRemote, token: str = Depends(oauth2_scheme)):
    '''Adiciona uma mucua remota a uma rota ou atualiza os dados da mucua remota para uma rota.'''
    MOCKED_MUCUA.territory.routes[route_uuid].mucuas[mucua.uuid] = mucua
    return DEFAULT_RESPONSE

@app.delete("/territory/route/{route_uuid}/mucua/{mucua_uuid}")
async def del_route_mucua(route_uuid: UUID, mucua_uuid: UUID, token: str = Depends(oauth2_scheme)):
    '''Remove uma mucua remota de uma rota.'''
    try:
        del MOCKED_MUCUA.territory.routes[route_uuid].mucuas[mucua_uuid]
    except KeyError:
        raise HTTPException(status_code=404, detail='Item not found.')
    return DEFAULT_RESPONSE

@app.get("/mocambola")
async def list_mocambolas(token: str = Depends(oauth2_scheme)):
    '''Retorna a lista de mocambolas da mucua local.'''
    return MOCKED_MUCUA.mocambolas

@app.get("/repository")
async def list_repositories(token: str = Depends(oauth2_scheme)):
    '''Retorna a lista de repositórios da mucua local.'''
    return RepositoryEndpoint(MOCKED_MUCUA_CONTEXT).list_repositories()

@app.post("/repository")
async def create_repository(repository: RepositoryMetadata, token: str = Depends(oauth2_scheme)):
    '''Cria um novo repositório.'''
    RepositoryEndpoint(MOCKED_MUCUA_CONTEXT).create_repository(repository)
    return DEFAULT_RESPONSE

@app.put("/repository")
async def update_repository(repository: RepositoryMetadata, token: str = Depends(oauth2_scheme)):
    '''Atualiza os metadados de um repositório existente.'''
    if repository.slug not in MOCKED_REPOS:
        raise HTTPException(status_code=404, detail='Item not found.')
    MOCKED_REPOS[repository.slug].metadata.update(repository, exclude=['uuid', 'slug'])
    return DEFAULT_RESPONSE

@app.delete("/repository/{repo_slug}")
async def delete_repository(repo_slug: str, token: str = Depends(oauth2_scheme)):
    '''Remove um repositório'''
    try:
        del MOCKED_REPOS[repo_slug]
    except KeyError:
        raise HTTPException(status_code=404, detail='Item not found.')
    return DEFAULT_RESPONSE

@app.get("/repository/browse/{path:path}")
async def browse_repository(path: str, token: str = Depends(oauth2_scheme)):
    '''Navega por um caminho no repositório, sendo o primeiro item do caminho o slug do repositório.'''
    if path.endswith('/'):
        path = path[:-1]

    dir_list = MOCKED_REPOS
    metadata = None
    path_parts = path.split('/')

    for p_part in path_parts:
        metadata = dir_list[p_part]
        if metadata.is_dir:
            dir_list = dir_list[p_part].items
        else:
            dir_list = None

    if metadata.is_dir:
        metadata = metadata.copy(exclude={'items'})
        metadata.items = dict()
        for dir_name, dir_item in dir_list.items():
            metadata.items[dir_name] = dir_item.copy(exclude={'items'})

    return metadata

@app.post("/repository/dir/{path:path}")
async def create_repository_dir(path: str, token: str = Depends(oauth2_scheme)):
    '''Cria nova(s) pasta(s) em um repositório.'''
    if path.endswith('/'):
        path = path[:-1]

    metadata = None
    path_parts = path.split('/')
    partial_path = ''
    for p_part in path_parts:
        if partial_path != '':
            partial_path += '/'
        partial_path += p_part
        if metadata is None:
            if p_part not in MOCKED_REPOS:
                raise HTTPException(status_code=403, detail='Create repository instead.')
            metadata = MOCKED_REPOS[p_part]
        else:
            if p_part not in metadata.items:
                metadata.items[p_part] = DirMetadata(path=partial_path, name=p_part, created=datetime.now(), creator=MOCKED_MOCAMBOLA)
            metadata = metadata.items[p_part]
    return DEFAULT_RESPONSE

@app.delete("/repository/dir/{path:path}")
async def delete_repository_dir(path: str, token: str = Depends(oauth2_scheme)):
    '''Deleta a pasta do repositório.'''
    if path.endswith('/'):
        path = path[:-1]

    dir_list = MOCKED_REPOS
    parent_list = None
    metadata = None
    path_parts = path.split('/')
    for p_part in path_parts:
        metadata = dir_list[p_part]
        parent_list = dir_list
        if metadata.is_dir:
            dir_list = metadata.items
        else:
            dir_list = None

    if metadata.is_dir:
        del parent_list[p_part]
    return DEFAULT_RESPONSE

@app.get("/repository/file/{path:path}")
async def get_repository_file(path: str, token: str = Depends(oauth2_scheme)):
    '''Faz o download de um arquivo do repositório.'''
    return FileResponse(path=MOCKED_TMP_FILES[path])

@app.post("/repository/file/{path:path}")
async def upload_repository_file(path: str,
                                 file_metadata: FileMetadata, 
                                 file: UploadFile = File(...),
                                 token: str = Depends(oauth2_scheme)):
    '''Envia o conteúdo e os metadados de um arquivo para o repositório.'''

    # Salva o arquivo termporário
    tmp_file = None
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_file = tmp.name
    finally:
        file.file.close()
    MOCKED_TMP_FILES[path] = tmp_file

    # Cria o BaseMetadata no mock
    dir_list = MOCKED_REPOS
    metadata = None
    path_parts = path.split('/')
    for p_part in path_parts:
        if p_part not in dir_list and path.endswith(p_part):
            dir_list[p_part] = FileMetadata(path=path, name=p_part,
                                            metadata=file_metadata)
            break
        metadata = dir_list[p_part]
        if metadata.is_dir:
            dir_list = metadata.items
        else:
            dir_list = None

    return DEFAULT_RESPONSE

@app.put("/repository/file/{path:path}")
async def set_repository_file_metadata(path: str,
                                       file: FileMetadata,
                                       token: str = Depends(oauth2_scheme)):
    '''Cria ou atualiza os metadados de um arquivo.'''
    if path.endswith('/'):
        path = path[:-1]

    dir_list = MOCKED_REPOS
    metadata = None
    path_parts = path.split('/')
    for p_part in path_parts:
        metadata = dir_list[p_part]
        if metadata.is_dir:
            dir_list = metadata.items
        else:
            dir_list = None

    if not metadata.is_dir:
        metadata.metadata = file
    return DEFAULT_RESPONSE

@app.delete("/repository/file/{path:path}")
async def delete_repository_file(path: str, token: str = Depends(oauth2_scheme)):
    '''Deleta o arquivo do repositório.'''
    if path.endswith('/'):
        path = path[:-1]

    dir_list = MOCKED_REPOS
    parent_list = None
    metadata = None
    path_parts = path.split('/')
    for p_part in path_parts:
        metadata = dir_list[p_part]
        parent_list = dir_list
        if metadata.is_dir:
            dir_list = metadata.items
        else:
            dir_list = None

    if not metadata.is_dir:
        del parent_list[p_part]
    del MOCKED_TMP_FILES[path]
    return DEFAULT_RESPONSE

@app.post("/auth")
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != 'baobaxia' or form_data.password != 'teste1234':
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return form_data.username + str(int(time()*1000))
