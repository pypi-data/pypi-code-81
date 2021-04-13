from pathlib import Path
from enum import Enum
from typing import Optional, List, Any

from fastapi import File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .saberes import Saber, SaberesConfig
from .rest import BaobaxiaAPI

from configparser import ConfigParser

class MidiaTipo(str, Enum):
    video = 'video'
    audio = 'audio'
    imagem = 'imagem'
    arquivo = 'arquivo'

class Midia(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    tipo: Optional[MidiaTipo] = None
    tags: List[str] = []

pastas_por_tipo = {
    MidiaTipo.video: 'videos',
    MidiaTipo.audio: 'audios',
    MidiaTipo.imagem: 'imagens',
    MidiaTipo.arquivo: 'arquivos',
}

tipos_por_content_type = {
    'application/ogg': MidiaTipo.audio, # FIXME Pode ser video mas normalmente e' audio :)
    'audio/ogg': MidiaTipo.audio,
    'audio/mpeg': MidiaTipo.audio,
    'image/jpeg': MidiaTipo.imagem,
    'image/png': MidiaTipo.imagem,
    'image/gif': MidiaTipo.imagem,
    'video/ogg': MidiaTipo.video,
    'video/ogv': MidiaTipo.video,
    'video/avi': MidiaTipo.video,
    'video/mp4': MidiaTipo.video,
    'video/webm': MidiaTipo.video,
    'application/pdf': MidiaTipo.arquivo,
    'application/odt': MidiaTipo.arquivo,
    'application/ods': MidiaTipo.arquivo,
    'application/odp': MidiaTipo.arquivo,
}

# TODO endpoint retornando formatos validos


api = BaobaxiaAPI()

base_path = api.baobaxia.config.data_path / \
    api.baobaxia.config.balaio_local / \
    api.baobaxia.config.mucua_local

acervo_path = base_path / 'acervo'
if not acervo_path.exists():
    acervo_path.mkdir()
for tipo, pasta in pastas_por_tipo.items():
    pasta_path = acervo_path / pasta
    if not pasta_path.exists():
        pasta_path.mkdir()


saberes_patterns = []
for pattern in pastas_por_tipo.values():
    saberes_patterns.append('acervo/'+pattern+'/*/')
api.baobaxia.discover_saberes(
    balaio_slug=api.baobaxia.config.balaio_local,
    mucua_slug=api.baobaxia.config.mucua_local,
    mocambola=api.baobaxia._MOCAMBOLA,
    model=Midia,
    patterns=saberes_patterns)

api.add_saberes_api(
    Midia,
    url_path='/acervo/midia',
    skip_post_method=True,
    put_summary='Atualizar informações da mídia',
    get_summary='Retornar informações da mídia')

async def post_midia(name: str, midia_data: Midia) -> Saber:
    return api.baobaxia.put_midia(
        path=Path('acervo') / pastas_por_tipo[midia_data.tipo],
        name=name,
        data=midia_data,
        slug_dir=True)
api.add_api_route('/acervo/midia', post_midia, response_model=Saber,
                  methods=['POST'],
                  summary='Enviar as informações de uma mídia')

async def upload_midia(path: Path, arquivo: UploadFile = File(...)):
    saber = api.baobaxia.get_midia(path)
    with (base_path / saber.path / saber.name).open(
            'wb') as arquivo_saber:
        arquivo_saber.write(arquivo.file.read())
        arquivo_saber.close()
    return {'detail': 'success'}
api.add_api_route('/acervo/upload/{path:path}', upload_midia,
                  response_model=dict, methods=['POST'],
                  summary='Enviar o arquivo uma mídia já existente')

async def download_midia(path: Path):
    saber = api.baobaxia.get_midia(path)
    return FileResponse(path=base_path / saber.path / saber.name)
api.add_api_route('/acervo/download/{path:path}', download_midia,
                  methods=['GET'],
                  summary='Retornar o arquivo de uma mídia')

async def get_tipos_por_content_type():
    return tipos_por_content_type
api.add_api_route('/acervo/tipos_por_content_type',
                  get_tipos_por_content_type, response_model=dict,
                  methods=['GET'],
                  summary='Retornar os content types aceitos e ' + \
                  'os tipos de mídia correspondentes para o json')

