# coding: utf-8

# (C) Copyright IBM Corp. 2021.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# IBM OpenAPI SDK Code Generator Version: 3.30.0-bd714324-20210406-200538
 
"""
Schematics Service is to provide the capability to manage resources  of (cloud) provider
infrastructure using file based configurations.  With the Schematics service the customer
is able to specify the  required set of resources and their configuration in ''config
files'',  and then pass these config files to the service to fulfill it by  calling the
necessary actions on the infrastructure.  This principle is also known as Infrastructure
as Code.  For more information refer to
https://cloud.ibm.com/docs/schematics?topic=schematics-getting-started'
"""

from datetime import datetime
from enum import Enum
from typing import BinaryIO, Dict, List
import base64
import json

from ibm_cloud_sdk_core import BaseService, DetailedResponse
from ibm_cloud_sdk_core.authenticators.authenticator import Authenticator
from ibm_cloud_sdk_core.get_authenticator import get_authenticator_from_environment
from ibm_cloud_sdk_core.utils import convert_model, datetime_to_string, string_to_datetime

from .common import get_sdk_headers

##############################################################################
# Service
##############################################################################

class SchematicsV1(BaseService):
    """The schematics V1 service."""

    DEFAULT_SERVICE_URL = 'https://schematics-dev.containers.appdomain.cloud'
    DEFAULT_SERVICE_NAME = 'schematics'

    @classmethod
    def new_instance(cls,
                     service_name: str = DEFAULT_SERVICE_NAME,
                    ) -> 'SchematicsV1':
        """
        Return a new client for the schematics service using the specified
               parameters and external configuration.
        """
        authenticator = get_authenticator_from_environment(service_name)
        service = cls(
            authenticator
            )
        service.configure_service(service_name)
        return service

    def __init__(self,
                 authenticator: Authenticator = None,
                ) -> None:
        """
        Construct a new client for the schematics service.

        :param Authenticator authenticator: The authenticator specifies the authentication mechanism.
               Get up to date information from https://github.com/IBM/python-sdk-core/blob/master/README.md
               about initializing the authenticator of your choice.
        """
        BaseService.__init__(self,
                             service_url=self.DEFAULT_SERVICE_URL,
                             authenticator=authenticator)


    #########################
    # schematics
    #########################


    def list_schematics_location(self,
        **kwargs
    ) -> DetailedResponse:
        """
        List supported schematics locations.

        List supported schematics locations.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[SchematicsLocations]` result
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_schematics_location')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/locations'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def list_resource_group(self,
        **kwargs
    ) -> DetailedResponse:
        """
        List of resource groups in the Account.

        List of resource groups in the Account.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[ResourceGroupResponse]` result
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_resource_group')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/resource_groups'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def get_schematics_version(self,
        **kwargs
    ) -> DetailedResponse:
        """
        Get schematics version.

        Get schematics version.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `VersionResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_schematics_version')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/version'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response

    #########################
    # workspaces
    #########################


    def list_workspaces(self,
        *,
        offset: int = None,
        limit: int = None,
        **kwargs
    ) -> DetailedResponse:
        """
        List all workspace definitions.

        List all workspace definitions.

        :param int offset: (optional) The number of items to skip before starting
               to collect the result set.
        :param int limit: (optional) The numbers of items to return.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceResponseList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_workspaces')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/workspaces'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def create_workspace(self,
        *,
        applied_shareddata_ids: List[str] = None,
        catalog_ref: 'CatalogRef' = None,
        description: str = None,
        location: str = None,
        name: str = None,
        resource_group: str = None,
        shared_data: 'SharedTargetData' = None,
        tags: List[str] = None,
        template_data: List['TemplateSourceDataRequest'] = None,
        template_ref: str = None,
        template_repo: 'TemplateRepoRequest' = None,
        type: List[str] = None,
        workspace_status: 'WorkspaceStatusRequest' = None,
        x_github_token: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create workspace definition.

        Create workspace definition.

        :param List[str] applied_shareddata_ids: (optional) List of applied shared
               dataset id.
        :param CatalogRef catalog_ref: (optional) CatalogRef -.
        :param str description: (optional) Workspace description.
        :param str location: (optional) Workspace location.
        :param str name: (optional) Workspace name.
        :param str resource_group: (optional) Workspace resource group.
        :param SharedTargetData shared_data: (optional) SharedTargetData -.
        :param List[str] tags: (optional) Workspace tags.
        :param List[TemplateSourceDataRequest] template_data: (optional)
               TemplateData -.
        :param str template_ref: (optional) Workspace template ref.
        :param TemplateRepoRequest template_repo: (optional) TemplateRepoRequest -.
        :param List[str] type: (optional) List of Workspace type.
        :param WorkspaceStatusRequest workspace_status: (optional)
               WorkspaceStatusRequest -.
        :param str x_github_token: (optional) The github token associated with the
               GIT. Required for cloning of repo.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceResponse` object
        """

        if catalog_ref is not None:
            catalog_ref = convert_model(catalog_ref)
        if shared_data is not None:
            shared_data = convert_model(shared_data)
        if template_data is not None:
            template_data = [convert_model(x) for x in template_data]
        if template_repo is not None:
            template_repo = convert_model(template_repo)
        if workspace_status is not None:
            workspace_status = convert_model(workspace_status)
        headers = {
            'X-Github-token': x_github_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_workspace')
        headers.update(sdk_headers)

        data = {
            'applied_shareddata_ids': applied_shareddata_ids,
            'catalog_ref': catalog_ref,
            'description': description,
            'location': location,
            'name': name,
            'resource_group': resource_group,
            'shared_data': shared_data,
            'tags': tags,
            'template_data': template_data,
            'template_ref': template_ref,
            'template_repo': template_repo,
            'type': type,
            'workspace_status': workspace_status
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/workspaces'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def get_workspace(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get workspace definition.

        Get workspace definition.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceResponse` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def replace_workspace(self,
        w_id: str,
        *,
        catalog_ref: 'CatalogRef' = None,
        description: str = None,
        name: str = None,
        shared_data: 'SharedTargetData' = None,
        tags: List[str] = None,
        template_data: List['TemplateSourceDataRequest'] = None,
        template_repo: 'TemplateRepoUpdateRequest' = None,
        type: List[str] = None,
        workspace_status: 'WorkspaceStatusUpdateRequest' = None,
        workspace_status_msg: 'WorkspaceStatusMessage' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Replace the workspace definition.

        Replace the workspace definition.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param CatalogRef catalog_ref: (optional) CatalogRef -.
        :param str description: (optional) Workspace description.
        :param str name: (optional) Workspace name.
        :param SharedTargetData shared_data: (optional) SharedTargetData -.
        :param List[str] tags: (optional) Tags -.
        :param List[TemplateSourceDataRequest] template_data: (optional)
               TemplateData -.
        :param TemplateRepoUpdateRequest template_repo: (optional)
               TemplateRepoUpdateRequest -.
        :param List[str] type: (optional) List of Workspace type.
        :param WorkspaceStatusUpdateRequest workspace_status: (optional)
               WorkspaceStatusUpdateRequest -.
        :param WorkspaceStatusMessage workspace_status_msg: (optional)
               WorkspaceStatusMessage -.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceResponse` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if catalog_ref is not None:
            catalog_ref = convert_model(catalog_ref)
        if shared_data is not None:
            shared_data = convert_model(shared_data)
        if template_data is not None:
            template_data = [convert_model(x) for x in template_data]
        if template_repo is not None:
            template_repo = convert_model(template_repo)
        if workspace_status is not None:
            workspace_status = convert_model(workspace_status)
        if workspace_status_msg is not None:
            workspace_status_msg = convert_model(workspace_status_msg)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='replace_workspace')
        headers.update(sdk_headers)

        data = {
            'catalog_ref': catalog_ref,
            'description': description,
            'name': name,
            'shared_data': shared_data,
            'tags': tags,
            'template_data': template_data,
            'template_repo': template_repo,
            'type': type,
            'workspace_status': workspace_status,
            'workspace_status_msg': workspace_status_msg
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def delete_workspace(self,
        w_id: str,
        refresh_token: str,
        *,
        destroy_resources: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete a workspace definition.

        Delete a workspace definition.  Use destroy_resource='true' to destroy the related
        cloud resource.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str refresh_token: The IAM refresh token associated with the IBM
               Cloud account.
        :param str destroy_resources: (optional) true or 1 - to destroy resources
               before deleting workspace;  If this is true, refresh_token is mandatory.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `str` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_workspace')
        headers.update(sdk_headers)

        params = {
            'destroy_resources': destroy_resources
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def update_workspace(self,
        w_id: str,
        *,
        catalog_ref: 'CatalogRef' = None,
        description: str = None,
        name: str = None,
        shared_data: 'SharedTargetData' = None,
        tags: List[str] = None,
        template_data: List['TemplateSourceDataRequest'] = None,
        template_repo: 'TemplateRepoUpdateRequest' = None,
        type: List[str] = None,
        workspace_status: 'WorkspaceStatusUpdateRequest' = None,
        workspace_status_msg: 'WorkspaceStatusMessage' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update the workspace definition.

        Update the workspace definition.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param CatalogRef catalog_ref: (optional) CatalogRef -.
        :param str description: (optional) Workspace description.
        :param str name: (optional) Workspace name.
        :param SharedTargetData shared_data: (optional) SharedTargetData -.
        :param List[str] tags: (optional) Tags -.
        :param List[TemplateSourceDataRequest] template_data: (optional)
               TemplateData -.
        :param TemplateRepoUpdateRequest template_repo: (optional)
               TemplateRepoUpdateRequest -.
        :param List[str] type: (optional) List of Workspace type.
        :param WorkspaceStatusUpdateRequest workspace_status: (optional)
               WorkspaceStatusUpdateRequest -.
        :param WorkspaceStatusMessage workspace_status_msg: (optional)
               WorkspaceStatusMessage -.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceResponse` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if catalog_ref is not None:
            catalog_ref = convert_model(catalog_ref)
        if shared_data is not None:
            shared_data = convert_model(shared_data)
        if template_data is not None:
            template_data = [convert_model(x) for x in template_data]
        if template_repo is not None:
            template_repo = convert_model(template_repo)
        if workspace_status is not None:
            workspace_status = convert_model(workspace_status)
        if workspace_status_msg is not None:
            workspace_status_msg = convert_model(workspace_status_msg)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='update_workspace')
        headers.update(sdk_headers)

        data = {
            'catalog_ref': catalog_ref,
            'description': description,
            'name': name,
            'shared_data': shared_data,
            'tags': tags,
            'template_data': template_data,
            'template_repo': template_repo,
            'type': type,
            'workspace_status': workspace_status,
            'workspace_status_msg': workspace_status_msg
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PATCH',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def upload_template_tar(self,
        w_id: str,
        t_id: str,
        *,
        file: BinaryIO = None,
        file_content_type: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Upload template tar file for the workspace.

        Upload template tar file for the workspace.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str t_id: The Template ID for which you want to get the values.  Use
               the GET /workspaces to look up the workspace IDs  or template IDs in your
               IBM Cloud account.
        :param BinaryIO file: (optional) Template tar file.
        :param str file_content_type: (optional) The content type of file.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `TemplateRepoTarUploadResponse` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='upload_template_tar')
        headers.update(sdk_headers)

        form_data = []
        if file:
            form_data.append(('file', (None, file, file_content_type or 'application/octet-stream')))

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/template_data/{t_id}/template_repo_upload'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       files=form_data)

        response = self.send(request)
        return response


    def get_workspace_readme(self,
        w_id: str,
        *,
        ref: str = None,
        formatted: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the workspace readme.

        Get the workspace readme.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str ref: (optional) The name of the commit/branch/tag.  Default, the
               repository’s default branch (usually master).
        :param str formatted: (optional) The format of the readme file.  Value
               ''markdown'' will give markdown, otherwise html.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `TemplateReadme` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_readme')
        headers.update(sdk_headers)

        params = {
            'ref': ref,
            'formatted': formatted
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/templates/readme'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response

    #########################
    # workspace-activities
    #########################


    def list_workspace_activities(self,
        w_id: str,
        *,
        offset: int = None,
        limit: int = None,
        **kwargs
    ) -> DetailedResponse:
        """
        List all workspace activities.

        List all workspace activities.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param int offset: (optional) The number of items to skip before starting
               to collect the result set.
        :param int limit: (optional) The numbers of items to return.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivities` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_workspace_activities')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/actions'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def get_workspace_activity(self,
        w_id: str,
        activity_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get workspace activity details.

        Get workspace activity details.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str activity_id: The activity ID that you want to see additional
               details.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivity` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if activity_id is None:
            raise ValueError('activity_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_activity')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 'activity_id']
        path_param_values = self.encode_path_vars(w_id, activity_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/actions/{activity_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def delete_workspace_activity(self,
        w_id: str,
        activity_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Stop the workspace activity.

        Stop the workspace activity.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str activity_id: The activity ID that you want to see additional
               details.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityApplyResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if activity_id is None:
            raise ValueError('activity_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_workspace_activity')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 'activity_id']
        path_param_values = self.encode_path_vars(w_id, activity_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/actions/{activity_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def run_workspace_commands(self,
        w_id: str,
        refresh_token: str,
        *,
        commands: List['TerraformCommand'] = None,
        operation_name: str = None,
        description: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Run terraform Commands.

        Run terraform Commands on workspaces.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str refresh_token: The IAM refresh token associated with the IBM
               Cloud account.
        :param List[TerraformCommand] commands: (optional) List of commands.
        :param str operation_name: (optional) Command name.
        :param str description: (optional) Command description.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityCommandResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        if commands is not None:
            commands = [convert_model(x) for x in commands]
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='run_workspace_commands')
        headers.update(sdk_headers)

        data = {
            'commands': commands,
            'operation_name': operation_name,
            'description': description
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/commands'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def apply_workspace_command(self,
        w_id: str,
        refresh_token: str,
        *,
        action_options: 'WorkspaceActivityOptionsTemplate' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Run schematics workspace 'apply' activity.

        Run schematics workspace 'apply' activity.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str refresh_token: The IAM refresh token associated with the IBM
               Cloud account.
        :param WorkspaceActivityOptionsTemplate action_options: (optional)
               Workspace Activity Options Template.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityApplyResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        if action_options is not None:
            action_options = convert_model(action_options)
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='apply_workspace_command')
        headers.update(sdk_headers)

        data = {
            'action_options': action_options
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/apply'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def destroy_workspace_command(self,
        w_id: str,
        refresh_token: str,
        *,
        action_options: 'WorkspaceActivityOptionsTemplate' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Run workspace 'destroy' activity.

        Run workspace 'destroy' activity,  to destroy all the resources associated with
        the workspace.  WARNING: This action cannot be reversed.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str refresh_token: The IAM refresh token associated with the IBM
               Cloud account.
        :param WorkspaceActivityOptionsTemplate action_options: (optional)
               Workspace Activity Options Template.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityDestroyResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        if action_options is not None:
            action_options = convert_model(action_options)
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='destroy_workspace_command')
        headers.update(sdk_headers)

        data = {
            'action_options': action_options
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/destroy'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def plan_workspace_command(self,
        w_id: str,
        refresh_token: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Run workspace 'plan' activity,.

        Run schematics workspace 'plan' activity,  to preview the change before running an
        'apply' activity.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str refresh_token: The IAM refresh token associated with the IBM
               Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityPlanResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='plan_workspace_command')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/plan'.format(**path_param_dict)
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def refresh_workspace_command(self,
        w_id: str,
        refresh_token: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Run workspace 'refresh' activity.

        Run workspace 'refresh' activity.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str refresh_token: The IAM refresh token associated with the IBM
               Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityRefreshResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='refresh_workspace_command')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/refresh'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response

    #########################
    # workspace-inputs
    #########################


    def get_workspace_inputs(self,
        w_id: str,
        t_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the input values of the workspace.

        Get the input values of the workspace.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str t_id: The Template ID for which you want to get the values.  Use
               the GET /workspaces to look up the workspace IDs  or template IDs in your
               IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `TemplateValues` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_inputs')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/template_data/{t_id}/values'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def replace_workspace_inputs(self,
        w_id: str,
        t_id: str,
        *,
        env_values: List[object] = None,
        values: str = None,
        variablestore: List['WorkspaceVariableRequest'] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Replace the input values for the workspace.

        Replace the input values for the workspace.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str t_id: The Template ID for which you want to get the values.  Use
               the GET /workspaces to look up the workspace IDs  or template IDs in your
               IBM Cloud account.
        :param List[object] env_values: (optional) EnvVariableRequest ..
        :param str values: (optional) User values.
        :param List[WorkspaceVariableRequest] variablestore: (optional)
               VariablesRequest -.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `UserValues` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        if variablestore is not None:
            variablestore = [convert_model(x) for x in variablestore]
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='replace_workspace_inputs')
        headers.update(sdk_headers)

        data = {
            'env_values': env_values,
            'values': values,
            'variablestore': variablestore
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/template_data/{t_id}/values'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def get_all_workspace_inputs(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all the input values of the workspace.

        Get all the input values of the workspace.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceTemplateValuesResponse` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_all_workspace_inputs')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/templates/values'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def get_workspace_input_metadata(self,
        w_id: str,
        t_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the input metadata of the workspace.

        Get the input metadata of the workspace.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str t_id: The Template ID for which you want to get the values.  Use
               the GET /workspaces to look up the workspace IDs  or template IDs in your
               IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[object]` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_input_metadata')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/template_data/{t_id}/values_metadata'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response

    #########################
    # workspace-outputs
    #########################


    def get_workspace_outputs(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all the output values of the workspace.

        Get all the output values from your workspace; (ex. result of terraform output
        command).

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[OutputValuesItem]` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_outputs')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/output_values'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def get_workspace_resources(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all the resources created by the workspace.

        Get all the resources created by the workspace.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[TemplateResources]` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_resources')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/resources'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def get_workspace_state(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the workspace state.

        Get the workspace state.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `StateStoreResponseList` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_state')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/state_stores'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def get_workspace_template_state(self,
        w_id: str,
        t_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the template state.

        Get the template state.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str t_id: The Template ID for which you want to get the values.  Use
               the GET /workspaces to look up the workspace IDs  or template IDs in your
               IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `TemplateStateStore` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_template_state')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/runtime_data/{t_id}/state_store'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response

    #########################
    # workspace-logs
    #########################


    def get_workspace_activity_logs(self,
        w_id: str,
        activity_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the workspace activity log urls.

        View an activity log for Terraform actions that ran against your workspace.  You
        can view logs for plan, apply, and destroy actions.      operationId:
        get_activity_log_urls.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str activity_id: The activity ID that you want to see additional
               details.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityLogs` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if activity_id is None:
            raise ValueError('activity_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_activity_logs')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 'activity_id']
        path_param_values = self.encode_path_vars(w_id, activity_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/actions/{activity_id}/logs'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def get_workspace_log_urls(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all workspace log urls.

        Get all workspace log urls.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `LogStoreResponseList` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_log_urls')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/log_stores'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def get_template_logs(self,
        w_id: str,
        t_id: str,
        *,
        log_tf_cmd: bool = None,
        log_tf_prefix: bool = None,
        log_tf_null_resource: bool = None,
        log_tf_ansible: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all template logs.

        Get all template logs.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str t_id: The Template ID for which you want to get the values.  Use
               the GET /workspaces to look up the workspace IDs  or template IDs in your
               IBM Cloud account.
        :param bool log_tf_cmd: (optional) `false` will hide the terraform command
               header in the logs.
        :param bool log_tf_prefix: (optional) `false` will hide all the terraform
               command prefix in the log statements.
        :param bool log_tf_null_resource: (optional) `false` will hide all the null
               resource prefix in the log statements.
        :param bool log_tf_ansible: (optional) `true` will format all logs to
               withhold the original format  of ansible output in the log statements.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `str` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_template_logs')
        headers.update(sdk_headers)

        params = {
            'log_tf_cmd': log_tf_cmd,
            'log_tf_prefix': log_tf_prefix,
            'log_tf_null_resource': log_tf_null_resource,
            'log_tf_ansible': log_tf_ansible
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/runtime_data/{t_id}/log_store'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def get_template_activity_log(self,
        w_id: str,
        t_id: str,
        activity_id: str,
        *,
        log_tf_cmd: bool = None,
        log_tf_prefix: bool = None,
        log_tf_null_resource: bool = None,
        log_tf_ansible: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the template activity logs.

        View an activity log for Terraform actions that ran for a template against your
        workspace.  You can view logs for plan, apply, and destroy actions.

        :param str w_id: The workspace ID for the workspace that you want to query.
                You can run the GET /workspaces call if you need to look up the  workspace
               IDs in your IBM Cloud account.
        :param str t_id: The Template ID for which you want to get the values.  Use
               the GET /workspaces to look up the workspace IDs  or template IDs in your
               IBM Cloud account.
        :param str activity_id: The activity ID that you want to see additional
               details.
        :param bool log_tf_cmd: (optional) `false` will hide the terraform command
               header in the logs.
        :param bool log_tf_prefix: (optional) `false` will hide all the terraform
               command prefix in the log statements.
        :param bool log_tf_null_resource: (optional) `false` will hide all the null
               resource prefix in the log statements.
        :param bool log_tf_ansible: (optional) `true` will format all logs to
               withhold the original format  of ansible output in the log statements.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `str` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        if activity_id is None:
            raise ValueError('activity_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_template_activity_log')
        headers.update(sdk_headers)

        params = {
            'log_tf_cmd': log_tf_cmd,
            'log_tf_prefix': log_tf_prefix,
            'log_tf_null_resource': log_tf_null_resource,
            'log_tf_ansible': log_tf_ansible
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id', 'activity_id']
        path_param_values = self.encode_path_vars(w_id, t_id, activity_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/runtime_data/{t_id}/log_store/actions/{activity_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response

    #########################
    # workspace-bulk-jobs
    #########################


    def create_workspace_deletion_job(self,
        refresh_token: str,
        *,
        new_delete_workspaces: bool = None,
        new_destroy_resources: bool = None,
        new_job: str = None,
        new_version: str = None,
        new_workspaces: List[str] = None,
        destroy_resources: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete multiple workspaces.

        Delete multiple workspaces.  Use ?destroy_resource="true" to destroy the related
        cloud resources,  otherwise the resources must be managed outside of Schematics.

        :param str refresh_token: The IAM refresh token associated with the IBM
               Cloud account.
        :param bool new_delete_workspaces: (optional) True to delete workspace.
        :param bool new_destroy_resources: (optional) True to destroy the resources
               managed by this workspace.
        :param str new_job: (optional) Workspace deletion job name.
        :param str new_version: (optional) Version.
        :param List[str] new_workspaces: (optional) List of workspaces to be
               deleted.
        :param str destroy_resources: (optional) true or 1 - to destroy resources
               before deleting workspace;  If this is true, refresh_token is mandatory.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceBulkDeleteResponse` object
        """

        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_workspace_deletion_job')
        headers.update(sdk_headers)

        params = {
            'destroy_resources': destroy_resources
        }

        data = {
            'delete_workspaces': new_delete_workspaces,
            'destroy_resources': new_destroy_resources,
            'job': new_job,
            'version': new_version,
            'workspaces': new_workspaces
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/workspace_jobs'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       params=params,
                                       data=data)

        response = self.send(request)
        return response


    def get_workspace_deletion_job_status(self,
        wj_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the workspace deletion job status.

        Get the workspace deletion job status.

        :param str wj_id: The workspace job deletion ID.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceJobResponse` object
        """

        if wj_id is None:
            raise ValueError('wj_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_deletion_job_status')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['wj_id']
        path_param_values = self.encode_path_vars(wj_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspace_jobs/{wj_id}/status'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response

    #########################
    # actions
    #########################


    def create_action(self,
        *,
        name: str = None,
        description: str = None,
        location: str = None,
        resource_group: str = None,
        tags: List[str] = None,
        user_state: 'UserState' = None,
        source_readme_url: str = None,
        source: 'ExternalSource' = None,
        source_type: str = None,
        command_parameter: str = None,
        bastion: 'BastionResourceDefinition' = None,
        inventory: str = None,
        bastion_credential: 'VariableData' = None,
        credentials: List['VariableData'] = None,
        inputs: List['VariableData'] = None,
        outputs: List['VariableData'] = None,
        settings: List['VariableData'] = None,
        state: 'ActionState' = None,
        sys_lock: 'SystemLock' = None,
        x_github_token: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create an Action definition.

        Create a new Action definition.

        :param str name: (optional) Action name (unique for an account).
        :param str description: (optional) Action description.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Action.
               By default, Action will be created in Default Resource Group.
        :param List[str] tags: (optional) Action tags.
        :param UserState user_state: (optional) User defined status of the
               Schematics object.
        :param str source_readme_url: (optional) URL of the README file, for the
               source.
        :param ExternalSource source: (optional) Source of templates, playbooks, or
               controls.
        :param str source_type: (optional) Type of source for the Template.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name).
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param str inventory: (optional) Inventory ID.
        :param VariableData bastion_credential: (optional) User editable variable
               data & system generated reference to value.
        :param List[VariableData] credentials: (optional) credentials of the
               Action.
        :param List[VariableData] inputs: (optional) Input variables for the
               Action.
        :param List[VariableData] outputs: (optional) Output variables for the
               Action.
        :param List[VariableData] settings: (optional) Environment variables for
               the Action.
        :param ActionState state: (optional) Computed state of the Action.
        :param SystemLock sys_lock: (optional) System lock status.
        :param str x_github_token: (optional) The github token associated with the
               GIT. Required for cloning of repo.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Action` object
        """

        if user_state is not None:
            user_state = convert_model(user_state)
        if source is not None:
            source = convert_model(source)
        if bastion is not None:
            bastion = convert_model(bastion)
        if bastion_credential is not None:
            bastion_credential = convert_model(bastion_credential)
        if credentials is not None:
            credentials = [convert_model(x) for x in credentials]
        if inputs is not None:
            inputs = [convert_model(x) for x in inputs]
        if outputs is not None:
            outputs = [convert_model(x) for x in outputs]
        if settings is not None:
            settings = [convert_model(x) for x in settings]
        if state is not None:
            state = convert_model(state)
        if sys_lock is not None:
            sys_lock = convert_model(sys_lock)
        headers = {
            'X-Github-token': x_github_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_action')
        headers.update(sdk_headers)

        data = {
            'name': name,
            'description': description,
            'location': location,
            'resource_group': resource_group,
            'tags': tags,
            'user_state': user_state,
            'source_readme_url': source_readme_url,
            'source': source,
            'source_type': source_type,
            'command_parameter': command_parameter,
            'bastion': bastion,
            'inventory': inventory,
            'bastion_credential': bastion_credential,
            'credentials': credentials,
            'inputs': inputs,
            'outputs': outputs,
            'settings': settings,
            'state': state,
            'sys_lock': sys_lock
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/actions'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def list_actions(self,
        *,
        offset: int = None,
        limit: int = None,
        sort: str = None,
        profile: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all the Action definitions.

        Get all the Action definitions.

        :param int offset: (optional) The number of items to skip before starting
               to collect the result set.
        :param int limit: (optional) The numbers of items to return.
        :param str sort: (optional) Name of the field to sort-by;  Use the '.'
               character to delineate sub-resources and sub-fields (eg. owner.last_name).
               Prepend the field with '+' or '-', indicating 'ascending' or 'descending'
               (default is ascending)   Ignore unrecognized or unsupported sort field.
        :param str profile: (optional) Level of details returned by the get method.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ActionList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_actions')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit,
            'sort': sort,
            'profile': profile
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/actions'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def get_action(self,
        action_id: str,
        *,
        profile: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the Action definition.

        Get the Action definition.

        :param str action_id: Action Id.  Use GET /actions API to look up the
               Action Ids in your IBM Cloud account.
        :param str profile: (optional) Level of details returned by the get method.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Action` object
        """

        if action_id is None:
            raise ValueError('action_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_action')
        headers.update(sdk_headers)

        params = {
            'profile': profile
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['action_id']
        path_param_values = self.encode_path_vars(action_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/actions/{action_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def delete_action(self,
        action_id: str,
        *,
        force: bool = None,
        propagate: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete the Action.

        Delete the Action definition.

        :param str action_id: Action Id.  Use GET /actions API to look up the
               Action Ids in your IBM Cloud account.
        :param bool force: (optional) Equivalent to -force options in the command
               line.
        :param bool propagate: (optional) Auto propagate the chaange or deletion to
               the dependent resources.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if action_id is None:
            raise ValueError('action_id must be provided')
        headers = {
            'force': force,
            'propagate': propagate
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_action')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        path_param_keys = ['action_id']
        path_param_values = self.encode_path_vars(action_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/actions/{action_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def update_action(self,
        action_id: str,
        *,
        name: str = None,
        description: str = None,
        location: str = None,
        resource_group: str = None,
        tags: List[str] = None,
        user_state: 'UserState' = None,
        source_readme_url: str = None,
        source: 'ExternalSource' = None,
        source_type: str = None,
        command_parameter: str = None,
        bastion: 'BastionResourceDefinition' = None,
        inventory: str = None,
        bastion_credential: 'VariableData' = None,
        credentials: List['VariableData'] = None,
        inputs: List['VariableData'] = None,
        outputs: List['VariableData'] = None,
        settings: List['VariableData'] = None,
        state: 'ActionState' = None,
        sys_lock: 'SystemLock' = None,
        x_github_token: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update the Action definition.

        Update the Action definition.

        :param str action_id: Action Id.  Use GET /actions API to look up the
               Action Ids in your IBM Cloud account.
        :param str name: (optional) Action name (unique for an account).
        :param str description: (optional) Action description.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Action.
               By default, Action will be created in Default Resource Group.
        :param List[str] tags: (optional) Action tags.
        :param UserState user_state: (optional) User defined status of the
               Schematics object.
        :param str source_readme_url: (optional) URL of the README file, for the
               source.
        :param ExternalSource source: (optional) Source of templates, playbooks, or
               controls.
        :param str source_type: (optional) Type of source for the Template.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name).
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param str inventory: (optional) Inventory ID.
        :param VariableData bastion_credential: (optional) User editable variable
               data & system generated reference to value.
        :param List[VariableData] credentials: (optional) credentials of the
               Action.
        :param List[VariableData] inputs: (optional) Input variables for the
               Action.
        :param List[VariableData] outputs: (optional) Output variables for the
               Action.
        :param List[VariableData] settings: (optional) Environment variables for
               the Action.
        :param ActionState state: (optional) Computed state of the Action.
        :param SystemLock sys_lock: (optional) System lock status.
        :param str x_github_token: (optional) The github token associated with the
               GIT. Required for cloning of repo.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Action` object
        """

        if action_id is None:
            raise ValueError('action_id must be provided')
        if user_state is not None:
            user_state = convert_model(user_state)
        if source is not None:
            source = convert_model(source)
        if bastion is not None:
            bastion = convert_model(bastion)
        if bastion_credential is not None:
            bastion_credential = convert_model(bastion_credential)
        if credentials is not None:
            credentials = [convert_model(x) for x in credentials]
        if inputs is not None:
            inputs = [convert_model(x) for x in inputs]
        if outputs is not None:
            outputs = [convert_model(x) for x in outputs]
        if settings is not None:
            settings = [convert_model(x) for x in settings]
        if state is not None:
            state = convert_model(state)
        if sys_lock is not None:
            sys_lock = convert_model(sys_lock)
        headers = {
            'X-Github-token': x_github_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='update_action')
        headers.update(sdk_headers)

        data = {
            'name': name,
            'description': description,
            'location': location,
            'resource_group': resource_group,
            'tags': tags,
            'user_state': user_state,
            'source_readme_url': source_readme_url,
            'source': source,
            'source_type': source_type,
            'command_parameter': command_parameter,
            'bastion': bastion,
            'inventory': inventory,
            'bastion_credential': bastion_credential,
            'credentials': credentials,
            'inputs': inputs,
            'outputs': outputs,
            'settings': settings,
            'state': state,
            'sys_lock': sys_lock
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['action_id']
        path_param_values = self.encode_path_vars(action_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/actions/{action_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PATCH',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def upload_template_tar_action(self,
        action_id: str,
        *,
        file: BinaryIO = None,
        file_content_type: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Upload template tar file for the action.

        Upload template tar file for the action.

        :param str action_id: Action Id.  Use GET /actions API to look up the
               Action Ids in your IBM Cloud account.
        :param BinaryIO file: (optional) Template tar file.
        :param str file_content_type: (optional) The content type of file.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `TemplateRepoTarUploadResponse` object
        """

        if action_id is None:
            raise ValueError('action_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='upload_template_tar_action')
        headers.update(sdk_headers)

        form_data = []
        if file:
            form_data.append(('file', (None, file, file_content_type or 'application/octet-stream')))

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['action_id']
        path_param_values = self.encode_path_vars(action_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/actions/{action_id}/template_repo_upload'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       files=form_data)

        response = self.send(request)
        return response

    #########################
    # jobs
    #########################


    def create_job(self,
        refresh_token: str,
        *,
        command_object: str = None,
        command_object_id: str = None,
        command_name: str = None,
        command_parameter: str = None,
        command_options: List[str] = None,
        inputs: List['VariableData'] = None,
        settings: List['VariableData'] = None,
        tags: List[str] = None,
        location: str = None,
        status: 'JobStatus' = None,
        data: 'JobData' = None,
        bastion: 'BastionResourceDefinition' = None,
        log_summary: 'JobLogSummary' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create a Job record and launch the Job.

        Creare a Job record and launch the Job.

        :param str refresh_token: The IAM refresh token associated with the IBM
               Cloud account.
        :param str command_object: (optional) Name of the Schematics automation
               resource.
        :param str command_object_id: (optional) Job command object id
               (workspace-id, action-id).
        :param str command_name: (optional) Schematics job command name.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name, capsule-name or flow-name).
        :param List[str] command_options: (optional) Command line options for the
               command.
        :param List[VariableData] inputs: (optional) Job inputs used by Action.
        :param List[VariableData] settings: (optional) Environment variables used
               by the Job while performing Action.
        :param List[str] tags: (optional) User defined tags, while running the job.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param JobStatus status: (optional) Job Status.
        :param JobData data: (optional) Job data.
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param JobLogSummary log_summary: (optional) Job log summary record.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Job` object
        """

        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        if inputs is not None:
            inputs = [convert_model(x) for x in inputs]
        if settings is not None:
            settings = [convert_model(x) for x in settings]
        if status is not None:
            status = convert_model(status)
        if data is not None:
            data = convert_model(data)
        if bastion is not None:
            bastion = convert_model(bastion)
        if log_summary is not None:
            log_summary = convert_model(log_summary)
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_job')
        headers.update(sdk_headers)

        data = {
            'command_object': command_object,
            'command_object_id': command_object_id,
            'command_name': command_name,
            'command_parameter': command_parameter,
            'command_options': command_options,
            'inputs': inputs,
            'settings': settings,
            'tags': tags,
            'location': location,
            'status': status,
            'data': data,
            'bastion': bastion,
            'log_summary': log_summary
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/jobs'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def list_jobs(self,
        *,
        offset: int = None,
        limit: int = None,
        sort: str = None,
        profile: str = None,
        resource: str = None,
        action_id: str = None,
        list: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all the Job records.

        Get all the Job records.

        :param int offset: (optional) The number of items to skip before starting
               to collect the result set.
        :param int limit: (optional) The numbers of items to return.
        :param str sort: (optional) Name of the field to sort-by;  Use the '.'
               character to delineate sub-resources and sub-fields (eg. owner.last_name).
               Prepend the field with '+' or '-', indicating 'ascending' or 'descending'
               (default is ascending)   Ignore unrecognized or unsupported sort field.
        :param str profile: (optional) Level of details returned by the get method.
        :param str resource: (optional) Name of the resource (workspace, actions or
               controls).
        :param str action_id: (optional) Action Id.
        :param str list: (optional) list jobs.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `JobList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_jobs')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit,
            'sort': sort,
            'profile': profile,
            'resource': resource,
            'action_id': action_id,
            'list': list
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/jobs'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def replace_job(self,
        job_id: str,
        refresh_token: str,
        *,
        command_object: str = None,
        command_object_id: str = None,
        command_name: str = None,
        command_parameter: str = None,
        command_options: List[str] = None,
        inputs: List['VariableData'] = None,
        settings: List['VariableData'] = None,
        tags: List[str] = None,
        location: str = None,
        status: 'JobStatus' = None,
        data: 'JobData' = None,
        bastion: 'BastionResourceDefinition' = None,
        log_summary: 'JobLogSummary' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Clone the Job-record, and relaunch the Job.

        Clone the Job-record, and relaunch the Job.

        :param str job_id: Job Id. Use GET /jobs API to look up the Job Ids in your
               IBM Cloud account.
        :param str refresh_token: The IAM refresh token associated with the IBM
               Cloud account.
        :param str command_object: (optional) Name of the Schematics automation
               resource.
        :param str command_object_id: (optional) Job command object id
               (workspace-id, action-id).
        :param str command_name: (optional) Schematics job command name.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name, capsule-name or flow-name).
        :param List[str] command_options: (optional) Command line options for the
               command.
        :param List[VariableData] inputs: (optional) Job inputs used by Action.
        :param List[VariableData] settings: (optional) Environment variables used
               by the Job while performing Action.
        :param List[str] tags: (optional) User defined tags, while running the job.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param JobStatus status: (optional) Job Status.
        :param JobData data: (optional) Job data.
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param JobLogSummary log_summary: (optional) Job log summary record.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Job` object
        """

        if job_id is None:
            raise ValueError('job_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        if inputs is not None:
            inputs = [convert_model(x) for x in inputs]
        if settings is not None:
            settings = [convert_model(x) for x in settings]
        if status is not None:
            status = convert_model(status)
        if data is not None:
            data = convert_model(data)
        if bastion is not None:
            bastion = convert_model(bastion)
        if log_summary is not None:
            log_summary = convert_model(log_summary)
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='replace_job')
        headers.update(sdk_headers)

        data = {
            'command_object': command_object,
            'command_object_id': command_object_id,
            'command_name': command_name,
            'command_parameter': command_parameter,
            'command_options': command_options,
            'inputs': inputs,
            'settings': settings,
            'tags': tags,
            'location': location,
            'status': status,
            'data': data,
            'bastion': bastion,
            'log_summary': log_summary
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['job_id']
        path_param_values = self.encode_path_vars(job_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/jobs/{job_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def delete_job(self,
        job_id: str,
        refresh_token: str,
        *,
        force: bool = None,
        propagate: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Stop the running Job, and delete the Job-record.

        Stop the running Job, and delete the Job-record.

        :param str job_id: Job Id. Use GET /jobs API to look up the Job Ids in your
               IBM Cloud account.
        :param str refresh_token: The IAM refresh token associated with the IBM
               Cloud account.
        :param bool force: (optional) Equivalent to -force options in the command
               line.
        :param bool propagate: (optional) Auto propagate the chaange or deletion to
               the dependent resources.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if job_id is None:
            raise ValueError('job_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        headers = {
            'refresh_token': refresh_token,
            'force': force,
            'propagate': propagate
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_job')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        path_param_keys = ['job_id']
        path_param_values = self.encode_path_vars(job_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/jobs/{job_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def get_job(self,
        job_id: str,
        *,
        profile: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the Job record.

        Get the Job record.

        :param str job_id: Job Id. Use GET /jobs API to look up the Job Ids in your
               IBM Cloud account.
        :param str profile: (optional) Level of details returned by the get method.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Job` object
        """

        if job_id is None:
            raise ValueError('job_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_job')
        headers.update(sdk_headers)

        params = {
            'profile': profile
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['job_id']
        path_param_values = self.encode_path_vars(job_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/jobs/{job_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def list_job_logs(self,
        job_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get log-file from the Job record.

        Get log-file from the Job record.

        :param str job_id: Job Id. Use GET /jobs API to look up the Job Ids in your
               IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `JobLog` object
        """

        if job_id is None:
            raise ValueError('job_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_job_logs')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['job_id']
        path_param_values = self.encode_path_vars(job_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/jobs/{job_id}/logs'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response

    #########################
    # datasets
    #########################


    def list_shared_datasets(self,
        **kwargs
    ) -> DetailedResponse:
        """
        List all shared datasets.

        List all shared datasets.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `SharedDatasetResponseList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_shared_datasets')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/shared_datasets'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def create_shared_dataset(self,
        *,
        auto_propagate_change: bool = None,
        description: str = None,
        effected_workspace_ids: List[str] = None,
        resource_group: str = None,
        shared_dataset_data: List['SharedDatasetData'] = None,
        shared_dataset_name: str = None,
        shared_dataset_source_name: str = None,
        shared_dataset_type: List[str] = None,
        tags: List[str] = None,
        version: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create a shared dataset definition.

        Create a shared dataset definition.

        :param bool auto_propagate_change: (optional) Automatically propagate
               changes to consumers.
        :param str description: (optional) Dataset description.
        :param List[str] effected_workspace_ids: (optional) Affected workspaces.
        :param str resource_group: (optional) Resource group name.
        :param List[SharedDatasetData] shared_dataset_data: (optional) Shared
               dataset data.
        :param str shared_dataset_name: (optional) Shared dataset name.
        :param str shared_dataset_source_name: (optional) Shared dataset source
               name.
        :param List[str] shared_dataset_type: (optional) Shared dataset type.
        :param List[str] tags: (optional) Shared dataset tags.
        :param str version: (optional) Shared dataset version.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `SharedDatasetResponse` object
        """

        if shared_dataset_data is not None:
            shared_dataset_data = [convert_model(x) for x in shared_dataset_data]
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_shared_dataset')
        headers.update(sdk_headers)

        data = {
            'auto_propagate_change': auto_propagate_change,
            'description': description,
            'effected_workspace_ids': effected_workspace_ids,
            'resource_group': resource_group,
            'shared_dataset_data': shared_dataset_data,
            'shared_dataset_name': shared_dataset_name,
            'shared_dataset_source_name': shared_dataset_source_name,
            'shared_dataset_type': shared_dataset_type,
            'tags': tags,
            'version': version
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/shared_datasets'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def get_shared_dataset(self,
        sd_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the shared dataset.

        Get the shared dataset.

        :param str sd_id: The shared dataset ID Use the GET /shared_datasets to
               look up the shared dataset IDs  in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `SharedDatasetResponse` object
        """

        if sd_id is None:
            raise ValueError('sd_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_shared_dataset')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['sd_id']
        path_param_values = self.encode_path_vars(sd_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/shared_datasets/{sd_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def replace_shared_dataset(self,
        sd_id: str,
        *,
        auto_propagate_change: bool = None,
        description: str = None,
        effected_workspace_ids: List[str] = None,
        resource_group: str = None,
        shared_dataset_data: List['SharedDatasetData'] = None,
        shared_dataset_name: str = None,
        shared_dataset_source_name: str = None,
        shared_dataset_type: List[str] = None,
        tags: List[str] = None,
        version: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Replace the shared dataset.

        Replace the shared dataset.

        :param str sd_id: The shared dataset ID Use the GET /shared_datasets to
               look up the shared dataset IDs  in your IBM Cloud account.
        :param bool auto_propagate_change: (optional) Automatically propagate
               changes to consumers.
        :param str description: (optional) Dataset description.
        :param List[str] effected_workspace_ids: (optional) Affected workspaces.
        :param str resource_group: (optional) Resource group name.
        :param List[SharedDatasetData] shared_dataset_data: (optional) Shared
               dataset data.
        :param str shared_dataset_name: (optional) Shared dataset name.
        :param str shared_dataset_source_name: (optional) Shared dataset source
               name.
        :param List[str] shared_dataset_type: (optional) Shared dataset type.
        :param List[str] tags: (optional) Shared dataset tags.
        :param str version: (optional) Shared dataset version.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `SharedDatasetResponse` object
        """

        if sd_id is None:
            raise ValueError('sd_id must be provided')
        if shared_dataset_data is not None:
            shared_dataset_data = [convert_model(x) for x in shared_dataset_data]
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='replace_shared_dataset')
        headers.update(sdk_headers)

        data = {
            'auto_propagate_change': auto_propagate_change,
            'description': description,
            'effected_workspace_ids': effected_workspace_ids,
            'resource_group': resource_group,
            'shared_dataset_data': shared_dataset_data,
            'shared_dataset_name': shared_dataset_name,
            'shared_dataset_source_name': shared_dataset_source_name,
            'shared_dataset_type': shared_dataset_type,
            'tags': tags,
            'version': version
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['sd_id']
        path_param_values = self.encode_path_vars(sd_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/shared_datasets/{sd_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def delete_shared_dataset(self,
        sd_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete the shared dataset.

        Replace the shared dataset.

        :param str sd_id: The shared dataset ID Use the GET /shared_datasets to
               look up the shared dataset IDs  in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `SharedDatasetResponse` object
        """

        if sd_id is None:
            raise ValueError('sd_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_shared_dataset')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['sd_id']
        path_param_values = self.encode_path_vars(sd_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/shared_datasets/{sd_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response

    #########################
    # settings-kms
    #########################


    def get_kms_settings(self,
        location: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the KMS settings for customer account.

        Get the KMS settings for customer account.

        :param str location: The location of the Resource.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `KMSSettings` object
        """

        if location is None:
            raise ValueError('location must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_kms_settings')
        headers.update(sdk_headers)

        params = {
            'location': location
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/settings/kms'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def replace_kms_settings(self,
        *,
        location: str = None,
        encryption_scheme: str = None,
        resource_group: str = None,
        primary_crk: 'KMSSettingsPrimaryCrk' = None,
        secondary_crk: 'KMSSettingsSecondaryCrk' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Set the KMS settings for customer account.

        Set the KMS settings for customer account.

        :param str location: (optional) Location.
        :param str encryption_scheme: (optional) Encryption scheme.
        :param str resource_group: (optional) Resource group.
        :param KMSSettingsPrimaryCrk primary_crk: (optional) Primary CRK details.
        :param KMSSettingsSecondaryCrk secondary_crk: (optional) Secondary CRK
               details.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `KMSSettings` object
        """

        if primary_crk is not None:
            primary_crk = convert_model(primary_crk)
        if secondary_crk is not None:
            secondary_crk = convert_model(secondary_crk)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='replace_kms_settings')
        headers.update(sdk_headers)

        data = {
            'location': location,
            'encryption_scheme': encryption_scheme,
            'resource_group': resource_group,
            'primary_crk': primary_crk,
            'secondary_crk': secondary_crk
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/settings/kms'
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def get_discovered_kms_instances(self,
        encryption_scheme: str,
        location: str,
        *,
        resource_group: str = None,
        limit: int = None,
        sort: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Discover the KMS instances in the account.

        Discover the KMS instances in the account.

        :param str encryption_scheme: The encryption scheme to be used.
        :param str location: The location of the Resource.
        :param str resource_group: (optional) The resource group (by default, fetch
               from all resource groups).
        :param int limit: (optional) The numbers of items to return.
        :param str sort: (optional) Name of the field to sort-by;  Use the '.'
               character to delineate sub-resources and sub-fields (eg. owner.last_name).
               Prepend the field with '+' or '-', indicating 'ascending' or 'descending'
               (default is ascending)   Ignore unrecognized or unsupported sort field.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `KMSDiscovery` object
        """

        if encryption_scheme is None:
            raise ValueError('encryption_scheme must be provided')
        if location is None:
            raise ValueError('location must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_discovered_kms_instances')
        headers.update(sdk_headers)

        params = {
            'encryption_scheme': encryption_scheme,
            'location': location,
            'resource_group': resource_group,
            'limit': limit,
            'sort': sort
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/settings/kms_instances'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response

    #########################
    # settingsInventory
    #########################


    def create_inventory(self,
        *,
        name: str = None,
        description: str = None,
        location: str = None,
        resource_group: str = None,
        inventories_ini: str = None,
        resource_queries: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create a resource inventory definition, used to target Actions or Controls.

        Create a resource inventory definition.

        :param str name: (optional) Inventory name.
        :param str description: (optional) Inventory description.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Inventory
               definition.  By default, Action will be created in Default Resource Group.
        :param str inventories_ini: (optional) Input inventory of host and host
               group for the playbook,  in the .ini file format.
        :param List[str] resource_queries: (optional) Input resource queries that
               is used to dynamically generate  the inventory of host and host group for
               the playbook.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecord` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_inventory')
        headers.update(sdk_headers)

        data = {
            'name': name,
            'description': description,
            'location': location,
            'resource_group': resource_group,
            'inventories_ini': inventories_ini,
            'resource_queries': resource_queries
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/inventories'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def list_inventories(self,
        *,
        offset: int = None,
        limit: int = None,
        sort: str = None,
        profile: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all resource inventory definitions.

        Get all resource inventory definition.

        :param int offset: (optional) The number of items to skip before starting
               to collect the result set.
        :param int limit: (optional) The numbers of items to return.
        :param str sort: (optional) Name of the field to sort-by;  Use the '.'
               character to delineate sub-resources and sub-fields (eg. owner.last_name).
               Prepend the field with '+' or '-', indicating 'ascending' or 'descending'
               (default is ascending)   Ignore unrecognized or unsupported sort field.
        :param str profile: (optional) Level of details returned by the get method.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecordList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_inventories')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit,
            'sort': sort,
            'profile': profile
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/inventories'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def replace_inventory(self,
        inventory_id: str,
        *,
        name: str = None,
        description: str = None,
        location: str = None,
        resource_group: str = None,
        inventories_ini: str = None,
        resource_queries: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Replace the resource inventory definition, used to target Actions or Controls.

        Replace the resource inventory definition.

        :param str inventory_id: Resource Inventory Id.  Use GET /inventories API
               to look up the Resource Inventory definition Ids  in your IBM Cloud
               account.
        :param str name: (optional) Inventory name.
        :param str description: (optional) Inventory description.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Inventory
               definition.  By default, Action will be created in Default Resource Group.
        :param str inventories_ini: (optional) Input inventory of host and host
               group for the playbook,  in the .ini file format.
        :param List[str] resource_queries: (optional) Input resource queries that
               is used to dynamically generate  the inventory of host and host group for
               the playbook.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecord` object
        """

        if inventory_id is None:
            raise ValueError('inventory_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='replace_inventory')
        headers.update(sdk_headers)

        data = {
            'name': name,
            'description': description,
            'location': location,
            'resource_group': resource_group,
            'inventories_ini': inventories_ini,
            'resource_queries': resource_queries
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['inventory_id']
        path_param_values = self.encode_path_vars(inventory_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/inventories/{inventory_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def update_inventory(self,
        inventory_id: str,
        *,
        name: str = None,
        description: str = None,
        location: str = None,
        resource_group: str = None,
        inventories_ini: str = None,
        resource_queries: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update the resource inventory definition, used to target Actions or Controls.

        Update the resource inventory definition.

        :param str inventory_id: Resource Inventory Id.  Use GET /inventories API
               to look up the Resource Inventory definition Ids  in your IBM Cloud
               account.
        :param str name: (optional) Inventory name.
        :param str description: (optional) Inventory description.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Inventory
               definition.  By default, Action will be created in Default Resource Group.
        :param str inventories_ini: (optional) Input inventory of host and host
               group for the playbook,  in the .ini file format.
        :param List[str] resource_queries: (optional) Input resource queries that
               is used to dynamically generate  the inventory of host and host group for
               the playbook.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecord` object
        """

        if inventory_id is None:
            raise ValueError('inventory_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='update_inventory')
        headers.update(sdk_headers)

        data = {
            'name': name,
            'description': description,
            'location': location,
            'resource_group': resource_group,
            'inventories_ini': inventories_ini,
            'resource_queries': resource_queries
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['inventory_id']
        path_param_values = self.encode_path_vars(inventory_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/inventories/{inventory_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PATCH',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def delete_inventory(self,
        inventory_id: str,
        *,
        force: bool = None,
        propagate: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete the resource inventory definition.

        Delete the resource inventory definition.

        :param str inventory_id: Resource Inventory Id.  Use GET /inventories API
               to look up the Resource Inventory definition Ids  in your IBM Cloud
               account.
        :param bool force: (optional) Equivalent to -force options in the command
               line.
        :param bool propagate: (optional) Auto propagate the chaange or deletion to
               the dependent resources.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if inventory_id is None:
            raise ValueError('inventory_id must be provided')
        headers = {
            'force': force,
            'propagate': propagate
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_inventory')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        path_param_keys = ['inventory_id']
        path_param_values = self.encode_path_vars(inventory_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/inventories/{inventory_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def get_inventory(self,
        inventory_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the resource inventory definition, used to target Actions or Controls.

        Get the resource inventory definition.

        :param str inventory_id: Resource Inventory Id.  Use GET /inventories API
               to look up the Resource Inventory definition Ids  in your IBM Cloud
               account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecord` object
        """

        if inventory_id is None:
            raise ValueError('inventory_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_inventory')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['inventory_id']
        path_param_values = self.encode_path_vars(inventory_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/inventories/{inventory_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def list_inventory_values(self,
        inventory_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all the resource inventory values.

        Get all the resource inventory values.

        :param str inventory_id: Resource Inventory Id.  Use GET /inventories API
               to look up the Resource Inventory definition Ids  in your IBM Cloud
               account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecordList` object
        """

        if inventory_id is None:
            raise ValueError('inventory_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_inventory_values')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['inventory_id']
        path_param_values = self.encode_path_vars(inventory_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/inventories/{inventory_id}/variables'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def get_inventory_value(self,
        inventory_id: str,
        var_name: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the resource inventory value.

        Get the resource inventory value.

        :param str inventory_id: Resource Inventory Id.  Use GET /inventories API
               to look up the Resource Inventory definition Ids  in your IBM Cloud
               account.
        :param str var_name: Name of the variable.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecord` object
        """

        if inventory_id is None:
            raise ValueError('inventory_id must be provided')
        if var_name is None:
            raise ValueError('var_name must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_inventory_value')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['inventory_id', 'var_name']
        path_param_values = self.encode_path_vars(inventory_id, var_name)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/inventories/{inventory_id}/variables/{var_name}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response

    #########################
    # settingsResources
    #########################


    def create_resource_query(self,
        *,
        type: str = None,
        name: str = None,
        queries: List['ResourceQuery'] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create a resource query definition.

        Create a resource query definition.

        :param str type: (optional) Resource type (cluster, vsi, icd, vpc).
        :param str name: (optional) Resource query name.
        :param List[ResourceQuery] queries: (optional)
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ResourceQueryRecord` object
        """

        if queries is not None:
            queries = [convert_model(x) for x in queries]
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_resource_query')
        headers.update(sdk_headers)

        data = {
            'type': type,
            'name': name,
            'queries': queries
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/resources_query'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def list_resource_query(self,
        *,
        offset: int = None,
        limit: int = None,
        sort: str = None,
        profile: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all resource query definitions.

        Get all resource query definition.

        :param int offset: (optional) The number of items to skip before starting
               to collect the result set.
        :param int limit: (optional) The numbers of items to return.
        :param str sort: (optional) Name of the field to sort-by;  Use the '.'
               character to delineate sub-resources and sub-fields (eg. owner.last_name).
               Prepend the field with '+' or '-', indicating 'ascending' or 'descending'
               (default is ascending)   Ignore unrecognized or unsupported sort field.
        :param str profile: (optional) Level of details returned by the get method.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ResourceQueryRecordList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_resource_query')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit,
            'sort': sort,
            'profile': profile
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/resources_query'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def execute_resource_query(self,
        query_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Run the resource query.

        Execute a resource query definition.

        :param str query_id: Resource query Id.  Use GET /resource_query API to
               look up the Resource query definition Ids  in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ResourceQueryResponseRecord` object
        """

        if query_id is None:
            raise ValueError('query_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='execute_resource_query')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['query_id']
        path_param_values = self.encode_path_vars(query_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/resources_query/{query_id}'.format(**path_param_dict)
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def replace_resources_query(self,
        query_id: str,
        *,
        type: str = None,
        name: str = None,
        queries: List['ResourceQuery'] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Replace the resources query definition.

        Replace the resources query definition.

        :param str query_id: Resource query Id.  Use GET /resource_query API to
               look up the Resource query definition Ids  in your IBM Cloud account.
        :param str type: (optional) Resource type (cluster, vsi, icd, vpc).
        :param str name: (optional) Resource query name.
        :param List[ResourceQuery] queries: (optional)
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ResourceQueryRecord` object
        """

        if query_id is None:
            raise ValueError('query_id must be provided')
        if queries is not None:
            queries = [convert_model(x) for x in queries]
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='replace_resources_query')
        headers.update(sdk_headers)

        data = {
            'type': type,
            'name': name,
            'queries': queries
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['query_id']
        path_param_values = self.encode_path_vars(query_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/resources_query/{query_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def delete_resources_query(self,
        query_id: str,
        *,
        force: bool = None,
        propagate: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete the resources query definition.

        Delete the resources query definition.

        :param str query_id: Resource query Id.  Use GET /resource_query API to
               look up the Resource query definition Ids  in your IBM Cloud account.
        :param bool force: (optional) Equivalent to -force options in the command
               line.
        :param bool propagate: (optional) Auto propagate the chaange or deletion to
               the dependent resources.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if query_id is None:
            raise ValueError('query_id must be provided')
        headers = {
            'force': force,
            'propagate': propagate
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_resources_query')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        path_param_keys = ['query_id']
        path_param_values = self.encode_path_vars(query_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/resources_query/{query_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def get_resources_query(self,
        query_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the resources query definition.

        Get the resources query definition.

        :param str query_id: Resource query Id.  Use GET /resource_query API to
               look up the Resource query definition Ids  in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ResourceQueryRecord` object
        """

        if query_id is None:
            raise ValueError('query_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_resources_query')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['query_id']
        path_param_values = self.encode_path_vars(query_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/resources_query/{query_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


class GetWorkspaceReadmeEnums:
    """
    Enums for get_workspace_readme parameters.
    """

    class Formatted(str, Enum):
        """
        The format of the readme file.  Value ''markdown'' will give markdown, otherwise
        html.
        """
        MARKDOWN = 'markdown'
        HTML = 'html'


class ListActionsEnums:
    """
    Enums for list_actions parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        IDS = 'ids'
        SUMMARY = 'summary'


class GetActionEnums:
    """
    Enums for get_action parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        SUMMARY = 'summary'
        DETAILED = 'detailed'


class ListJobsEnums:
    """
    Enums for list_jobs parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        IDS = 'ids'
        SUMMARY = 'summary'
    class Resource(str, Enum):
        """
        Name of the resource (workspace, actions or controls).
        """
        WORKSPACE = 'workspace'
        ACTION = 'action'
    class List(str, Enum):
        """
        list jobs.
        """
        ALL = 'all'


class GetJobEnums:
    """
    Enums for get_job parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        SUMMARY = 'summary'
        DETAILED = 'detailed'


class ListInventoriesEnums:
    """
    Enums for list_inventories parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        IDS = 'ids'
        SUMMARY = 'summary'


class ListResourceQueryEnums:
    """
    Enums for list_resource_query parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        IDS = 'ids'
        SUMMARY = 'summary'


##############################################################################
# Models
##############################################################################


class Action():
    """
    Complete Action details with user inputs and system generated data.

    :attr str name: (optional) Action name (unique for an account).
    :attr str description: (optional) Action description.
    :attr str location: (optional) List of workspace locations supported by IBM
          Cloud Schematics service.  Note, this does not limit the location of the
          resources provisioned using Schematics.
    :attr str resource_group: (optional) Resource-group name for the Action.  By
          default, Action will be created in Default Resource Group.
    :attr List[str] tags: (optional) Action tags.
    :attr UserState user_state: (optional) User defined status of the Schematics
          object.
    :attr str source_readme_url: (optional) URL of the README file, for the source.
    :attr ExternalSource source: (optional) Source of templates, playbooks, or
          controls.
    :attr str source_type: (optional) Type of source for the Template.
    :attr str command_parameter: (optional) Schematics job command parameter
          (playbook-name).
    :attr BastionResourceDefinition bastion: (optional) Describes a bastion
          resource.
    :attr str inventory: (optional) Inventory ID.
    :attr VariableData bastion_credential: (optional) User editable variable data &
          system generated reference to value.
    :attr List[VariableData] credentials: (optional) credentials of the Action.
    :attr List[VariableData] inputs: (optional) Input variables for the Action.
    :attr List[VariableData] outputs: (optional) Output variables for the Action.
    :attr List[VariableData] settings: (optional) Environment variables for the
          Action.
    :attr str id: (optional) Action Id.
    :attr str crn: (optional) Action Cloud Resource Name.
    :attr str account: (optional) Action account id.
    :attr datetime source_created_at: (optional) Action Playbook Source creation
          time.
    :attr str source_created_by: (optional) Email address of user who created the
          Action Playbook Source.
    :attr datetime source_updated_at: (optional) Action Playbook updation time.
    :attr str source_updated_by: (optional) Email address of user who updated the
          Action Playbook Source.
    :attr datetime created_at: (optional) Action creation time.
    :attr str created_by: (optional) Email address of user who created the action.
    :attr datetime updated_at: (optional) Action updation time.
    :attr str updated_by: (optional) Email address of user who updated the action.
    :attr ActionState state: (optional) Computed state of the Action.
    :attr List[str] playbook_names: (optional) Playbook names retrieved from repo.
    :attr SystemLock sys_lock: (optional) System lock status.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 description: str = None,
                 location: str = None,
                 resource_group: str = None,
                 tags: List[str] = None,
                 user_state: 'UserState' = None,
                 source_readme_url: str = None,
                 source: 'ExternalSource' = None,
                 source_type: str = None,
                 command_parameter: str = None,
                 bastion: 'BastionResourceDefinition' = None,
                 inventory: str = None,
                 bastion_credential: 'VariableData' = None,
                 credentials: List['VariableData'] = None,
                 inputs: List['VariableData'] = None,
                 outputs: List['VariableData'] = None,
                 settings: List['VariableData'] = None,
                 id: str = None,
                 crn: str = None,
                 account: str = None,
                 source_created_at: datetime = None,
                 source_created_by: str = None,
                 source_updated_at: datetime = None,
                 source_updated_by: str = None,
                 created_at: datetime = None,
                 created_by: str = None,
                 updated_at: datetime = None,
                 updated_by: str = None,
                 state: 'ActionState' = None,
                 playbook_names: List[str] = None,
                 sys_lock: 'SystemLock' = None) -> None:
        """
        Initialize a Action object.

        :param str name: (optional) Action name (unique for an account).
        :param str description: (optional) Action description.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Action.
               By default, Action will be created in Default Resource Group.
        :param List[str] tags: (optional) Action tags.
        :param UserState user_state: (optional) User defined status of the
               Schematics object.
        :param str source_readme_url: (optional) URL of the README file, for the
               source.
        :param ExternalSource source: (optional) Source of templates, playbooks, or
               controls.
        :param str source_type: (optional) Type of source for the Template.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name).
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param str inventory: (optional) Inventory ID.
        :param VariableData bastion_credential: (optional) User editable variable
               data & system generated reference to value.
        :param List[VariableData] credentials: (optional) credentials of the
               Action.
        :param List[VariableData] inputs: (optional) Input variables for the
               Action.
        :param List[VariableData] outputs: (optional) Output variables for the
               Action.
        :param List[VariableData] settings: (optional) Environment variables for
               the Action.
        :param ActionState state: (optional) Computed state of the Action.
        :param SystemLock sys_lock: (optional) System lock status.
        """
        self.name = name
        self.description = description
        self.location = location
        self.resource_group = resource_group
        self.tags = tags
        self.user_state = user_state
        self.source_readme_url = source_readme_url
        self.source = source
        self.source_type = source_type
        self.command_parameter = command_parameter
        self.bastion = bastion
        self.inventory = inventory
        self.bastion_credential = bastion_credential
        self.credentials = credentials
        self.inputs = inputs
        self.outputs = outputs
        self.settings = settings
        self.id = id
        self.crn = crn
        self.account = account
        self.source_created_at = source_created_at
        self.source_created_by = source_created_by
        self.source_updated_at = source_updated_at
        self.source_updated_by = source_updated_by
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.state = state
        self.playbook_names = playbook_names
        self.sys_lock = sys_lock

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Action':
        """Initialize a Action object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'user_state' in _dict:
            args['user_state'] = UserState.from_dict(_dict.get('user_state'))
        if 'source_readme_url' in _dict:
            args['source_readme_url'] = _dict.get('source_readme_url')
        if 'source' in _dict:
            args['source'] = ExternalSource.from_dict(_dict.get('source'))
        if 'source_type' in _dict:
            args['source_type'] = _dict.get('source_type')
        if 'command_parameter' in _dict:
            args['command_parameter'] = _dict.get('command_parameter')
        if 'bastion' in _dict:
            args['bastion'] = BastionResourceDefinition.from_dict(_dict.get('bastion'))
        if 'inventory' in _dict:
            args['inventory'] = _dict.get('inventory')
        if 'bastion_credential' in _dict:
            args['bastion_credential'] = VariableData.from_dict(_dict.get('bastion_credential'))
        if 'credentials' in _dict:
            args['credentials'] = [VariableData.from_dict(x) for x in _dict.get('credentials')]
        if 'inputs' in _dict:
            args['inputs'] = [VariableData.from_dict(x) for x in _dict.get('inputs')]
        if 'outputs' in _dict:
            args['outputs'] = [VariableData.from_dict(x) for x in _dict.get('outputs')]
        if 'settings' in _dict:
            args['settings'] = [VariableData.from_dict(x) for x in _dict.get('settings')]
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'crn' in _dict:
            args['crn'] = _dict.get('crn')
        if 'account' in _dict:
            args['account'] = _dict.get('account')
        if 'source_created_at' in _dict:
            args['source_created_at'] = string_to_datetime(_dict.get('source_created_at'))
        if 'source_created_by' in _dict:
            args['source_created_by'] = _dict.get('source_created_by')
        if 'source_updated_at' in _dict:
            args['source_updated_at'] = string_to_datetime(_dict.get('source_updated_at'))
        if 'source_updated_by' in _dict:
            args['source_updated_by'] = _dict.get('source_updated_by')
        if 'created_at' in _dict:
            args['created_at'] = string_to_datetime(_dict.get('created_at'))
        if 'created_by' in _dict:
            args['created_by'] = _dict.get('created_by')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'updated_by' in _dict:
            args['updated_by'] = _dict.get('updated_by')
        if 'state' in _dict:
            args['state'] = ActionState.from_dict(_dict.get('state'))
        if 'playbook_names' in _dict:
            args['playbook_names'] = _dict.get('playbook_names')
        if 'sys_lock' in _dict:
            args['sys_lock'] = SystemLock.from_dict(_dict.get('sys_lock'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Action object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'user_state') and self.user_state is not None:
            _dict['user_state'] = self.user_state.to_dict()
        if hasattr(self, 'source_readme_url') and self.source_readme_url is not None:
            _dict['source_readme_url'] = self.source_readme_url
        if hasattr(self, 'source') and self.source is not None:
            _dict['source'] = self.source.to_dict()
        if hasattr(self, 'source_type') and self.source_type is not None:
            _dict['source_type'] = self.source_type
        if hasattr(self, 'command_parameter') and self.command_parameter is not None:
            _dict['command_parameter'] = self.command_parameter
        if hasattr(self, 'bastion') and self.bastion is not None:
            _dict['bastion'] = self.bastion.to_dict()
        if hasattr(self, 'inventory') and self.inventory is not None:
            _dict['inventory'] = self.inventory
        if hasattr(self, 'bastion_credential') and self.bastion_credential is not None:
            _dict['bastion_credential'] = self.bastion_credential.to_dict()
        if hasattr(self, 'credentials') and self.credentials is not None:
            _dict['credentials'] = [x.to_dict() for x in self.credentials]
        if hasattr(self, 'inputs') and self.inputs is not None:
            _dict['inputs'] = [x.to_dict() for x in self.inputs]
        if hasattr(self, 'outputs') and self.outputs is not None:
            _dict['outputs'] = [x.to_dict() for x in self.outputs]
        if hasattr(self, 'settings') and self.settings is not None:
            _dict['settings'] = [x.to_dict() for x in self.settings]
        if hasattr(self, 'id') and getattr(self, 'id') is not None:
            _dict['id'] = getattr(self, 'id')
        if hasattr(self, 'crn') and getattr(self, 'crn') is not None:
            _dict['crn'] = getattr(self, 'crn')
        if hasattr(self, 'account') and getattr(self, 'account') is not None:
            _dict['account'] = getattr(self, 'account')
        if hasattr(self, 'source_created_at') and getattr(self, 'source_created_at') is not None:
            _dict['source_created_at'] = datetime_to_string(getattr(self, 'source_created_at'))
        if hasattr(self, 'source_created_by') and getattr(self, 'source_created_by') is not None:
            _dict['source_created_by'] = getattr(self, 'source_created_by')
        if hasattr(self, 'source_updated_at') and getattr(self, 'source_updated_at') is not None:
            _dict['source_updated_at'] = datetime_to_string(getattr(self, 'source_updated_at'))
        if hasattr(self, 'source_updated_by') and getattr(self, 'source_updated_by') is not None:
            _dict['source_updated_by'] = getattr(self, 'source_updated_by')
        if hasattr(self, 'created_at') and getattr(self, 'created_at') is not None:
            _dict['created_at'] = datetime_to_string(getattr(self, 'created_at'))
        if hasattr(self, 'created_by') and getattr(self, 'created_by') is not None:
            _dict['created_by'] = getattr(self, 'created_by')
        if hasattr(self, 'updated_at') and getattr(self, 'updated_at') is not None:
            _dict['updated_at'] = datetime_to_string(getattr(self, 'updated_at'))
        if hasattr(self, 'updated_by') and getattr(self, 'updated_by') is not None:
            _dict['updated_by'] = getattr(self, 'updated_by')
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state.to_dict()
        if hasattr(self, 'playbook_names') and getattr(self, 'playbook_names') is not None:
            _dict['playbook_names'] = getattr(self, 'playbook_names')
        if hasattr(self, 'sys_lock') and self.sys_lock is not None:
            _dict['sys_lock'] = self.sys_lock.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Action object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Action') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Action') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class LocationEnum(str, Enum):
        """
        List of workspace locations supported by IBM Cloud Schematics service.  Note, this
        does not limit the location of the resources provisioned using Schematics.
        """
        US_SOUTH = 'us-south'
        US_EAST = 'us-east'
        EU_GB = 'eu-gb'
        EU_DE = 'eu-de'


    class SourceTypeEnum(str, Enum):
        """
        Type of source for the Template.
        """
        LOCAL = 'local'
        GIT_HUB = 'git_hub'
        GIT_HUB_ENTERPRISE = 'git_hub_enterprise'
        GIT_LAB = 'git_lab'
        IBM_GIT_LAB = 'ibm_git_lab'
        IBM_CLOUD_CATALOG = 'ibm_cloud_catalog'
        EXTERNAL_SCM = 'external_scm'


class ActionList():
    """
    List of Action definition response.

    :attr int total_count: (optional) Total number of records.
    :attr int limit: Number of records returned.
    :attr int offset: Skipped number of records.
    :attr List[ActionLite] actions: (optional) List of action records.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 total_count: int = None,
                 actions: List['ActionLite'] = None) -> None:
        """
        Initialize a ActionList object.

        :param int limit: Number of records returned.
        :param int offset: Skipped number of records.
        :param int total_count: (optional) Total number of records.
        :param List[ActionLite] actions: (optional) List of action records.
        """
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.actions = actions

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionList':
        """Initialize a ActionList object from a json dictionary."""
        args = {}
        if 'total_count' in _dict:
            args['total_count'] = _dict.get('total_count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in ActionList JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in ActionList JSON')
        if 'actions' in _dict:
            args['actions'] = [ActionLite.from_dict(x) for x in _dict.get('actions')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'total_count') and self.total_count is not None:
            _dict['total_count'] = self.total_count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'actions') and self.actions is not None:
            _dict['actions'] = [x.to_dict() for x in self.actions]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ActionLite():
    """
    Action summary profile with user inputs and system generated data.

    :attr str name: (optional) Action name (unique for an account).
    :attr str description: (optional) Action description.
    :attr str id: (optional) Action Id.
    :attr str crn: (optional) Action Cloud Resource Name.
    :attr str location: (optional) List of workspace locations supported by IBM
          Cloud Schematics service.  Note, this does not limit the location of the
          resources provisioned using Schematics.
    :attr str resource_group: (optional) Resource-group name for the Action.  By
          default, Action will be created in Default Resource Group.
    :attr str namespace: (optional) name of the namespace.
    :attr List[str] tags: (optional) Action tags.
    :attr str playbook_name: (optional) Name of the selected playbook.
    :attr UserState user_state: (optional) User defined status of the Schematics
          object.
    :attr ActionLiteState state: (optional) Computed state of the Action.
    :attr SystemLock sys_lock: (optional) System lock status.
    :attr datetime created_at: (optional) Action creation time.
    :attr str created_by: (optional) Email address of user who created the action.
    :attr datetime updated_at: (optional) Action updation time.
    :attr str updated_by: (optional) Email address of user who updated the action.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 description: str = None,
                 id: str = None,
                 crn: str = None,
                 location: str = None,
                 resource_group: str = None,
                 namespace: str = None,
                 tags: List[str] = None,
                 playbook_name: str = None,
                 user_state: 'UserState' = None,
                 state: 'ActionLiteState' = None,
                 sys_lock: 'SystemLock' = None,
                 created_at: datetime = None,
                 created_by: str = None,
                 updated_at: datetime = None,
                 updated_by: str = None) -> None:
        """
        Initialize a ActionLite object.

        :param str name: (optional) Action name (unique for an account).
        :param str description: (optional) Action description.
        :param str id: (optional) Action Id.
        :param str crn: (optional) Action Cloud Resource Name.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Action.
               By default, Action will be created in Default Resource Group.
        :param str namespace: (optional) name of the namespace.
        :param List[str] tags: (optional) Action tags.
        :param str playbook_name: (optional) Name of the selected playbook.
        :param UserState user_state: (optional) User defined status of the
               Schematics object.
        :param ActionLiteState state: (optional) Computed state of the Action.
        :param SystemLock sys_lock: (optional) System lock status.
        :param datetime created_at: (optional) Action creation time.
        :param str created_by: (optional) Email address of user who created the
               action.
        :param datetime updated_at: (optional) Action updation time.
        :param str updated_by: (optional) Email address of user who updated the
               action.
        """
        self.name = name
        self.description = description
        self.id = id
        self.crn = crn
        self.location = location
        self.resource_group = resource_group
        self.namespace = namespace
        self.tags = tags
        self.playbook_name = playbook_name
        self.user_state = user_state
        self.state = state
        self.sys_lock = sys_lock
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionLite':
        """Initialize a ActionLite object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'crn' in _dict:
            args['crn'] = _dict.get('crn')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'namespace' in _dict:
            args['namespace'] = _dict.get('namespace')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'playbook_name' in _dict:
            args['playbook_name'] = _dict.get('playbook_name')
        if 'user_state' in _dict:
            args['user_state'] = UserState.from_dict(_dict.get('user_state'))
        if 'state' in _dict:
            args['state'] = ActionLiteState.from_dict(_dict.get('state'))
        if 'sys_lock' in _dict:
            args['sys_lock'] = SystemLock.from_dict(_dict.get('sys_lock'))
        if 'created_at' in _dict:
            args['created_at'] = string_to_datetime(_dict.get('created_at'))
        if 'created_by' in _dict:
            args['created_by'] = _dict.get('created_by')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'updated_by' in _dict:
            args['updated_by'] = _dict.get('updated_by')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionLite object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'crn') and self.crn is not None:
            _dict['crn'] = self.crn
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'namespace') and self.namespace is not None:
            _dict['namespace'] = self.namespace
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'playbook_name') and self.playbook_name is not None:
            _dict['playbook_name'] = self.playbook_name
        if hasattr(self, 'user_state') and self.user_state is not None:
            _dict['user_state'] = self.user_state.to_dict()
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state.to_dict()
        if hasattr(self, 'sys_lock') and self.sys_lock is not None:
            _dict['sys_lock'] = self.sys_lock.to_dict()
        if hasattr(self, 'created_at') and self.created_at is not None:
            _dict['created_at'] = datetime_to_string(self.created_at)
        if hasattr(self, 'created_by') and self.created_by is not None:
            _dict['created_by'] = self.created_by
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        if hasattr(self, 'updated_by') and self.updated_by is not None:
            _dict['updated_by'] = self.updated_by
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionLite object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionLite') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionLite') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class LocationEnum(str, Enum):
        """
        List of workspace locations supported by IBM Cloud Schematics service.  Note, this
        does not limit the location of the resources provisioned using Schematics.
        """
        US_SOUTH = 'us-south'
        US_EAST = 'us-east'
        EU_GB = 'eu-gb'
        EU_DE = 'eu-de'


class ActionLiteState():
    """
    Computed state of the Action.

    :attr str status_code: (optional) Status of automation (workspace or action).
    :attr str status_message: (optional) Automation status message - to be displayed
          along with the status_code.
    """

    def __init__(self,
                 *,
                 status_code: str = None,
                 status_message: str = None) -> None:
        """
        Initialize a ActionLiteState object.

        :param str status_code: (optional) Status of automation (workspace or
               action).
        :param str status_message: (optional) Automation status message - to be
               displayed along with the status_code.
        """
        self.status_code = status_code
        self.status_message = status_message

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionLiteState':
        """Initialize a ActionLiteState object from a json dictionary."""
        args = {}
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionLiteState object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionLiteState object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionLiteState') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionLiteState') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of automation (workspace or action).
        """
        NORMAL = 'normal'
        PENDING = 'pending'
        DISABLED = 'disabled'
        CRITICAL = 'critical'


class ActionState():
    """
    Computed state of the Action.

    :attr str status_code: (optional) Status of automation (workspace or action).
    :attr str status_job_id: (optional) Job id reference for this status.
    :attr str status_message: (optional) Automation status message - to be displayed
          along with the status_code.
    """

    def __init__(self,
                 *,
                 status_code: str = None,
                 status_job_id: str = None,
                 status_message: str = None) -> None:
        """
        Initialize a ActionState object.

        :param str status_code: (optional) Status of automation (workspace or
               action).
        :param str status_job_id: (optional) Job id reference for this status.
        :param str status_message: (optional) Automation status message - to be
               displayed along with the status_code.
        """
        self.status_code = status_code
        self.status_job_id = status_job_id
        self.status_message = status_message

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionState':
        """Initialize a ActionState object from a json dictionary."""
        args = {}
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_job_id' in _dict:
            args['status_job_id'] = _dict.get('status_job_id')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionState object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_job_id') and self.status_job_id is not None:
            _dict['status_job_id'] = self.status_job_id
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionState object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionState') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionState') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of automation (workspace or action).
        """
        NORMAL = 'normal'
        PENDING = 'pending'
        DISABLED = 'disabled'
        CRITICAL = 'critical'


class BastionResourceDefinition():
    """
    Describes a bastion resource.

    :attr str name: (optional) Bastion Name(Unique).
    :attr str host: (optional) Reference to the Inventory resource definition.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 host: str = None) -> None:
        """
        Initialize a BastionResourceDefinition object.

        :param str name: (optional) Bastion Name(Unique).
        :param str host: (optional) Reference to the Inventory resource definition.
        """
        self.name = name
        self.host = host

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'BastionResourceDefinition':
        """Initialize a BastionResourceDefinition object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'host' in _dict:
            args['host'] = _dict.get('host')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a BastionResourceDefinition object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'host') and self.host is not None:
            _dict['host'] = self.host
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this BastionResourceDefinition object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'BastionResourceDefinition') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'BastionResourceDefinition') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CatalogRef():
    """
    CatalogRef -.

    :attr bool dry_run: (optional) Dry run.
    :attr str item_icon_url: (optional) Catalog item icon url.
    :attr str item_id: (optional) Catalog item id.
    :attr str item_name: (optional) Catalog item name.
    :attr str item_readme_url: (optional) Catalog item readme url.
    :attr str item_url: (optional) Catalog item url.
    :attr str launch_url: (optional) Catalog item launch url.
    :attr str offering_version: (optional) Catalog item offering version.
    """

    def __init__(self,
                 *,
                 dry_run: bool = None,
                 item_icon_url: str = None,
                 item_id: str = None,
                 item_name: str = None,
                 item_readme_url: str = None,
                 item_url: str = None,
                 launch_url: str = None,
                 offering_version: str = None) -> None:
        """
        Initialize a CatalogRef object.

        :param bool dry_run: (optional) Dry run.
        :param str item_icon_url: (optional) Catalog item icon url.
        :param str item_id: (optional) Catalog item id.
        :param str item_name: (optional) Catalog item name.
        :param str item_readme_url: (optional) Catalog item readme url.
        :param str item_url: (optional) Catalog item url.
        :param str launch_url: (optional) Catalog item launch url.
        :param str offering_version: (optional) Catalog item offering version.
        """
        self.dry_run = dry_run
        self.item_icon_url = item_icon_url
        self.item_id = item_id
        self.item_name = item_name
        self.item_readme_url = item_readme_url
        self.item_url = item_url
        self.launch_url = launch_url
        self.offering_version = offering_version

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CatalogRef':
        """Initialize a CatalogRef object from a json dictionary."""
        args = {}
        if 'dry_run' in _dict:
            args['dry_run'] = _dict.get('dry_run')
        if 'item_icon_url' in _dict:
            args['item_icon_url'] = _dict.get('item_icon_url')
        if 'item_id' in _dict:
            args['item_id'] = _dict.get('item_id')
        if 'item_name' in _dict:
            args['item_name'] = _dict.get('item_name')
        if 'item_readme_url' in _dict:
            args['item_readme_url'] = _dict.get('item_readme_url')
        if 'item_url' in _dict:
            args['item_url'] = _dict.get('item_url')
        if 'launch_url' in _dict:
            args['launch_url'] = _dict.get('launch_url')
        if 'offering_version' in _dict:
            args['offering_version'] = _dict.get('offering_version')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CatalogRef object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'dry_run') and self.dry_run is not None:
            _dict['dry_run'] = self.dry_run
        if hasattr(self, 'item_icon_url') and self.item_icon_url is not None:
            _dict['item_icon_url'] = self.item_icon_url
        if hasattr(self, 'item_id') and self.item_id is not None:
            _dict['item_id'] = self.item_id
        if hasattr(self, 'item_name') and self.item_name is not None:
            _dict['item_name'] = self.item_name
        if hasattr(self, 'item_readme_url') and self.item_readme_url is not None:
            _dict['item_readme_url'] = self.item_readme_url
        if hasattr(self, 'item_url') and self.item_url is not None:
            _dict['item_url'] = self.item_url
        if hasattr(self, 'launch_url') and self.launch_url is not None:
            _dict['launch_url'] = self.launch_url
        if hasattr(self, 'offering_version') and self.offering_version is not None:
            _dict['offering_version'] = self.offering_version
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CatalogRef object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CatalogRef') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CatalogRef') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class EnvVariableResponse():
    """
    EnvVariableResponse -.

    :attr bool hidden: (optional) Env variable is hidden.
    :attr str name: (optional) Env variable name.
    :attr bool secure: (optional) Env variable is secure.
    :attr str value: (optional) Value for env variable.
    """

    def __init__(self,
                 *,
                 hidden: bool = None,
                 name: str = None,
                 secure: bool = None,
                 value: str = None) -> None:
        """
        Initialize a EnvVariableResponse object.

        :param bool hidden: (optional) Env variable is hidden.
        :param str name: (optional) Env variable name.
        :param bool secure: (optional) Env variable is secure.
        :param str value: (optional) Value for env variable.
        """
        self.hidden = hidden
        self.name = name
        self.secure = secure
        self.value = value

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'EnvVariableResponse':
        """Initialize a EnvVariableResponse object from a json dictionary."""
        args = {}
        if 'hidden' in _dict:
            args['hidden'] = _dict.get('hidden')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'secure' in _dict:
            args['secure'] = _dict.get('secure')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a EnvVariableResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'hidden') and self.hidden is not None:
            _dict['hidden'] = self.hidden
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'secure') and self.secure is not None:
            _dict['secure'] = self.secure
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this EnvVariableResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'EnvVariableResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'EnvVariableResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ExternalSource():
    """
    Source of templates, playbooks, or controls.

    :attr str source_type: Type of source for the Template.
    :attr ExternalSourceGit git: (optional) Connection details to Git source.
    """

    def __init__(self,
                 source_type: str,
                 *,
                 git: 'ExternalSourceGit' = None) -> None:
        """
        Initialize a ExternalSource object.

        :param str source_type: Type of source for the Template.
        :param ExternalSourceGit git: (optional) Connection details to Git source.
        """
        self.source_type = source_type
        self.git = git

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ExternalSource':
        """Initialize a ExternalSource object from a json dictionary."""
        args = {}
        if 'source_type' in _dict:
            args['source_type'] = _dict.get('source_type')
        else:
            raise ValueError('Required property \'source_type\' not present in ExternalSource JSON')
        if 'git' in _dict:
            args['git'] = ExternalSourceGit.from_dict(_dict.get('git'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ExternalSource object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'source_type') and self.source_type is not None:
            _dict['source_type'] = self.source_type
        if hasattr(self, 'git') and self.git is not None:
            _dict['git'] = self.git.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ExternalSource object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ExternalSource') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ExternalSource') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class SourceTypeEnum(str, Enum):
        """
        Type of source for the Template.
        """
        LOCAL = 'local'
        GIT_HUB = 'git_hub'
        GIT_HUB_ENTERPRISE = 'git_hub_enterprise'
        GIT_LAB = 'git_lab'
        IBM_GIT_LAB = 'ibm_git_lab'
        IBM_CLOUD_CATALOG = 'ibm_cloud_catalog'
        EXTERNAL_SCM = 'external_scm'


class ExternalSourceGit():
    """
    Connection details to Git source.

    :attr str git_repo_url: (optional) URL to the GIT Repo that can be used to clone
          the template.
    :attr str git_token: (optional) Personal Access Token to connect to Git URLs.
    :attr str git_repo_folder: (optional) Name of the folder in the Git Repo, that
          contains the template.
    :attr str git_release: (optional) Name of the release tag, used to fetch the Git
          Repo.
    :attr str git_branch: (optional) Name of the branch, used to fetch the Git Repo.
    """

    def __init__(self,
                 *,
                 git_repo_url: str = None,
                 git_token: str = None,
                 git_repo_folder: str = None,
                 git_release: str = None,
                 git_branch: str = None) -> None:
        """
        Initialize a ExternalSourceGit object.

        :param str git_repo_url: (optional) URL to the GIT Repo that can be used to
               clone the template.
        :param str git_token: (optional) Personal Access Token to connect to Git
               URLs.
        :param str git_repo_folder: (optional) Name of the folder in the Git Repo,
               that contains the template.
        :param str git_release: (optional) Name of the release tag, used to fetch
               the Git Repo.
        :param str git_branch: (optional) Name of the branch, used to fetch the Git
               Repo.
        """
        self.git_repo_url = git_repo_url
        self.git_token = git_token
        self.git_repo_folder = git_repo_folder
        self.git_release = git_release
        self.git_branch = git_branch

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ExternalSourceGit':
        """Initialize a ExternalSourceGit object from a json dictionary."""
        args = {}
        if 'git_repo_url' in _dict:
            args['git_repo_url'] = _dict.get('git_repo_url')
        if 'git_token' in _dict:
            args['git_token'] = _dict.get('git_token')
        if 'git_repo_folder' in _dict:
            args['git_repo_folder'] = _dict.get('git_repo_folder')
        if 'git_release' in _dict:
            args['git_release'] = _dict.get('git_release')
        if 'git_branch' in _dict:
            args['git_branch'] = _dict.get('git_branch')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ExternalSourceGit object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'git_repo_url') and self.git_repo_url is not None:
            _dict['git_repo_url'] = self.git_repo_url
        if hasattr(self, 'git_token') and self.git_token is not None:
            _dict['git_token'] = self.git_token
        if hasattr(self, 'git_repo_folder') and self.git_repo_folder is not None:
            _dict['git_repo_folder'] = self.git_repo_folder
        if hasattr(self, 'git_release') and self.git_release is not None:
            _dict['git_release'] = self.git_release
        if hasattr(self, 'git_branch') and self.git_branch is not None:
            _dict['git_branch'] = self.git_branch
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ExternalSourceGit object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ExternalSourceGit') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ExternalSourceGit') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class InventoryResourceRecord():
    """
    Complete inventory resource details with user inputs and system generated data.

    :attr str name: (optional) Inventory name.
    :attr str id: (optional) Inventory id.
    :attr str description: (optional) Inventory description.
    :attr str location: (optional) List of workspace locations supported by IBM
          Cloud Schematics service.  Note, this does not limit the location of the
          resources provisioned using Schematics.
    :attr str resource_group: (optional) Resource-group name for the Inventory
          definition.  By default, Action will be created in Default Resource Group.
    :attr datetime created_at: (optional) Inventory creation time.
    :attr str created_by: (optional) Email address of user who created the
          Inventory.
    :attr datetime updated_at: (optional) Inventory updation time.
    :attr str updated_by: (optional) Email address of user who updated the
          Inventory.
    :attr str inventories_ini: (optional) Input inventory of host and host group for
          the playbook,  in the .ini file format.
    :attr List[str] resource_queries: (optional) Input resource queries that is used
          to dynamically generate  the inventory of host and host group for the playbook.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 id: str = None,
                 description: str = None,
                 location: str = None,
                 resource_group: str = None,
                 created_at: datetime = None,
                 created_by: str = None,
                 updated_at: datetime = None,
                 updated_by: str = None,
                 inventories_ini: str = None,
                 resource_queries: List[str] = None) -> None:
        """
        Initialize a InventoryResourceRecord object.

        :param str name: (optional) Inventory name.
        :param str description: (optional) Inventory description.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Inventory
               definition.  By default, Action will be created in Default Resource Group.
        :param str inventories_ini: (optional) Input inventory of host and host
               group for the playbook,  in the .ini file format.
        :param List[str] resource_queries: (optional) Input resource queries that
               is used to dynamically generate  the inventory of host and host group for
               the playbook.
        """
        self.name = name
        self.id = id
        self.description = description
        self.location = location
        self.resource_group = resource_group
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.inventories_ini = inventories_ini
        self.resource_queries = resource_queries

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'InventoryResourceRecord':
        """Initialize a InventoryResourceRecord object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'created_at' in _dict:
            args['created_at'] = string_to_datetime(_dict.get('created_at'))
        if 'created_by' in _dict:
            args['created_by'] = _dict.get('created_by')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'updated_by' in _dict:
            args['updated_by'] = _dict.get('updated_by')
        if 'inventories_ini' in _dict:
            args['inventories_ini'] = _dict.get('inventories_ini')
        if 'resource_queries' in _dict:
            args['resource_queries'] = _dict.get('resource_queries')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a InventoryResourceRecord object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'id') and getattr(self, 'id') is not None:
            _dict['id'] = getattr(self, 'id')
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'created_at') and getattr(self, 'created_at') is not None:
            _dict['created_at'] = datetime_to_string(getattr(self, 'created_at'))
        if hasattr(self, 'created_by') and getattr(self, 'created_by') is not None:
            _dict['created_by'] = getattr(self, 'created_by')
        if hasattr(self, 'updated_at') and getattr(self, 'updated_at') is not None:
            _dict['updated_at'] = datetime_to_string(getattr(self, 'updated_at'))
        if hasattr(self, 'updated_by') and getattr(self, 'updated_by') is not None:
            _dict['updated_by'] = getattr(self, 'updated_by')
        if hasattr(self, 'inventories_ini') and self.inventories_ini is not None:
            _dict['inventories_ini'] = self.inventories_ini
        if hasattr(self, 'resource_queries') and self.resource_queries is not None:
            _dict['resource_queries'] = self.resource_queries
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this InventoryResourceRecord object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'InventoryResourceRecord') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'InventoryResourceRecord') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class LocationEnum(str, Enum):
        """
        List of workspace locations supported by IBM Cloud Schematics service.  Note, this
        does not limit the location of the resources provisioned using Schematics.
        """
        US_SOUTH = 'us-south'
        US_EAST = 'us-east'
        EU_GB = 'eu-gb'
        EU_DE = 'eu-de'


class InventoryResourceRecordList():
    """
    List of Inventory resource records.

    :attr int total_count: (optional) Total number of records.
    :attr int limit: Number of records returned.
    :attr int offset: Skipped number of records.
    :attr List[InventoryResourceRecord] inventories: (optional) List of inventory
          resource records.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 total_count: int = None,
                 inventories: List['InventoryResourceRecord'] = None) -> None:
        """
        Initialize a InventoryResourceRecordList object.

        :param int limit: Number of records returned.
        :param int offset: Skipped number of records.
        :param int total_count: (optional) Total number of records.
        :param List[InventoryResourceRecord] inventories: (optional) List of
               inventory resource records.
        """
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.inventories = inventories

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'InventoryResourceRecordList':
        """Initialize a InventoryResourceRecordList object from a json dictionary."""
        args = {}
        if 'total_count' in _dict:
            args['total_count'] = _dict.get('total_count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in InventoryResourceRecordList JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in InventoryResourceRecordList JSON')
        if 'inventories' in _dict:
            args['inventories'] = [InventoryResourceRecord.from_dict(x) for x in _dict.get('inventories')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a InventoryResourceRecordList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'total_count') and self.total_count is not None:
            _dict['total_count'] = self.total_count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'inventories') and self.inventories is not None:
            _dict['inventories'] = [x.to_dict() for x in self.inventories]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this InventoryResourceRecordList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'InventoryResourceRecordList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'InventoryResourceRecordList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Job():
    """
    Complete Job with user inputs and system generated data.

    :attr str command_object: (optional) Name of the Schematics automation resource.
    :attr str command_object_id: (optional) Job command object id (workspace-id,
          action-id).
    :attr str command_name: (optional) Schematics job command name.
    :attr str command_parameter: (optional) Schematics job command parameter
          (playbook-name, capsule-name or flow-name).
    :attr List[str] command_options: (optional) Command line options for the
          command.
    :attr List[VariableData] inputs: (optional) Job inputs used by Action.
    :attr List[VariableData] settings: (optional) Environment variables used by the
          Job while performing Action.
    :attr List[str] tags: (optional) User defined tags, while running the job.
    :attr str id: (optional) Job ID.
    :attr str name: (optional) Job name, uniquely derived from the related Action.
    :attr str description: (optional) Job description derived from the related
          Action.
    :attr str location: (optional) List of workspace locations supported by IBM
          Cloud Schematics service.  Note, this does not limit the location of the
          resources provisioned using Schematics.
    :attr str resource_group: (optional) Resource-group name derived from the
          related Action.
    :attr datetime submitted_at: (optional) Job submission time.
    :attr str submitted_by: (optional) Email address of user who submitted the job.
    :attr datetime start_at: (optional) Job start time.
    :attr datetime end_at: (optional) Job end time.
    :attr str duration: (optional) Duration of job execution; example 40 sec.
    :attr JobStatus status: (optional) Job Status.
    :attr JobData data: (optional) Job data.
    :attr BastionResourceDefinition bastion: (optional) Describes a bastion
          resource.
    :attr JobLogSummary log_summary: (optional) Job log summary record.
    :attr str log_store_url: (optional) Job log store URL.
    :attr str state_store_url: (optional) Job state store URL.
    :attr str results_url: (optional) Job results store URL.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 command_object: str = None,
                 command_object_id: str = None,
                 command_name: str = None,
                 command_parameter: str = None,
                 command_options: List[str] = None,
                 inputs: List['VariableData'] = None,
                 settings: List['VariableData'] = None,
                 tags: List[str] = None,
                 id: str = None,
                 name: str = None,
                 description: str = None,
                 location: str = None,
                 resource_group: str = None,
                 submitted_at: datetime = None,
                 submitted_by: str = None,
                 start_at: datetime = None,
                 end_at: datetime = None,
                 duration: str = None,
                 status: 'JobStatus' = None,
                 data: 'JobData' = None,
                 bastion: 'BastionResourceDefinition' = None,
                 log_summary: 'JobLogSummary' = None,
                 log_store_url: str = None,
                 state_store_url: str = None,
                 results_url: str = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a Job object.

        :param str command_object: (optional) Name of the Schematics automation
               resource.
        :param str command_object_id: (optional) Job command object id
               (workspace-id, action-id).
        :param str command_name: (optional) Schematics job command name.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name, capsule-name or flow-name).
        :param List[str] command_options: (optional) Command line options for the
               command.
        :param List[VariableData] inputs: (optional) Job inputs used by Action.
        :param List[VariableData] settings: (optional) Environment variables used
               by the Job while performing Action.
        :param List[str] tags: (optional) User defined tags, while running the job.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param JobStatus status: (optional) Job Status.
        :param JobData data: (optional) Job data.
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param JobLogSummary log_summary: (optional) Job log summary record.
        """
        self.command_object = command_object
        self.command_object_id = command_object_id
        self.command_name = command_name
        self.command_parameter = command_parameter
        self.command_options = command_options
        self.inputs = inputs
        self.settings = settings
        self.tags = tags
        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.resource_group = resource_group
        self.submitted_at = submitted_at
        self.submitted_by = submitted_by
        self.start_at = start_at
        self.end_at = end_at
        self.duration = duration
        self.status = status
        self.data = data
        self.bastion = bastion
        self.log_summary = log_summary
        self.log_store_url = log_store_url
        self.state_store_url = state_store_url
        self.results_url = results_url
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Job':
        """Initialize a Job object from a json dictionary."""
        args = {}
        if 'command_object' in _dict:
            args['command_object'] = _dict.get('command_object')
        if 'command_object_id' in _dict:
            args['command_object_id'] = _dict.get('command_object_id')
        if 'command_name' in _dict:
            args['command_name'] = _dict.get('command_name')
        if 'command_parameter' in _dict:
            args['command_parameter'] = _dict.get('command_parameter')
        if 'command_options' in _dict:
            args['command_options'] = _dict.get('command_options')
        if 'inputs' in _dict:
            args['inputs'] = [VariableData.from_dict(x) for x in _dict.get('inputs')]
        if 'settings' in _dict:
            args['settings'] = [VariableData.from_dict(x) for x in _dict.get('settings')]
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'submitted_at' in _dict:
            args['submitted_at'] = string_to_datetime(_dict.get('submitted_at'))
        if 'submitted_by' in _dict:
            args['submitted_by'] = _dict.get('submitted_by')
        if 'start_at' in _dict:
            args['start_at'] = string_to_datetime(_dict.get('start_at'))
        if 'end_at' in _dict:
            args['end_at'] = string_to_datetime(_dict.get('end_at'))
        if 'duration' in _dict:
            args['duration'] = _dict.get('duration')
        if 'status' in _dict:
            args['status'] = JobStatus.from_dict(_dict.get('status'))
        if 'data' in _dict:
            args['data'] = JobData.from_dict(_dict.get('data'))
        if 'bastion' in _dict:
            args['bastion'] = BastionResourceDefinition.from_dict(_dict.get('bastion'))
        if 'log_summary' in _dict:
            args['log_summary'] = JobLogSummary.from_dict(_dict.get('log_summary'))
        if 'log_store_url' in _dict:
            args['log_store_url'] = _dict.get('log_store_url')
        if 'state_store_url' in _dict:
            args['state_store_url'] = _dict.get('state_store_url')
        if 'results_url' in _dict:
            args['results_url'] = _dict.get('results_url')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Job object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'command_object') and self.command_object is not None:
            _dict['command_object'] = self.command_object
        if hasattr(self, 'command_object_id') and self.command_object_id is not None:
            _dict['command_object_id'] = self.command_object_id
        if hasattr(self, 'command_name') and self.command_name is not None:
            _dict['command_name'] = self.command_name
        if hasattr(self, 'command_parameter') and self.command_parameter is not None:
            _dict['command_parameter'] = self.command_parameter
        if hasattr(self, 'command_options') and self.command_options is not None:
            _dict['command_options'] = self.command_options
        if hasattr(self, 'inputs') and self.inputs is not None:
            _dict['inputs'] = [x.to_dict() for x in self.inputs]
        if hasattr(self, 'settings') and self.settings is not None:
            _dict['settings'] = [x.to_dict() for x in self.settings]
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'id') and getattr(self, 'id') is not None:
            _dict['id'] = getattr(self, 'id')
        if hasattr(self, 'name') and getattr(self, 'name') is not None:
            _dict['name'] = getattr(self, 'name')
        if hasattr(self, 'description') and getattr(self, 'description') is not None:
            _dict['description'] = getattr(self, 'description')
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'resource_group') and getattr(self, 'resource_group') is not None:
            _dict['resource_group'] = getattr(self, 'resource_group')
        if hasattr(self, 'submitted_at') and getattr(self, 'submitted_at') is not None:
            _dict['submitted_at'] = datetime_to_string(getattr(self, 'submitted_at'))
        if hasattr(self, 'submitted_by') and getattr(self, 'submitted_by') is not None:
            _dict['submitted_by'] = getattr(self, 'submitted_by')
        if hasattr(self, 'start_at') and getattr(self, 'start_at') is not None:
            _dict['start_at'] = datetime_to_string(getattr(self, 'start_at'))
        if hasattr(self, 'end_at') and getattr(self, 'end_at') is not None:
            _dict['end_at'] = datetime_to_string(getattr(self, 'end_at'))
        if hasattr(self, 'duration') and getattr(self, 'duration') is not None:
            _dict['duration'] = getattr(self, 'duration')
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status.to_dict()
        if hasattr(self, 'data') and self.data is not None:
            _dict['data'] = self.data.to_dict()
        if hasattr(self, 'bastion') and self.bastion is not None:
            _dict['bastion'] = self.bastion.to_dict()
        if hasattr(self, 'log_summary') and self.log_summary is not None:
            _dict['log_summary'] = self.log_summary.to_dict()
        if hasattr(self, 'log_store_url') and getattr(self, 'log_store_url') is not None:
            _dict['log_store_url'] = getattr(self, 'log_store_url')
        if hasattr(self, 'state_store_url') and getattr(self, 'state_store_url') is not None:
            _dict['state_store_url'] = getattr(self, 'state_store_url')
        if hasattr(self, 'results_url') and getattr(self, 'results_url') is not None:
            _dict['results_url'] = getattr(self, 'results_url')
        if hasattr(self, 'updated_at') and getattr(self, 'updated_at') is not None:
            _dict['updated_at'] = datetime_to_string(getattr(self, 'updated_at'))
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Job object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Job') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Job') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class CommandObjectEnum(str, Enum):
        """
        Name of the Schematics automation resource.
        """
        WORKSPACE = 'workspace'
        ACTION = 'action'
        SYSTEM = 'system'


    class CommandNameEnum(str, Enum):
        """
        Schematics job command name.
        """
        ANSIBLE_PLAYBOOK_RUN = 'ansible_playbook_run'
        ANSIBLE_PLAYBOOK_CHECK = 'ansible_playbook_check'
        SYSTEM_KEY_ENABLE = 'system_key_enable'
        SYTEM_KEY_DELETE = 'sytem_key_delete'
        SYSTEM_KEY_DISABLE = 'system_key_disable'
        SYSTEM_KEY_ROTATE = 'system_key_rotate'
        SYSTEM_KEY_RESTORE = 'system_key_restore'


    class LocationEnum(str, Enum):
        """
        List of workspace locations supported by IBM Cloud Schematics service.  Note, this
        does not limit the location of the resources provisioned using Schematics.
        """
        US_SOUTH = 'us-south'
        US_EAST = 'us-east'
        EU_GB = 'eu-gb'
        EU_DE = 'eu-de'


class JobData():
    """
    Job data.

    :attr str job_type: Type of Job.
    :attr JobDataAction action_job_data: (optional) Action Job data.
    :attr JobDataSystem system_job_data: (optional) Controls Job data.
    """

    def __init__(self,
                 job_type: str,
                 *,
                 action_job_data: 'JobDataAction' = None,
                 system_job_data: 'JobDataSystem' = None) -> None:
        """
        Initialize a JobData object.

        :param str job_type: Type of Job.
        :param JobDataAction action_job_data: (optional) Action Job data.
        :param JobDataSystem system_job_data: (optional) Controls Job data.
        """
        self.job_type = job_type
        self.action_job_data = action_job_data
        self.system_job_data = system_job_data

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobData':
        """Initialize a JobData object from a json dictionary."""
        args = {}
        if 'job_type' in _dict:
            args['job_type'] = _dict.get('job_type')
        else:
            raise ValueError('Required property \'job_type\' not present in JobData JSON')
        if 'action_job_data' in _dict:
            args['action_job_data'] = JobDataAction.from_dict(_dict.get('action_job_data'))
        if 'system_job_data' in _dict:
            args['system_job_data'] = JobDataSystem.from_dict(_dict.get('system_job_data'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'job_type') and self.job_type is not None:
            _dict['job_type'] = self.job_type
        if hasattr(self, 'action_job_data') and self.action_job_data is not None:
            _dict['action_job_data'] = self.action_job_data.to_dict()
        if hasattr(self, 'system_job_data') and self.system_job_data is not None:
            _dict['system_job_data'] = self.system_job_data.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class JobTypeEnum(str, Enum):
        """
        Type of Job.
        """
        REPO_DOWNLOAD_JOB = 'repo_download_job'
        ACTION_JOB = 'action_job'
        SYSTEM_JOB = 'system_job'


class JobDataAction():
    """
    Action Job data.

    :attr str action_name: (optional) Flow name.
    :attr List[VariableData] inputs: (optional) Input variables data used by the
          Action Job.
    :attr List[VariableData] outputs: (optional) Output variables data from the
          Action Job.
    :attr List[VariableData] settings: (optional) Environment variables used by all
          the templates in the Action.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    :attr InventoryResourceRecord inventory_record: (optional) Complete inventory
          resource details with user inputs and system generated data.
    :attr str materialized_inventory: (optional) Materialized inventory details used
          by the Action Job, in .ini format.
    """

    def __init__(self,
                 *,
                 action_name: str = None,
                 inputs: List['VariableData'] = None,
                 outputs: List['VariableData'] = None,
                 settings: List['VariableData'] = None,
                 updated_at: datetime = None,
                 inventory_record: 'InventoryResourceRecord' = None,
                 materialized_inventory: str = None) -> None:
        """
        Initialize a JobDataAction object.

        :param str action_name: (optional) Flow name.
        :param List[VariableData] inputs: (optional) Input variables data used by
               the Action Job.
        :param List[VariableData] outputs: (optional) Output variables data from
               the Action Job.
        :param List[VariableData] settings: (optional) Environment variables used
               by all the templates in the Action.
        :param datetime updated_at: (optional) Job status updation timestamp.
        :param InventoryResourceRecord inventory_record: (optional) Complete
               inventory resource details with user inputs and system generated data.
        :param str materialized_inventory: (optional) Materialized inventory
               details used by the Action Job, in .ini format.
        """
        self.action_name = action_name
        self.inputs = inputs
        self.outputs = outputs
        self.settings = settings
        self.updated_at = updated_at
        self.inventory_record = inventory_record
        self.materialized_inventory = materialized_inventory

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobDataAction':
        """Initialize a JobDataAction object from a json dictionary."""
        args = {}
        if 'action_name' in _dict:
            args['action_name'] = _dict.get('action_name')
        if 'inputs' in _dict:
            args['inputs'] = [VariableData.from_dict(x) for x in _dict.get('inputs')]
        if 'outputs' in _dict:
            args['outputs'] = [VariableData.from_dict(x) for x in _dict.get('outputs')]
        if 'settings' in _dict:
            args['settings'] = [VariableData.from_dict(x) for x in _dict.get('settings')]
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'inventory_record' in _dict:
            args['inventory_record'] = InventoryResourceRecord.from_dict(_dict.get('inventory_record'))
        if 'materialized_inventory' in _dict:
            args['materialized_inventory'] = _dict.get('materialized_inventory')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobDataAction object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'action_name') and self.action_name is not None:
            _dict['action_name'] = self.action_name
        if hasattr(self, 'inputs') and self.inputs is not None:
            _dict['inputs'] = [x.to_dict() for x in self.inputs]
        if hasattr(self, 'outputs') and self.outputs is not None:
            _dict['outputs'] = [x.to_dict() for x in self.outputs]
        if hasattr(self, 'settings') and self.settings is not None:
            _dict['settings'] = [x.to_dict() for x in self.settings]
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        if hasattr(self, 'inventory_record') and self.inventory_record is not None:
            _dict['inventory_record'] = self.inventory_record.to_dict()
        if hasattr(self, 'materialized_inventory') and self.materialized_inventory is not None:
            _dict['materialized_inventory'] = self.materialized_inventory
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobDataAction object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobDataAction') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobDataAction') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobDataSystem():
    """
    Controls Job data.

    :attr str key_id: (optional) Key ID for which key event is generated.
    :attr List[str] schematics_resource_id: (optional) List of the schematics
          resource id.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 key_id: str = None,
                 schematics_resource_id: List[str] = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobDataSystem object.

        :param str key_id: (optional) Key ID for which key event is generated.
        :param List[str] schematics_resource_id: (optional) List of the schematics
               resource id.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.key_id = key_id
        self.schematics_resource_id = schematics_resource_id
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobDataSystem':
        """Initialize a JobDataSystem object from a json dictionary."""
        args = {}
        if 'key_id' in _dict:
            args['key_id'] = _dict.get('key_id')
        if 'schematics_resource_id' in _dict:
            args['schematics_resource_id'] = _dict.get('schematics_resource_id')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobDataSystem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'key_id') and self.key_id is not None:
            _dict['key_id'] = self.key_id
        if hasattr(self, 'schematics_resource_id') and self.schematics_resource_id is not None:
            _dict['schematics_resource_id'] = self.schematics_resource_id
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobDataSystem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobDataSystem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobDataSystem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobList():
    """
    List of Job details.

    :attr int total_count: (optional) Total number of records.
    :attr int limit: Number of records returned.
    :attr int offset: Skipped number of records.
    :attr List[JobLite] jobs: (optional) List of job records.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 total_count: int = None,
                 jobs: List['JobLite'] = None) -> None:
        """
        Initialize a JobList object.

        :param int limit: Number of records returned.
        :param int offset: Skipped number of records.
        :param int total_count: (optional) Total number of records.
        :param List[JobLite] jobs: (optional) List of job records.
        """
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.jobs = jobs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobList':
        """Initialize a JobList object from a json dictionary."""
        args = {}
        if 'total_count' in _dict:
            args['total_count'] = _dict.get('total_count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in JobList JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in JobList JSON')
        if 'jobs' in _dict:
            args['jobs'] = [JobLite.from_dict(x) for x in _dict.get('jobs')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'total_count') and self.total_count is not None:
            _dict['total_count'] = self.total_count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'jobs') and self.jobs is not None:
            _dict['jobs'] = [x.to_dict() for x in self.jobs]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLite():
    """
    Job summary profile with system generated data.

    :attr str id: (optional) Job ID.
    :attr str name: (optional) Job name, uniquely derived from the related Action.
    :attr str description: (optional) Job description derived from the related
          Action.
    :attr str command_object: (optional) Name of the Schematics automation resource.
    :attr str command_object_id: (optional) Job command object id (action-id).
    :attr str command_name: (optional) Schematics job command name.
    :attr List[str] tags: (optional) User defined tags, while running the job.
    :attr str location: (optional) List of workspace locations supported by IBM
          Cloud Schematics service.  Note, this does not limit the location of the
          resources provisioned using Schematics.
    :attr str resource_group: (optional) Resource-group name derived from the
          related Action,.
    :attr datetime submitted_at: (optional) Job submission time.
    :attr str submitted_by: (optional) Email address of user who submitted the job.
    :attr str duration: (optional) Duration of job execution; example 40 sec.
    :attr datetime start_at: (optional) Job start time.
    :attr datetime end_at: (optional) Job end time.
    :attr JobStatus status: (optional) Job Status.
    :attr JobLogSummary log_summary: (optional) Job log summary record.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 id: str = None,
                 name: str = None,
                 description: str = None,
                 command_object: str = None,
                 command_object_id: str = None,
                 command_name: str = None,
                 tags: List[str] = None,
                 location: str = None,
                 resource_group: str = None,
                 submitted_at: datetime = None,
                 submitted_by: str = None,
                 duration: str = None,
                 start_at: datetime = None,
                 end_at: datetime = None,
                 status: 'JobStatus' = None,
                 log_summary: 'JobLogSummary' = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobLite object.

        :param str id: (optional) Job ID.
        :param str name: (optional) Job name, uniquely derived from the related
               Action.
        :param str description: (optional) Job description derived from the related
               Action.
        :param str command_object: (optional) Name of the Schematics automation
               resource.
        :param str command_object_id: (optional) Job command object id (action-id).
        :param str command_name: (optional) Schematics job command name.
        :param List[str] tags: (optional) User defined tags, while running the job.
        :param str location: (optional) List of workspace locations supported by
               IBM Cloud Schematics service.  Note, this does not limit the location of
               the resources provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name derived from the
               related Action,.
        :param datetime submitted_at: (optional) Job submission time.
        :param str submitted_by: (optional) Email address of user who submitted the
               job.
        :param str duration: (optional) Duration of job execution; example 40 sec.
        :param datetime start_at: (optional) Job start time.
        :param datetime end_at: (optional) Job end time.
        :param JobStatus status: (optional) Job Status.
        :param JobLogSummary log_summary: (optional) Job log summary record.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.id = id
        self.name = name
        self.description = description
        self.command_object = command_object
        self.command_object_id = command_object_id
        self.command_name = command_name
        self.tags = tags
        self.location = location
        self.resource_group = resource_group
        self.submitted_at = submitted_at
        self.submitted_by = submitted_by
        self.duration = duration
        self.start_at = start_at
        self.end_at = end_at
        self.status = status
        self.log_summary = log_summary
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLite':
        """Initialize a JobLite object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'command_object' in _dict:
            args['command_object'] = _dict.get('command_object')
        if 'command_object_id' in _dict:
            args['command_object_id'] = _dict.get('command_object_id')
        if 'command_name' in _dict:
            args['command_name'] = _dict.get('command_name')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'submitted_at' in _dict:
            args['submitted_at'] = string_to_datetime(_dict.get('submitted_at'))
        if 'submitted_by' in _dict:
            args['submitted_by'] = _dict.get('submitted_by')
        if 'duration' in _dict:
            args['duration'] = _dict.get('duration')
        if 'start_at' in _dict:
            args['start_at'] = string_to_datetime(_dict.get('start_at'))
        if 'end_at' in _dict:
            args['end_at'] = string_to_datetime(_dict.get('end_at'))
        if 'status' in _dict:
            args['status'] = JobStatus.from_dict(_dict.get('status'))
        if 'log_summary' in _dict:
            args['log_summary'] = JobLogSummary.from_dict(_dict.get('log_summary'))
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLite object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'command_object') and self.command_object is not None:
            _dict['command_object'] = self.command_object
        if hasattr(self, 'command_object_id') and self.command_object_id is not None:
            _dict['command_object_id'] = self.command_object_id
        if hasattr(self, 'command_name') and self.command_name is not None:
            _dict['command_name'] = self.command_name
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'submitted_at') and self.submitted_at is not None:
            _dict['submitted_at'] = datetime_to_string(self.submitted_at)
        if hasattr(self, 'submitted_by') and self.submitted_by is not None:
            _dict['submitted_by'] = self.submitted_by
        if hasattr(self, 'duration') and self.duration is not None:
            _dict['duration'] = self.duration
        if hasattr(self, 'start_at') and self.start_at is not None:
            _dict['start_at'] = datetime_to_string(self.start_at)
        if hasattr(self, 'end_at') and self.end_at is not None:
            _dict['end_at'] = datetime_to_string(self.end_at)
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status.to_dict()
        if hasattr(self, 'log_summary') and self.log_summary is not None:
            _dict['log_summary'] = self.log_summary.to_dict()
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLite object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLite') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLite') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class CommandObjectEnum(str, Enum):
        """
        Name of the Schematics automation resource.
        """
        WORKSPACE = 'workspace'
        ACTION = 'action'
        SYSTEM = 'system'


    class CommandNameEnum(str, Enum):
        """
        Schematics job command name.
        """
        ANSIBLE_PLAYBOOK_RUN = 'ansible_playbook_run'
        ANSIBLE_PLAYBOOK_CHECK = 'ansible_playbook_check'
        SYSTEM_KEY_ENABLE = 'system_key_enable'
        SYTEM_KEY_DELETE = 'sytem_key_delete'
        SYSTEM_KEY_DISABLE = 'system_key_disable'
        SYSTEM_KEY_ROTATE = 'system_key_rotate'
        SYSTEM_KEY_RESTORE = 'system_key_restore'


    class LocationEnum(str, Enum):
        """
        List of workspace locations supported by IBM Cloud Schematics service.  Note, this
        does not limit the location of the resources provisioned using Schematics.
        """
        US_SOUTH = 'us-south'
        US_EAST = 'us-east'
        EU_GB = 'eu-gb'
        EU_DE = 'eu-de'


class JobLog():
    """
    Job Log details.

    :attr str job_id: (optional) Job Id.
    :attr str job_name: (optional) Job name, uniquely derived from the related
          Action.
    :attr JobLogSummary log_summary: (optional) Job log summary record.
    :attr str format: (optional) Format of the Log text.
    :attr bytes details: (optional) Log text, generated by the Job.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 job_id: str = None,
                 job_name: str = None,
                 log_summary: 'JobLogSummary' = None,
                 format: str = None,
                 details: bytes = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobLog object.

        :param str job_id: (optional) Job Id.
        :param str job_name: (optional) Job name, uniquely derived from the related
               Action.
        :param JobLogSummary log_summary: (optional) Job log summary record.
        :param str format: (optional) Format of the Log text.
        :param bytes details: (optional) Log text, generated by the Job.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.job_id = job_id
        self.job_name = job_name
        self.log_summary = log_summary
        self.format = format
        self.details = details
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLog':
        """Initialize a JobLog object from a json dictionary."""
        args = {}
        if 'job_id' in _dict:
            args['job_id'] = _dict.get('job_id')
        if 'job_name' in _dict:
            args['job_name'] = _dict.get('job_name')
        if 'log_summary' in _dict:
            args['log_summary'] = JobLogSummary.from_dict(_dict.get('log_summary'))
        if 'format' in _dict:
            args['format'] = _dict.get('format')
        if 'details' in _dict:
            args['details'] = base64.b64decode(_dict.get('details'))
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLog object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'job_id') and self.job_id is not None:
            _dict['job_id'] = self.job_id
        if hasattr(self, 'job_name') and self.job_name is not None:
            _dict['job_name'] = self.job_name
        if hasattr(self, 'log_summary') and self.log_summary is not None:
            _dict['log_summary'] = self.log_summary.to_dict()
        if hasattr(self, 'format') and self.format is not None:
            _dict['format'] = self.format
        if hasattr(self, 'details') and self.details is not None:
            _dict['details'] = str(base64.b64encode(self.details), 'utf-8')
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLog object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLog') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLog') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class FormatEnum(str, Enum):
        """
        Format of the Log text.
        """
        JSON = 'json'
        HTML = 'html'
        MARKDOWN = 'markdown'
        RTF = 'rtf'


class JobLogSummary():
    """
    Job log summary record.

    :attr str job_id: (optional) Workspace Id.
    :attr str job_type: (optional) Type of Job.
    :attr datetime log_start_at: (optional) Job log start timestamp.
    :attr datetime log_analyzed_till: (optional) Job log update timestamp.
    :attr float elapsed_time: (optional) Job log elapsed time (log_analyzed_till -
          log_start_at).
    :attr List[JobLogSummaryLogErrorsItem] log_errors: (optional) Job log errors.
    :attr JobLogSummaryRepoDownloadJob repo_download_job: (optional) Repo download
          Job log summary.
    :attr JobLogSummaryActionJob action_job: (optional) Action Job.
    :attr JobLogSummarySystemJob system_job: (optional) System Job log summary.
    """

    def __init__(self,
                 *,
                 job_id: str = None,
                 job_type: str = None,
                 log_start_at: datetime = None,
                 log_analyzed_till: datetime = None,
                 elapsed_time: float = None,
                 log_errors: List['JobLogSummaryLogErrorsItem'] = None,
                 repo_download_job: 'JobLogSummaryRepoDownloadJob' = None,
                 action_job: 'JobLogSummaryActionJob' = None,
                 system_job: 'JobLogSummarySystemJob' = None) -> None:
        """
        Initialize a JobLogSummary object.

        :param str job_type: (optional) Type of Job.
        :param JobLogSummaryRepoDownloadJob repo_download_job: (optional) Repo
               download Job log summary.
        :param JobLogSummaryActionJob action_job: (optional) Action Job.
        :param JobLogSummarySystemJob system_job: (optional) System Job log
               summary.
        """
        self.job_id = job_id
        self.job_type = job_type
        self.log_start_at = log_start_at
        self.log_analyzed_till = log_analyzed_till
        self.elapsed_time = elapsed_time
        self.log_errors = log_errors
        self.repo_download_job = repo_download_job
        self.action_job = action_job
        self.system_job = system_job

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummary':
        """Initialize a JobLogSummary object from a json dictionary."""
        args = {}
        if 'job_id' in _dict:
            args['job_id'] = _dict.get('job_id')
        if 'job_type' in _dict:
            args['job_type'] = _dict.get('job_type')
        if 'log_start_at' in _dict:
            args['log_start_at'] = string_to_datetime(_dict.get('log_start_at'))
        if 'log_analyzed_till' in _dict:
            args['log_analyzed_till'] = string_to_datetime(_dict.get('log_analyzed_till'))
        if 'elapsed_time' in _dict:
            args['elapsed_time'] = _dict.get('elapsed_time')
        if 'log_errors' in _dict:
            args['log_errors'] = [JobLogSummaryLogErrorsItem.from_dict(x) for x in _dict.get('log_errors')]
        if 'repo_download_job' in _dict:
            args['repo_download_job'] = JobLogSummaryRepoDownloadJob.from_dict(_dict.get('repo_download_job'))
        if 'action_job' in _dict:
            args['action_job'] = JobLogSummaryActionJob.from_dict(_dict.get('action_job'))
        if 'system_job' in _dict:
            args['system_job'] = JobLogSummarySystemJob.from_dict(_dict.get('system_job'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummary object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'job_id') and getattr(self, 'job_id') is not None:
            _dict['job_id'] = getattr(self, 'job_id')
        if hasattr(self, 'job_type') and self.job_type is not None:
            _dict['job_type'] = self.job_type
        if hasattr(self, 'log_start_at') and getattr(self, 'log_start_at') is not None:
            _dict['log_start_at'] = datetime_to_string(getattr(self, 'log_start_at'))
        if hasattr(self, 'log_analyzed_till') and getattr(self, 'log_analyzed_till') is not None:
            _dict['log_analyzed_till'] = datetime_to_string(getattr(self, 'log_analyzed_till'))
        if hasattr(self, 'elapsed_time') and getattr(self, 'elapsed_time') is not None:
            _dict['elapsed_time'] = getattr(self, 'elapsed_time')
        if hasattr(self, 'log_errors') and getattr(self, 'log_errors') is not None:
            _dict['log_errors'] = [x.to_dict() for x in getattr(self, 'log_errors')]
        if hasattr(self, 'repo_download_job') and self.repo_download_job is not None:
            _dict['repo_download_job'] = self.repo_download_job.to_dict()
        if hasattr(self, 'action_job') and self.action_job is not None:
            _dict['action_job'] = self.action_job.to_dict()
        if hasattr(self, 'system_job') and self.system_job is not None:
            _dict['system_job'] = self.system_job.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummary object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummary') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummary') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class JobTypeEnum(str, Enum):
        """
        Type of Job.
        """
        REPO_DOWNLOAD_JOB = 'repo_download_job'
        WORKSPACE_JOB = 'workspace_job'
        ACTION_JOB = 'action_job'
        SYSTEM_JOB = 'system_job'


class JobLogSummaryActionJob():
    """
    Action Job.

    :attr float host_count: (optional) number of hosts.
    :attr float task_count: (optional) number of tasks in playbook.
    :attr float play_count: (optional) number of plays in playbook.
    :attr JobLogSummaryActionJobRecap recap: (optional) Recap records.
    """

    def __init__(self,
                 *,
                 host_count: float = None,
                 task_count: float = None,
                 play_count: float = None,
                 recap: 'JobLogSummaryActionJobRecap' = None) -> None:
        """
        Initialize a JobLogSummaryActionJob object.

        :param JobLogSummaryActionJobRecap recap: (optional) Recap records.
        """
        self.host_count = host_count
        self.task_count = task_count
        self.play_count = play_count
        self.recap = recap

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummaryActionJob':
        """Initialize a JobLogSummaryActionJob object from a json dictionary."""
        args = {}
        if 'host_count' in _dict:
            args['host_count'] = _dict.get('host_count')
        if 'task_count' in _dict:
            args['task_count'] = _dict.get('task_count')
        if 'play_count' in _dict:
            args['play_count'] = _dict.get('play_count')
        if 'recap' in _dict:
            args['recap'] = JobLogSummaryActionJobRecap.from_dict(_dict.get('recap'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummaryActionJob object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'host_count') and getattr(self, 'host_count') is not None:
            _dict['host_count'] = getattr(self, 'host_count')
        if hasattr(self, 'task_count') and getattr(self, 'task_count') is not None:
            _dict['task_count'] = getattr(self, 'task_count')
        if hasattr(self, 'play_count') and getattr(self, 'play_count') is not None:
            _dict['play_count'] = getattr(self, 'play_count')
        if hasattr(self, 'recap') and self.recap is not None:
            _dict['recap'] = self.recap.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummaryActionJob object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummaryActionJob') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummaryActionJob') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLogSummaryActionJobRecap():
    """
    Recap records.

    :attr List[str] hosts: (optional) List of host name.
    :attr float ok: (optional) Number of OK.
    :attr float changed: (optional) Number of changed.
    :attr float failed: (optional) Number of failed.
    :attr float skipped: (optional) Number of skipped.
    :attr float unreachable: (optional) Number of unreachable.
    """

    def __init__(self,
                 *,
                 hosts: List[str] = None,
                 ok: float = None,
                 changed: float = None,
                 failed: float = None,
                 skipped: float = None,
                 unreachable: float = None) -> None:
        """
        Initialize a JobLogSummaryActionJobRecap object.

        :param List[str] hosts: (optional) List of host name.
        :param float ok: (optional) Number of OK.
        :param float changed: (optional) Number of changed.
        :param float failed: (optional) Number of failed.
        :param float skipped: (optional) Number of skipped.
        :param float unreachable: (optional) Number of unreachable.
        """
        self.hosts = hosts
        self.ok = ok
        self.changed = changed
        self.failed = failed
        self.skipped = skipped
        self.unreachable = unreachable

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummaryActionJobRecap':
        """Initialize a JobLogSummaryActionJobRecap object from a json dictionary."""
        args = {}
        if 'hosts' in _dict:
            args['hosts'] = _dict.get('hosts')
        if 'ok' in _dict:
            args['ok'] = _dict.get('ok')
        if 'changed' in _dict:
            args['changed'] = _dict.get('changed')
        if 'failed' in _dict:
            args['failed'] = _dict.get('failed')
        if 'skipped' in _dict:
            args['skipped'] = _dict.get('skipped')
        if 'unreachable' in _dict:
            args['unreachable'] = _dict.get('unreachable')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummaryActionJobRecap object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'hosts') and self.hosts is not None:
            _dict['hosts'] = self.hosts
        if hasattr(self, 'ok') and self.ok is not None:
            _dict['ok'] = self.ok
        if hasattr(self, 'changed') and self.changed is not None:
            _dict['changed'] = self.changed
        if hasattr(self, 'failed') and self.failed is not None:
            _dict['failed'] = self.failed
        if hasattr(self, 'skipped') and self.skipped is not None:
            _dict['skipped'] = self.skipped
        if hasattr(self, 'unreachable') and self.unreachable is not None:
            _dict['unreachable'] = self.unreachable
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummaryActionJobRecap object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummaryActionJobRecap') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummaryActionJobRecap') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLogSummaryLogErrorsItem():
    """
    JobLogSummaryLogErrorsItem.

    :attr str error_code: (optional) Error code in the Log.
    :attr str error_msg: (optional) Summary error message in the log.
    :attr float error_count: (optional) Number of occurrence.
    """

    def __init__(self,
                 *,
                 error_code: str = None,
                 error_msg: str = None,
                 error_count: float = None) -> None:
        """
        Initialize a JobLogSummaryLogErrorsItem object.

        :param str error_code: (optional) Error code in the Log.
        :param str error_msg: (optional) Summary error message in the log.
        :param float error_count: (optional) Number of occurrence.
        """
        self.error_code = error_code
        self.error_msg = error_msg
        self.error_count = error_count

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummaryLogErrorsItem':
        """Initialize a JobLogSummaryLogErrorsItem object from a json dictionary."""
        args = {}
        if 'error_code' in _dict:
            args['error_code'] = _dict.get('error_code')
        if 'error_msg' in _dict:
            args['error_msg'] = _dict.get('error_msg')
        if 'error_count' in _dict:
            args['error_count'] = _dict.get('error_count')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummaryLogErrorsItem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'error_code') and self.error_code is not None:
            _dict['error_code'] = self.error_code
        if hasattr(self, 'error_msg') and self.error_msg is not None:
            _dict['error_msg'] = self.error_msg
        if hasattr(self, 'error_count') and self.error_count is not None:
            _dict['error_count'] = self.error_count
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummaryLogErrorsItem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummaryLogErrorsItem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummaryLogErrorsItem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLogSummaryRepoDownloadJob():
    """
    Repo download Job log summary.

    :attr float scanned_file_count: (optional) Number of files scanned.
    :attr float quarantined_file_count: (optional) Number of files quarantined.
    :attr str detected_filetype: (optional) Detected template or data file type.
    :attr str inputs_count: (optional) Number of inputs detected.
    :attr str outputs_count: (optional) Number of outputs detected.
    """

    def __init__(self,
                 *,
                 scanned_file_count: float = None,
                 quarantined_file_count: float = None,
                 detected_filetype: str = None,
                 inputs_count: str = None,
                 outputs_count: str = None) -> None:
        """
        Initialize a JobLogSummaryRepoDownloadJob object.

        """
        self.scanned_file_count = scanned_file_count
        self.quarantined_file_count = quarantined_file_count
        self.detected_filetype = detected_filetype
        self.inputs_count = inputs_count
        self.outputs_count = outputs_count

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummaryRepoDownloadJob':
        """Initialize a JobLogSummaryRepoDownloadJob object from a json dictionary."""
        args = {}
        if 'scanned_file_count' in _dict:
            args['scanned_file_count'] = _dict.get('scanned_file_count')
        if 'quarantined_file_count' in _dict:
            args['quarantined_file_count'] = _dict.get('quarantined_file_count')
        if 'detected_filetype' in _dict:
            args['detected_filetype'] = _dict.get('detected_filetype')
        if 'inputs_count' in _dict:
            args['inputs_count'] = _dict.get('inputs_count')
        if 'outputs_count' in _dict:
            args['outputs_count'] = _dict.get('outputs_count')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummaryRepoDownloadJob object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'scanned_file_count') and getattr(self, 'scanned_file_count') is not None:
            _dict['scanned_file_count'] = getattr(self, 'scanned_file_count')
        if hasattr(self, 'quarantined_file_count') and getattr(self, 'quarantined_file_count') is not None:
            _dict['quarantined_file_count'] = getattr(self, 'quarantined_file_count')
        if hasattr(self, 'detected_filetype') and getattr(self, 'detected_filetype') is not None:
            _dict['detected_filetype'] = getattr(self, 'detected_filetype')
        if hasattr(self, 'inputs_count') and getattr(self, 'inputs_count') is not None:
            _dict['inputs_count'] = getattr(self, 'inputs_count')
        if hasattr(self, 'outputs_count') and getattr(self, 'outputs_count') is not None:
            _dict['outputs_count'] = getattr(self, 'outputs_count')
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummaryRepoDownloadJob object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummaryRepoDownloadJob') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummaryRepoDownloadJob') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLogSummarySystemJob():
    """
    System Job log summary.

    :attr float target_count: (optional) number of targets or hosts.
    :attr float success: (optional) Number of passed.
    :attr float failed: (optional) Number of failed.
    """

    def __init__(self,
                 *,
                 target_count: float = None,
                 success: float = None,
                 failed: float = None) -> None:
        """
        Initialize a JobLogSummarySystemJob object.

        :param float success: (optional) Number of passed.
        :param float failed: (optional) Number of failed.
        """
        self.target_count = target_count
        self.success = success
        self.failed = failed

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummarySystemJob':
        """Initialize a JobLogSummarySystemJob object from a json dictionary."""
        args = {}
        if 'target_count' in _dict:
            args['target_count'] = _dict.get('target_count')
        if 'success' in _dict:
            args['success'] = _dict.get('success')
        if 'failed' in _dict:
            args['failed'] = _dict.get('failed')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummarySystemJob object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'target_count') and getattr(self, 'target_count') is not None:
            _dict['target_count'] = getattr(self, 'target_count')
        if hasattr(self, 'success') and self.success is not None:
            _dict['success'] = self.success
        if hasattr(self, 'failed') and self.failed is not None:
            _dict['failed'] = self.failed
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummarySystemJob object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummarySystemJob') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummarySystemJob') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobStatus():
    """
    Job Status.

    :attr JobStatusAction action_job_status: (optional) Action Job Status.
    :attr JobStatusSystem system_job_status: (optional) System Job Status.
    """

    def __init__(self,
                 *,
                 action_job_status: 'JobStatusAction' = None,
                 system_job_status: 'JobStatusSystem' = None) -> None:
        """
        Initialize a JobStatus object.

        :param JobStatusAction action_job_status: (optional) Action Job Status.
        :param JobStatusSystem system_job_status: (optional) System Job Status.
        """
        self.action_job_status = action_job_status
        self.system_job_status = system_job_status

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatus':
        """Initialize a JobStatus object from a json dictionary."""
        args = {}
        if 'action_job_status' in _dict:
            args['action_job_status'] = JobStatusAction.from_dict(_dict.get('action_job_status'))
        if 'system_job_status' in _dict:
            args['system_job_status'] = JobStatusSystem.from_dict(_dict.get('system_job_status'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatus object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'action_job_status') and self.action_job_status is not None:
            _dict['action_job_status'] = self.action_job_status.to_dict()
        if hasattr(self, 'system_job_status') and self.system_job_status is not None:
            _dict['system_job_status'] = self.system_job_status.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatus object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatus') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatus') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobStatusAction():
    """
    Action Job Status.

    :attr str action_name: (optional) Action name.
    :attr str status_code: (optional) Status of Jobs.
    :attr str status_message: (optional) Action Job status message - to be displayed
          along with the action_status_code.
    :attr str bastion_status_code: (optional) Status of Resources.
    :attr str bastion_status_message: (optional) Bastion status message - to be
          displayed along with the bastion_status_code;.
    :attr str inventory_status_code: (optional) Status of Resources.
    :attr str inventory_status_message: (optional) Aggregated status message for all
          inventory resources,  to be displayed along with the inventory_status_code;.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 action_name: str = None,
                 status_code: str = None,
                 status_message: str = None,
                 bastion_status_code: str = None,
                 bastion_status_message: str = None,
                 inventory_status_code: str = None,
                 inventory_status_message: str = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobStatusAction object.

        :param str action_name: (optional) Action name.
        :param str status_code: (optional) Status of Jobs.
        :param str status_message: (optional) Action Job status message - to be
               displayed along with the action_status_code.
        :param str bastion_status_code: (optional) Status of Resources.
        :param str bastion_status_message: (optional) Bastion status message - to
               be displayed along with the bastion_status_code;.
        :param str inventory_status_code: (optional) Status of Resources.
        :param str inventory_status_message: (optional) Aggregated status message
               for all inventory resources,  to be displayed along with the
               inventory_status_code;.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.action_name = action_name
        self.status_code = status_code
        self.status_message = status_message
        self.bastion_status_code = bastion_status_code
        self.bastion_status_message = bastion_status_message
        self.inventory_status_code = inventory_status_code
        self.inventory_status_message = inventory_status_message
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatusAction':
        """Initialize a JobStatusAction object from a json dictionary."""
        args = {}
        if 'action_name' in _dict:
            args['action_name'] = _dict.get('action_name')
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        if 'bastion_status_code' in _dict:
            args['bastion_status_code'] = _dict.get('bastion_status_code')
        if 'bastion_status_message' in _dict:
            args['bastion_status_message'] = _dict.get('bastion_status_message')
        if 'inventory_status_code' in _dict:
            args['inventory_status_code'] = _dict.get('inventory_status_code')
        if 'inventory_status_message' in _dict:
            args['inventory_status_message'] = _dict.get('inventory_status_message')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatusAction object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'action_name') and self.action_name is not None:
            _dict['action_name'] = self.action_name
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        if hasattr(self, 'bastion_status_code') and self.bastion_status_code is not None:
            _dict['bastion_status_code'] = self.bastion_status_code
        if hasattr(self, 'bastion_status_message') and self.bastion_status_message is not None:
            _dict['bastion_status_message'] = self.bastion_status_message
        if hasattr(self, 'inventory_status_code') and self.inventory_status_code is not None:
            _dict['inventory_status_code'] = self.inventory_status_code
        if hasattr(self, 'inventory_status_message') and self.inventory_status_message is not None:
            _dict['inventory_status_message'] = self.inventory_status_message
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatusAction object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatusAction') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatusAction') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of Jobs.
        """
        JOB_PENDING = 'job_pending'
        JOB_IN_PROGRESS = 'job_in_progress'
        IOB_FINISHED = 'iob_finished'
        JOB_FAILED = 'job_failed'
        JOB_CANCELLED = 'job_cancelled'


    class BastionStatusCodeEnum(str, Enum):
        """
        Status of Resources.
        """
        NONE = 'none'
        READY = 'ready'
        PROCESSING = 'processing'
        ERROR = 'error'


    class InventoryStatusCodeEnum(str, Enum):
        """
        Status of Resources.
        """
        NONE = 'none'
        READY = 'ready'
        PROCESSING = 'processing'
        ERROR = 'error'


class JobStatusSchematicsResources():
    """
    schematics Resources Job Status.

    :attr str status_code: (optional) Status of Jobs.
    :attr str status_message: (optional) system job status message.
    :attr str schematics_resource_id: (optional) id for each resource which is
          targeted as a part of system job.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 status_code: str = None,
                 status_message: str = None,
                 schematics_resource_id: str = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobStatusSchematicsResources object.

        :param str status_code: (optional) Status of Jobs.
        :param str status_message: (optional) system job status message.
        :param str schematics_resource_id: (optional) id for each resource which is
               targeted as a part of system job.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.status_code = status_code
        self.status_message = status_message
        self.schematics_resource_id = schematics_resource_id
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatusSchematicsResources':
        """Initialize a JobStatusSchematicsResources object from a json dictionary."""
        args = {}
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        if 'schematics_resource_id' in _dict:
            args['schematics_resource_id'] = _dict.get('schematics_resource_id')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatusSchematicsResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        if hasattr(self, 'schematics_resource_id') and self.schematics_resource_id is not None:
            _dict['schematics_resource_id'] = self.schematics_resource_id
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatusSchematicsResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatusSchematicsResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatusSchematicsResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of Jobs.
        """
        JOB_PENDING = 'job_pending'
        JOB_IN_PROGRESS = 'job_in_progress'
        IOB_FINISHED = 'iob_finished'
        JOB_FAILED = 'job_failed'
        JOB_CANCELLED = 'job_cancelled'


class JobStatusSystem():
    """
    System Job Status.

    :attr str system_status_message: (optional) System job message.
    :attr str system_status_code: (optional) Status of Jobs.
    :attr List[JobStatusSchematicsResources] schematics_resource_status: (optional)
          job staus for each schematics resource.
    :attr datetime updated_at: (optional) Job status updation timestamp urces'.
    """

    def __init__(self,
                 *,
                 system_status_message: str = None,
                 system_status_code: str = None,
                 schematics_resource_status: List['JobStatusSchematicsResources'] = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobStatusSystem object.

        :param str system_status_message: (optional) System job message.
        :param str system_status_code: (optional) Status of Jobs.
        :param List[JobStatusSchematicsResources] schematics_resource_status:
               (optional) job staus for each schematics resource.
        :param datetime updated_at: (optional) Job status updation timestamp
               urces'.
        """
        self.system_status_message = system_status_message
        self.system_status_code = system_status_code
        self.schematics_resource_status = schematics_resource_status
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatusSystem':
        """Initialize a JobStatusSystem object from a json dictionary."""
        args = {}
        if 'system_status_message' in _dict:
            args['system_status_message'] = _dict.get('system_status_message')
        if 'system_status_code' in _dict:
            args['system_status_code'] = _dict.get('system_status_code')
        if 'schematics_resource_status' in _dict:
            args['schematics_resource_status'] = [JobStatusSchematicsResources.from_dict(x) for x in _dict.get('schematics_resource_status')]
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatusSystem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'system_status_message') and self.system_status_message is not None:
            _dict['system_status_message'] = self.system_status_message
        if hasattr(self, 'system_status_code') and self.system_status_code is not None:
            _dict['system_status_code'] = self.system_status_code
        if hasattr(self, 'schematics_resource_status') and self.schematics_resource_status is not None:
            _dict['schematics_resource_status'] = [x.to_dict() for x in self.schematics_resource_status]
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatusSystem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatusSystem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatusSystem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class SystemStatusCodeEnum(str, Enum):
        """
        Status of Jobs.
        """
        JOB_PENDING = 'job_pending'
        JOB_IN_PROGRESS = 'job_in_progress'
        IOB_FINISHED = 'iob_finished'
        JOB_FAILED = 'job_failed'
        JOB_CANCELLED = 'job_cancelled'


class JobStatusType():
    """
    JobStatusType -.

    :attr List[str] failed: (optional) List of failed workspace jobs.
    :attr List[str] in_progress: (optional) List of in_progress workspace jobs.
    :attr List[str] success: (optional) List of successful workspace jobs.
    :attr datetime last_updated_on: (optional) Workspace job status updated at.
    """

    def __init__(self,
                 *,
                 failed: List[str] = None,
                 in_progress: List[str] = None,
                 success: List[str] = None,
                 last_updated_on: datetime = None) -> None:
        """
        Initialize a JobStatusType object.

        :param List[str] failed: (optional) List of failed workspace jobs.
        :param List[str] in_progress: (optional) List of in_progress workspace
               jobs.
        :param List[str] success: (optional) List of successful workspace jobs.
        :param datetime last_updated_on: (optional) Workspace job status updated
               at.
        """
        self.failed = failed
        self.in_progress = in_progress
        self.success = success
        self.last_updated_on = last_updated_on

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatusType':
        """Initialize a JobStatusType object from a json dictionary."""
        args = {}
        if 'failed' in _dict:
            args['failed'] = _dict.get('failed')
        if 'in_progress' in _dict:
            args['in_progress'] = _dict.get('in_progress')
        if 'success' in _dict:
            args['success'] = _dict.get('success')
        if 'last_updated_on' in _dict:
            args['last_updated_on'] = string_to_datetime(_dict.get('last_updated_on'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatusType object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'failed') and self.failed is not None:
            _dict['failed'] = self.failed
        if hasattr(self, 'in_progress') and self.in_progress is not None:
            _dict['in_progress'] = self.in_progress
        if hasattr(self, 'success') and self.success is not None:
            _dict['success'] = self.success
        if hasattr(self, 'last_updated_on') and self.last_updated_on is not None:
            _dict['last_updated_on'] = datetime_to_string(self.last_updated_on)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatusType object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatusType') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatusType') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class KMSDiscovery():
    """
    Discovered KMS instances.

    :attr int total_count: (optional) Total number of records.
    :attr int limit: Number of records returned.
    :attr int offset: Skipped number of records.
    :attr List[KMSInstances] kms_instances: (optional) List of KMS instances.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 total_count: int = None,
                 kms_instances: List['KMSInstances'] = None) -> None:
        """
        Initialize a KMSDiscovery object.

        :param int limit: Number of records returned.
        :param int offset: Skipped number of records.
        :param int total_count: (optional) Total number of records.
        :param List[KMSInstances] kms_instances: (optional) List of KMS instances.
        """
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.kms_instances = kms_instances

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSDiscovery':
        """Initialize a KMSDiscovery object from a json dictionary."""
        args = {}
        if 'total_count' in _dict:
            args['total_count'] = _dict.get('total_count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in KMSDiscovery JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in KMSDiscovery JSON')
        if 'kms_instances' in _dict:
            args['kms_instances'] = [KMSInstances.from_dict(x) for x in _dict.get('kms_instances')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSDiscovery object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'total_count') and self.total_count is not None:
            _dict['total_count'] = self.total_count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'kms_instances') and self.kms_instances is not None:
            _dict['kms_instances'] = [x.to_dict() for x in self.kms_instances]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSDiscovery object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSDiscovery') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSDiscovery') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class KMSInstances():
    """
    KMS Instances.

    :attr str location: (optional) Location.
    :attr str encryption_scheme: (optional) Encryption schema.
    :attr str resource_group: (optional) Resource groups.
    :attr str kms_crn: (optional) KMS CRN.
    :attr str kms_name: (optional) KMS Name.
    :attr str kms_private_endpoint: (optional) KMS private endpoint.
    :attr str kms_public_endpoint: (optional) KMS public endpoint.
    :attr List[KMSInstancesKeysItem] keys: (optional) List of keys.
    """

    def __init__(self,
                 *,
                 location: str = None,
                 encryption_scheme: str = None,
                 resource_group: str = None,
                 kms_crn: str = None,
                 kms_name: str = None,
                 kms_private_endpoint: str = None,
                 kms_public_endpoint: str = None,
                 keys: List['KMSInstancesKeysItem'] = None) -> None:
        """
        Initialize a KMSInstances object.

        :param str location: (optional) Location.
        :param str encryption_scheme: (optional) Encryption schema.
        :param str resource_group: (optional) Resource groups.
        :param str kms_crn: (optional) KMS CRN.
        :param str kms_name: (optional) KMS Name.
        :param str kms_private_endpoint: (optional) KMS private endpoint.
        :param str kms_public_endpoint: (optional) KMS public endpoint.
        :param List[KMSInstancesKeysItem] keys: (optional) List of keys.
        """
        self.location = location
        self.encryption_scheme = encryption_scheme
        self.resource_group = resource_group
        self.kms_crn = kms_crn
        self.kms_name = kms_name
        self.kms_private_endpoint = kms_private_endpoint
        self.kms_public_endpoint = kms_public_endpoint
        self.keys = keys

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSInstances':
        """Initialize a KMSInstances object from a json dictionary."""
        args = {}
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'encryption_scheme' in _dict:
            args['encryption_scheme'] = _dict.get('encryption_scheme')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'kms_crn' in _dict:
            args['kms_crn'] = _dict.get('kms_crn')
        if 'kms_name' in _dict:
            args['kms_name'] = _dict.get('kms_name')
        if 'kms_private_endpoint' in _dict:
            args['kms_private_endpoint'] = _dict.get('kms_private_endpoint')
        if 'kms_public_endpoint' in _dict:
            args['kms_public_endpoint'] = _dict.get('kms_public_endpoint')
        if 'keys' in _dict:
            args['keys'] = [KMSInstancesKeysItem.from_dict(x) for x in _dict.get('keys')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSInstances object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'encryption_scheme') and self.encryption_scheme is not None:
            _dict['encryption_scheme'] = self.encryption_scheme
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'kms_crn') and self.kms_crn is not None:
            _dict['kms_crn'] = self.kms_crn
        if hasattr(self, 'kms_name') and self.kms_name is not None:
            _dict['kms_name'] = self.kms_name
        if hasattr(self, 'kms_private_endpoint') and self.kms_private_endpoint is not None:
            _dict['kms_private_endpoint'] = self.kms_private_endpoint
        if hasattr(self, 'kms_public_endpoint') and self.kms_public_endpoint is not None:
            _dict['kms_public_endpoint'] = self.kms_public_endpoint
        if hasattr(self, 'keys') and self.keys is not None:
            _dict['keys'] = [x.to_dict() for x in self.keys]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSInstances object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSInstances') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSInstances') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class KMSInstancesKeysItem():
    """
    KMSInstancesKeysItem.

    :attr str name: (optional) Key name.
    :attr str crn: (optional) CRN of the Key.
    :attr str error: (optional) Error message.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 crn: str = None,
                 error: str = None) -> None:
        """
        Initialize a KMSInstancesKeysItem object.

        :param str name: (optional) Key name.
        :param str crn: (optional) CRN of the Key.
        :param str error: (optional) Error message.
        """
        self.name = name
        self.crn = crn
        self.error = error

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSInstancesKeysItem':
        """Initialize a KMSInstancesKeysItem object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'crn' in _dict:
            args['crn'] = _dict.get('crn')
        if 'error' in _dict:
            args['error'] = _dict.get('error')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSInstancesKeysItem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'crn') and self.crn is not None:
            _dict['crn'] = self.crn
        if hasattr(self, 'error') and self.error is not None:
            _dict['error'] = self.error
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSInstancesKeysItem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSInstancesKeysItem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSInstancesKeysItem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class KMSSettings():
    """
    User defined KMS Settings details.

    :attr str location: (optional) Location.
    :attr str encryption_scheme: (optional) Encryption scheme.
    :attr str resource_group: (optional) Resource group.
    :attr KMSSettingsPrimaryCrk primary_crk: (optional) Primary CRK details.
    :attr KMSSettingsSecondaryCrk secondary_crk: (optional) Secondary CRK details.
    """

    def __init__(self,
                 *,
                 location: str = None,
                 encryption_scheme: str = None,
                 resource_group: str = None,
                 primary_crk: 'KMSSettingsPrimaryCrk' = None,
                 secondary_crk: 'KMSSettingsSecondaryCrk' = None) -> None:
        """
        Initialize a KMSSettings object.

        :param str location: (optional) Location.
        :param str encryption_scheme: (optional) Encryption scheme.
        :param str resource_group: (optional) Resource group.
        :param KMSSettingsPrimaryCrk primary_crk: (optional) Primary CRK details.
        :param KMSSettingsSecondaryCrk secondary_crk: (optional) Secondary CRK
               details.
        """
        self.location = location
        self.encryption_scheme = encryption_scheme
        self.resource_group = resource_group
        self.primary_crk = primary_crk
        self.secondary_crk = secondary_crk

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSSettings':
        """Initialize a KMSSettings object from a json dictionary."""
        args = {}
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'encryption_scheme' in _dict:
            args['encryption_scheme'] = _dict.get('encryption_scheme')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'primary_crk' in _dict:
            args['primary_crk'] = KMSSettingsPrimaryCrk.from_dict(_dict.get('primary_crk'))
        if 'secondary_crk' in _dict:
            args['secondary_crk'] = KMSSettingsSecondaryCrk.from_dict(_dict.get('secondary_crk'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSSettings object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'encryption_scheme') and self.encryption_scheme is not None:
            _dict['encryption_scheme'] = self.encryption_scheme
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'primary_crk') and self.primary_crk is not None:
            _dict['primary_crk'] = self.primary_crk.to_dict()
        if hasattr(self, 'secondary_crk') and self.secondary_crk is not None:
            _dict['secondary_crk'] = self.secondary_crk.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSSettings object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSSettings') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSSettings') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class KMSSettingsPrimaryCrk():
    """
    Primary CRK details.

    :attr str kms_name: (optional) Primary KMS name.
    :attr str kms_private_endpoint: (optional) Primary KMS endpoint.
    :attr str key_crn: (optional) CRN of the Primary Key.
    """

    def __init__(self,
                 *,
                 kms_name: str = None,
                 kms_private_endpoint: str = None,
                 key_crn: str = None) -> None:
        """
        Initialize a KMSSettingsPrimaryCrk object.

        :param str kms_name: (optional) Primary KMS name.
        :param str kms_private_endpoint: (optional) Primary KMS endpoint.
        :param str key_crn: (optional) CRN of the Primary Key.
        """
        self.kms_name = kms_name
        self.kms_private_endpoint = kms_private_endpoint
        self.key_crn = key_crn

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSSettingsPrimaryCrk':
        """Initialize a KMSSettingsPrimaryCrk object from a json dictionary."""
        args = {}
        if 'kms_name' in _dict:
            args['kms_name'] = _dict.get('kms_name')
        if 'kms_private_endpoint' in _dict:
            args['kms_private_endpoint'] = _dict.get('kms_private_endpoint')
        if 'key_crn' in _dict:
            args['key_crn'] = _dict.get('key_crn')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSSettingsPrimaryCrk object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'kms_name') and self.kms_name is not None:
            _dict['kms_name'] = self.kms_name
        if hasattr(self, 'kms_private_endpoint') and self.kms_private_endpoint is not None:
            _dict['kms_private_endpoint'] = self.kms_private_endpoint
        if hasattr(self, 'key_crn') and self.key_crn is not None:
            _dict['key_crn'] = self.key_crn
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSSettingsPrimaryCrk object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSSettingsPrimaryCrk') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSSettingsPrimaryCrk') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class KMSSettingsSecondaryCrk():
    """
    Secondary CRK details.

    :attr str kms_name: (optional) Secondary KMS name.
    :attr str kms_private_endpoint: (optional) Secondary KMS endpoint.
    :attr str key_crn: (optional) CRN of the Secondary Key.
    """

    def __init__(self,
                 *,
                 kms_name: str = None,
                 kms_private_endpoint: str = None,
                 key_crn: str = None) -> None:
        """
        Initialize a KMSSettingsSecondaryCrk object.

        :param str kms_name: (optional) Secondary KMS name.
        :param str kms_private_endpoint: (optional) Secondary KMS endpoint.
        :param str key_crn: (optional) CRN of the Secondary Key.
        """
        self.kms_name = kms_name
        self.kms_private_endpoint = kms_private_endpoint
        self.key_crn = key_crn

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSSettingsSecondaryCrk':
        """Initialize a KMSSettingsSecondaryCrk object from a json dictionary."""
        args = {}
        if 'kms_name' in _dict:
            args['kms_name'] = _dict.get('kms_name')
        if 'kms_private_endpoint' in _dict:
            args['kms_private_endpoint'] = _dict.get('kms_private_endpoint')
        if 'key_crn' in _dict:
            args['key_crn'] = _dict.get('key_crn')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSSettingsSecondaryCrk object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'kms_name') and self.kms_name is not None:
            _dict['kms_name'] = self.kms_name
        if hasattr(self, 'kms_private_endpoint') and self.kms_private_endpoint is not None:
            _dict['kms_private_endpoint'] = self.kms_private_endpoint
        if hasattr(self, 'key_crn') and self.key_crn is not None:
            _dict['key_crn'] = self.key_crn
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSSettingsSecondaryCrk object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSSettingsSecondaryCrk') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSSettingsSecondaryCrk') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class LogStoreResponse():
    """
    LogStoreResponse -.

    :attr str engine_name: (optional) Engine name.
    :attr str engine_version: (optional) Engine version.
    :attr str id: (optional) Engine id.
    :attr str log_store_url: (optional) Log store url.
    """

    def __init__(self,
                 *,
                 engine_name: str = None,
                 engine_version: str = None,
                 id: str = None,
                 log_store_url: str = None) -> None:
        """
        Initialize a LogStoreResponse object.

        :param str engine_name: (optional) Engine name.
        :param str engine_version: (optional) Engine version.
        :param str id: (optional) Engine id.
        :param str log_store_url: (optional) Log store url.
        """
        self.engine_name = engine_name
        self.engine_version = engine_version
        self.id = id
        self.log_store_url = log_store_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'LogStoreResponse':
        """Initialize a LogStoreResponse object from a json dictionary."""
        args = {}
        if 'engine_name' in _dict:
            args['engine_name'] = _dict.get('engine_name')
        if 'engine_version' in _dict:
            args['engine_version'] = _dict.get('engine_version')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'log_store_url' in _dict:
            args['log_store_url'] = _dict.get('log_store_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a LogStoreResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'engine_name') and self.engine_name is not None:
            _dict['engine_name'] = self.engine_name
        if hasattr(self, 'engine_version') and self.engine_version is not None:
            _dict['engine_version'] = self.engine_version
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'log_store_url') and self.log_store_url is not None:
            _dict['log_store_url'] = self.log_store_url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this LogStoreResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'LogStoreResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'LogStoreResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class LogStoreResponseList():
    """
    LogStoreResponseList -.

    :attr List[LogStoreResponse] runtime_data: (optional) Runtime data.
    """

    def __init__(self,
                 *,
                 runtime_data: List['LogStoreResponse'] = None) -> None:
        """
        Initialize a LogStoreResponseList object.

        :param List[LogStoreResponse] runtime_data: (optional) Runtime data.
        """
        self.runtime_data = runtime_data

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'LogStoreResponseList':
        """Initialize a LogStoreResponseList object from a json dictionary."""
        args = {}
        if 'runtime_data' in _dict:
            args['runtime_data'] = [LogStoreResponse.from_dict(x) for x in _dict.get('runtime_data')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a LogStoreResponseList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'runtime_data') and self.runtime_data is not None:
            _dict['runtime_data'] = [x.to_dict() for x in self.runtime_data]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this LogStoreResponseList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'LogStoreResponseList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'LogStoreResponseList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class LogSummary():
    """
    LogSummary ...

    :attr str activity_status: (optional) WorkspaceActivityStatus activity status
          type.
    :attr str detected_template_type: (optional) Template detected type.
    :attr int discarded_files: (optional) Numner of discarded files.
    :attr str error: (optional) Numner of errors in log.
    :attr int resources_added: (optional) Numner of resources added.
    :attr int resources_destroyed: (optional) Numner of resources destroyed.
    :attr int resources_modified: (optional) Numner of resources modified.
    :attr int scanned_files: (optional) Numner of filed scanned.
    :attr int template_variable_count: (optional) Numner of template variables.
    :attr float time_taken: (optional) Time takemn to perform activity.
    """

    def __init__(self,
                 *,
                 activity_status: str = None,
                 detected_template_type: str = None,
                 discarded_files: int = None,
                 error: str = None,
                 resources_added: int = None,
                 resources_destroyed: int = None,
                 resources_modified: int = None,
                 scanned_files: int = None,
                 template_variable_count: int = None,
                 time_taken: float = None) -> None:
        """
        Initialize a LogSummary object.

        :param str activity_status: (optional) WorkspaceActivityStatus activity
               status type.
        :param str detected_template_type: (optional) Template detected type.
        :param int discarded_files: (optional) Numner of discarded files.
        :param str error: (optional) Numner of errors in log.
        :param int resources_added: (optional) Numner of resources added.
        :param int resources_destroyed: (optional) Numner of resources destroyed.
        :param int resources_modified: (optional) Numner of resources modified.
        :param int scanned_files: (optional) Numner of filed scanned.
        :param int template_variable_count: (optional) Numner of template
               variables.
        :param float time_taken: (optional) Time takemn to perform activity.
        """
        self.activity_status = activity_status
        self.detected_template_type = detected_template_type
        self.discarded_files = discarded_files
        self.error = error
        self.resources_added = resources_added
        self.resources_destroyed = resources_destroyed
        self.resources_modified = resources_modified
        self.scanned_files = scanned_files
        self.template_variable_count = template_variable_count
        self.time_taken = time_taken

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'LogSummary':
        """Initialize a LogSummary object from a json dictionary."""
        args = {}
        if 'activity_status' in _dict:
            args['activity_status'] = _dict.get('activity_status')
        if 'detected_template_type' in _dict:
            args['detected_template_type'] = _dict.get('detected_template_type')
        if 'discarded_files' in _dict:
            args['discarded_files'] = _dict.get('discarded_files')
        if 'error' in _dict:
            args['error'] = _dict.get('error')
        if 'resources_added' in _dict:
            args['resources_added'] = _dict.get('resources_added')
        if 'resources_destroyed' in _dict:
            args['resources_destroyed'] = _dict.get('resources_destroyed')
        if 'resources_modified' in _dict:
            args['resources_modified'] = _dict.get('resources_modified')
        if 'scanned_files' in _dict:
            args['scanned_files'] = _dict.get('scanned_files')
        if 'template_variable_count' in _dict:
            args['template_variable_count'] = _dict.get('template_variable_count')
        if 'time_taken' in _dict:
            args['time_taken'] = _dict.get('time_taken')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a LogSummary object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activity_status') and self.activity_status is not None:
            _dict['activity_status'] = self.activity_status
        if hasattr(self, 'detected_template_type') and self.detected_template_type is not None:
            _dict['detected_template_type'] = self.detected_template_type
        if hasattr(self, 'discarded_files') and self.discarded_files is not None:
            _dict['discarded_files'] = self.discarded_files
        if hasattr(self, 'error') and self.error is not None:
            _dict['error'] = self.error
        if hasattr(self, 'resources_added') and self.resources_added is not None:
            _dict['resources_added'] = self.resources_added
        if hasattr(self, 'resources_destroyed') and self.resources_destroyed is not None:
            _dict['resources_destroyed'] = self.resources_destroyed
        if hasattr(self, 'resources_modified') and self.resources_modified is not None:
            _dict['resources_modified'] = self.resources_modified
        if hasattr(self, 'scanned_files') and self.scanned_files is not None:
            _dict['scanned_files'] = self.scanned_files
        if hasattr(self, 'template_variable_count') and self.template_variable_count is not None:
            _dict['template_variable_count'] = self.template_variable_count
        if hasattr(self, 'time_taken') and self.time_taken is not None:
            _dict['time_taken'] = self.time_taken
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this LogSummary object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'LogSummary') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'LogSummary') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class OutputValuesItem():
    """
    OutputValuesItem.

    :attr str folder: (optional) Output variable name.
    :attr str id: (optional) Output variable id.
    :attr List[object] output_values: (optional) List of Output values.
    :attr str value_type: (optional) Output variable type.
    """

    def __init__(self,
                 *,
                 folder: str = None,
                 id: str = None,
                 output_values: List[object] = None,
                 value_type: str = None) -> None:
        """
        Initialize a OutputValuesItem object.

        :param str folder: (optional) Output variable name.
        :param str id: (optional) Output variable id.
        :param List[object] output_values: (optional) List of Output values.
        :param str value_type: (optional) Output variable type.
        """
        self.folder = folder
        self.id = id
        self.output_values = output_values
        self.value_type = value_type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'OutputValuesItem':
        """Initialize a OutputValuesItem object from a json dictionary."""
        args = {}
        if 'folder' in _dict:
            args['folder'] = _dict.get('folder')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'output_values' in _dict:
            args['output_values'] = _dict.get('output_values')
        if 'value_type' in _dict:
            args['value_type'] = _dict.get('value_type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a OutputValuesItem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'folder') and self.folder is not None:
            _dict['folder'] = self.folder
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'output_values') and self.output_values is not None:
            _dict['output_values'] = self.output_values
        if hasattr(self, 'value_type') and self.value_type is not None:
            _dict['value_type'] = self.value_type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this OutputValuesItem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'OutputValuesItem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'OutputValuesItem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceGroupResponse():
    """
    ResourceGroupResponse -.

    :attr str account_id: (optional) Account id.
    :attr str crn: (optional) CRN.
    :attr bool default: (optional) default.
    :attr str name: (optional) Resource group name.
    :attr str resource_group_id: (optional) Resource group id.
    :attr str state: (optional) Resource group state.
    """

    def __init__(self,
                 *,
                 account_id: str = None,
                 crn: str = None,
                 default: bool = None,
                 name: str = None,
                 resource_group_id: str = None,
                 state: str = None) -> None:
        """
        Initialize a ResourceGroupResponse object.

        :param str account_id: (optional) Account id.
        :param str crn: (optional) CRN.
        :param bool default: (optional) default.
        :param str name: (optional) Resource group name.
        :param str resource_group_id: (optional) Resource group id.
        :param str state: (optional) Resource group state.
        """
        self.account_id = account_id
        self.crn = crn
        self.default = default
        self.name = name
        self.resource_group_id = resource_group_id
        self.state = state

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceGroupResponse':
        """Initialize a ResourceGroupResponse object from a json dictionary."""
        args = {}
        if 'account_id' in _dict:
            args['account_id'] = _dict.get('account_id')
        if 'crn' in _dict:
            args['crn'] = _dict.get('crn')
        if 'default' in _dict:
            args['default'] = _dict.get('default')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'resource_group_id' in _dict:
            args['resource_group_id'] = _dict.get('resource_group_id')
        if 'state' in _dict:
            args['state'] = _dict.get('state')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceGroupResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'account_id') and self.account_id is not None:
            _dict['account_id'] = self.account_id
        if hasattr(self, 'crn') and self.crn is not None:
            _dict['crn'] = self.crn
        if hasattr(self, 'default') and self.default is not None:
            _dict['default'] = self.default
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'resource_group_id') and self.resource_group_id is not None:
            _dict['resource_group_id'] = self.resource_group_id
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceGroupResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceGroupResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceGroupResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceQuery():
    """
    Describe resource query.

    :attr str query_type: (optional) Type of the query(workspaces).
    :attr List[ResourceQueryParam] query_condition: (optional)
    :attr List[str] query_select: (optional) List of query selection parameters.
    """

    def __init__(self,
                 *,
                 query_type: str = None,
                 query_condition: List['ResourceQueryParam'] = None,
                 query_select: List[str] = None) -> None:
        """
        Initialize a ResourceQuery object.

        :param str query_type: (optional) Type of the query(workspaces).
        :param List[ResourceQueryParam] query_condition: (optional)
        :param List[str] query_select: (optional) List of query selection
               parameters.
        """
        self.query_type = query_type
        self.query_condition = query_condition
        self.query_select = query_select

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQuery':
        """Initialize a ResourceQuery object from a json dictionary."""
        args = {}
        if 'query_type' in _dict:
            args['query_type'] = _dict.get('query_type')
        if 'query_condition' in _dict:
            args['query_condition'] = [ResourceQueryParam.from_dict(x) for x in _dict.get('query_condition')]
        if 'query_select' in _dict:
            args['query_select'] = _dict.get('query_select')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQuery object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'query_type') and self.query_type is not None:
            _dict['query_type'] = self.query_type
        if hasattr(self, 'query_condition') and self.query_condition is not None:
            _dict['query_condition'] = [x.to_dict() for x in self.query_condition]
        if hasattr(self, 'query_select') and self.query_select is not None:
            _dict['query_select'] = self.query_select
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQuery object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQuery') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQuery') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class QueryTypeEnum(str, Enum):
        """
        Type of the query(workspaces).
        """
        WORKSPACES = 'workspaces'


class ResourceQueryParam():
    """
    Describe resource query param.

    :attr str name: (optional) Name of the resource query param.
    :attr str value: (optional) Value of the resource query param.
    :attr str description: (optional) Description of resource query param variable.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 value: str = None,
                 description: str = None) -> None:
        """
        Initialize a ResourceQueryParam object.

        :param str name: (optional) Name of the resource query param.
        :param str value: (optional) Value of the resource query param.
        :param str description: (optional) Description of resource query param
               variable.
        """
        self.name = name
        self.value = value
        self.description = description

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryParam':
        """Initialize a ResourceQueryParam object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryParam object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryParam object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryParam') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryParam') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceQueryRecord():
    """
    Describe resource query record.

    :attr str type: (optional) Resource type (cluster, vsi, icd, vpc).
    :attr str name: (optional) Resource query name.
    :attr str id: (optional) Resource Query id.
    :attr datetime created_at: (optional) Resource query creation time.
    :attr str created_by: (optional) Email address of user who created the Resource
          query.
    :attr datetime updated_at: (optional) Resource query updation time.
    :attr str updated_by: (optional) Email address of user who updated the Resource
          query.
    :attr List[ResourceQuery] queries: (optional)
    """

    def __init__(self,
                 *,
                 type: str = None,
                 name: str = None,
                 id: str = None,
                 created_at: datetime = None,
                 created_by: str = None,
                 updated_at: datetime = None,
                 updated_by: str = None,
                 queries: List['ResourceQuery'] = None) -> None:
        """
        Initialize a ResourceQueryRecord object.

        :param str type: (optional) Resource type (cluster, vsi, icd, vpc).
        :param str name: (optional) Resource query name.
        :param List[ResourceQuery] queries: (optional)
        """
        self.type = type
        self.name = name
        self.id = id
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.queries = queries

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryRecord':
        """Initialize a ResourceQueryRecord object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'created_at' in _dict:
            args['created_at'] = string_to_datetime(_dict.get('created_at'))
        if 'created_by' in _dict:
            args['created_by'] = _dict.get('created_by')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'updated_by' in _dict:
            args['updated_by'] = _dict.get('updated_by')
        if 'queries' in _dict:
            args['queries'] = [ResourceQuery.from_dict(x) for x in _dict.get('queries')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryRecord object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'id') and getattr(self, 'id') is not None:
            _dict['id'] = getattr(self, 'id')
        if hasattr(self, 'created_at') and getattr(self, 'created_at') is not None:
            _dict['created_at'] = datetime_to_string(getattr(self, 'created_at'))
        if hasattr(self, 'created_by') and getattr(self, 'created_by') is not None:
            _dict['created_by'] = getattr(self, 'created_by')
        if hasattr(self, 'updated_at') and getattr(self, 'updated_at') is not None:
            _dict['updated_at'] = datetime_to_string(getattr(self, 'updated_at'))
        if hasattr(self, 'updated_by') and getattr(self, 'updated_by') is not None:
            _dict['updated_by'] = getattr(self, 'updated_by')
        if hasattr(self, 'queries') and self.queries is not None:
            _dict['queries'] = [x.to_dict() for x in self.queries]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryRecord object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryRecord') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryRecord') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class TypeEnum(str, Enum):
        """
        Resource type (cluster, vsi, icd, vpc).
        """
        VSI = 'vsi'


class ResourceQueryRecordList():
    """
    List of Resource query records.

    :attr int total_count: (optional) Total number of records.
    :attr int limit: Number of records returned.
    :attr int offset: Skipped number of records.
    :attr List[ResourceQueryRecord] resource_queries: (optional) List of resource
          query records.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 total_count: int = None,
                 resource_queries: List['ResourceQueryRecord'] = None) -> None:
        """
        Initialize a ResourceQueryRecordList object.

        :param int limit: Number of records returned.
        :param int offset: Skipped number of records.
        :param int total_count: (optional) Total number of records.
        :param List[ResourceQueryRecord] resource_queries: (optional) List of
               resource query records.
        """
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.resource_queries = resource_queries

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryRecordList':
        """Initialize a ResourceQueryRecordList object from a json dictionary."""
        args = {}
        if 'total_count' in _dict:
            args['total_count'] = _dict.get('total_count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in ResourceQueryRecordList JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in ResourceQueryRecordList JSON')
        if 'ResourceQueries' in _dict:
            args['resource_queries'] = [ResourceQueryRecord.from_dict(x) for x in _dict.get('ResourceQueries')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryRecordList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'total_count') and self.total_count is not None:
            _dict['total_count'] = self.total_count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'resource_queries') and self.resource_queries is not None:
            _dict['ResourceQueries'] = [x.to_dict() for x in self.resource_queries]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryRecordList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryRecordList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryRecordList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceQueryResponseRecord():
    """
    Describe resource query.

    :attr List[ResourceQueryResponseRecordResponseItem] response: (optional)
    """

    def __init__(self,
                 *,
                 response: List['ResourceQueryResponseRecordResponseItem'] = None) -> None:
        """
        Initialize a ResourceQueryResponseRecord object.

        :param List[ResourceQueryResponseRecordResponseItem] response: (optional)
        """
        self.response = response

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryResponseRecord':
        """Initialize a ResourceQueryResponseRecord object from a json dictionary."""
        args = {}
        if 'response' in _dict:
            args['response'] = [ResourceQueryResponseRecordResponseItem.from_dict(x) for x in _dict.get('response')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryResponseRecord object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'response') and self.response is not None:
            _dict['response'] = [x.to_dict() for x in self.response]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryResponseRecord object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryResponseRecord') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryResponseRecord') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceQueryResponseRecordResponseItem():
    """
    ResourceQueryResponseRecordResponseItem.

    :attr str query_type: (optional) Type of the query(workspaces).
    :attr List[ResourceQueryParam] query_condition: (optional)
    :attr List[str] query_select: (optional) List of query selection parameters.
    :attr List[ResourceQueryResponseRecordResponseItemQueryOutputItem] query_output:
          (optional)
    """

    def __init__(self,
                 *,
                 query_type: str = None,
                 query_condition: List['ResourceQueryParam'] = None,
                 query_select: List[str] = None,
                 query_output: List['ResourceQueryResponseRecordResponseItemQueryOutputItem'] = None) -> None:
        """
        Initialize a ResourceQueryResponseRecordResponseItem object.

        :param str query_type: (optional) Type of the query(workspaces).
        :param List[ResourceQueryParam] query_condition: (optional)
        :param List[str] query_select: (optional) List of query selection
               parameters.
        :param List[ResourceQueryResponseRecordResponseItemQueryOutputItem]
               query_output: (optional)
        """
        self.query_type = query_type
        self.query_condition = query_condition
        self.query_select = query_select
        self.query_output = query_output

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryResponseRecordResponseItem':
        """Initialize a ResourceQueryResponseRecordResponseItem object from a json dictionary."""
        args = {}
        if 'query_type' in _dict:
            args['query_type'] = _dict.get('query_type')
        if 'query_condition' in _dict:
            args['query_condition'] = [ResourceQueryParam.from_dict(x) for x in _dict.get('query_condition')]
        if 'query_select' in _dict:
            args['query_select'] = _dict.get('query_select')
        if 'query_output' in _dict:
            args['query_output'] = [ResourceQueryResponseRecordResponseItemQueryOutputItem.from_dict(x) for x in _dict.get('query_output')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryResponseRecordResponseItem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'query_type') and self.query_type is not None:
            _dict['query_type'] = self.query_type
        if hasattr(self, 'query_condition') and self.query_condition is not None:
            _dict['query_condition'] = [x.to_dict() for x in self.query_condition]
        if hasattr(self, 'query_select') and self.query_select is not None:
            _dict['query_select'] = self.query_select
        if hasattr(self, 'query_output') and self.query_output is not None:
            _dict['query_output'] = [x.to_dict() for x in self.query_output]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryResponseRecordResponseItem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryResponseRecordResponseItem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryResponseRecordResponseItem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class QueryTypeEnum(str, Enum):
        """
        Type of the query(workspaces).
        """
        WORKSPACES = 'workspaces'


class ResourceQueryResponseRecordResponseItemQueryOutputItem():
    """
    List of query output values.

    :attr str name: (optional) Name of the output param.
    :attr str value: (optional) value of the output param.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 value: str = None) -> None:
        """
        Initialize a ResourceQueryResponseRecordResponseItemQueryOutputItem object.

        :param str name: (optional) Name of the output param.
        :param str value: (optional) value of the output param.
        """
        self.name = name
        self.value = value

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryResponseRecordResponseItemQueryOutputItem':
        """Initialize a ResourceQueryResponseRecordResponseItemQueryOutputItem object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryResponseRecordResponseItemQueryOutputItem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryResponseRecordResponseItemQueryOutputItem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryResponseRecordResponseItemQueryOutputItem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryResponseRecordResponseItemQueryOutputItem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SchematicsLocations():
    """
    Schematics locations.

    :attr str country: (optional) Country.
    :attr str geography: (optional) Geography.
    :attr str id: (optional) Location id.
    :attr str kind: (optional) Kind.
    :attr str metro: (optional) Metro.
    :attr str multizone_metro: (optional) Multizone metro.
    :attr str name: (optional) Location name.
    """

    def __init__(self,
                 *,
                 country: str = None,
                 geography: str = None,
                 id: str = None,
                 kind: str = None,
                 metro: str = None,
                 multizone_metro: str = None,
                 name: str = None) -> None:
        """
        Initialize a SchematicsLocations object.

        :param str country: (optional) Country.
        :param str geography: (optional) Geography.
        :param str id: (optional) Location id.
        :param str kind: (optional) Kind.
        :param str metro: (optional) Metro.
        :param str multizone_metro: (optional) Multizone metro.
        :param str name: (optional) Location name.
        """
        self.country = country
        self.geography = geography
        self.id = id
        self.kind = kind
        self.metro = metro
        self.multizone_metro = multizone_metro
        self.name = name

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SchematicsLocations':
        """Initialize a SchematicsLocations object from a json dictionary."""
        args = {}
        if 'country' in _dict:
            args['country'] = _dict.get('country')
        if 'geography' in _dict:
            args['geography'] = _dict.get('geography')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'kind' in _dict:
            args['kind'] = _dict.get('kind')
        if 'metro' in _dict:
            args['metro'] = _dict.get('metro')
        if 'multizone_metro' in _dict:
            args['multizone_metro'] = _dict.get('multizone_metro')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SchematicsLocations object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'country') and self.country is not None:
            _dict['country'] = self.country
        if hasattr(self, 'geography') and self.geography is not None:
            _dict['geography'] = self.geography
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'kind') and self.kind is not None:
            _dict['kind'] = self.kind
        if hasattr(self, 'metro') and self.metro is not None:
            _dict['metro'] = self.metro
        if hasattr(self, 'multizone_metro') and self.multizone_metro is not None:
            _dict['multizone_metro'] = self.multizone_metro
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SchematicsLocations object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SchematicsLocations') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SchematicsLocations') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SharedDatasetData():
    """
    SharedDatasetData ...

    :attr str default_value: (optional) Default values.
    :attr str description: (optional) Data description.
    :attr bool hidden: (optional) Data is hidden.
    :attr bool immutable: (optional) Data is readonly.
    :attr str matches: (optional) Data is matches regular expression.
    :attr str max_value: (optional) Max value of the data.
    :attr str max_value_len: (optional) Max string length of the data.
    :attr str min_value: (optional) Min value of the data.
    :attr str min_value_len: (optional) Min string length of the data.
    :attr List[str] options: (optional) Possible options for the Data.
    :attr str override_value: (optional) Override value for the Data.
    :attr bool secure: (optional) Data is secure.
    :attr List[str] var_aliases: (optional) Alias strings for the variable names.
    :attr str var_name: (optional) Variable name.
    :attr str var_ref: (optional) Variable reference.
    :attr str var_type: (optional) Variable type.
    """

    def __init__(self,
                 *,
                 default_value: str = None,
                 description: str = None,
                 hidden: bool = None,
                 immutable: bool = None,
                 matches: str = None,
                 max_value: str = None,
                 max_value_len: str = None,
                 min_value: str = None,
                 min_value_len: str = None,
                 options: List[str] = None,
                 override_value: str = None,
                 secure: bool = None,
                 var_aliases: List[str] = None,
                 var_name: str = None,
                 var_ref: str = None,
                 var_type: str = None) -> None:
        """
        Initialize a SharedDatasetData object.

        :param str default_value: (optional) Default values.
        :param str description: (optional) Data description.
        :param bool hidden: (optional) Data is hidden.
        :param bool immutable: (optional) Data is readonly.
        :param str matches: (optional) Data is matches regular expression.
        :param str max_value: (optional) Max value of the data.
        :param str max_value_len: (optional) Max string length of the data.
        :param str min_value: (optional) Min value of the data.
        :param str min_value_len: (optional) Min string length of the data.
        :param List[str] options: (optional) Possible options for the Data.
        :param str override_value: (optional) Override value for the Data.
        :param bool secure: (optional) Data is secure.
        :param List[str] var_aliases: (optional) Alias strings for the variable
               names.
        :param str var_name: (optional) Variable name.
        :param str var_ref: (optional) Variable reference.
        :param str var_type: (optional) Variable type.
        """
        self.default_value = default_value
        self.description = description
        self.hidden = hidden
        self.immutable = immutable
        self.matches = matches
        self.max_value = max_value
        self.max_value_len = max_value_len
        self.min_value = min_value
        self.min_value_len = min_value_len
        self.options = options
        self.override_value = override_value
        self.secure = secure
        self.var_aliases = var_aliases
        self.var_name = var_name
        self.var_ref = var_ref
        self.var_type = var_type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SharedDatasetData':
        """Initialize a SharedDatasetData object from a json dictionary."""
        args = {}
        if 'default_value' in _dict:
            args['default_value'] = _dict.get('default_value')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'hidden' in _dict:
            args['hidden'] = _dict.get('hidden')
        if 'immutable' in _dict:
            args['immutable'] = _dict.get('immutable')
        if 'matches' in _dict:
            args['matches'] = _dict.get('matches')
        if 'max_value' in _dict:
            args['max_value'] = _dict.get('max_value')
        if 'max_value_len' in _dict:
            args['max_value_len'] = _dict.get('max_value_len')
        if 'min_value' in _dict:
            args['min_value'] = _dict.get('min_value')
        if 'min_value_len' in _dict:
            args['min_value_len'] = _dict.get('min_value_len')
        if 'options' in _dict:
            args['options'] = _dict.get('options')
        if 'override_value' in _dict:
            args['override_value'] = _dict.get('override_value')
        if 'secure' in _dict:
            args['secure'] = _dict.get('secure')
        if 'var_aliases' in _dict:
            args['var_aliases'] = _dict.get('var_aliases')
        if 'var_name' in _dict:
            args['var_name'] = _dict.get('var_name')
        if 'var_ref' in _dict:
            args['var_ref'] = _dict.get('var_ref')
        if 'var_type' in _dict:
            args['var_type'] = _dict.get('var_type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SharedDatasetData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'default_value') and self.default_value is not None:
            _dict['default_value'] = self.default_value
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'hidden') and self.hidden is not None:
            _dict['hidden'] = self.hidden
        if hasattr(self, 'immutable') and self.immutable is not None:
            _dict['immutable'] = self.immutable
        if hasattr(self, 'matches') and self.matches is not None:
            _dict['matches'] = self.matches
        if hasattr(self, 'max_value') and self.max_value is not None:
            _dict['max_value'] = self.max_value
        if hasattr(self, 'max_value_len') and self.max_value_len is not None:
            _dict['max_value_len'] = self.max_value_len
        if hasattr(self, 'min_value') and self.min_value is not None:
            _dict['min_value'] = self.min_value
        if hasattr(self, 'min_value_len') and self.min_value_len is not None:
            _dict['min_value_len'] = self.min_value_len
        if hasattr(self, 'options') and self.options is not None:
            _dict['options'] = self.options
        if hasattr(self, 'override_value') and self.override_value is not None:
            _dict['override_value'] = self.override_value
        if hasattr(self, 'secure') and self.secure is not None:
            _dict['secure'] = self.secure
        if hasattr(self, 'var_aliases') and self.var_aliases is not None:
            _dict['var_aliases'] = self.var_aliases
        if hasattr(self, 'var_name') and self.var_name is not None:
            _dict['var_name'] = self.var_name
        if hasattr(self, 'var_ref') and self.var_ref is not None:
            _dict['var_ref'] = self.var_ref
        if hasattr(self, 'var_type') and self.var_type is not None:
            _dict['var_type'] = self.var_type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SharedDatasetData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SharedDatasetData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SharedDatasetData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SharedDatasetResponse():
    """
    SharedDatasetResponse - request returned by create.

    :attr str account: (optional) Account id.
    :attr datetime created_at: (optional) Dataset created at.
    :attr str created_by: (optional) Dataset created by.
    :attr str description: (optional) Dataset description.
    :attr List[str] effected_workspace_ids: (optional) Affected workspace id.
    :attr str resource_group: (optional) Resource group name.
    :attr List[SharedDatasetData] shared_dataset_data: (optional) Shared dataset
          data.
    :attr str shared_dataset_id: (optional) Shared dataset id.
    :attr str shared_dataset_name: (optional) Shared dataset name.
    :attr List[str] shared_dataset_type: (optional) Shared dataset type.
    :attr str state: (optional) shareddata variable status type.
    :attr List[str] tags: (optional) Shared dataset tags.
    :attr datetime updated_at: (optional) Shared dataset updated at.
    :attr str updated_by: (optional) Shared dataset updated by.
    :attr str version: (optional) Shared dataset version.
    """

    def __init__(self,
                 *,
                 account: str = None,
                 created_at: datetime = None,
                 created_by: str = None,
                 description: str = None,
                 effected_workspace_ids: List[str] = None,
                 resource_group: str = None,
                 shared_dataset_data: List['SharedDatasetData'] = None,
                 shared_dataset_id: str = None,
                 shared_dataset_name: str = None,
                 shared_dataset_type: List[str] = None,
                 state: str = None,
                 tags: List[str] = None,
                 updated_at: datetime = None,
                 updated_by: str = None,
                 version: str = None) -> None:
        """
        Initialize a SharedDatasetResponse object.

        :param str account: (optional) Account id.
        :param datetime created_at: (optional) Dataset created at.
        :param str created_by: (optional) Dataset created by.
        :param str description: (optional) Dataset description.
        :param List[str] effected_workspace_ids: (optional) Affected workspace id.
        :param str resource_group: (optional) Resource group name.
        :param List[SharedDatasetData] shared_dataset_data: (optional) Shared
               dataset data.
        :param str shared_dataset_id: (optional) Shared dataset id.
        :param str shared_dataset_name: (optional) Shared dataset name.
        :param List[str] shared_dataset_type: (optional) Shared dataset type.
        :param str state: (optional) shareddata variable status type.
        :param List[str] tags: (optional) Shared dataset tags.
        :param datetime updated_at: (optional) Shared dataset updated at.
        :param str updated_by: (optional) Shared dataset updated by.
        :param str version: (optional) Shared dataset version.
        """
        self.account = account
        self.created_at = created_at
        self.created_by = created_by
        self.description = description
        self.effected_workspace_ids = effected_workspace_ids
        self.resource_group = resource_group
        self.shared_dataset_data = shared_dataset_data
        self.shared_dataset_id = shared_dataset_id
        self.shared_dataset_name = shared_dataset_name
        self.shared_dataset_type = shared_dataset_type
        self.state = state
        self.tags = tags
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.version = version

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SharedDatasetResponse':
        """Initialize a SharedDatasetResponse object from a json dictionary."""
        args = {}
        if 'account' in _dict:
            args['account'] = _dict.get('account')
        if 'created_at' in _dict:
            args['created_at'] = string_to_datetime(_dict.get('created_at'))
        if 'created_by' in _dict:
            args['created_by'] = _dict.get('created_by')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'effected_workspace_ids' in _dict:
            args['effected_workspace_ids'] = _dict.get('effected_workspace_ids')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'shared_dataset_data' in _dict:
            args['shared_dataset_data'] = [SharedDatasetData.from_dict(x) for x in _dict.get('shared_dataset_data')]
        if 'shared_dataset_id' in _dict:
            args['shared_dataset_id'] = _dict.get('shared_dataset_id')
        if 'shared_dataset_name' in _dict:
            args['shared_dataset_name'] = _dict.get('shared_dataset_name')
        if 'shared_dataset_type' in _dict:
            args['shared_dataset_type'] = _dict.get('shared_dataset_type')
        if 'state' in _dict:
            args['state'] = _dict.get('state')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'updated_by' in _dict:
            args['updated_by'] = _dict.get('updated_by')
        if 'version' in _dict:
            args['version'] = _dict.get('version')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SharedDatasetResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'account') and self.account is not None:
            _dict['account'] = self.account
        if hasattr(self, 'created_at') and self.created_at is not None:
            _dict['created_at'] = datetime_to_string(self.created_at)
        if hasattr(self, 'created_by') and self.created_by is not None:
            _dict['created_by'] = self.created_by
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'effected_workspace_ids') and self.effected_workspace_ids is not None:
            _dict['effected_workspace_ids'] = self.effected_workspace_ids
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'shared_dataset_data') and self.shared_dataset_data is not None:
            _dict['shared_dataset_data'] = [x.to_dict() for x in self.shared_dataset_data]
        if hasattr(self, 'shared_dataset_id') and self.shared_dataset_id is not None:
            _dict['shared_dataset_id'] = self.shared_dataset_id
        if hasattr(self, 'shared_dataset_name') and self.shared_dataset_name is not None:
            _dict['shared_dataset_name'] = self.shared_dataset_name
        if hasattr(self, 'shared_dataset_type') and self.shared_dataset_type is not None:
            _dict['shared_dataset_type'] = self.shared_dataset_type
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        if hasattr(self, 'updated_by') and self.updated_by is not None:
            _dict['updated_by'] = self.updated_by
        if hasattr(self, 'version') and self.version is not None:
            _dict['version'] = self.version
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SharedDatasetResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SharedDatasetResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SharedDatasetResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SharedDatasetResponseList():
    """
    SharedDatasetResponseList -.

    :attr int count: (optional) Shared dataset count.
    :attr List[SharedDatasetResponse] shared_datasets: (optional) List of datasets.
    """

    def __init__(self,
                 *,
                 count: int = None,
                 shared_datasets: List['SharedDatasetResponse'] = None) -> None:
        """
        Initialize a SharedDatasetResponseList object.

        :param int count: (optional) Shared dataset count.
        :param List[SharedDatasetResponse] shared_datasets: (optional) List of
               datasets.
        """
        self.count = count
        self.shared_datasets = shared_datasets

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SharedDatasetResponseList':
        """Initialize a SharedDatasetResponseList object from a json dictionary."""
        args = {}
        if 'count' in _dict:
            args['count'] = _dict.get('count')
        if 'shared_datasets' in _dict:
            args['shared_datasets'] = [SharedDatasetResponse.from_dict(x) for x in _dict.get('shared_datasets')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SharedDatasetResponseList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'count') and self.count is not None:
            _dict['count'] = self.count
        if hasattr(self, 'shared_datasets') and self.shared_datasets is not None:
            _dict['shared_datasets'] = [x.to_dict() for x in self.shared_datasets]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SharedDatasetResponseList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SharedDatasetResponseList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SharedDatasetResponseList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SharedTargetData():
    """
    SharedTargetData -.

    :attr str cluster_created_on: (optional) Cluster created on.
    :attr str cluster_id: (optional) Cluster id.
    :attr str cluster_name: (optional) Cluster name.
    :attr str cluster_type: (optional) Cluster type.
    :attr List[object] entitlement_keys: (optional) Entitlement keys.
    :attr str namespace: (optional) Target namespace.
    :attr str region: (optional) Target region.
    :attr str resource_group_id: (optional) Target resource group id.
    :attr int worker_count: (optional) Cluster worker count.
    :attr str worker_machine_type: (optional) Cluster worker type.
    """

    def __init__(self,
                 *,
                 cluster_created_on: str = None,
                 cluster_id: str = None,
                 cluster_name: str = None,
                 cluster_type: str = None,
                 entitlement_keys: List[object] = None,
                 namespace: str = None,
                 region: str = None,
                 resource_group_id: str = None,
                 worker_count: int = None,
                 worker_machine_type: str = None) -> None:
        """
        Initialize a SharedTargetData object.

        :param str cluster_created_on: (optional) Cluster created on.
        :param str cluster_id: (optional) Cluster id.
        :param str cluster_name: (optional) Cluster name.
        :param str cluster_type: (optional) Cluster type.
        :param List[object] entitlement_keys: (optional) Entitlement keys.
        :param str namespace: (optional) Target namespace.
        :param str region: (optional) Target region.
        :param str resource_group_id: (optional) Target resource group id.
        :param int worker_count: (optional) Cluster worker count.
        :param str worker_machine_type: (optional) Cluster worker type.
        """
        self.cluster_created_on = cluster_created_on
        self.cluster_id = cluster_id
        self.cluster_name = cluster_name
        self.cluster_type = cluster_type
        self.entitlement_keys = entitlement_keys
        self.namespace = namespace
        self.region = region
        self.resource_group_id = resource_group_id
        self.worker_count = worker_count
        self.worker_machine_type = worker_machine_type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SharedTargetData':
        """Initialize a SharedTargetData object from a json dictionary."""
        args = {}
        if 'cluster_created_on' in _dict:
            args['cluster_created_on'] = _dict.get('cluster_created_on')
        if 'cluster_id' in _dict:
            args['cluster_id'] = _dict.get('cluster_id')
        if 'cluster_name' in _dict:
            args['cluster_name'] = _dict.get('cluster_name')
        if 'cluster_type' in _dict:
            args['cluster_type'] = _dict.get('cluster_type')
        if 'entitlement_keys' in _dict:
            args['entitlement_keys'] = _dict.get('entitlement_keys')
        if 'namespace' in _dict:
            args['namespace'] = _dict.get('namespace')
        if 'region' in _dict:
            args['region'] = _dict.get('region')
        if 'resource_group_id' in _dict:
            args['resource_group_id'] = _dict.get('resource_group_id')
        if 'worker_count' in _dict:
            args['worker_count'] = _dict.get('worker_count')
        if 'worker_machine_type' in _dict:
            args['worker_machine_type'] = _dict.get('worker_machine_type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SharedTargetData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cluster_created_on') and self.cluster_created_on is not None:
            _dict['cluster_created_on'] = self.cluster_created_on
        if hasattr(self, 'cluster_id') and self.cluster_id is not None:
            _dict['cluster_id'] = self.cluster_id
        if hasattr(self, 'cluster_name') and self.cluster_name is not None:
            _dict['cluster_name'] = self.cluster_name
        if hasattr(self, 'cluster_type') and self.cluster_type is not None:
            _dict['cluster_type'] = self.cluster_type
        if hasattr(self, 'entitlement_keys') and self.entitlement_keys is not None:
            _dict['entitlement_keys'] = self.entitlement_keys
        if hasattr(self, 'namespace') and self.namespace is not None:
            _dict['namespace'] = self.namespace
        if hasattr(self, 'region') and self.region is not None:
            _dict['region'] = self.region
        if hasattr(self, 'resource_group_id') and self.resource_group_id is not None:
            _dict['resource_group_id'] = self.resource_group_id
        if hasattr(self, 'worker_count') and self.worker_count is not None:
            _dict['worker_count'] = self.worker_count
        if hasattr(self, 'worker_machine_type') and self.worker_machine_type is not None:
            _dict['worker_machine_type'] = self.worker_machine_type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SharedTargetData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SharedTargetData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SharedTargetData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SharedTargetDataResponse():
    """
    SharedTargetDataResponse -.

    :attr str cluster_id: (optional) Target cluster id.
    :attr str cluster_name: (optional) Target cluster name.
    :attr List[object] entitlement_keys: (optional) Entitlement keys.
    :attr str namespace: (optional) Target namespace.
    :attr str region: (optional) Target region.
    :attr str resource_group_id: (optional) Target resource group id.
    """

    def __init__(self,
                 *,
                 cluster_id: str = None,
                 cluster_name: str = None,
                 entitlement_keys: List[object] = None,
                 namespace: str = None,
                 region: str = None,
                 resource_group_id: str = None) -> None:
        """
        Initialize a SharedTargetDataResponse object.

        :param str cluster_id: (optional) Target cluster id.
        :param str cluster_name: (optional) Target cluster name.
        :param List[object] entitlement_keys: (optional) Entitlement keys.
        :param str namespace: (optional) Target namespace.
        :param str region: (optional) Target region.
        :param str resource_group_id: (optional) Target resource group id.
        """
        self.cluster_id = cluster_id
        self.cluster_name = cluster_name
        self.entitlement_keys = entitlement_keys
        self.namespace = namespace
        self.region = region
        self.resource_group_id = resource_group_id

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SharedTargetDataResponse':
        """Initialize a SharedTargetDataResponse object from a json dictionary."""
        args = {}
        if 'cluster_id' in _dict:
            args['cluster_id'] = _dict.get('cluster_id')
        if 'cluster_name' in _dict:
            args['cluster_name'] = _dict.get('cluster_name')
        if 'entitlement_keys' in _dict:
            args['entitlement_keys'] = _dict.get('entitlement_keys')
        if 'namespace' in _dict:
            args['namespace'] = _dict.get('namespace')
        if 'region' in _dict:
            args['region'] = _dict.get('region')
        if 'resource_group_id' in _dict:
            args['resource_group_id'] = _dict.get('resource_group_id')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SharedTargetDataResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cluster_id') and self.cluster_id is not None:
            _dict['cluster_id'] = self.cluster_id
        if hasattr(self, 'cluster_name') and self.cluster_name is not None:
            _dict['cluster_name'] = self.cluster_name
        if hasattr(self, 'entitlement_keys') and self.entitlement_keys is not None:
            _dict['entitlement_keys'] = self.entitlement_keys
        if hasattr(self, 'namespace') and self.namespace is not None:
            _dict['namespace'] = self.namespace
        if hasattr(self, 'region') and self.region is not None:
            _dict['region'] = self.region
        if hasattr(self, 'resource_group_id') and self.resource_group_id is not None:
            _dict['resource_group_id'] = self.resource_group_id
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SharedTargetDataResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SharedTargetDataResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SharedTargetDataResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class StateStoreResponse():
    """
    StateStoreResponse -.

    :attr str engine_name: (optional) Engine name.
    :attr str engine_version: (optional) Engine version.
    :attr str id: (optional) State store id.
    :attr str state_store_url: (optional) State store url.
    """

    def __init__(self,
                 *,
                 engine_name: str = None,
                 engine_version: str = None,
                 id: str = None,
                 state_store_url: str = None) -> None:
        """
        Initialize a StateStoreResponse object.

        :param str engine_name: (optional) Engine name.
        :param str engine_version: (optional) Engine version.
        :param str id: (optional) State store id.
        :param str state_store_url: (optional) State store url.
        """
        self.engine_name = engine_name
        self.engine_version = engine_version
        self.id = id
        self.state_store_url = state_store_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'StateStoreResponse':
        """Initialize a StateStoreResponse object from a json dictionary."""
        args = {}
        if 'engine_name' in _dict:
            args['engine_name'] = _dict.get('engine_name')
        if 'engine_version' in _dict:
            args['engine_version'] = _dict.get('engine_version')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'state_store_url' in _dict:
            args['state_store_url'] = _dict.get('state_store_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a StateStoreResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'engine_name') and self.engine_name is not None:
            _dict['engine_name'] = self.engine_name
        if hasattr(self, 'engine_version') and self.engine_version is not None:
            _dict['engine_version'] = self.engine_version
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'state_store_url') and self.state_store_url is not None:
            _dict['state_store_url'] = self.state_store_url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this StateStoreResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'StateStoreResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'StateStoreResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class StateStoreResponseList():
    """
    StateStoreResponseList -.

    :attr List[StateStoreResponse] runtime_data: (optional) List of state stores.
    """

    def __init__(self,
                 *,
                 runtime_data: List['StateStoreResponse'] = None) -> None:
        """
        Initialize a StateStoreResponseList object.

        :param List[StateStoreResponse] runtime_data: (optional) List of state
               stores.
        """
        self.runtime_data = runtime_data

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'StateStoreResponseList':
        """Initialize a StateStoreResponseList object from a json dictionary."""
        args = {}
        if 'runtime_data' in _dict:
            args['runtime_data'] = [StateStoreResponse.from_dict(x) for x in _dict.get('runtime_data')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a StateStoreResponseList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'runtime_data') and self.runtime_data is not None:
            _dict['runtime_data'] = [x.to_dict() for x in self.runtime_data]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this StateStoreResponseList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'StateStoreResponseList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'StateStoreResponseList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SystemLock():
    """
    System lock status.

    :attr bool sys_locked: (optional) Is the Workspace locked by a Schematic action
          ?.
    :attr str sys_locked_by: (optional) Name of the User who performed the action,
          that lead to the locking of the Workspace.
    :attr datetime sys_locked_at: (optional) When the User performed the action that
          lead to locking of the Workspace ?.
    """

    def __init__(self,
                 *,
                 sys_locked: bool = None,
                 sys_locked_by: str = None,
                 sys_locked_at: datetime = None) -> None:
        """
        Initialize a SystemLock object.

        :param bool sys_locked: (optional) Is the Workspace locked by a Schematic
               action ?.
        :param str sys_locked_by: (optional) Name of the User who performed the
               action, that lead to the locking of the Workspace.
        :param datetime sys_locked_at: (optional) When the User performed the
               action that lead to locking of the Workspace ?.
        """
        self.sys_locked = sys_locked
        self.sys_locked_by = sys_locked_by
        self.sys_locked_at = sys_locked_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SystemLock':
        """Initialize a SystemLock object from a json dictionary."""
        args = {}
        if 'sys_locked' in _dict:
            args['sys_locked'] = _dict.get('sys_locked')
        if 'sys_locked_by' in _dict:
            args['sys_locked_by'] = _dict.get('sys_locked_by')
        if 'sys_locked_at' in _dict:
            args['sys_locked_at'] = string_to_datetime(_dict.get('sys_locked_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SystemLock object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'sys_locked') and self.sys_locked is not None:
            _dict['sys_locked'] = self.sys_locked
        if hasattr(self, 'sys_locked_by') and self.sys_locked_by is not None:
            _dict['sys_locked_by'] = self.sys_locked_by
        if hasattr(self, 'sys_locked_at') and self.sys_locked_at is not None:
            _dict['sys_locked_at'] = datetime_to_string(self.sys_locked_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SystemLock object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SystemLock') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SystemLock') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateReadme():
    """
    TemplateReadme -.

    :attr str readme: (optional) Readme string.
    """

    def __init__(self,
                 *,
                 readme: str = None) -> None:
        """
        Initialize a TemplateReadme object.

        :param str readme: (optional) Readme string.
        """
        self.readme = readme

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateReadme':
        """Initialize a TemplateReadme object from a json dictionary."""
        args = {}
        if 'readme' in _dict:
            args['readme'] = _dict.get('readme')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateReadme object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'readme') and self.readme is not None:
            _dict['readme'] = self.readme
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateReadme object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateReadme') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateReadme') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateRepoRequest():
    """
    TemplateRepoRequest -.

    :attr str branch: (optional) Repo branch.
    :attr str release: (optional) Repo release.
    :attr str repo_sha_value: (optional) Repo SHA value.
    :attr str repo_url: (optional) Repo URL.
    :attr str url: (optional) Source URL.
    """

    def __init__(self,
                 *,
                 branch: str = None,
                 release: str = None,
                 repo_sha_value: str = None,
                 repo_url: str = None,
                 url: str = None) -> None:
        """
        Initialize a TemplateRepoRequest object.

        :param str branch: (optional) Repo branch.
        :param str release: (optional) Repo release.
        :param str repo_sha_value: (optional) Repo SHA value.
        :param str repo_url: (optional) Repo URL.
        :param str url: (optional) Source URL.
        """
        self.branch = branch
        self.release = release
        self.repo_sha_value = repo_sha_value
        self.repo_url = repo_url
        self.url = url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateRepoRequest':
        """Initialize a TemplateRepoRequest object from a json dictionary."""
        args = {}
        if 'branch' in _dict:
            args['branch'] = _dict.get('branch')
        if 'release' in _dict:
            args['release'] = _dict.get('release')
        if 'repo_sha_value' in _dict:
            args['repo_sha_value'] = _dict.get('repo_sha_value')
        if 'repo_url' in _dict:
            args['repo_url'] = _dict.get('repo_url')
        if 'url' in _dict:
            args['url'] = _dict.get('url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateRepoRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'branch') and self.branch is not None:
            _dict['branch'] = self.branch
        if hasattr(self, 'release') and self.release is not None:
            _dict['release'] = self.release
        if hasattr(self, 'repo_sha_value') and self.repo_sha_value is not None:
            _dict['repo_sha_value'] = self.repo_sha_value
        if hasattr(self, 'repo_url') and self.repo_url is not None:
            _dict['repo_url'] = self.repo_url
        if hasattr(self, 'url') and self.url is not None:
            _dict['url'] = self.url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateRepoRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateRepoRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateRepoRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateRepoResponse():
    """
    TemplateRepoResponse -.

    :attr str branch: (optional) Repo branch.
    :attr str full_url: (optional) Full repo URL.
    :attr bool has_uploadedgitrepotar: (optional) Has uploaded git repo tar.
    :attr str release: (optional) Repo release.
    :attr str repo_sha_value: (optional) Repo SHA value.
    :attr str repo_url: (optional) Repo URL.
    :attr str url: (optional) Source URL.
    """

    def __init__(self,
                 *,
                 branch: str = None,
                 full_url: str = None,
                 has_uploadedgitrepotar: bool = None,
                 release: str = None,
                 repo_sha_value: str = None,
                 repo_url: str = None,
                 url: str = None) -> None:
        """
        Initialize a TemplateRepoResponse object.

        :param str branch: (optional) Repo branch.
        :param str full_url: (optional) Full repo URL.
        :param bool has_uploadedgitrepotar: (optional) Has uploaded git repo tar.
        :param str release: (optional) Repo release.
        :param str repo_sha_value: (optional) Repo SHA value.
        :param str repo_url: (optional) Repo URL.
        :param str url: (optional) Source URL.
        """
        self.branch = branch
        self.full_url = full_url
        self.has_uploadedgitrepotar = has_uploadedgitrepotar
        self.release = release
        self.repo_sha_value = repo_sha_value
        self.repo_url = repo_url
        self.url = url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateRepoResponse':
        """Initialize a TemplateRepoResponse object from a json dictionary."""
        args = {}
        if 'branch' in _dict:
            args['branch'] = _dict.get('branch')
        if 'full_url' in _dict:
            args['full_url'] = _dict.get('full_url')
        if 'has_uploadedgitrepotar' in _dict:
            args['has_uploadedgitrepotar'] = _dict.get('has_uploadedgitrepotar')
        if 'release' in _dict:
            args['release'] = _dict.get('release')
        if 'repo_sha_value' in _dict:
            args['repo_sha_value'] = _dict.get('repo_sha_value')
        if 'repo_url' in _dict:
            args['repo_url'] = _dict.get('repo_url')
        if 'url' in _dict:
            args['url'] = _dict.get('url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateRepoResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'branch') and self.branch is not None:
            _dict['branch'] = self.branch
        if hasattr(self, 'full_url') and self.full_url is not None:
            _dict['full_url'] = self.full_url
        if hasattr(self, 'has_uploadedgitrepotar') and self.has_uploadedgitrepotar is not None:
            _dict['has_uploadedgitrepotar'] = self.has_uploadedgitrepotar
        if hasattr(self, 'release') and self.release is not None:
            _dict['release'] = self.release
        if hasattr(self, 'repo_sha_value') and self.repo_sha_value is not None:
            _dict['repo_sha_value'] = self.repo_sha_value
        if hasattr(self, 'repo_url') and self.repo_url is not None:
            _dict['repo_url'] = self.repo_url
        if hasattr(self, 'url') and self.url is not None:
            _dict['url'] = self.url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateRepoResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateRepoResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateRepoResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateRepoTarUploadResponse():
    """
    TemplateRepoTarUploadResponse -.

    :attr str file_value: (optional) Tar file value.
    :attr bool has_received_file: (optional) Has received tar file.
    :attr str id: (optional) Template id.
    """

    def __init__(self,
                 *,
                 file_value: str = None,
                 has_received_file: bool = None,
                 id: str = None) -> None:
        """
        Initialize a TemplateRepoTarUploadResponse object.

        :param str file_value: (optional) Tar file value.
        :param bool has_received_file: (optional) Has received tar file.
        :param str id: (optional) Template id.
        """
        self.file_value = file_value
        self.has_received_file = has_received_file
        self.id = id

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateRepoTarUploadResponse':
        """Initialize a TemplateRepoTarUploadResponse object from a json dictionary."""
        args = {}
        if 'file_value' in _dict:
            args['file_value'] = _dict.get('file_value')
        if 'has_received_file' in _dict:
            args['has_received_file'] = _dict.get('has_received_file')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateRepoTarUploadResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'file_value') and self.file_value is not None:
            _dict['file_value'] = self.file_value
        if hasattr(self, 'has_received_file') and self.has_received_file is not None:
            _dict['has_received_file'] = self.has_received_file
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateRepoTarUploadResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateRepoTarUploadResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateRepoTarUploadResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateRepoUpdateRequest():
    """
    TemplateRepoUpdateRequest -.

    :attr str branch: (optional) Repo branch.
    :attr str release: (optional) Repo release.
    :attr str repo_sha_value: (optional) Repo SHA value.
    :attr str repo_url: (optional) Repo URL.
    :attr str url: (optional) Source URL.
    """

    def __init__(self,
                 *,
                 branch: str = None,
                 release: str = None,
                 repo_sha_value: str = None,
                 repo_url: str = None,
                 url: str = None) -> None:
        """
        Initialize a TemplateRepoUpdateRequest object.

        :param str branch: (optional) Repo branch.
        :param str release: (optional) Repo release.
        :param str repo_sha_value: (optional) Repo SHA value.
        :param str repo_url: (optional) Repo URL.
        :param str url: (optional) Source URL.
        """
        self.branch = branch
        self.release = release
        self.repo_sha_value = repo_sha_value
        self.repo_url = repo_url
        self.url = url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateRepoUpdateRequest':
        """Initialize a TemplateRepoUpdateRequest object from a json dictionary."""
        args = {}
        if 'branch' in _dict:
            args['branch'] = _dict.get('branch')
        if 'release' in _dict:
            args['release'] = _dict.get('release')
        if 'repo_sha_value' in _dict:
            args['repo_sha_value'] = _dict.get('repo_sha_value')
        if 'repo_url' in _dict:
            args['repo_url'] = _dict.get('repo_url')
        if 'url' in _dict:
            args['url'] = _dict.get('url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateRepoUpdateRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'branch') and self.branch is not None:
            _dict['branch'] = self.branch
        if hasattr(self, 'release') and self.release is not None:
            _dict['release'] = self.release
        if hasattr(self, 'repo_sha_value') and self.repo_sha_value is not None:
            _dict['repo_sha_value'] = self.repo_sha_value
        if hasattr(self, 'repo_url') and self.repo_url is not None:
            _dict['repo_url'] = self.repo_url
        if hasattr(self, 'url') and self.url is not None:
            _dict['url'] = self.url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateRepoUpdateRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateRepoUpdateRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateRepoUpdateRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateResources():
    """
    TemplateResources -.

    :attr str folder: (optional) Template folder name.
    :attr str id: (optional) Template id.
    :attr List[object] null_resources: (optional) List of null resources.
    :attr List[object] related_resources: (optional) List of related resources.
    :attr List[object] resources: (optional) List of resources.
    :attr int resources_count: (optional) Number of resources.
    :attr str template_type: (optional) Type of templaes.
    """

    def __init__(self,
                 *,
                 folder: str = None,
                 id: str = None,
                 null_resources: List[object] = None,
                 related_resources: List[object] = None,
                 resources: List[object] = None,
                 resources_count: int = None,
                 template_type: str = None) -> None:
        """
        Initialize a TemplateResources object.

        :param str folder: (optional) Template folder name.
        :param str id: (optional) Template id.
        :param List[object] null_resources: (optional) List of null resources.
        :param List[object] related_resources: (optional) List of related
               resources.
        :param List[object] resources: (optional) List of resources.
        :param int resources_count: (optional) Number of resources.
        :param str template_type: (optional) Type of templaes.
        """
        self.folder = folder
        self.id = id
        self.null_resources = null_resources
        self.related_resources = related_resources
        self.resources = resources
        self.resources_count = resources_count
        self.template_type = template_type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateResources':
        """Initialize a TemplateResources object from a json dictionary."""
        args = {}
        if 'folder' in _dict:
            args['folder'] = _dict.get('folder')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'null_resources' in _dict:
            args['null_resources'] = _dict.get('null_resources')
        if 'related_resources' in _dict:
            args['related_resources'] = _dict.get('related_resources')
        if 'resources' in _dict:
            args['resources'] = _dict.get('resources')
        if 'resources_count' in _dict:
            args['resources_count'] = _dict.get('resources_count')
        if 'template_type' in _dict:
            args['template_type'] = _dict.get('template_type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'folder') and self.folder is not None:
            _dict['folder'] = self.folder
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'null_resources') and self.null_resources is not None:
            _dict['null_resources'] = self.null_resources
        if hasattr(self, 'related_resources') and self.related_resources is not None:
            _dict['related_resources'] = self.related_resources
        if hasattr(self, 'resources') and self.resources is not None:
            _dict['resources'] = self.resources
        if hasattr(self, 'resources_count') and self.resources_count is not None:
            _dict['resources_count'] = self.resources_count
        if hasattr(self, 'template_type') and self.template_type is not None:
            _dict['template_type'] = self.template_type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateRunTimeDataResponse():
    """
    TemplateRunTimeDataResponse -.

    :attr str engine_cmd: (optional) Engine command.
    :attr str engine_name: (optional) Engine name.
    :attr str engine_version: (optional) Engine version.
    :attr str id: (optional) Template id.
    :attr str log_store_url: (optional) Log store url.
    :attr List[object] output_values: (optional) List of Output values.
    :attr List[List[object]] resources: (optional) List of resources.
    :attr str state_store_url: (optional) State store URL.
    """

    def __init__(self,
                 *,
                 engine_cmd: str = None,
                 engine_name: str = None,
                 engine_version: str = None,
                 id: str = None,
                 log_store_url: str = None,
                 output_values: List[object] = None,
                 resources: List[List[object]] = None,
                 state_store_url: str = None) -> None:
        """
        Initialize a TemplateRunTimeDataResponse object.

        :param str engine_cmd: (optional) Engine command.
        :param str engine_name: (optional) Engine name.
        :param str engine_version: (optional) Engine version.
        :param str id: (optional) Template id.
        :param str log_store_url: (optional) Log store url.
        :param List[object] output_values: (optional) List of Output values.
        :param List[List[object]] resources: (optional) List of resources.
        :param str state_store_url: (optional) State store URL.
        """
        self.engine_cmd = engine_cmd
        self.engine_name = engine_name
        self.engine_version = engine_version
        self.id = id
        self.log_store_url = log_store_url
        self.output_values = output_values
        self.resources = resources
        self.state_store_url = state_store_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateRunTimeDataResponse':
        """Initialize a TemplateRunTimeDataResponse object from a json dictionary."""
        args = {}
        if 'engine_cmd' in _dict:
            args['engine_cmd'] = _dict.get('engine_cmd')
        if 'engine_name' in _dict:
            args['engine_name'] = _dict.get('engine_name')
        if 'engine_version' in _dict:
            args['engine_version'] = _dict.get('engine_version')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'log_store_url' in _dict:
            args['log_store_url'] = _dict.get('log_store_url')
        if 'output_values' in _dict:
            args['output_values'] = _dict.get('output_values')
        if 'resources' in _dict:
            args['resources'] = _dict.get('resources')
        if 'state_store_url' in _dict:
            args['state_store_url'] = _dict.get('state_store_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateRunTimeDataResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'engine_cmd') and self.engine_cmd is not None:
            _dict['engine_cmd'] = self.engine_cmd
        if hasattr(self, 'engine_name') and self.engine_name is not None:
            _dict['engine_name'] = self.engine_name
        if hasattr(self, 'engine_version') and self.engine_version is not None:
            _dict['engine_version'] = self.engine_version
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'log_store_url') and self.log_store_url is not None:
            _dict['log_store_url'] = self.log_store_url
        if hasattr(self, 'output_values') and self.output_values is not None:
            _dict['output_values'] = self.output_values
        if hasattr(self, 'resources') and self.resources is not None:
            _dict['resources'] = self.resources
        if hasattr(self, 'state_store_url') and self.state_store_url is not None:
            _dict['state_store_url'] = self.state_store_url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateRunTimeDataResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateRunTimeDataResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateRunTimeDataResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateSourceDataRequest():
    """
    TemplateSourceDataRequest -.

    :attr List[object] env_values: (optional) EnvVariableRequest ..
    :attr str folder: (optional) Folder name.
    :attr str init_state_file: (optional) Init state file.
    :attr str type: (optional) Template type.
    :attr str uninstall_script_name: (optional) Uninstall script name.
    :attr str values: (optional) Value.
    :attr List[object] values_metadata: (optional) List of values metadata.
    :attr List[WorkspaceVariableRequest] variablestore: (optional) VariablesRequest
          -.
    """

    def __init__(self,
                 *,
                 env_values: List[object] = None,
                 folder: str = None,
                 init_state_file: str = None,
                 type: str = None,
                 uninstall_script_name: str = None,
                 values: str = None,
                 values_metadata: List[object] = None,
                 variablestore: List['WorkspaceVariableRequest'] = None) -> None:
        """
        Initialize a TemplateSourceDataRequest object.

        :param List[object] env_values: (optional) EnvVariableRequest ..
        :param str folder: (optional) Folder name.
        :param str init_state_file: (optional) Init state file.
        :param str type: (optional) Template type.
        :param str uninstall_script_name: (optional) Uninstall script name.
        :param str values: (optional) Value.
        :param List[object] values_metadata: (optional) List of values metadata.
        :param List[WorkspaceVariableRequest] variablestore: (optional)
               VariablesRequest -.
        """
        self.env_values = env_values
        self.folder = folder
        self.init_state_file = init_state_file
        self.type = type
        self.uninstall_script_name = uninstall_script_name
        self.values = values
        self.values_metadata = values_metadata
        self.variablestore = variablestore

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateSourceDataRequest':
        """Initialize a TemplateSourceDataRequest object from a json dictionary."""
        args = {}
        if 'env_values' in _dict:
            args['env_values'] = _dict.get('env_values')
        if 'folder' in _dict:
            args['folder'] = _dict.get('folder')
        if 'init_state_file' in _dict:
            args['init_state_file'] = _dict.get('init_state_file')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'uninstall_script_name' in _dict:
            args['uninstall_script_name'] = _dict.get('uninstall_script_name')
        if 'values' in _dict:
            args['values'] = _dict.get('values')
        if 'values_metadata' in _dict:
            args['values_metadata'] = _dict.get('values_metadata')
        if 'variablestore' in _dict:
            args['variablestore'] = [WorkspaceVariableRequest.from_dict(x) for x in _dict.get('variablestore')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateSourceDataRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'env_values') and self.env_values is not None:
            _dict['env_values'] = self.env_values
        if hasattr(self, 'folder') and self.folder is not None:
            _dict['folder'] = self.folder
        if hasattr(self, 'init_state_file') and self.init_state_file is not None:
            _dict['init_state_file'] = self.init_state_file
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'uninstall_script_name') and self.uninstall_script_name is not None:
            _dict['uninstall_script_name'] = self.uninstall_script_name
        if hasattr(self, 'values') and self.values is not None:
            _dict['values'] = self.values
        if hasattr(self, 'values_metadata') and self.values_metadata is not None:
            _dict['values_metadata'] = self.values_metadata
        if hasattr(self, 'variablestore') and self.variablestore is not None:
            _dict['variablestore'] = [x.to_dict() for x in self.variablestore]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateSourceDataRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateSourceDataRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateSourceDataRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateSourceDataResponse():
    """
    TemplateSourceDataResponse -.

    :attr List[EnvVariableResponse] env_values: (optional) List of environment
          values.
    :attr str folder: (optional) Folder name.
    :attr bool has_githubtoken: (optional) Has github token.
    :attr str id: (optional) Template id.
    :attr str type: (optional) Template tyoe.
    :attr str uninstall_script_name: (optional) Uninstall script name.
    :attr str values: (optional) Values.
    :attr List[object] values_metadata: (optional) List of values metadata.
    :attr str values_url: (optional) Values URL.
    :attr List[WorkspaceVariableResponse] variablestore: (optional)
          VariablesResponse -.
    """

    def __init__(self,
                 *,
                 env_values: List['EnvVariableResponse'] = None,
                 folder: str = None,
                 has_githubtoken: bool = None,
                 id: str = None,
                 type: str = None,
                 uninstall_script_name: str = None,
                 values: str = None,
                 values_metadata: List[object] = None,
                 values_url: str = None,
                 variablestore: List['WorkspaceVariableResponse'] = None) -> None:
        """
        Initialize a TemplateSourceDataResponse object.

        :param List[EnvVariableResponse] env_values: (optional) List of environment
               values.
        :param str folder: (optional) Folder name.
        :param bool has_githubtoken: (optional) Has github token.
        :param str id: (optional) Template id.
        :param str type: (optional) Template tyoe.
        :param str uninstall_script_name: (optional) Uninstall script name.
        :param str values: (optional) Values.
        :param List[object] values_metadata: (optional) List of values metadata.
        :param str values_url: (optional) Values URL.
        :param List[WorkspaceVariableResponse] variablestore: (optional)
               VariablesResponse -.
        """
        self.env_values = env_values
        self.folder = folder
        self.has_githubtoken = has_githubtoken
        self.id = id
        self.type = type
        self.uninstall_script_name = uninstall_script_name
        self.values = values
        self.values_metadata = values_metadata
        self.values_url = values_url
        self.variablestore = variablestore

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateSourceDataResponse':
        """Initialize a TemplateSourceDataResponse object from a json dictionary."""
        args = {}
        if 'env_values' in _dict:
            args['env_values'] = [EnvVariableResponse.from_dict(x) for x in _dict.get('env_values')]
        if 'folder' in _dict:
            args['folder'] = _dict.get('folder')
        if 'has_githubtoken' in _dict:
            args['has_githubtoken'] = _dict.get('has_githubtoken')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'uninstall_script_name' in _dict:
            args['uninstall_script_name'] = _dict.get('uninstall_script_name')
        if 'values' in _dict:
            args['values'] = _dict.get('values')
        if 'values_metadata' in _dict:
            args['values_metadata'] = _dict.get('values_metadata')
        if 'values_url' in _dict:
            args['values_url'] = _dict.get('values_url')
        if 'variablestore' in _dict:
            args['variablestore'] = [WorkspaceVariableResponse.from_dict(x) for x in _dict.get('variablestore')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateSourceDataResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'env_values') and self.env_values is not None:
            _dict['env_values'] = [x.to_dict() for x in self.env_values]
        if hasattr(self, 'folder') and self.folder is not None:
            _dict['folder'] = self.folder
        if hasattr(self, 'has_githubtoken') and self.has_githubtoken is not None:
            _dict['has_githubtoken'] = self.has_githubtoken
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'uninstall_script_name') and self.uninstall_script_name is not None:
            _dict['uninstall_script_name'] = self.uninstall_script_name
        if hasattr(self, 'values') and self.values is not None:
            _dict['values'] = self.values
        if hasattr(self, 'values_metadata') and self.values_metadata is not None:
            _dict['values_metadata'] = self.values_metadata
        if hasattr(self, 'values_url') and self.values_url is not None:
            _dict['values_url'] = self.values_url
        if hasattr(self, 'variablestore') and self.variablestore is not None:
            _dict['variablestore'] = [x.to_dict() for x in self.variablestore]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateSourceDataResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateSourceDataResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateSourceDataResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateStateStore():
    """
    TemplateStateStore -.

    :attr float version: (optional)
    :attr str terraform_version: (optional)
    :attr float serial: (optional)
    :attr str lineage: (optional)
    :attr List[object] modules: (optional)
    """

    def __init__(self,
                 *,
                 version: float = None,
                 terraform_version: str = None,
                 serial: float = None,
                 lineage: str = None,
                 modules: List[object] = None) -> None:
        """
        Initialize a TemplateStateStore object.

        :param float version: (optional)
        :param str terraform_version: (optional)
        :param float serial: (optional)
        :param str lineage: (optional)
        :param List[object] modules: (optional)
        """
        self.version = version
        self.terraform_version = terraform_version
        self.serial = serial
        self.lineage = lineage
        self.modules = modules

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateStateStore':
        """Initialize a TemplateStateStore object from a json dictionary."""
        args = {}
        if 'version' in _dict:
            args['version'] = _dict.get('version')
        if 'terraform_version' in _dict:
            args['terraform_version'] = _dict.get('terraform_version')
        if 'serial' in _dict:
            args['serial'] = _dict.get('serial')
        if 'lineage' in _dict:
            args['lineage'] = _dict.get('lineage')
        if 'modules' in _dict:
            args['modules'] = _dict.get('modules')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateStateStore object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'version') and self.version is not None:
            _dict['version'] = self.version
        if hasattr(self, 'terraform_version') and self.terraform_version is not None:
            _dict['terraform_version'] = self.terraform_version
        if hasattr(self, 'serial') and self.serial is not None:
            _dict['serial'] = self.serial
        if hasattr(self, 'lineage') and self.lineage is not None:
            _dict['lineage'] = self.lineage
        if hasattr(self, 'modules') and self.modules is not None:
            _dict['modules'] = self.modules
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateStateStore object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateStateStore') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateStateStore') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateValues():
    """
    TemplateValues -.

    :attr List[object] values_metadata: (optional)
    """

    def __init__(self,
                 *,
                 values_metadata: List[object] = None) -> None:
        """
        Initialize a TemplateValues object.

        :param List[object] values_metadata: (optional)
        """
        self.values_metadata = values_metadata

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateValues':
        """Initialize a TemplateValues object from a json dictionary."""
        args = {}
        if 'values_metadata' in _dict:
            args['values_metadata'] = _dict.get('values_metadata')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateValues object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'values_metadata') and self.values_metadata is not None:
            _dict['values_metadata'] = self.values_metadata
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateValues object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateValues') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateValues') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TerraformCommand():
    """
    TerraformCommand -.

    :attr str command: (optional) Command to execute.
    :attr str command_params: (optional) Command Parameters.
    :attr str command_name: (optional) Command name.
    :attr str command_desc: (optional) Command description.
    :attr str command_on_error: (optional) Instruction to continue or break in case
          of error.
    :attr str command_depends_on: (optional) Dependency on previous commands.
    :attr str command_status: (optional) Command status.
    """

    def __init__(self,
                 *,
                 command: str = None,
                 command_params: str = None,
                 command_name: str = None,
                 command_desc: str = None,
                 command_on_error: str = None,
                 command_depends_on: str = None,
                 command_status: str = None) -> None:
        """
        Initialize a TerraformCommand object.

        :param str command: (optional) Command to execute.
        :param str command_params: (optional) Command Parameters.
        :param str command_name: (optional) Command name.
        :param str command_desc: (optional) Command description.
        :param str command_on_error: (optional) Instruction to continue or break in
               case of error.
        :param str command_depends_on: (optional) Dependency on previous commands.
        :param str command_status: (optional) Command status.
        """
        self.command = command
        self.command_params = command_params
        self.command_name = command_name
        self.command_desc = command_desc
        self.command_on_error = command_on_error
        self.command_depends_on = command_depends_on
        self.command_status = command_status

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TerraformCommand':
        """Initialize a TerraformCommand object from a json dictionary."""
        args = {}
        if 'command' in _dict:
            args['command'] = _dict.get('command')
        if 'command_params' in _dict:
            args['command_params'] = _dict.get('command_params')
        if 'command_name' in _dict:
            args['command_name'] = _dict.get('command_name')
        if 'command_desc' in _dict:
            args['command_desc'] = _dict.get('command_desc')
        if 'command_onError' in _dict:
            args['command_on_error'] = _dict.get('command_onError')
        if 'command_dependsOn' in _dict:
            args['command_depends_on'] = _dict.get('command_dependsOn')
        if 'command_status' in _dict:
            args['command_status'] = _dict.get('command_status')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TerraformCommand object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'command') and self.command is not None:
            _dict['command'] = self.command
        if hasattr(self, 'command_params') and self.command_params is not None:
            _dict['command_params'] = self.command_params
        if hasattr(self, 'command_name') and self.command_name is not None:
            _dict['command_name'] = self.command_name
        if hasattr(self, 'command_desc') and self.command_desc is not None:
            _dict['command_desc'] = self.command_desc
        if hasattr(self, 'command_on_error') and self.command_on_error is not None:
            _dict['command_onError'] = self.command_on_error
        if hasattr(self, 'command_depends_on') and self.command_depends_on is not None:
            _dict['command_dependsOn'] = self.command_depends_on
        if hasattr(self, 'command_status') and self.command_status is not None:
            _dict['command_status'] = self.command_status
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TerraformCommand object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TerraformCommand') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TerraformCommand') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UserState():
    """
    User defined status of the Schematics object.

    :attr str state: (optional) User-defined states
            * `draft` Object can be modified; can be used by Jobs run by the author,
          during execution
            * `live` Object can be modified; can be used by Jobs during execution
            * `locked` Object cannot be modified; can be used by Jobs during execution
            * `disable` Object can be modified. cannot be used by Jobs during execution.
    :attr str set_by: (optional) Name of the User who set the state of the Object.
    :attr datetime set_at: (optional) When the User who set the state of the Object.
    """

    def __init__(self,
                 *,
                 state: str = None,
                 set_by: str = None,
                 set_at: datetime = None) -> None:
        """
        Initialize a UserState object.

        :param str state: (optional) User-defined states
                 * `draft` Object can be modified; can be used by Jobs run by the author,
               during execution
                 * `live` Object can be modified; can be used by Jobs during execution
                 * `locked` Object cannot be modified; can be used by Jobs during
               execution
                 * `disable` Object can be modified. cannot be used by Jobs during
               execution.
        :param str set_by: (optional) Name of the User who set the state of the
               Object.
        :param datetime set_at: (optional) When the User who set the state of the
               Object.
        """
        self.state = state
        self.set_by = set_by
        self.set_at = set_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UserState':
        """Initialize a UserState object from a json dictionary."""
        args = {}
        if 'state' in _dict:
            args['state'] = _dict.get('state')
        if 'set_by' in _dict:
            args['set_by'] = _dict.get('set_by')
        if 'set_at' in _dict:
            args['set_at'] = string_to_datetime(_dict.get('set_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UserState object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state
        if hasattr(self, 'set_by') and self.set_by is not None:
            _dict['set_by'] = self.set_by
        if hasattr(self, 'set_at') and self.set_at is not None:
            _dict['set_at'] = datetime_to_string(self.set_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UserState object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UserState') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UserState') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StateEnum(str, Enum):
        """
        User-defined states
          * `draft` Object can be modified; can be used by Jobs run by the author, during
        execution
          * `live` Object can be modified; can be used by Jobs during execution
          * `locked` Object cannot be modified; can be used by Jobs during execution
          * `disable` Object can be modified. cannot be used by Jobs during execution.
        """
        DRAFT = 'draft'
        LIVE = 'live'
        LOCKED = 'locked'
        DISABLE = 'disable'


class UserValues():
    """
    UserValues -.

    :attr List[object] env_values: (optional) EnvVariableRequest ..
    :attr str values: (optional) User values.
    :attr List[WorkspaceVariableResponse] variablestore: (optional)
          VariablesResponse -.
    """

    def __init__(self,
                 *,
                 env_values: List[object] = None,
                 values: str = None,
                 variablestore: List['WorkspaceVariableResponse'] = None) -> None:
        """
        Initialize a UserValues object.

        :param List[object] env_values: (optional) EnvVariableRequest ..
        :param str values: (optional) User values.
        :param List[WorkspaceVariableResponse] variablestore: (optional)
               VariablesResponse -.
        """
        self.env_values = env_values
        self.values = values
        self.variablestore = variablestore

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UserValues':
        """Initialize a UserValues object from a json dictionary."""
        args = {}
        if 'env_values' in _dict:
            args['env_values'] = _dict.get('env_values')
        if 'values' in _dict:
            args['values'] = _dict.get('values')
        if 'variablestore' in _dict:
            args['variablestore'] = [WorkspaceVariableResponse.from_dict(x) for x in _dict.get('variablestore')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UserValues object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'env_values') and self.env_values is not None:
            _dict['env_values'] = self.env_values
        if hasattr(self, 'values') and self.values is not None:
            _dict['values'] = self.values
        if hasattr(self, 'variablestore') and self.variablestore is not None:
            _dict['variablestore'] = [x.to_dict() for x in self.variablestore]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UserValues object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UserValues') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UserValues') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class VariableData():
    """
    User editable variable data & system generated reference to value.

    :attr str name: (optional) Name of the variable.
    :attr str value: (optional) Value for the variable or reference to the value.
    :attr VariableMetadata metadata: (optional) User editable metadata for the
          variables.
    :attr str link: (optional) Reference link to the variable value By default the
          expression will point to self.value.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 value: str = None,
                 metadata: 'VariableMetadata' = None,
                 link: str = None) -> None:
        """
        Initialize a VariableData object.

        :param str name: (optional) Name of the variable.
        :param str value: (optional) Value for the variable or reference to the
               value.
        :param VariableMetadata metadata: (optional) User editable metadata for the
               variables.
        """
        self.name = name
        self.value = value
        self.metadata = metadata
        self.link = link

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'VariableData':
        """Initialize a VariableData object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        if 'metadata' in _dict:
            args['metadata'] = VariableMetadata.from_dict(_dict.get('metadata'))
        if 'link' in _dict:
            args['link'] = _dict.get('link')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a VariableData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        if hasattr(self, 'metadata') and self.metadata is not None:
            _dict['metadata'] = self.metadata.to_dict()
        if hasattr(self, 'link') and getattr(self, 'link') is not None:
            _dict['link'] = getattr(self, 'link')
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this VariableData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'VariableData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'VariableData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class VariableMetadata():
    """
    User editable metadata for the variables.

    :attr str type: (optional) Type of the variable.
    :attr List[str] aliases: (optional) List of aliases for the variable name.
    :attr str description: (optional) Description of the meta data.
    :attr str default_value: (optional) Default value for the variable, if the
          override value is not specified.
    :attr bool secure: (optional) Is the variable secure or sensitive ?.
    :attr bool immutable: (optional) Is the variable readonly ?.
    :attr bool hidden: (optional) If true, the variable will not be displayed on UI
          or CLI.
    :attr List[str] options: (optional) List of possible values for this variable.
          If type is integer or date, then the array of string will be  converted to array
          of integers or date during runtime.
    :attr int min_value: (optional) Minimum value of the variable. Applicable for
          integer type.
    :attr int max_value: (optional) Maximum value of the variable. Applicable for
          integer type.
    :attr int min_length: (optional) Minimum length of the variable value.
          Applicable for string type.
    :attr int max_length: (optional) Maximum length of the variable value.
          Applicable for string type.
    :attr str matches: (optional) Regex for the variable value.
    :attr int position: (optional) Relative position of this variable in a list.
    :attr str group_by: (optional) Display name of the group this variable belongs
          to.
    :attr str source: (optional) Source of this meta-data.
    """

    def __init__(self,
                 *,
                 type: str = None,
                 aliases: List[str] = None,
                 description: str = None,
                 default_value: str = None,
                 secure: bool = None,
                 immutable: bool = None,
                 hidden: bool = None,
                 options: List[str] = None,
                 min_value: int = None,
                 max_value: int = None,
                 min_length: int = None,
                 max_length: int = None,
                 matches: str = None,
                 position: int = None,
                 group_by: str = None,
                 source: str = None) -> None:
        """
        Initialize a VariableMetadata object.

        :param str type: (optional) Type of the variable.
        :param List[str] aliases: (optional) List of aliases for the variable name.
        :param str description: (optional) Description of the meta data.
        :param str default_value: (optional) Default value for the variable, if the
               override value is not specified.
        :param bool secure: (optional) Is the variable secure or sensitive ?.
        :param bool immutable: (optional) Is the variable readonly ?.
        :param bool hidden: (optional) If true, the variable will not be displayed
               on UI or CLI.
        :param List[str] options: (optional) List of possible values for this
               variable.  If type is integer or date, then the array of string will be
               converted to array of integers or date during runtime.
        :param int min_value: (optional) Minimum value of the variable. Applicable
               for integer type.
        :param int max_value: (optional) Maximum value of the variable. Applicable
               for integer type.
        :param int min_length: (optional) Minimum length of the variable value.
               Applicable for string type.
        :param int max_length: (optional) Maximum length of the variable value.
               Applicable for string type.
        :param str matches: (optional) Regex for the variable value.
        :param int position: (optional) Relative position of this variable in a
               list.
        :param str group_by: (optional) Display name of the group this variable
               belongs to.
        :param str source: (optional) Source of this meta-data.
        """
        self.type = type
        self.aliases = aliases
        self.description = description
        self.default_value = default_value
        self.secure = secure
        self.immutable = immutable
        self.hidden = hidden
        self.options = options
        self.min_value = min_value
        self.max_value = max_value
        self.min_length = min_length
        self.max_length = max_length
        self.matches = matches
        self.position = position
        self.group_by = group_by
        self.source = source

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'VariableMetadata':
        """Initialize a VariableMetadata object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'aliases' in _dict:
            args['aliases'] = _dict.get('aliases')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'default_value' in _dict:
            args['default_value'] = _dict.get('default_value')
        if 'secure' in _dict:
            args['secure'] = _dict.get('secure')
        if 'immutable' in _dict:
            args['immutable'] = _dict.get('immutable')
        if 'hidden' in _dict:
            args['hidden'] = _dict.get('hidden')
        if 'options' in _dict:
            args['options'] = _dict.get('options')
        if 'min_value' in _dict:
            args['min_value'] = _dict.get('min_value')
        if 'max_value' in _dict:
            args['max_value'] = _dict.get('max_value')
        if 'min_length' in _dict:
            args['min_length'] = _dict.get('min_length')
        if 'max_length' in _dict:
            args['max_length'] = _dict.get('max_length')
        if 'matches' in _dict:
            args['matches'] = _dict.get('matches')
        if 'position' in _dict:
            args['position'] = _dict.get('position')
        if 'group_by' in _dict:
            args['group_by'] = _dict.get('group_by')
        if 'source' in _dict:
            args['source'] = _dict.get('source')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a VariableMetadata object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'aliases') and self.aliases is not None:
            _dict['aliases'] = self.aliases
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'default_value') and self.default_value is not None:
            _dict['default_value'] = self.default_value
        if hasattr(self, 'secure') and self.secure is not None:
            _dict['secure'] = self.secure
        if hasattr(self, 'immutable') and self.immutable is not None:
            _dict['immutable'] = self.immutable
        if hasattr(self, 'hidden') and self.hidden is not None:
            _dict['hidden'] = self.hidden
        if hasattr(self, 'options') and self.options is not None:
            _dict['options'] = self.options
        if hasattr(self, 'min_value') and self.min_value is not None:
            _dict['min_value'] = self.min_value
        if hasattr(self, 'max_value') and self.max_value is not None:
            _dict['max_value'] = self.max_value
        if hasattr(self, 'min_length') and self.min_length is not None:
            _dict['min_length'] = self.min_length
        if hasattr(self, 'max_length') and self.max_length is not None:
            _dict['max_length'] = self.max_length
        if hasattr(self, 'matches') and self.matches is not None:
            _dict['matches'] = self.matches
        if hasattr(self, 'position') and self.position is not None:
            _dict['position'] = self.position
        if hasattr(self, 'group_by') and self.group_by is not None:
            _dict['group_by'] = self.group_by
        if hasattr(self, 'source') and self.source is not None:
            _dict['source'] = self.source
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this VariableMetadata object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'VariableMetadata') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'VariableMetadata') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class TypeEnum(str, Enum):
        """
        Type of the variable.
        """
        BOOLEAN = 'boolean'
        STRING = 'string'
        INTEGER = 'integer'
        DATE = 'date'
        ARRAY = 'array'
        LIST = 'list'
        MAP = 'map'
        COMPLEX = 'complex'


class VersionResponse():
    """
    VersionResponse -.

    :attr str builddate: (optional) Build data.
    :attr str buildno: (optional) Build number.
    :attr str commitsha: (optional) Commit SHA.
    :attr str helm_provider_version: (optional) Version number of 'Helm provider for
          Terraform'.
    :attr str helm_version: (optional) Helm Version.
    :attr object supported_template_types: (optional) Supported template types.
    :attr str terraform_provider_version: (optional) Terraform provider versions.
    :attr str terraform_version: (optional) Terraform versions.
    """

    def __init__(self,
                 *,
                 builddate: str = None,
                 buildno: str = None,
                 commitsha: str = None,
                 helm_provider_version: str = None,
                 helm_version: str = None,
                 supported_template_types: object = None,
                 terraform_provider_version: str = None,
                 terraform_version: str = None) -> None:
        """
        Initialize a VersionResponse object.

        :param str builddate: (optional) Build data.
        :param str buildno: (optional) Build number.
        :param str commitsha: (optional) Commit SHA.
        :param str helm_provider_version: (optional) Version number of 'Helm
               provider for Terraform'.
        :param str helm_version: (optional) Helm Version.
        :param object supported_template_types: (optional) Supported template
               types.
        :param str terraform_provider_version: (optional) Terraform provider
               versions.
        :param str terraform_version: (optional) Terraform versions.
        """
        self.builddate = builddate
        self.buildno = buildno
        self.commitsha = commitsha
        self.helm_provider_version = helm_provider_version
        self.helm_version = helm_version
        self.supported_template_types = supported_template_types
        self.terraform_provider_version = terraform_provider_version
        self.terraform_version = terraform_version

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'VersionResponse':
        """Initialize a VersionResponse object from a json dictionary."""
        args = {}
        if 'builddate' in _dict:
            args['builddate'] = _dict.get('builddate')
        if 'buildno' in _dict:
            args['buildno'] = _dict.get('buildno')
        if 'commitsha' in _dict:
            args['commitsha'] = _dict.get('commitsha')
        if 'helm_provider_version' in _dict:
            args['helm_provider_version'] = _dict.get('helm_provider_version')
        if 'helm_version' in _dict:
            args['helm_version'] = _dict.get('helm_version')
        if 'supported_template_types' in _dict:
            args['supported_template_types'] = _dict.get('supported_template_types')
        if 'terraform_provider_version' in _dict:
            args['terraform_provider_version'] = _dict.get('terraform_provider_version')
        if 'terraform_version' in _dict:
            args['terraform_version'] = _dict.get('terraform_version')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a VersionResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'builddate') and self.builddate is not None:
            _dict['builddate'] = self.builddate
        if hasattr(self, 'buildno') and self.buildno is not None:
            _dict['buildno'] = self.buildno
        if hasattr(self, 'commitsha') and self.commitsha is not None:
            _dict['commitsha'] = self.commitsha
        if hasattr(self, 'helm_provider_version') and self.helm_provider_version is not None:
            _dict['helm_provider_version'] = self.helm_provider_version
        if hasattr(self, 'helm_version') and self.helm_version is not None:
            _dict['helm_version'] = self.helm_version
        if hasattr(self, 'supported_template_types') and self.supported_template_types is not None:
            _dict['supported_template_types'] = self.supported_template_types
        if hasattr(self, 'terraform_provider_version') and self.terraform_provider_version is not None:
            _dict['terraform_provider_version'] = self.terraform_provider_version
        if hasattr(self, 'terraform_version') and self.terraform_version is not None:
            _dict['terraform_version'] = self.terraform_version
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this VersionResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'VersionResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'VersionResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivities():
    """
    WorkspaceActivities -.

    :attr List[WorkspaceActivity] actions: (optional) List of workspace activities.
    :attr str workspace_id: (optional) Workspace id.
    :attr str workspace_name: (optional) Workspace name.
    """

    def __init__(self,
                 *,
                 actions: List['WorkspaceActivity'] = None,
                 workspace_id: str = None,
                 workspace_name: str = None) -> None:
        """
        Initialize a WorkspaceActivities object.

        :param List[WorkspaceActivity] actions: (optional) List of workspace
               activities.
        :param str workspace_id: (optional) Workspace id.
        :param str workspace_name: (optional) Workspace name.
        """
        self.actions = actions
        self.workspace_id = workspace_id
        self.workspace_name = workspace_name

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivities':
        """Initialize a WorkspaceActivities object from a json dictionary."""
        args = {}
        if 'actions' in _dict:
            args['actions'] = [WorkspaceActivity.from_dict(x) for x in _dict.get('actions')]
        if 'workspace_id' in _dict:
            args['workspace_id'] = _dict.get('workspace_id')
        if 'workspace_name' in _dict:
            args['workspace_name'] = _dict.get('workspace_name')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivities object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'actions') and self.actions is not None:
            _dict['actions'] = [x.to_dict() for x in self.actions]
        if hasattr(self, 'workspace_id') and self.workspace_id is not None:
            _dict['workspace_id'] = self.workspace_id
        if hasattr(self, 'workspace_name') and self.workspace_name is not None:
            _dict['workspace_name'] = self.workspace_name
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivities object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivities') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivities') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivity():
    """
    WorkspaceActivity -.

    :attr str action_id: (optional) Activity id.
    :attr List[str] message: (optional) StatusMessages -.
    :attr str name: (optional) WorkspaceActivityAction activity action type.
    :attr datetime performed_at: (optional) Activity performed at.
    :attr str performed_by: (optional) Activity performed by.
    :attr str status: (optional) WorkspaceActivityStatus activity status type.
    :attr List[WorkspaceActivityTemplate] templates: (optional) List of template
          activities.
    """

    def __init__(self,
                 *,
                 action_id: str = None,
                 message: List[str] = None,
                 name: str = None,
                 performed_at: datetime = None,
                 performed_by: str = None,
                 status: str = None,
                 templates: List['WorkspaceActivityTemplate'] = None) -> None:
        """
        Initialize a WorkspaceActivity object.

        :param str action_id: (optional) Activity id.
        :param List[str] message: (optional) StatusMessages -.
        :param str name: (optional) WorkspaceActivityAction activity action type.
        :param datetime performed_at: (optional) Activity performed at.
        :param str performed_by: (optional) Activity performed by.
        :param str status: (optional) WorkspaceActivityStatus activity status type.
        :param List[WorkspaceActivityTemplate] templates: (optional) List of
               template activities.
        """
        self.action_id = action_id
        self.message = message
        self.name = name
        self.performed_at = performed_at
        self.performed_by = performed_by
        self.status = status
        self.templates = templates

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivity':
        """Initialize a WorkspaceActivity object from a json dictionary."""
        args = {}
        if 'action_id' in _dict:
            args['action_id'] = _dict.get('action_id')
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'performed_at' in _dict:
            args['performed_at'] = string_to_datetime(_dict.get('performed_at'))
        if 'performed_by' in _dict:
            args['performed_by'] = _dict.get('performed_by')
        if 'status' in _dict:
            args['status'] = _dict.get('status')
        if 'templates' in _dict:
            args['templates'] = [WorkspaceActivityTemplate.from_dict(x) for x in _dict.get('templates')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivity object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'action_id') and self.action_id is not None:
            _dict['action_id'] = self.action_id
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'performed_at') and self.performed_at is not None:
            _dict['performed_at'] = datetime_to_string(self.performed_at)
        if hasattr(self, 'performed_by') and self.performed_by is not None:
            _dict['performed_by'] = self.performed_by
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status
        if hasattr(self, 'templates') and self.templates is not None:
            _dict['templates'] = [x.to_dict() for x in self.templates]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivity object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivity') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivity') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityApplyResult():
    """
    WorkspaceActivityApplyResult -.

    :attr str activityid: (optional) Activity id.
    """

    def __init__(self,
                 *,
                 activityid: str = None) -> None:
        """
        Initialize a WorkspaceActivityApplyResult object.

        :param str activityid: (optional) Activity id.
        """
        self.activityid = activityid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityApplyResult':
        """Initialize a WorkspaceActivityApplyResult object from a json dictionary."""
        args = {}
        if 'activityid' in _dict:
            args['activityid'] = _dict.get('activityid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityApplyResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activityid') and self.activityid is not None:
            _dict['activityid'] = self.activityid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityApplyResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityApplyResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityApplyResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityCommandResult():
    """
    WorkspaceActivityCommandResult -.

    :attr str activityid: (optional) Activity id.
    """

    def __init__(self,
                 *,
                 activityid: str = None) -> None:
        """
        Initialize a WorkspaceActivityCommandResult object.

        :param str activityid: (optional) Activity id.
        """
        self.activityid = activityid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityCommandResult':
        """Initialize a WorkspaceActivityCommandResult object from a json dictionary."""
        args = {}
        if 'activityid' in _dict:
            args['activityid'] = _dict.get('activityid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityCommandResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activityid') and self.activityid is not None:
            _dict['activityid'] = self.activityid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityCommandResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityCommandResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityCommandResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityDestroyResult():
    """
    WorkspaceActivityDestroyResult -.

    :attr str activityid: (optional) Activity id.
    """

    def __init__(self,
                 *,
                 activityid: str = None) -> None:
        """
        Initialize a WorkspaceActivityDestroyResult object.

        :param str activityid: (optional) Activity id.
        """
        self.activityid = activityid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityDestroyResult':
        """Initialize a WorkspaceActivityDestroyResult object from a json dictionary."""
        args = {}
        if 'activityid' in _dict:
            args['activityid'] = _dict.get('activityid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityDestroyResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activityid') and self.activityid is not None:
            _dict['activityid'] = self.activityid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityDestroyResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityDestroyResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityDestroyResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityLogs():
    """
    WorkspaceActivityLogs -.

    :attr str action_id: (optional) Activity id.
    :attr str name: (optional) WorkspaceActivityAction activity action type.
    :attr List[WorkspaceActivityTemplateLogs] templates: (optional) List of activity
          logs.
    """

    def __init__(self,
                 *,
                 action_id: str = None,
                 name: str = None,
                 templates: List['WorkspaceActivityTemplateLogs'] = None) -> None:
        """
        Initialize a WorkspaceActivityLogs object.

        :param str action_id: (optional) Activity id.
        :param str name: (optional) WorkspaceActivityAction activity action type.
        :param List[WorkspaceActivityTemplateLogs] templates: (optional) List of
               activity logs.
        """
        self.action_id = action_id
        self.name = name
        self.templates = templates

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityLogs':
        """Initialize a WorkspaceActivityLogs object from a json dictionary."""
        args = {}
        if 'action_id' in _dict:
            args['action_id'] = _dict.get('action_id')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'templates' in _dict:
            args['templates'] = [WorkspaceActivityTemplateLogs.from_dict(x) for x in _dict.get('templates')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityLogs object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'action_id') and self.action_id is not None:
            _dict['action_id'] = self.action_id
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'templates') and self.templates is not None:
            _dict['templates'] = [x.to_dict() for x in self.templates]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityLogs object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityLogs') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityLogs') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityOptionsTemplate():
    """
    Workspace Activity Options Template.

    :attr List[str] target: (optional) Workspace Activity targets.
    :attr List[str] tf_vars: (optional) Workspace Activity tfvars.
    """

    def __init__(self,
                 *,
                 target: List[str] = None,
                 tf_vars: List[str] = None) -> None:
        """
        Initialize a WorkspaceActivityOptionsTemplate object.

        :param List[str] target: (optional) Workspace Activity targets.
        :param List[str] tf_vars: (optional) Workspace Activity tfvars.
        """
        self.target = target
        self.tf_vars = tf_vars

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityOptionsTemplate':
        """Initialize a WorkspaceActivityOptionsTemplate object from a json dictionary."""
        args = {}
        if 'target' in _dict:
            args['target'] = _dict.get('target')
        if 'tf_vars' in _dict:
            args['tf_vars'] = _dict.get('tf_vars')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityOptionsTemplate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'target') and self.target is not None:
            _dict['target'] = self.target
        if hasattr(self, 'tf_vars') and self.tf_vars is not None:
            _dict['tf_vars'] = self.tf_vars
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityOptionsTemplate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityOptionsTemplate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityOptionsTemplate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityPlanResult():
    """
    WorkspaceActivityPlanResult -.

    :attr str activityid: (optional) Activity id.
    """

    def __init__(self,
                 *,
                 activityid: str = None) -> None:
        """
        Initialize a WorkspaceActivityPlanResult object.

        :param str activityid: (optional) Activity id.
        """
        self.activityid = activityid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityPlanResult':
        """Initialize a WorkspaceActivityPlanResult object from a json dictionary."""
        args = {}
        if 'activityid' in _dict:
            args['activityid'] = _dict.get('activityid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityPlanResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activityid') and self.activityid is not None:
            _dict['activityid'] = self.activityid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityPlanResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityPlanResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityPlanResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityRefreshResult():
    """
    WorkspaceActivityRefreshResult -.

    :attr str activityid: (optional) Activity id.
    """

    def __init__(self,
                 *,
                 activityid: str = None) -> None:
        """
        Initialize a WorkspaceActivityRefreshResult object.

        :param str activityid: (optional) Activity id.
        """
        self.activityid = activityid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityRefreshResult':
        """Initialize a WorkspaceActivityRefreshResult object from a json dictionary."""
        args = {}
        if 'activityid' in _dict:
            args['activityid'] = _dict.get('activityid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityRefreshResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activityid') and self.activityid is not None:
            _dict['activityid'] = self.activityid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityRefreshResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityRefreshResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityRefreshResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityTemplate():
    """
    WorkspaceActivityTemplate -.

    :attr datetime end_time: (optional) End time for the activity.
    :attr LogSummary log_summary: (optional) LogSummary ...
    :attr str log_url: (optional) Log URL.
    :attr str message: (optional) Message.
    :attr datetime start_time: (optional) Activity start time.
    :attr str status: (optional) WorkspaceActivityStatus activity status type.
    :attr str template_id: (optional) Template id.
    :attr str template_type: (optional) Template type.
    """

    def __init__(self,
                 *,
                 end_time: datetime = None,
                 log_summary: 'LogSummary' = None,
                 log_url: str = None,
                 message: str = None,
                 start_time: datetime = None,
                 status: str = None,
                 template_id: str = None,
                 template_type: str = None) -> None:
        """
        Initialize a WorkspaceActivityTemplate object.

        :param datetime end_time: (optional) End time for the activity.
        :param LogSummary log_summary: (optional) LogSummary ...
        :param str log_url: (optional) Log URL.
        :param str message: (optional) Message.
        :param datetime start_time: (optional) Activity start time.
        :param str status: (optional) WorkspaceActivityStatus activity status type.
        :param str template_id: (optional) Template id.
        :param str template_type: (optional) Template type.
        """
        self.end_time = end_time
        self.log_summary = log_summary
        self.log_url = log_url
        self.message = message
        self.start_time = start_time
        self.status = status
        self.template_id = template_id
        self.template_type = template_type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityTemplate':
        """Initialize a WorkspaceActivityTemplate object from a json dictionary."""
        args = {}
        if 'end_time' in _dict:
            args['end_time'] = string_to_datetime(_dict.get('end_time'))
        if 'log_summary' in _dict:
            args['log_summary'] = LogSummary.from_dict(_dict.get('log_summary'))
        if 'log_url' in _dict:
            args['log_url'] = _dict.get('log_url')
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'start_time' in _dict:
            args['start_time'] = string_to_datetime(_dict.get('start_time'))
        if 'status' in _dict:
            args['status'] = _dict.get('status')
        if 'template_id' in _dict:
            args['template_id'] = _dict.get('template_id')
        if 'template_type' in _dict:
            args['template_type'] = _dict.get('template_type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityTemplate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'end_time') and self.end_time is not None:
            _dict['end_time'] = datetime_to_string(self.end_time)
        if hasattr(self, 'log_summary') and self.log_summary is not None:
            _dict['log_summary'] = self.log_summary.to_dict()
        if hasattr(self, 'log_url') and self.log_url is not None:
            _dict['log_url'] = self.log_url
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'start_time') and self.start_time is not None:
            _dict['start_time'] = datetime_to_string(self.start_time)
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status
        if hasattr(self, 'template_id') and self.template_id is not None:
            _dict['template_id'] = self.template_id
        if hasattr(self, 'template_type') and self.template_type is not None:
            _dict['template_type'] = self.template_type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityTemplate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityTemplate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityTemplate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityTemplateLogs():
    """
    WorkspaceActivityTemplateLogs -.

    :attr str log_url: (optional) Log URL.
    :attr str template_id: (optional) Template id.
    :attr str template_type: (optional) Template type.
    """

    def __init__(self,
                 *,
                 log_url: str = None,
                 template_id: str = None,
                 template_type: str = None) -> None:
        """
        Initialize a WorkspaceActivityTemplateLogs object.

        :param str log_url: (optional) Log URL.
        :param str template_id: (optional) Template id.
        :param str template_type: (optional) Template type.
        """
        self.log_url = log_url
        self.template_id = template_id
        self.template_type = template_type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityTemplateLogs':
        """Initialize a WorkspaceActivityTemplateLogs object from a json dictionary."""
        args = {}
        if 'log_url' in _dict:
            args['log_url'] = _dict.get('log_url')
        if 'template_id' in _dict:
            args['template_id'] = _dict.get('template_id')
        if 'template_type' in _dict:
            args['template_type'] = _dict.get('template_type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityTemplateLogs object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'log_url') and self.log_url is not None:
            _dict['log_url'] = self.log_url
        if hasattr(self, 'template_id') and self.template_id is not None:
            _dict['template_id'] = self.template_id
        if hasattr(self, 'template_type') and self.template_type is not None:
            _dict['template_type'] = self.template_type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityTemplateLogs object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityTemplateLogs') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityTemplateLogs') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceBulkDeleteResponse():
    """
    WorkspaceBulkDeleteResponse -.

    :attr str job: (optional) Workspace deletion job name.
    :attr str job_id: (optional) Workspace deletion job id.
    """

    def __init__(self,
                 *,
                 job: str = None,
                 job_id: str = None) -> None:
        """
        Initialize a WorkspaceBulkDeleteResponse object.

        :param str job: (optional) Workspace deletion job name.
        :param str job_id: (optional) Workspace deletion job id.
        """
        self.job = job
        self.job_id = job_id

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceBulkDeleteResponse':
        """Initialize a WorkspaceBulkDeleteResponse object from a json dictionary."""
        args = {}
        if 'job' in _dict:
            args['job'] = _dict.get('job')
        if 'job_id' in _dict:
            args['job_id'] = _dict.get('job_id')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceBulkDeleteResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'job') and self.job is not None:
            _dict['job'] = self.job
        if hasattr(self, 'job_id') and self.job_id is not None:
            _dict['job_id'] = self.job_id
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceBulkDeleteResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceBulkDeleteResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceBulkDeleteResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceJobResponse():
    """
    WorkspaceJobResponse -.

    :attr JobStatusType job_status: (optional) JobStatusType -.
    """

    def __init__(self,
                 *,
                 job_status: 'JobStatusType' = None) -> None:
        """
        Initialize a WorkspaceJobResponse object.

        :param JobStatusType job_status: (optional) JobStatusType -.
        """
        self.job_status = job_status

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceJobResponse':
        """Initialize a WorkspaceJobResponse object from a json dictionary."""
        args = {}
        if 'job_status' in _dict:
            args['job_status'] = JobStatusType.from_dict(_dict.get('job_status'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceJobResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'job_status') and self.job_status is not None:
            _dict['job_status'] = self.job_status.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceJobResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceJobResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceJobResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceResponse():
    """
    WorkspaceResponse - request returned by create.

    :attr List[str] applied_shareddata_ids: (optional) List of applied shared
          dataset id.
    :attr CatalogRef catalog_ref: (optional) CatalogRef -.
    :attr datetime created_at: (optional) Workspace created at.
    :attr str created_by: (optional) Workspace created by.
    :attr str crn: (optional) Workspace CRN.
    :attr str description: (optional) Workspace description.
    :attr str id: (optional) Workspace id.
    :attr datetime last_health_check_at: (optional) Last health checked at.
    :attr str location: (optional) Workspace location.
    :attr str name: (optional) Workspace name.
    :attr str resource_group: (optional) Workspace resource group.
    :attr List[TemplateRunTimeDataResponse] runtime_data: (optional) Workspace
          runtime data.
    :attr SharedTargetDataResponse shared_data: (optional) SharedTargetDataResponse
          -.
    :attr str status: (optional) Workspace status type.
    :attr List[str] tags: (optional) Workspace tags.
    :attr List[TemplateSourceDataResponse] template_data: (optional) Workspace
          template data.
    :attr str template_ref: (optional) Workspace template ref.
    :attr TemplateRepoResponse template_repo: (optional) TemplateRepoResponse -.
    :attr List[str] type: (optional) List of Workspace type.
    :attr datetime updated_at: (optional) Workspace updated at.
    :attr str updated_by: (optional) Workspace updated by.
    :attr WorkspaceStatusResponse workspace_status: (optional)
          WorkspaceStatusResponse -.
    :attr WorkspaceStatusMessage workspace_status_msg: (optional)
          WorkspaceStatusMessage -.
    """

    def __init__(self,
                 *,
                 applied_shareddata_ids: List[str] = None,
                 catalog_ref: 'CatalogRef' = None,
                 created_at: datetime = None,
                 created_by: str = None,
                 crn: str = None,
                 description: str = None,
                 id: str = None,
                 last_health_check_at: datetime = None,
                 location: str = None,
                 name: str = None,
                 resource_group: str = None,
                 runtime_data: List['TemplateRunTimeDataResponse'] = None,
                 shared_data: 'SharedTargetDataResponse' = None,
                 status: str = None,
                 tags: List[str] = None,
                 template_data: List['TemplateSourceDataResponse'] = None,
                 template_ref: str = None,
                 template_repo: 'TemplateRepoResponse' = None,
                 type: List[str] = None,
                 updated_at: datetime = None,
                 updated_by: str = None,
                 workspace_status: 'WorkspaceStatusResponse' = None,
                 workspace_status_msg: 'WorkspaceStatusMessage' = None) -> None:
        """
        Initialize a WorkspaceResponse object.

        :param List[str] applied_shareddata_ids: (optional) List of applied shared
               dataset id.
        :param CatalogRef catalog_ref: (optional) CatalogRef -.
        :param datetime created_at: (optional) Workspace created at.
        :param str created_by: (optional) Workspace created by.
        :param str crn: (optional) Workspace CRN.
        :param str description: (optional) Workspace description.
        :param str id: (optional) Workspace id.
        :param datetime last_health_check_at: (optional) Last health checked at.
        :param str location: (optional) Workspace location.
        :param str name: (optional) Workspace name.
        :param str resource_group: (optional) Workspace resource group.
        :param List[TemplateRunTimeDataResponse] runtime_data: (optional) Workspace
               runtime data.
        :param SharedTargetDataResponse shared_data: (optional)
               SharedTargetDataResponse -.
        :param str status: (optional) Workspace status type.
        :param List[str] tags: (optional) Workspace tags.
        :param List[TemplateSourceDataResponse] template_data: (optional) Workspace
               template data.
        :param str template_ref: (optional) Workspace template ref.
        :param TemplateRepoResponse template_repo: (optional) TemplateRepoResponse
               -.
        :param List[str] type: (optional) List of Workspace type.
        :param datetime updated_at: (optional) Workspace updated at.
        :param str updated_by: (optional) Workspace updated by.
        :param WorkspaceStatusResponse workspace_status: (optional)
               WorkspaceStatusResponse -.
        :param WorkspaceStatusMessage workspace_status_msg: (optional)
               WorkspaceStatusMessage -.
        """
        self.applied_shareddata_ids = applied_shareddata_ids
        self.catalog_ref = catalog_ref
        self.created_at = created_at
        self.created_by = created_by
        self.crn = crn
        self.description = description
        self.id = id
        self.last_health_check_at = last_health_check_at
        self.location = location
        self.name = name
        self.resource_group = resource_group
        self.runtime_data = runtime_data
        self.shared_data = shared_data
        self.status = status
        self.tags = tags
        self.template_data = template_data
        self.template_ref = template_ref
        self.template_repo = template_repo
        self.type = type
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.workspace_status = workspace_status
        self.workspace_status_msg = workspace_status_msg

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceResponse':
        """Initialize a WorkspaceResponse object from a json dictionary."""
        args = {}
        if 'applied_shareddata_ids' in _dict:
            args['applied_shareddata_ids'] = _dict.get('applied_shareddata_ids')
        if 'catalog_ref' in _dict:
            args['catalog_ref'] = CatalogRef.from_dict(_dict.get('catalog_ref'))
        if 'created_at' in _dict:
            args['created_at'] = string_to_datetime(_dict.get('created_at'))
        if 'created_by' in _dict:
            args['created_by'] = _dict.get('created_by')
        if 'crn' in _dict:
            args['crn'] = _dict.get('crn')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'last_health_check_at' in _dict:
            args['last_health_check_at'] = string_to_datetime(_dict.get('last_health_check_at'))
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'runtime_data' in _dict:
            args['runtime_data'] = [TemplateRunTimeDataResponse.from_dict(x) for x in _dict.get('runtime_data')]
        if 'shared_data' in _dict:
            args['shared_data'] = SharedTargetDataResponse.from_dict(_dict.get('shared_data'))
        if 'status' in _dict:
            args['status'] = _dict.get('status')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'template_data' in _dict:
            args['template_data'] = [TemplateSourceDataResponse.from_dict(x) for x in _dict.get('template_data')]
        if 'template_ref' in _dict:
            args['template_ref'] = _dict.get('template_ref')
        if 'template_repo' in _dict:
            args['template_repo'] = TemplateRepoResponse.from_dict(_dict.get('template_repo'))
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'updated_by' in _dict:
            args['updated_by'] = _dict.get('updated_by')
        if 'workspace_status' in _dict:
            args['workspace_status'] = WorkspaceStatusResponse.from_dict(_dict.get('workspace_status'))
        if 'workspace_status_msg' in _dict:
            args['workspace_status_msg'] = WorkspaceStatusMessage.from_dict(_dict.get('workspace_status_msg'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'applied_shareddata_ids') and self.applied_shareddata_ids is not None:
            _dict['applied_shareddata_ids'] = self.applied_shareddata_ids
        if hasattr(self, 'catalog_ref') and self.catalog_ref is not None:
            _dict['catalog_ref'] = self.catalog_ref.to_dict()
        if hasattr(self, 'created_at') and self.created_at is not None:
            _dict['created_at'] = datetime_to_string(self.created_at)
        if hasattr(self, 'created_by') and self.created_by is not None:
            _dict['created_by'] = self.created_by
        if hasattr(self, 'crn') and self.crn is not None:
            _dict['crn'] = self.crn
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'last_health_check_at') and self.last_health_check_at is not None:
            _dict['last_health_check_at'] = datetime_to_string(self.last_health_check_at)
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'runtime_data') and self.runtime_data is not None:
            _dict['runtime_data'] = [x.to_dict() for x in self.runtime_data]
        if hasattr(self, 'shared_data') and self.shared_data is not None:
            _dict['shared_data'] = self.shared_data.to_dict()
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'template_data') and self.template_data is not None:
            _dict['template_data'] = [x.to_dict() for x in self.template_data]
        if hasattr(self, 'template_ref') and self.template_ref is not None:
            _dict['template_ref'] = self.template_ref
        if hasattr(self, 'template_repo') and self.template_repo is not None:
            _dict['template_repo'] = self.template_repo.to_dict()
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        if hasattr(self, 'updated_by') and self.updated_by is not None:
            _dict['updated_by'] = self.updated_by
        if hasattr(self, 'workspace_status') and self.workspace_status is not None:
            _dict['workspace_status'] = self.workspace_status.to_dict()
        if hasattr(self, 'workspace_status_msg') and self.workspace_status_msg is not None:
            _dict['workspace_status_msg'] = self.workspace_status_msg.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceResponseList():
    """
    WorkspaceResponseList -.

    :attr int count: (optional) Total number of workspaces.
    :attr int limit: Limit for the list.
    :attr int offset: Offset for the list.
    :attr List[WorkspaceResponse] workspaces: (optional) List of Workspaces.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 count: int = None,
                 workspaces: List['WorkspaceResponse'] = None) -> None:
        """
        Initialize a WorkspaceResponseList object.

        :param int limit: Limit for the list.
        :param int offset: Offset for the list.
        :param int count: (optional) Total number of workspaces.
        :param List[WorkspaceResponse] workspaces: (optional) List of Workspaces.
        """
        self.count = count
        self.limit = limit
        self.offset = offset
        self.workspaces = workspaces

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceResponseList':
        """Initialize a WorkspaceResponseList object from a json dictionary."""
        args = {}
        if 'count' in _dict:
            args['count'] = _dict.get('count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in WorkspaceResponseList JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in WorkspaceResponseList JSON')
        if 'workspaces' in _dict:
            args['workspaces'] = [WorkspaceResponse.from_dict(x) for x in _dict.get('workspaces')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceResponseList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'count') and self.count is not None:
            _dict['count'] = self.count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'workspaces') and self.workspaces is not None:
            _dict['workspaces'] = [x.to_dict() for x in self.workspaces]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceResponseList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceResponseList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceResponseList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceStatusMessage():
    """
    WorkspaceStatusMessage -.

    :attr str status_code: (optional) Status code.
    :attr str status_msg: (optional) Status message.
    """

    def __init__(self,
                 *,
                 status_code: str = None,
                 status_msg: str = None) -> None:
        """
        Initialize a WorkspaceStatusMessage object.

        :param str status_code: (optional) Status code.
        :param str status_msg: (optional) Status message.
        """
        self.status_code = status_code
        self.status_msg = status_msg

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceStatusMessage':
        """Initialize a WorkspaceStatusMessage object from a json dictionary."""
        args = {}
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_msg' in _dict:
            args['status_msg'] = _dict.get('status_msg')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceStatusMessage object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_msg') and self.status_msg is not None:
            _dict['status_msg'] = self.status_msg
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceStatusMessage object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceStatusMessage') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceStatusMessage') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceStatusRequest():
    """
    WorkspaceStatusRequest -.

    :attr bool frozen: (optional) Frozen status.
    :attr datetime frozen_at: (optional) Frozen at.
    :attr str frozen_by: (optional) Frozen by.
    :attr bool locked: (optional) Locked status.
    :attr str locked_by: (optional) Locked by.
    :attr datetime locked_time: (optional) Locked at.
    """

    def __init__(self,
                 *,
                 frozen: bool = None,
                 frozen_at: datetime = None,
                 frozen_by: str = None,
                 locked: bool = None,
                 locked_by: str = None,
                 locked_time: datetime = None) -> None:
        """
        Initialize a WorkspaceStatusRequest object.

        :param bool frozen: (optional) Frozen status.
        :param datetime frozen_at: (optional) Frozen at.
        :param str frozen_by: (optional) Frozen by.
        :param bool locked: (optional) Locked status.
        :param str locked_by: (optional) Locked by.
        :param datetime locked_time: (optional) Locked at.
        """
        self.frozen = frozen
        self.frozen_at = frozen_at
        self.frozen_by = frozen_by
        self.locked = locked
        self.locked_by = locked_by
        self.locked_time = locked_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceStatusRequest':
        """Initialize a WorkspaceStatusRequest object from a json dictionary."""
        args = {}
        if 'frozen' in _dict:
            args['frozen'] = _dict.get('frozen')
        if 'frozen_at' in _dict:
            args['frozen_at'] = string_to_datetime(_dict.get('frozen_at'))
        if 'frozen_by' in _dict:
            args['frozen_by'] = _dict.get('frozen_by')
        if 'locked' in _dict:
            args['locked'] = _dict.get('locked')
        if 'locked_by' in _dict:
            args['locked_by'] = _dict.get('locked_by')
        if 'locked_time' in _dict:
            args['locked_time'] = string_to_datetime(_dict.get('locked_time'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceStatusRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'frozen') and self.frozen is not None:
            _dict['frozen'] = self.frozen
        if hasattr(self, 'frozen_at') and self.frozen_at is not None:
            _dict['frozen_at'] = datetime_to_string(self.frozen_at)
        if hasattr(self, 'frozen_by') and self.frozen_by is not None:
            _dict['frozen_by'] = self.frozen_by
        if hasattr(self, 'locked') and self.locked is not None:
            _dict['locked'] = self.locked
        if hasattr(self, 'locked_by') and self.locked_by is not None:
            _dict['locked_by'] = self.locked_by
        if hasattr(self, 'locked_time') and self.locked_time is not None:
            _dict['locked_time'] = datetime_to_string(self.locked_time)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceStatusRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceStatusRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceStatusRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceStatusResponse():
    """
    WorkspaceStatusResponse -.

    :attr bool frozen: (optional) Frozen status.
    :attr datetime frozen_at: (optional) Frozen at.
    :attr str frozen_by: (optional) Frozen by.
    :attr bool locked: (optional) Locked status.
    :attr str locked_by: (optional) Locked by.
    :attr datetime locked_time: (optional) Locked at.
    """

    def __init__(self,
                 *,
                 frozen: bool = None,
                 frozen_at: datetime = None,
                 frozen_by: str = None,
                 locked: bool = None,
                 locked_by: str = None,
                 locked_time: datetime = None) -> None:
        """
        Initialize a WorkspaceStatusResponse object.

        :param bool frozen: (optional) Frozen status.
        :param datetime frozen_at: (optional) Frozen at.
        :param str frozen_by: (optional) Frozen by.
        :param bool locked: (optional) Locked status.
        :param str locked_by: (optional) Locked by.
        :param datetime locked_time: (optional) Locked at.
        """
        self.frozen = frozen
        self.frozen_at = frozen_at
        self.frozen_by = frozen_by
        self.locked = locked
        self.locked_by = locked_by
        self.locked_time = locked_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceStatusResponse':
        """Initialize a WorkspaceStatusResponse object from a json dictionary."""
        args = {}
        if 'frozen' in _dict:
            args['frozen'] = _dict.get('frozen')
        if 'frozen_at' in _dict:
            args['frozen_at'] = string_to_datetime(_dict.get('frozen_at'))
        if 'frozen_by' in _dict:
            args['frozen_by'] = _dict.get('frozen_by')
        if 'locked' in _dict:
            args['locked'] = _dict.get('locked')
        if 'locked_by' in _dict:
            args['locked_by'] = _dict.get('locked_by')
        if 'locked_time' in _dict:
            args['locked_time'] = string_to_datetime(_dict.get('locked_time'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceStatusResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'frozen') and self.frozen is not None:
            _dict['frozen'] = self.frozen
        if hasattr(self, 'frozen_at') and self.frozen_at is not None:
            _dict['frozen_at'] = datetime_to_string(self.frozen_at)
        if hasattr(self, 'frozen_by') and self.frozen_by is not None:
            _dict['frozen_by'] = self.frozen_by
        if hasattr(self, 'locked') and self.locked is not None:
            _dict['locked'] = self.locked
        if hasattr(self, 'locked_by') and self.locked_by is not None:
            _dict['locked_by'] = self.locked_by
        if hasattr(self, 'locked_time') and self.locked_time is not None:
            _dict['locked_time'] = datetime_to_string(self.locked_time)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceStatusResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceStatusResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceStatusResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceStatusUpdateRequest():
    """
    WorkspaceStatusUpdateRequest -.

    :attr bool frozen: (optional) Frozen status.
    :attr datetime frozen_at: (optional) Frozen at.
    :attr str frozen_by: (optional) Frozen by.
    :attr bool locked: (optional) Locked status.
    :attr str locked_by: (optional) Locked by.
    :attr datetime locked_time: (optional) Locked at.
    """

    def __init__(self,
                 *,
                 frozen: bool = None,
                 frozen_at: datetime = None,
                 frozen_by: str = None,
                 locked: bool = None,
                 locked_by: str = None,
                 locked_time: datetime = None) -> None:
        """
        Initialize a WorkspaceStatusUpdateRequest object.

        :param bool frozen: (optional) Frozen status.
        :param datetime frozen_at: (optional) Frozen at.
        :param str frozen_by: (optional) Frozen by.
        :param bool locked: (optional) Locked status.
        :param str locked_by: (optional) Locked by.
        :param datetime locked_time: (optional) Locked at.
        """
        self.frozen = frozen
        self.frozen_at = frozen_at
        self.frozen_by = frozen_by
        self.locked = locked
        self.locked_by = locked_by
        self.locked_time = locked_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceStatusUpdateRequest':
        """Initialize a WorkspaceStatusUpdateRequest object from a json dictionary."""
        args = {}
        if 'frozen' in _dict:
            args['frozen'] = _dict.get('frozen')
        if 'frozen_at' in _dict:
            args['frozen_at'] = string_to_datetime(_dict.get('frozen_at'))
        if 'frozen_by' in _dict:
            args['frozen_by'] = _dict.get('frozen_by')
        if 'locked' in _dict:
            args['locked'] = _dict.get('locked')
        if 'locked_by' in _dict:
            args['locked_by'] = _dict.get('locked_by')
        if 'locked_time' in _dict:
            args['locked_time'] = string_to_datetime(_dict.get('locked_time'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceStatusUpdateRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'frozen') and self.frozen is not None:
            _dict['frozen'] = self.frozen
        if hasattr(self, 'frozen_at') and self.frozen_at is not None:
            _dict['frozen_at'] = datetime_to_string(self.frozen_at)
        if hasattr(self, 'frozen_by') and self.frozen_by is not None:
            _dict['frozen_by'] = self.frozen_by
        if hasattr(self, 'locked') and self.locked is not None:
            _dict['locked'] = self.locked
        if hasattr(self, 'locked_by') and self.locked_by is not None:
            _dict['locked_by'] = self.locked_by
        if hasattr(self, 'locked_time') and self.locked_time is not None:
            _dict['locked_time'] = datetime_to_string(self.locked_time)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceStatusUpdateRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceStatusUpdateRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceStatusUpdateRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceTemplateValuesResponse():
    """
    WorkspaceTemplateValuesResponse -.

    :attr List[TemplateRunTimeDataResponse] runtime_data: (optional) List of runtime
          data.
    :attr SharedTargetData shared_data: (optional) SharedTargetData -.
    :attr List[TemplateSourceDataResponse] template_data: (optional) List of source
          data.
    """

    def __init__(self,
                 *,
                 runtime_data: List['TemplateRunTimeDataResponse'] = None,
                 shared_data: 'SharedTargetData' = None,
                 template_data: List['TemplateSourceDataResponse'] = None) -> None:
        """
        Initialize a WorkspaceTemplateValuesResponse object.

        :param List[TemplateRunTimeDataResponse] runtime_data: (optional) List of
               runtime data.
        :param SharedTargetData shared_data: (optional) SharedTargetData -.
        :param List[TemplateSourceDataResponse] template_data: (optional) List of
               source data.
        """
        self.runtime_data = runtime_data
        self.shared_data = shared_data
        self.template_data = template_data

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceTemplateValuesResponse':
        """Initialize a WorkspaceTemplateValuesResponse object from a json dictionary."""
        args = {}
        if 'runtime_data' in _dict:
            args['runtime_data'] = [TemplateRunTimeDataResponse.from_dict(x) for x in _dict.get('runtime_data')]
        if 'shared_data' in _dict:
            args['shared_data'] = SharedTargetData.from_dict(_dict.get('shared_data'))
        if 'template_data' in _dict:
            args['template_data'] = [TemplateSourceDataResponse.from_dict(x) for x in _dict.get('template_data')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceTemplateValuesResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'runtime_data') and self.runtime_data is not None:
            _dict['runtime_data'] = [x.to_dict() for x in self.runtime_data]
        if hasattr(self, 'shared_data') and self.shared_data is not None:
            _dict['shared_data'] = self.shared_data.to_dict()
        if hasattr(self, 'template_data') and self.template_data is not None:
            _dict['template_data'] = [x.to_dict() for x in self.template_data]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceTemplateValuesResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceTemplateValuesResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceTemplateValuesResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceVariableRequest():
    """
    WorkspaceVariableRequest -.

    :attr str description: (optional) Variable description.
    :attr str name: (optional) Variable name.
    :attr bool secure: (optional) Variable is secure.
    :attr str type: (optional) Variable type.
    :attr bool use_default: (optional) Variable uses default value; and is not
          over-ridden.
    :attr str value: (optional) Value of the Variable.
    """

    def __init__(self,
                 *,
                 description: str = None,
                 name: str = None,
                 secure: bool = None,
                 type: str = None,
                 use_default: bool = None,
                 value: str = None) -> None:
        """
        Initialize a WorkspaceVariableRequest object.

        :param str description: (optional) Variable description.
        :param str name: (optional) Variable name.
        :param bool secure: (optional) Variable is secure.
        :param str type: (optional) Variable type.
        :param bool use_default: (optional) Variable uses default value; and is not
               over-ridden.
        :param str value: (optional) Value of the Variable.
        """
        self.description = description
        self.name = name
        self.secure = secure
        self.type = type
        self.use_default = use_default
        self.value = value

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceVariableRequest':
        """Initialize a WorkspaceVariableRequest object from a json dictionary."""
        args = {}
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'secure' in _dict:
            args['secure'] = _dict.get('secure')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'use_default' in _dict:
            args['use_default'] = _dict.get('use_default')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceVariableRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'secure') and self.secure is not None:
            _dict['secure'] = self.secure
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'use_default') and self.use_default is not None:
            _dict['use_default'] = self.use_default
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceVariableRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceVariableRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceVariableRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceVariableResponse():
    """
    WorkspaceVariableResponse -.

    :attr str description: (optional) Variable descrption.
    :attr str name: (optional) Variable name.
    :attr bool secure: (optional) Variable is secure.
    :attr str type: (optional) Variable type.
    :attr str value: (optional) Value of the Variable.
    """

    def __init__(self,
                 *,
                 description: str = None,
                 name: str = None,
                 secure: bool = None,
                 type: str = None,
                 value: str = None) -> None:
        """
        Initialize a WorkspaceVariableResponse object.

        :param str description: (optional) Variable descrption.
        :param str name: (optional) Variable name.
        :param bool secure: (optional) Variable is secure.
        :param str type: (optional) Variable type.
        :param str value: (optional) Value of the Variable.
        """
        self.description = description
        self.name = name
        self.secure = secure
        self.type = type
        self.value = value

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceVariableResponse':
        """Initialize a WorkspaceVariableResponse object from a json dictionary."""
        args = {}
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'secure' in _dict:
            args['secure'] = _dict.get('secure')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceVariableResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'secure') and self.secure is not None:
            _dict['secure'] = self.secure
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceVariableResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceVariableResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceVariableResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other
