import importlib.metadata
import importlib.util
import io
import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import ClassVar, Dict, List
from zipfile import ZipFile

import requests

from PIModelManager.pandora_model import PandoraModel

logging.getLogger('urllib3').setLevel(logging.ERROR)

model_manager_logger = logging.getLogger("PIModelManager")
model_manager_logger.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
ch.setFormatter(formatter)

model_manager_logger.addHandler(ch)
model_manager_logger.propagate = False


class ModelManager:
    """Singleton class that manages ML models"""

    __instance: ClassVar[object] = None

    _config: ClassVar[Dict] = {}

    _credentials: ClassVar[Dict[str, str]] = {}
    _container: ClassVar[str] = None
    _login_url: ClassVar[str] = None
    _get_files_url: ClassVar[str] = None
    _download_file_url: ClassVar[str] = None
    _upload_file_url: ClassVar[str] = None
    _delete_file_url: ClassVar[str] = None

    _available_files: ClassVar[List[str]] = []
    _downloaded_models: ClassVar[List[PandoraModel]] = []

    def __new__(cls):
        model_manager_logger.info("__new__")
        if ModelManager.__instance is None:
            ModelManager.__instance = object.__new__(cls)
            model_manager_logger.info("__new__: instance is set")
        return ModelManager.__instance

    class BearerAuth(requests.auth.AuthBase):
        def __init__(self, token):
            self.token = token

        def __call__(self, r):
            r.headers["authorization"] = "Bearer " + self.token
            return r

    @classmethod
    def set_credentials(
        cls,
        grant_type: str = os.environ.get("MODEL_MANAGER_GRANT_TYPE", None),
        client_id: str = os.environ.get("MODEL_MANAGER_CLIENT_ID", None),
        client_secret: str = os.environ.get("MODEL_MANAGER_CLIENT_SECRET", None),
        scope: str = os.environ.get("MODEL_MANAGER_SCOPE", None),
        container: str = os.environ.get("MODEL_MANAGER_CONTAINER", None),
        login_url: str = os.environ.get("MODEL_MANAGER_LOGIN_URL", None),
        get_files_url: str = os.environ.get("MODEL_MANAGER_GET_FILES_URL", None),
        download_file_url: str = os.environ.get("MODEL_MANAGER_DOWNLOAD_FILE_URL", None),
    ) -> None:
        """Set credentials for the ModelManager. If args are empty, they are read from environment vars.

        Args:
            grant_type (str): Type of grant
            client_id (str): The consumer key
            client_secret (str): The consumer secret
            scope (str): The control scope
            container (str): The name of the storage container
            login_url (str): The sts login url
            get_files_url (str): The URL for getting a list of available files in a container. Put variables in curly brackets.
            download_file_url (str): The URL for downloading a specific file from a container. Put variables in curly brackets.
        """

        if(not all(
            [
                grant_type,
                client_id,
                client_secret,
                scope,
                container,
                login_url,
                get_files_url,
                download_file_url,
            ]
        )):
            raise Exception("Missing environment variables.")

        cls._credentials = {
            "grant_type": grant_type,
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope,
        }

        cls._container = container
        cls._login_url = login_url
        cls._get_files_url = get_files_url
        cls._download_file_url = download_file_url
        cls._upload_file_url = cls._get_files_url + "/upload"
        cls._delete_file_url = cls._get_files_url + "/{filename}"

    @classmethod
    def __authenticate(cls) -> str:
        """Authenticate with the server.

        Raises:
            Exception: in case the credentials are not previously set using 'set_credentials' method.

        Returns:
            str: Access token
        """
        if not cls._credentials or not cls._login_url:
            raise Exception("Credentials not set. Use method set_credentials.")

        # Authentication request
        response = requests.post(cls._login_url, data=cls._credentials)
        if response.ok:
            result = json.loads(response.text)

            return result["access_token"]
        else:
            return None
    
    @classmethod
    def set_config(cls, path: str) -> None:
        """Set the models configuration

        Args:
            path (str): A Path to the json configuration file

        Raises:
            Exception: if the path does not exist
            Exception: if the configuration file is empty
        """
        if(not Path(path).exists()):
            raise Exception("Path does not exist.")
        
        with open(path) as f:
            config = json.load(f)
            if(not config):
                raise Exception("Config file is empty.")
            
        cls._config = config
        

    @classmethod
    def download_models(cls) -> None:
        """Download all models described in a config.

        Raises:
            Exception: if the config file is invalid.
        """

        if(not cls._config):
            raise Exception("Models config not set.")

        for model in cls._config:
            download_scenario = model.get("download_scenario", None)
            if download_scenario == "pip":
                if model["model_type"] == "spacy":
                    cls.__download_model_pip(model)
                else:
                    raise Exception(f"Invalid config file - pip not supported for model type {model['model_type']}")
            elif download_scenario == "dataservices":
                cls.__download_model_dataservices(model)
            else:
                raise Exception("Invalid config file - missing download scenario.")

    @classmethod
    def __download_model_pip(cls, model: Dict[str, str]) -> None:
        """Download a model as a pip package.

        Args:
            model (Dict[str, str]): model description from a config file

        Raises:
            Exception: if the config file is invalid.
        """

        if model["model_type"] == "spacy":
            name = model.get("name", None)
            version = model.get("version", None)

            if name and version:
                if cls.__pip_package_is_available(name, version):
                    model_manager_logger.info(f"Package {name}-{version} is already installed.")
                else:
                    model_manager_logger.info(f"Downloading package {name}-{version}")
                    package = name + "-" + version
                    subprocess.check_call([sys.executable, "-m", "spacy", "download", package, "--direct"])

                pandora_model = PandoraModel(
                    type=model["model_type"],
                    language=model["language"],
                    size=model["size"],
                    name=name,
                    client=model.get("client", "default"),
                    version=version,
                    path=model.get("path", name),
                )

                if pandora_model not in cls._downloaded_models:
                    cls._downloaded_models.append(pandora_model)
            else:
                raise Exception(
                    "Invalid config file - missing name and/or version fields."
                )
        else:
            Exception(f"Invalid config file - pip not supported for model type {model['model_type']}")

    @classmethod
    def __pip_package_is_available(cls, name: str, version: str) -> bool:
        """Check if a pip package is already installed

        Args:
            name (str): name of the package
            version (str): version of the package

        Returns:
            bool: if the package is installed or not
        """

        try:
            if importlib.util.find_spec(name):
                if importlib.metadata.version(name) == version:
                    return True
        except Exception:
            return False

        return False

    @classmethod
    def __download_model_dataservices(cls, model: Dict[str, str]) -> None:
        """Download a model from dataservices.

        Args:
            model (Dict[str, str]): model description from a config file

        Raises:
            Exception: if the config file is invalid.
        """
        if not cls._credentials:
            raise Exception("Authentication credentials have not been set.")

        cls.__update_available_files()

        language = cls.__clean_str(model["language"])
        name = cls.__clean_str(model["name"])
        client = cls.__clean_str(model.get("client", "default"))
        version = cls.__clean_str(model["version"])

        query = "_".join([language, name, client, version])

        matched_models = [f for f in cls._available_files if f.startswith(query)]
        if len(matched_models) == 0:
            raise Exception(f"Specified model {query} not found in dataservices.")
        elif len(matched_models) > 1:
            raise Exception(
                f"More than one models match the one provided in the config file: {query}."
            )
        else:
            filename = matched_models[0]
            extension = "".join(Path(filename).suffixes)
            #filename = filename.rstrip(extension)
            #extension = filename.split("_")[-1]

            if extension == ".zip":
                model_filename = filename.rstrip(extension)
                temp_path = Path(Path.cwd(), "models", language, name, client, version)
            else:
                model_filename = filename
                temp_path = Path(
                    Path.cwd(), "models", language, name, client, version, filename
                )

            pandora_model = PandoraModel(
                type=model["model_type"],
                language=language,
                size=model.get("size", None),
                name=name,
                client=client,
                version=version,
                path=None,
                filename=model_filename,
            )

            if temp_path.exists():
                # Update model object path and add to _downloaded_models
                pandora_model.path = temp_path
                if pandora_model not in cls._downloaded_models:
                    cls._downloaded_models.append(pandora_model)
                    model_manager_logger.info(f"Model already downloaded in {temp_path}")
            else:
                # Download the model and add to _downloaded_models
                model_manager_logger.info(f"Downloading model in {temp_path}")
                access_token = cls.__authenticate()
                url = cls._download_file_url.replace("{container}", cls._container)
                url = url.replace("{filename}", filename)
                response = requests.get(url, auth=cls.BearerAuth(access_token))

                if response.ok:
                    dir = Path(
                        Path.cwd(),
                        "models",
                        pandora_model.language,
                        pandora_model.name,
                        pandora_model.client,
                        pandora_model.version,
                    )
                    dir.mkdir(parents=True, exist_ok=True)
                    
                    if extension == ".zip":
                        zf = ZipFile(io.BytesIO(response.content), "r")

                        if not zf.namelist():
                            raise Exception(f"Zip file {filename} is empty.")

                        zf.extractall(dir)

                        pandora_model.path = dir
                        cls._downloaded_models.append(pandora_model)

                        model_manager_logger.info(f"Extracted model to: {pandora_model.path}")
                    else:
                        path = Path(dir, pandora_model.filename)

                        with open(path, "wb") as f:
                            f.write(response.content)

                        pandora_model.path = path
                        cls._downloaded_models.append(pandora_model)

                        model_manager_logger.info(f"Saved model to: {pandora_model.path}")

    @classmethod
    def __get_files(cls, token: str) -> List[str]:
        """Returns a list of available model files.

        Args:
            token (str): Authentication bearer token

        Returns:
            List[str]: List of all available model files
        """
        url = cls._get_files_url.replace("{container}", cls._container)
        response = requests.get(url, auth=cls.BearerAuth(token))
        #response.raise_for_status()
        if response.ok:
            return [dict(x)["name"] for x in json.loads(response.text)]
        else:
            return []

    @classmethod
    def __update_available_files(cls) -> None:
        """Updates the list of available files from dataservices."""
        
        access_token = cls.__authenticate()
        cls._available_files = cls.__get_files(access_token)

    @classmethod
    def get_model_path(cls, **kwargs) -> Path:
        """Finds the matching model based on the provided keyword arguments and returns its path.

        Raises:
            Exception: if more than one models are matching the provided arguments
            Exception: if no models are matching the provided arguments

        Returns:
            Path: the local model directory
        """

        matching_models = [
            x
            for x in cls._downloaded_models
            if all([getattr(x, attr) == value for (attr, value) in kwargs.items()])
        ]

        if len(matching_models) > 1:
            raise Exception(f"More than one models are matching your arguments: {kwargs}")
        elif len(matching_models) == 1:
            return matching_models[0].path
        else:
            raise Exception(f"No models are matching your arguments: {kwargs}")


    @classmethod
    def __clean_str(cls, s: str) -> str:
        """Cleans a string by replacing underscores and dots with hyphens

        Args:
            s (str): input string

        Returns:
            str: cleaned string
        """
        
        s = s.replace(".", "-").replace("_","-").lower()
        return s

    @classmethod
    def upload_model(
        cls,
        path: Path,
        zip: bool,
        language: str,
        name: str,
        client: str,
        version: str,
    ) -> None:
        """Uploads a model to dataservices

        Args:
            path (Path): The local path to the model file or directory
            zip (bool): Whether to zip a model directory, or not (upload a file directly)
            language (str): Language of the model
            name (str): Name of the model
            client (str): The target client of the model
            version (str): Version of the model

        Raises:
            Exception: if the model path does not exist
        """
        if path.exists():
            filename = "_".join(map(cls.__clean_str, [language, name, client, version]))
            if zip:
                final_path = Path(shutil.make_archive(filename, "zip", path))
            else:
                extension = "".join(path.suffixes)
                final_path = path.rename(Path(path.parent, f"{filename}{extension}"))

            access_token = cls.__authenticate()
            url = cls._upload_file_url.replace("{container}", cls._container)
            files = {"file": (final_path.name, open(final_path, "rb"), "multipart/form-data")}
            response = requests.post(url, auth=cls.BearerAuth(access_token), files=files)
            if response.ok:
                model_manager_logger.info(f"Successfully uploaded file:\n {response.text}")
            else:
                model_manager_logger.info(f"Error with uploading: {response.status_code}, {response.text}")
        else:
            raise Exception("Model path does not exist.")
        
        
    @classmethod
    def get_files(cls) -> List[str]:
        """Get a list of the latest available model files in dataservices

        Returns:
            List[str]: A list of filenames
        """
        
        cls.__update_available_files()
        return cls._available_files
    
    
    @classmethod
    def delete_file(cls, name: str) -> bool:
        """Delete a file from dataservices

        Args:
            name (str): name of the file (incl. file extension)

        Raises:
            Exception: if the delete method is not successful

        Returns:
            bool: whether the file was successfully deleted
        """
        
        files = cls.get_files()
        if(name in files):
            access_token = cls.__authenticate()
            url = cls._delete_file_url.replace("{container}", cls._container)
            url = url.replace("{filename}", name)
            response = requests.delete(url, auth=cls.BearerAuth(access_token))

            if response.ok:
                return True
            else:
                raise Exception(f"Error with deleting file {name}: {response.status_code}, {response.text}")
        else:
            return False
        
    @classmethod
    def delete_models(cls) -> None:
        """Delete all downloaded and/or installed models."""
        
        for m in cls._downloaded_models:
            if not isinstance(m.path, Path):
                model_manager_logger.info(f"Uninstalling {m.path}")
                subprocess.check_call([sys.executable, "-m", "pip", "uninstall", m.path, "-y"])
        
        if(Path("models").exists()):
            model_manager_logger.info(f"Deleting downloaded models")
            shutil.rmtree(Path("models"))
        
        del cls._downloaded_models[:]