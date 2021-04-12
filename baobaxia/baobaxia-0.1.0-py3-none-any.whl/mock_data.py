from os.path import abspath
import base64
from datetime import datetime
from uuid import UUID
from pathlib import Path

from .model import *

REPOSITORIES_PATH = 'repositories'

descr_test='Dados temporários não persistidos.'
created = datetime.fromisoformat('2020-03-14 10:00')
mocambola = Mocambola(username='baobaxia', email='baobaxia@taina.net.br', _password_hash='123')

MOCKED_MUCUA = MucuaLocal(uuid=UUID('ee2dcf8288f311eb8c68c7be26122900'), name='Mucua Teste', description=descr_test, repositories_path=Path(REPOSITORIES_PATH))
MOCKED_MUCUA.mocambolas[mocambola.username] = mocambola
MOCKED_MOCAMBOLA = mocambola

remote1 = MucuaRemote(uuid=UUID('0dd23a13ea5731cab3e8c84eaa722fe6'), name='Remote 1', description=descr_test)
remote2 = MucuaRemote(uuid=UUID('0797792f9eb738c1998f44ee9c2826d7'), name='Remote 2', description=descr_test)
remote3 = MucuaRemote(uuid=UUID('2705eac283283e95adfb3f26a093be4f'), name='Remote 3', description=descr_test)

MOCKED_MUCUA.connections[remote1.uuid] = remote1
MOCKED_MUCUA.connections[remote3.uuid] = remote3

MOCKED_MUCUA.territory = Territory(uuid=UUID('6b386ad6eb7730bd8dd009daaf8f19b5'), name='Território Teste', description=descr_test)
MOCKED_MUCUA.territory.location = GeoLocation(description='Casa de Cultura Tainã', latitude=-22.91342, longitude=-47.11427)
MOCKED_MUCUA.territory.mucuas[remote2.uuid] = remote2
MOCKED_MUCUA.territory.mucuas[remote3.uuid] = remote3

route1 = Route(uuid=UUID('461e9c858e103a30898464846ffbefbe'), name='Rota 1', description=descr_test, ssh_data='ssh mocambola@remote1')
route1.mucuas[remote1.uuid] = remote1
route1.mucuas[remote2.uuid] = remote2
MOCKED_MUCUA.territory.routes[route1.uuid] = route1

route2 = Route(uuid=UUID('022b4a8c60e33fd79292a80e76d7ebb1'), name='Rota 2', description=descr_test, ssh_data='ssh mocambola@remote2')
route2.mucuas[remote1.uuid] = remote1
route2.mucuas[remote3.uuid] = remote3
MOCKED_MUCUA.territory.routes[route2.uuid] = route2

repo1 = RepositoryMetadata(uuid=UUID('8af1c0952c833a35b1379d8ee1896c89'), title='Mocambos', description=descr_test, created=created, creator=mocambola)
repo1.slugfy()
repo1.name = repo1.get_name()
repo1.path = repo1.get_path()

repo2 = RepositoryMetadata(uuid=UUID('1f266f443e023a3685a4330096f68234'), title='Abadias', description=descr_test, created=created, creator=mocambola)
repo2.slugfy()
repo2.name = repo2.get_name()
repo2.path = repo2.get_path()

MOCKED_REPOS = {}
MOCKED_REPOS[repo1.slug] = repo1
MOCKED_REPOS[repo1.slug].items['arquivo'] = DirMetadata(path=repo1.slug+'/arquivo', name='arquivo', created=created, creator=mocambola)
MOCKED_REPOS[repo1.slug].items['audio'] = DirMetadata(path=repo1.slug+'/audio', name='audio', created=created, creator=mocambola)
MOCKED_REPOS[repo1.slug].items['audio'].items['estudio'] = DirMetadata(path=repo1.slug+'/audio/estudio', name='estudio', created=created, creator=mocambola)
MOCKED_REPOS[repo1.slug].items['audio'].items['estudio'].items['2021-03'] = DirMetadata(path=repo1.slug+'/audio/estudio/2021-03', name='2021-03', created=created, creator=mocambola)
MOCKED_REPOS[repo1.slug].items['audio'].items['ao_vivo'] = DirMetadata(path=repo1.slug+'/audio/ao_vivo', name='ao_vivo', created=created, creator=mocambola)
MOCKED_REPOS[repo1.slug].items['imagem'] = DirMetadata(path=repo1.slug+'/imagem', name='imagem', created=created, creator=mocambola)
MOCKED_REPOS[repo1.slug].items['mocambolas'] = DirMetadata(path=repo1.slug+'/mocambolas', name='mocambolas', created=created, creator=mocambola)
MOCKED_REPOS[repo1.slug].items['request'] = DirMetadata(path=repo1.slug+'/request', name='request', created=created, creator=mocambola)
MOCKED_REPOS[repo1.slug].items['video'] = DirMetadata(path=repo1.slug+'/video', name='video', created=created, creator=mocambola)

MOCKED_REPOS[repo2.slug] = repo2 
MOCKED_REPOS[repo2.slug].items['arquivo'] = DirMetadata(path=repo2.slug+'/arquivo', name='arquivo', created=created, creator=mocambola)
MOCKED_REPOS[repo2.slug].items['audio'] = DirMetadata(path=repo2.slug+'/audio', name='audio', created=created, creator=mocambola)
MOCKED_REPOS[repo2.slug].items['imagem'] = DirMetadata(path=repo2.slug+'/imagem', name='imagem', created=created, creator=mocambola)
MOCKED_REPOS[repo2.slug].items['mocambolas'] = DirMetadata(path=repo2.slug+'/mocambolas', name='mocambolas', created=created, creator=mocambola)
MOCKED_REPOS[repo2.slug].items['request'] = DirMetadata(path=repo2.slug+'/request', name='request', created=created, creator=mocambola)
MOCKED_REPOS[repo2.slug].items['video'] = DirMetadata(path=repo2.slug+'/video', name='video', created=created, creator=mocambola)

MOCKED_REPOS[repo2.slug].items['imagem'].items['baobaxia.png'] = FileMetadata(path=repo2.slug+'/imagem/baobaxia.png', name='baobaxia.png', created=created, creator=mocambola)
MOCKED_REPOS[repo2.slug].items['imagem'].items['baobaxia.png']._file_name = '/data/baobaxia/'+repo2.slug+'/imagem/baobaxia.png.json'
MOCKED_REPOS[repo2.slug].items['imagem'].items['baobaxia.png'].content_type = 'image/png'
MOCKED_REPOS[repo2.slug].items['imagem'].items['baobaxia.png'].tags.extend(['baobaxia', 'logo'])

img_file = open('resources/baobaxia_100.png', 'rb')
MOCKED_REPOS[repo2.slug].items['imagem'].items['baobaxia.png'].thumbnail = base64.b64encode(img_file.read())
img_file.close()

MOCKED_TMP_FILES = {}
MOCKED_TMP_FILES[repo2.slug+'/imagem/baobaxia.png'] = abspath('resources/baobaxia.png')
