import io
from os.path import splitext

import requests

from .authentification import Authentification
from .utils import MIME


class PostRequestError(Exception):
    def __init__(self, response):
        self.message = f"Error status code: {response.status_code}"
        super().__init__(self.message)


class NotTechnologyError(Exception):
    def __init__(self, id):
        self.message = f"The entity with id={id} is not a technology."
        super().__init__(self.message)


class MissingInformationError(Exception):
    def __init__(self, id, information):
        self.message = f"The entity with id={id} does not have the information: {information}."
        super().__init__(self.message)


def need_authentification():
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            self.authentification.refresh_if_needed()
            result = func(self, *args, **kwargs)
            return result

        return wrapper

    return decorator


class Technology(object):

    api_url = "{}/catalogue_backend/api/registry/"

    def __init__(self, id, authentification_filename=None, scope=None, domain=None):

        if isinstance(authentification_filename, str):
            if scope != None or domain != None:
                print(
                    "Warning: scope and domain arguments saved in the authentification filename will overwrite the scope and domain arguments you put."
                )
            self.authentification = Authentification.from_json(authentification_filename)
        else:
            scope = scope if scope != None else "openid"
            domain = domain if domain != None else "live"
            self.authentification = Authentification.init(scope, domain)

        self.id = id
        self._get_metadatarecord()
        self._check_is_technology()
        self._get_elg_execution_location_sync()
        self._get_resource_info()

    def _get_metadatarecord(self):
        response = requests.get(self.api_url.format(self.authentification.domain) + f"metadatarecord/{self.id}")
        if not response.ok:
            raise PostRequestError(response)
        record = response.json()
        if record == None:
            raise PostRequestError(response)
        self.record = record

    def _check_is_technology(self):
        entity_type = self.record.get("described_entity").get("entity_type")
        if entity_type == None or entity_type != "LanguageResource":
            raise NotTechnologyError(self.id)
        lr_type = self.record.get("described_entity").get("lr_subclass").get("lr_type")
        if lr_type == None or lr_type != "ToolService":
            raise NotTechnologyError(self.id)

    def _get_elg_execution_location_sync(self):
        service_info = self.record.get("service_info")
        if service_info == None:
            raise MissingInformationError(self.id, "service_info")
        elg_execution_location_sync = service_info.get("elg_execution_location_sync")
        if elg_execution_location_sync == None:
            raise MissingInformationError(self.id, "elg_execution_location_sync")
        self.elg_execution_location_sync = elg_execution_location_sync

    def _get_resource_info(self):
        # input
        input_content_resource = self.record.get("described_entity").get("lr_subclass").get("input_content_resource")
        assert input_content_resource != None
        assert len(input_content_resource) == 1, f"Entity {self.id} has multiple input content resource"
        input_content_resource = input_content_resource[0]
        self.processing_resource_type = input_content_resource.get("processing_resource_type")
        self.input_media_type = input_content_resource.get("media_type")
        self.input_data_format = input_content_resource.get("data_format")
        self.input_character_encoding = input_content_resource.get("character_encoding")
        if "text" in self.input_media_type:
            self.default_content_type = "text/plain"
        elif "audio" in self.input_media_type:
            self.default_content_type = "audio/x-wav"
        else:
            raise ValueError(f"Content-Type not detected in {self.input_media_type}")
        self._get_opening_mode()
        # output
        output_content_resource = self.record.get("described_entity").get("lr_subclass").get("output_resource")
        assert output_content_resource != None
        assert len(output_content_resource) == 1, f"Entity {self.id} has multiple output content resource"
        output_content_resource = output_content_resource[0]
        self.output_media_type = output_content_resource.get("media_type")
        self.output_data_format = output_content_resource.get("data_format")
        self.output_character_encoding = output_content_resource.get("character_encoding")

    @need_authentification()
    def __call__(self, filename=None, text_data=None):
        if (filename == None and text_data == None) or (filename != None and text_data != None):
            raise ValueError("You need to provide at least a filename or text_data, but not the two.")
        headers = {
            "Authorization": f"Bearer {self.authentification.access_token}",
        }
        if isinstance(filename, str):
            headers["Content-Type"] = self._get_content_type(filename)
            with open(filename, self.opening_mode) as f:
                response = requests.post(self.elg_execution_location_sync, headers=headers, files={"file": f})
        else:
            headers["Content-Type"] = "text/plain"
            f = io.StringIO(text_data)
            response = requests.post(self.elg_execution_location_sync, headers=headers, files={"file": f})
        if response.ok:
            return response.json(), response.status_code
        return response.content, response.status_code

    def _get_content_type(self, filename):
        _, extension = splitext(filename)
        content_type = MIME.get_content_type(extension)
        if content_type == None:
            content_type = self.default_content_type
        return content_type

    def _get_opening_mode(self):
        if self.input_character_encoding == None:
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
