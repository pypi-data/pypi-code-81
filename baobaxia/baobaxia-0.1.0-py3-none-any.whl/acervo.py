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

class AcervoAPI(BaobaxiaAPI):

    def __init__(
            self,
            config: Optional[SaberesConfig] = None,
            prefix: Optional[str] = None,
            tags: Optional[List[str]] = None,
            **kwargs: Any) -> None:
        super().__init__(
            config=config,
            prefix=prefix,
            tags=tags,
            **kwargs)

        base_path = self.baobaxia.config.data_path / \
            self.baobaxia.config.balaio_local / \
            self.baobaxia.config.mucua_local
        
        for tipo, pasta in pastas_por_tipo.items():
            pasta_path = base_path / pasta
            if not pasta_path.exists():
                pasta_path.mkdir()

        def find_saberes_path(**kwargs):
            # kwargs pode ter: tipo (só aqui) slug name data
            pass

        async def post_midia(midia_data: Midia,
                       arquivo: UploadFile = File(...)):
            if arquivo.content_type not in tipos_por_content_type:
                raise HTTPException(status_code=415, detail='Tipo de arquivo inválido')
            midia_data.tipo = tipos_por_content_type[arquivo.content_type]
            saber = self.baobaxia.put_midia(
                path=find_saberes_path(tipo=midia_data.tipo),
                name=arquivo.filename,
                data=midia_data,
                slug_dir=True)
            with (base_path / saber.path / saber.name).open(
                    'w') as arquivo_saber:
                arquivo_saber.write(arquivo.file.read())
                arquivo_saber.close()

        saberes_patterns = []
        for pattern in pastas_por_tipo.values():
            saberes_patterns.append(pattern+'/*/')
        self.baobaxia.discover_saberes(
            balaio_slug=self.baobaxia.config.balaio_local,
            mucua_slug=self.baobaxia.config.mucua_local,
            mocambola=self.baobaxia._MOCAMBOLA,
            model=Midia,
            patterns=saberes_patterns)
        self.add_saberes_api(Midia,
                             saberes_path_method=find_saberes_path,
                             post_method=post_midia,
                             post_summary='Enviar mídia',
                             put_summary='Atualizar informações da mídia',
                             get_summary='Retornar informações da mídia')

        async def download_midia(slug: str):
            saber = self.baobaxia.get_midia(
                find_saberes_path(slug=slug))
            return FileResponse(path=base_path / saber.path / saber.name)
        super().add_api_route(
            'midia/download/{slug}',
            download_midia,
            methods=['GET'],
            summary='Baixa uma mídia')

api = AcervoAPI()
