from uuid import UUID
from .model import *
from .storage import RepositoryBrowser

class MucuaContext():

    ROLE_KAITIAKI = "Kaitiaki"
    ROLE_MIRIM = "Mirim"

    @CLASSMETHOD
    def authenticate(cls, username: str,
                     password: str) -> MucuaContext:
        pass

    def mocambola(self) -> Mocambola:
        return self._mocambola

    def has_role(self, role: str) -> bool:
        return role in self._mocambola.roles
    
    def is_kaitiaki(self) -> bool:
        return self.has_role(MucuaContext.ROLE_KAITIAKI)

    def is_mirim(self) -> bool:
        return self.has_role(MucuaContext.ROLE_MIRIM)


class BaseEndpoint():

    def __init__(self, context: MucuaContext):
        super.__init__()
        self.context = context
        
    def check_kaitiaki(self):
        if not self.context.is_kaitiaki():
            raise RuntimeError('Permission error')

    def check_mirim(self):
        if not self.context.is_mirim():
            raise RuntimeError('Permission error')

    
class MucuaEndpoint(BaseEndpoint):

    def get_mucua(self):
        pass
    
    def update_mucua(self, mucua: BaseBaobaxiaModel):
        self.check_kaitiaki()
        # TODO
    
    def list_connections(self):
        pass
    def save_connection(self, mucua: MucuaRemote):
        pass
    def delete_connection(self, mucua_uuid: UUID):
        pass
    def get_territory(self):
        pass
    def update_territory(self, territory: BaseTerritory):
        pass
    def list_territory_mucuas(self):
        pass
    def save_territory_mucua(self, mucua: MucuaRemote):
        pass
    def delete_territory_mucua(self, mucua_uuid: UUID):
        pass
    def list_routes(self):
        pass
    def save_route(self, route: Route):
        pass
    def delete_route(self, route_uuid: UUID):
        pass
    def list_route_mucuas(self, route_uuid: UUID):
        pass
    def save_route_mucua(self, route_uuid: UUID, mucua: MucuaRemote):
        pass
    def delete_route_mucua(self, route_uuid: UUID, mucua_uuid: UUID):
        pass

class MocambolaEndpoint(BaseEndpoint):

    def list_mocambolas(self):
        pass
    def get_mocambola(self, username: str):
        pass
    def create_mocambola(self, mocambola: Mocambola):
        pass
    def update_mocambola(self, mocambola: Mocambola):
        pass
    def delete_mocambola(self, username: str):
        pass
    def update_password(self, old_password: str, new_password: str):
        pass
    def check_password(self, password: str):
        pass
    def check_validation_code(self, validation_code: str):
        pass
    def update_password_by_validation_code(self, validation_code: str, new_password: str):
        pass

class RepositoryEndpoint(BaseEndpoint):

    def list_repositories(self):
        return RepositoryBrowser().list_repositories()

    def create_repository(self, repository: RepositoryMetadata):
        RepositoryBrowser().create_repository(repository)

    def update_repository(self, repository: RepositoryMetadata):
        pass
    def delete_repository(self, repository_slug: str):
        pass

    def browse(self, path: str):
        return RepositoryBrowser().select(path).list_dir()

    def save_dir(self, dir_metadata: DirMetadata):
        pass
    def delete_dir(self, path: str):
        pass
    def save_file(self, file_metadata: FileMetadata):
        pass
    def delete_file(self, path: str):
        pass
    def download_file(self, path: str):
        pass
    def upload_file(self, path: str, file_content: NamedTemporaryFile):
        pass


class AcervoEndpoint(BaseEndpoint):

    def list_audio(self):
        pass
    def get_audio(self, audio_uuid: UUID):
        pass
    def save_audio(self, file_metadata: FileMetadata):
        pass
    def delete_audio(self, audio_uuid: UUID):
        pass

    def list_video(self):
        pass
    def get_video(self, video_uuid: UUID):
        pass
    def save_video(self, file_metadata: FileMetadata):
        pass
    def delete_video(self, video_uuid: UUID):
        pass

    def list_image(self):
        pass
    def get_image(self, image_uuid: UUID):
        pass
    def save_image(self, file_metadata: FileMetadata):
        pass
    def delete_image(self, image_uuid: UUID):
        pass

    def list_arquivo(self):
        pass
    def get_arquivo(self, arquivo_uuid: UUID):
        pass
    def save_arquivo(self, file_metadata: FileMetadata):
        pass
    def delete_arquivo(self, arquivo_uuid: UUID):
        pass
