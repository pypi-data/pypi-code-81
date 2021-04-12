import hashlib
import io
import pickle
import time
from functools import wraps
from os import makedirs
from os.path import expanduser, isfile, splitext
from pathlib import Path
from time import sleep
from typing import Callable, List, Union

import requests

from .authentication import (Authentication, NeedAuthentication,
                             need_authentication)
from .entity import Entity
from .utils import (MIME, get_argument_from_json, get_content_from_response,
                    get_domain, get_information, get_metadatarecord,
                    map_metadatarecord_to_result)
from .utils.errors import (DomainException, NotServiceException,
                           RefreshTokenExpirationException,
                           catch_requests_error, ensure_response_ok)


class Service(Entity, NeedAuthentication):
    """
    Class to use ELG service. Run an ELG service directly from python.

    Examples::

        from elg import Service

        # You can initialize a service from its id. You will be asked to authenticate on the ELG website.
        service = Service.from_id(474)

        # You can then directly run the service.
        result = service("Nikolas Tesla lives in Berlin.")
        print(f"\\nResult:\\n{result.get('response')}")

        # You can also create a service from a catalog search result.

        # First you need to search for a service using the catalog. Let's search an English to French Machine Translation service.
        from elg import Catalog

        catalog = Catalog()
        results = catalog.search(
            resource = "Tool/Service",
            function = "Machine Translation",
            languages = ["en", "fr"],
            limit = 1,
        )

        # Now you can initialize the service using the first result. You will not be asked to authenticate because your token has been cached.
        service = Service.from_entity(results[0])

        # And run the service as before.
        result = service("ELG is an amazing project.")
        print(f"\\nResult:\\n{result.get('response')}")

        # It is possible to use a file as input when running the service.
        with open("/tmp/example.txt", "w") as f:
            f.write("ELG is an amazing project.")

        result = service("/tmp/example.txt")
        print(f"\\nResult:\\n{result.get('response')}")

        # You can apply a method to the result to extract the information needed. To do so, you have to pass a 
        # callable object in the ouput_func parameter.
        service = Service.from_id(5228)
        pretty_result = service("Ich habe diesen Film geliebt. Die Schauspieler, das Drehbuch: alles von einem Meisterwerk.", output_func=lambda x: x["response"]["texts"][0]["content"])
        print("Translation to Finnish: ", pretty_result)

        # You can also set the output_func parameter to "auto" to extract the information needed automaticly. 
        # This is not working for all the services.
        service = Service.from_id(5228)
        pretty_result = service("Ich habe diesen Film geliebt. Die Schauspieler, das Drehbuch: alles von einem Meisterwerk.", output_func="auto")
        print("Translation to Finnish: ", pretty_result)
    """

    def __init__(
        self,
        id: int,
        resource_name: str,
        resource_short_name: List[str],
        resource_type: str,
        entity_type: str,
        description: str,
        keywords: List[str],
        detail: str,
        licences: List[str],
        languages: List[str],
        country_of_registration: List[str],
        creation_date: str,
        last_date_updated: str,
        functional_service: bool,
        functions: List[str],
        intended_applications: List[str],
        views: int,
        downloads: int,
        size: int,
        service_execution_count: int,
        status: str,
        under_construction: bool,
        record: dict,
        auth_object: Authentication,
        auth_file: str,
        scope: str,
        domain: str,
        use_cache: bool,
        cache_dir: str,
    ):
        """
        Init a Service object with the service information
        """
        super().__init__(
            id=id,
            resource_name=resource_name,
            resource_short_name=resource_short_name,
            resource_type=resource_type,
            entity_type=entity_type,
            description=description,
            keywords=keywords,
            detail=detail,
            licences=licences,
            languages=languages,
            country_of_registration=country_of_registration,
            creation_date=creation_date,
            last_date_updated=last_date_updated,
            functional_service=functional_service,
            functions=functions,
            intended_applications=intended_applications,
            views=views,
            downloads=downloads,
            size=size,
            service_execution_count=service_execution_count,
            status=status,
            under_construction=under_construction,
            domain=domain,
            record=record,
        )
        if self.resource_type != "ToolService" and self.resource_type != "Tool/Service":
            raise NotServiceException(self.id)
        self._authenticate(
            auth_object=auth_object, auth_file=auth_file, scope=scope, use_cache=use_cache, cache_dir=cache_dir
        )
        self._get_elg_execution_location()
        self._get_resource_info()

    @classmethod
    def from_id(
        cls,
        id: int,
        auth_object: Authentication = None,
        auth_file: str = None,
        scope: str = None,
        domain: str = None,
        use_cache: bool = True,
        cache_dir: str = "~/.cache/elg",
    ):
        """
        Class method to init a Service class from its id. You can provide authentication information through the
        auth_object or the auth_file attributes. If not authentication information is provided, the Authentication
        object will be initialized.

        Args:
            id (int): id of the service.
            auth_object (elg.Authentication, optional): elg.Authentication object to use. Defaults to None.
            auth_file (str, optional): json file that contains the authentication tokens. Defaults to None.
            scope (str, optional): scope to use when requesting tokens. Can be set to "openid" or "offline_access"
                to get offline tokens. Defaults to "openid".
            domain (str, optional): ELG domain you want to use. "live" to use the public ELG, "dev" to use the
                development ELG and another value to use a local ELG. Defaults to "live".
            use_cache (bool, optional): True if you want to use cached files. Defaults to True.
            cache_dir (str, optional): path to the cache_dir. Set it to None to not store any cached files. Defaults to "~/.cache/elg".

        Returns:
            elg.Service: Service object with authentication information.
        """
        # Use auth_object/file domain if auth_object/file given
        if auth_object is not None:
            assert isinstance(
                auth_object, Authentication
            ), f"auth_object ({type(auth_object)}) must be an Authentication object."
            auth_domain = auth_object.domain
            if domain is not None:
                print(
                    "Warning: domain argument saved in the authentication object will overwrite the "
                    "domain argument you put."
                )
            domain = auth_domain
        elif isinstance(auth_file, str):
            auth_domain = get_argument_from_json(auth_file, "domain")
            if domain is not None:
                print(
                    "Warning: domain argument saved in the authentication filename will overwrite the "
                    "domain argument you put."
                )
            domain = auth_domain
        # Use "live" domain by default
        domain = get_domain(domain=domain if domain is not None else "live")
        record = get_metadatarecord(id=id, domain=domain, use_cache=use_cache, cache_dir=cache_dir)
        result = map_metadatarecord_to_result(id=id, record=record)
        result["auth_object"] = auth_object
        result["auth_file"] = auth_file
        result["scope"] = scope
        result["domain"] = domain
        result["use_cache"] = use_cache
        result["cache_dir"] = cache_dir
        return cls(**result)

    @classmethod
    def from_entity(
        cls,
        entity: Entity,
        auth_object: str = None,
        auth_file: str = None,
        scope: str = None,
        use_cache: bool = True,
        cache_dir="~/.cache/elg",
    ):
        """
        Class method to init a Service class from an Entity object. You can provide authentication information through the
        auth_object or the auth_file attributes. If not authentication information is provided, the Authentication object will be initialized.

        Args:
            entity (elg.Entity): Entity object to init as a Service.
            auth_object (elg.Authentication, optional): elg.Authentication object to use. Defaults to None.
            auth_file (str, optional): json file that contains the authentication tokens. Defaults to None.
            scope (str, optional): scope to use when requesting tokens. Can be set to "openid" or "offline_access"
                to get offline tokens. Defaults to "openid".
            domain (str, optional): ELG domain you want to use. "live" to use the public ELG, "dev" to use the
                development ELG and another value to use a local ELG. Defaults to "live".
            use_cache (bool, optional): True if you want to use cached files. Defaults to True.
            cache_dir (str, optional): path to the cache_dir. Set it to None to not store any cached files. Defaults to "~/.cache/elg".

        Returns:
            elg.Service: Service object with authentication information.
        """
        if entity.record is None:
            entity.record = get_metadatarecord(
                id=entity.id, domain=entity.domain, use_cache=use_cache, cache_dir=cache_dir
            )
        parameters = entity.__dict__
        parameters["auth_object"] = auth_object
        parameters["auth_file"] = auth_file
        parameters["scope"] = scope
        parameters["use_cache"] = use_cache
        parameters["cache_dir"] = cache_dir
        return cls(**parameters)

    def _get_elg_execution_location(self):
        """
        Method to get the elg execution location information from the metadata record.
        """
        self.elg_execution_location_sync = get_information(
            id=self.id, obj=self.record, infos=["service_info", "elg_execution_location_sync"]
        )
        self.elg_execution_location = get_information(
            id=self.id, obj=self.record, infos=["service_info", "elg_execution_location"]
        )

    def _get_resource_info(self):
        """
        Method to get the resource information from the metadata record.
        """
        self.processing_resource_type = None
        self.input_media_type = None
        self.input_data_format = None
        self.input_character_encoding = None
        self.default_content_type = None
        self.output_media_type = None
        self.output_data_format = None
        self.output_character_encoding = None
        # input
        input_content_resources = get_information(
            id=self.id, obj=self.record, infos=["described_entity", "lr_subclass", "input_content_resource"]
        )
        for input_content_resource in input_content_resources:
            self.processing_resource_type = input_content_resource.get("processing_resource_type")
            self.input_media_type = input_content_resource.get("media_type")
            self.input_data_format = input_content_resource.get("data_format")
            self.input_character_encoding = input_content_resource.get("character_encoding")
            if isinstance(self.input_media_type, str) and "text" in self.input_media_type:
                self.default_content_type = "text/plain"
            elif isinstance(self.input_media_type, str) and "audio" in self.input_media_type:
                self.default_content_type = "audio/x-wav"
            else:
                self.default_content_type = (
                    "text/plain"  # put text/plain as default_content_type to not raise an Error
                )
            if isinstance(self.input_media_type, str):
                break
        self._get_opening_mode()
        # output
        output_content_resources = get_information(
            id=id, obj=self.record, infos=["described_entity", "lr_subclass", "output_resource"]
        )
        for output_content_resource in output_content_resources:
            self.output_media_type = output_content_resource.get("media_type")
            self.output_data_format = output_content_resource.get("data_format")
            self.output_character_encoding = output_content_resource.get("character_encoding")
            if isinstance(self.output_media_type, str):
                break

    def _get_content_type(self, filename: str) -> str:
        """
        Method to get the content type of a file.

        Args:
            filename (str): name of the file.

        Returns:
            str: content type of the file
        """
        _, extension = splitext(filename)
        content_type = MIME.get_content_type(extension)
        if content_type is None:
            content_type = self.default_content_type
        return content_type

    def _get_opening_mode(self):
        """
        Method to get the opening mode of the service.

        Raises:
            ValueError: the character encoding is not recognized.
        """
        if self.input_character_encoding is None or (
            isinstance(self.input_character_encoding, list) and len(self.input_character_encoding) == 0
        ):
            mode = "rb"
        elif isinstance(self.input_character_encoding, list):
            assert len(self.input_character_encoding) == 1, f"Entity {self.id} has multiple input character encoding"
            if "UTF-8" in self.input_character_encoding[0]:
                mode = "r"
            else:
                raise ValueError(f"Character encoding ({self.input_character_encoding}) not recognized.")
        else:
            raise ValueError(f"Character encoding ({self.input_character_encoding}) not recognized.")
        self.opening_mode = mode

    @need_authentication()
    def __call__(
        self,
        input_str: str = None,
        sync_mode: bool = False,
        timeout: int = None,
        check_file: bool = True,
        verbose: bool = True,
        output_func: Union[str, Callable] = lambda response: response,
    ) -> Union[dict, str]:
        """
        Method to call a service. You can enter a string input or the path to the file to process.
        The output is returned in JSON format.

        Args:
            input_str (str, optional): can be the text to process directly or the name of the file to process.
                Defaults to None.
            sync_mode (bool, optional): True to use the sync_mode. Defaults to False.
            timeout (int, optional): number of seconds before timeout. Defaults to None.
            check_file (bool, optional): True to check if input_str can be a file or not. Defaults to True.
            verbose (bool, optional): False to avoid print messages. Defaults to True.
            output_func (Union[str, Callable], optional): function applied to the service response. It can be used
                to extract only the content from the response. If set to 'auto', a generic extractive function will
                be used. Defaults to lambda response: response.

        Raises:
            ValueError: the input_str is None.
            ElgException: can raise a specific Elg exception if the request to the service did not succeed.

        Returns:
            Union[dict, str]: service response in JSON format or as a string if output_func returns a string.
        """
        if input_str is None:
            raise ValueError("You need to provide at least a filename or text as string.")

        if isinstance(output_func, str) and output_func == "auto":
            output_func = get_content_from_response
        if not callable(output_func):
            raise ValueError("output_func should be a callable object or 'auto'.")

        if verbose:
            print(f"Calling:\n\t[{self.id}] {self.resource_name}")

        headers = {
            "Authorization": f"Bearer {self.authentication.access_token}",
        }
        if check_file and isfile(input_str):
            headers["Content-Type"] = self._get_content_type(input_str)
            if verbose:
                print(f"Found filename as input:\n\t{input_str}\n")
            with open(input_str, self.opening_mode) as f:
                if sync_mode:
                    return self._call_sync(f=f, headers=headers, timeout=timeout, output_func=output_func)
                else:
                    return self._call_async(f=f, headers=headers, timeout=timeout, output_func=output_func)
        else:
            headers["Content-Type"] = "text/plain"
            if verbose:
                print(f"Found plain text as input:\n\t{input_str}\n")
            with io.BytesIO(input_str.encode("utf-8")) as f:
                if sync_mode:
                    return self._call_sync(f=f, headers=headers, timeout=timeout, output_func=output_func)
                else:
                    return self._call_async(f=f, headers=headers, timeout=timeout, output_func=output_func)

    @catch_requests_error
    def _call_sync(self, f: io.IOBase, headers: dict, timeout: int, output_func: Callable) -> Union[dict, str]:
        """
        Method used by __call__ to call a service synchronously.

        Args:
            f (io.IOBase): input file.
            headers (dict): headers for the call.
            timeout (int): number of seconds before timeout.
            output_func (Union[str, Callable], optional): function applied to the service response. It can be used
                to extract only the content from the response. If set to 'auto', a generic extractive function will
                be used. Defaults to lambda response: response.

        Returns:
            Union[dict, str]: service response in JSON format or as a string if output_func returns a string.
        """
        response = requests.post(self.elg_execution_location_sync, headers=headers, data=f, timeout=timeout)
        ensure_response_ok(response)
        return output_func(response.json())

    @catch_requests_error
    def _call_async(self, f: io.IOBase, headers: dict, timeout: int, output_func: Callable) -> Union[dict, str]:
        """
        Method used by __call__ to call a service asynchronously.

        Args:
            f (io.IOBase): input file.
            headers (dict): headers for the call.
            timeout (int): number of seconds before timeout.
            output_func (Union[str, Callable], optional): function applied to the service response. It can be used
                to extract only the content from the response. If set to 'auto', a generic extractive function will
                be used. Defaults to lambda response: response.

        Returns:
            Union[dict, str]: service response in JSON format or as a string if output_func returns a string.
        """
        response = requests.post(self.elg_execution_location, headers=headers, data=f, timeout=timeout)
        ensure_response_ok(response)
        response = response.json()["response"]
        assert response["type"] == "stored"
        headers.pop("Content-Type")
        uri = response["uri"]
        response = requests.get(uri, headers=headers)
        waiting_time = time.time()
        while response.ok and "progress" in response.json().keys():
            sleep(1)
            response = requests.get(uri, headers=headers, timeout=timeout)
            if time.time() - waiting_time > (timeout if timeout is not None else float("inf")):
                raise requests.exceptions.Timeout("The service didn't respond before the end of the timeout.")
        ensure_response_ok(response)
        return output_func(response.json())
