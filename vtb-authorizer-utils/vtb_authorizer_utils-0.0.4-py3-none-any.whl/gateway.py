from typing import Dict, Any, Optional, List, FrozenSet, Callable

from vtb_http_interaction.keycloak_gateway import KeycloakConfig
from vtb_http_interaction.services import AuthorizationHttpService, HttpService

from vtb_authorizer_utils.converters import convert_user, convert_organization, convert_project, \
    convert_folder, convert_children
from vtb_authorizer_utils.data_objects import User, Organization, Project, Folder, Children
from vtb_authorizer_utils.errors import NotAllowedParameterError


class AuthorizerGateway:
    """
    Сервис оргструктуры
    Пример вложенности  organization->folder1->folder1.1->project1
    """
    _users_allowed_parameters = frozenset({"page", "per_page", "q", "username", "firstname", "lastname", "email"})
    _organizations_allowed_parameters = frozenset({"page", "per_page", "include"})
    _organization_projects_allowed_parameters = frozenset({"page", "per_page", "include"})

    _USERS_URL = 'users'
    _ORGANIZATIONS_URL = 'organizations'
    _FOLDERS_URL = 'folders'
    _PROJECTS_URL = 'projects'
    _STRUCTURE_URL = 'structure'

    def __init__(self, base_url: str,
                 keycloak_config: Optional[KeycloakConfig] = None,
                 redis_connection_string: Optional[str] = None,
                 access_token: Optional[str] = None):
        if keycloak_config is None and access_token is None:
            raise ValueError("keycloak_config is none and access_token is none. You must specify something.")

        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}

        self.service = HttpService() if access_token else AuthorizationHttpService(keycloak_config,
                                                                                   redis_connection_string)

    # Пользователи
    async def get_user(self, keycloak_id: str) -> Optional[User]:
        """ Получение пользователя по keycloak_id (Keycloak ID) """
        return await self._get_item([self._USERS_URL], keycloak_id, convert_user)

    async def get_users(self, **query_params) -> Optional[List[User]]:
        """ Получение списка пользователей """
        _check_request(query_params, self._users_allowed_parameters)

        return await self._get_list([self._USERS_URL], convert_user, **query_params)

    # Организации
    async def get_organization(self, name: str) -> Optional[Organization]:
        """ Получение организации по name (кодовое название) """
        return await self._get_item([self._ORGANIZATIONS_URL], name, convert_organization)

    async def get_organizations(self, **query_params) -> Optional[List[Organization]]:
        """ Получение списка организаций """
        _check_request(query_params, self._organizations_allowed_parameters)

        return await self._get_list([self._ORGANIZATIONS_URL], convert_organization, **query_params)

    async def get_organization_projects(self, name: str, **query_params) -> Optional[List[Project]]:
        """ Получение проектов организации """
        _check_request(query_params, self._organization_projects_allowed_parameters)

        return await self._get_list([self._ORGANIZATIONS_URL, name, self._PROJECTS_URL], convert_project,
                                    **query_params)

    async def get_organization_children(self, name: str, **query_params) -> Optional[List[Children]]:
        """ Получение потомков организации """
        _check_request(query_params, None)

        return await self._get_list([self._ORGANIZATIONS_URL, name, 'children'], convert_children,
                                    **query_params)

    async def get_organization_structure(self, name: str, **query_params) -> Optional[List[Children]]:
        """ Получение структуры организации """
        _check_request(query_params, None)

        return await self._get_list([self._ORGANIZATIONS_URL, name, self._STRUCTURE_URL], convert_children,
                                    **query_params)

    # Folders
    async def get_folder(self, name: str) -> Optional[Folder]:
        """ Получение папки по name """
        return await self._get_item([self._FOLDERS_URL], name, convert_folder)

    async def get_folder_children(self, name: str, **query_params) -> Optional[List[Children]]:
        """ Получение потомков папки """

        return await self._get_list([self._FOLDERS_URL, name, 'children'], convert_children,
                                    **query_params)

    async def get_folder_ancestors(self, name: str, **query_params) -> Optional[List[Children]]:
        """ Получение предков папки """

        return await self._get_list([self._FOLDERS_URL, name, 'ancestors'], convert_children,
                                    **query_params)

    # Projects
    async def get_project(self, name: str) -> Optional[Project]:
        """ Получение проекта по name """
        return await self._get_item([self._PROJECTS_URL], name, convert_project)

    async def get_project_ancestors(self, name: str, **query_params) -> Optional[List[Children]]:
        """ Получение предков проекта """

        return await self._get_list([self._PROJECTS_URL, name, 'ancestors'], convert_children,
                                    **query_params)

    async def _get_item(self, url_path: List[str], item_id: Any, converter: Callable[[Dict[str, Any]], Any]) -> \
            Optional[Any]:
        """ Получение объекта """
        request = {
            'method': "GET",
            'url': _join_str(self.base_url, *url_path, str(item_id)),
            'cfg': {'headers': self.headers}
        }
        status, response = await self.service.send_request(**request)

        return converter(response['data']) if status == 200 else None

    async def _get_list(self, url_path: List[str], converter: Callable[[Dict[str, Any]], Any],
                        **query_params) -> Optional[List]:
        """ Получение списка объектов """
        request = {
            'method': "GET",
            'url': _join_str(self.base_url, *url_path),
            'cfg': {'params': query_params, 'headers': self.headers}
        }
        status, response = await self.service.send_request(**request)

        return list(map(converter, response['data'])) if status == 200 else None


def _check_request(query_params: Dict[str, Any], allowed_parameters: Optional[FrozenSet[str]]=None):
    """ Проверка параметров запроса """
    if not allowed_parameters:
        allowed_parameters = frozenset()
    keys = frozenset(query_params.keys())
    not_allowed_parameters = keys - allowed_parameters
    if len(not_allowed_parameters) > 0:
        raise NotAllowedParameterError(not_allowed_parameters, allowed_parameters)


def _join_str(*args, sep: Optional[str] = '/') -> str:
    return sep.join(arg.strip(sep) for arg in args)
