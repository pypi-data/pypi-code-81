from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import pickle
import json
import os
import pathlib
from typing import Dict, Any, Union, Iterable, Optional, Tuple
from google_auth_oauthlib import flow
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

KeyT = Union[str, bytes, pathlib.Path]


def _load_file(path: pathlib.Path) -> Dict[str, Any]:
    if path.suffix == ".json":
        with open(path, "rb") as f:
            data = json.load(f)
    elif path.suffix == ".pickle":
        with open(path, "rb") as f:
            data = pickle.load(f)
    else:
        raise ValueError(f"Unknown file type: {path}")
    return data


def get_credentials(client_id: str, client_secret: str) -> Credentials:
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        }
    }
    scopes = ("https://www.googleapis.com/auth/devstorage.read_write",)

    app_flow = flow.InstalledAppFlow.from_client_config(client_config, scopes=scopes)
    app_flow.run_local_server()  # Should catch exception here?
    return app_flow.credentials


def credentials_to_dict(credentials: Credentials) -> Dict[str, Any]:
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def pickle_user_credentials(
    credentials: Credentials,
    path: pathlib.Path,
    key: KeyT,
) -> None:
    path = pathlib.Path(path)
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True, exist_ok=True)
    credentials.token = None
    data = credentials_to_dict(credentials)
    encrypt_fields(data, ("refresh_token", "client_id", "client_secret"), key)
    with open(path, "wb") as f:
        pickle.dump(data, f)


def unpickle_user_credentials(path: pathlib.Path, key: KeyT) -> Credentials:
    data = _load_file(path)
    decrypt_fields(data, ("refresh_token", "client_id", "client_secret"), key)
    return Credentials(**data)


def key_from_password(pw, salt):
    if os.path.isfile(salt):
        with open(salt, "rb") as f:
            salt = f.read()
    elif isinstance(salt, str):
        salt = salt.encode('utf-8')
    if isinstance(pw, str):
        pw = pw.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(pw))
    return key

def encrypt_fields(data: Dict[str, Any], keys: Iterable[str], key: KeyT) -> None:
    cipher = get_cipher(key)
    for k in keys:
        data[k] = cipher.encrypt(data[k].encode("utf-8"))


def decrypt_fields(data: Dict[str, Any], keys: Iterable[str], key: KeyT) -> None:
    if key is None:
        return
    cipher = get_cipher(key)
    for k in keys:
        data[k] = cipher.decrypt(data[k]).decode("utf-8")


def unpickle_service_account_credentials(
    path: pathlib.Path, key: KeyT, as_credentials: bool = True
) -> Tuple[Union[Credentials, Dict[str, Any]], Optional[str]]:
    data = _load_file(path)
    decrypt_fields(data, ("private_key_id", "private_key"), key)
    bucket = data.pop("bucket") if "bucket" in data else None
    if as_credentials:
        creds: Credentials = service_account.Credentials.from_service_account_info(data)
        return creds, bucket
    return data, bucket


def pickle_service_account_credentials(
    data: Dict[str, Any], path: pathlib.Path, key: KeyT, bucket: Optional[str] = None
) -> None:
    data = {
        k: data[k]
        for k in [
            "private_key",
            "private_key_id",
            "token_uri",
            "client_email",
        ]
    }
    encrypt_fields(data, ("private_key_id", "private_key"), key)
    if bucket is not None:
        data["bucket"] = bucket
    with open(path, "wb") as f:
        pickle.dump(data, f)


def unpickle_client_secret_file(path: pathlib.Path, key: KeyT) -> Dict[str, Any]:
    with open(path, "rb") as f:
        data: Dict[str, Any] = pickle.load(f)
    decrypt_fields(
        data["installed"],
        ("client_secret",),
        key,
    )
    return data


def pickle_client_secret_file(
    data: Dict[str, Any], path: pathlib.Path, key: KeyT
) -> None:
    encrypt_fields(data["installed"], ("client_secret",), key)
    with open(path, "wb") as f:
        pickle.dump(data, f)


def get_credentials_via_client_secrets_file(
    pickled_client_secret_file: pathlib.Path, key: KeyT
) -> Credentials:
    data = unpickle_client_secret_file(pickled_client_secret_file, key)
    appflow = flow.InstalledAppFlow.from_client_config(
        data,
        scopes=["https://www.googleapis.com/auth/devstorage.read_write"],
    )
    appflow.run_local_server()
    return appflow.credentials


def gen_key() -> bytes:
    return Fernet.generate_key()


def get_cipher(key: KeyT) -> Fernet:
    if os.path.isfile(key):
        with open(key, "rb") as f:
            return Fernet(f.read())
    elif isinstance(key, (str, bytes)):
        return Fernet(key)
    else:
        raise ValueError(f"Failed to instantiate new `Fernet` from {key}")


def default_bucket_from_service_account_file(
    service_account_path: pathlib.Path,
) -> Optional[str]:
    if not os.path.isfile(service_account_path):
        return None
    data = _load_file(service_account_path)
    return data.pop("bucket") if "bucket" in data else None
