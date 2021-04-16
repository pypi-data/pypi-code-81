import json
import click
from .uploader import Uploader
from .app import App
from . import config, auth


@click.group()
def main():
    pass


@main.command()
@click.argument("path")
@click.argument("bucket_id", type=str)
@click.option("--service-account-json", type=click.Path(exists=False))
def upload(path, bucket_id, service_account_json):
    u = Uploader(
        bucket_id=bucket_id,
        service_account_json=service_account_json,
    )
    u.start(path)


@main.command()
@click.option("--client-secrets-json", type=click.Path(exists=False), default=None)
def authenticate(client_secrets_json):
    json = client_secrets_json if client_secrets_json else config.client_secrets_path
    credentials = auth.get_credentials(json)
    auth.save_credentials(credentials, config.user_credentials_path)


@main.command()
@click.argument("path")
def gen_key(path):
    key = auth.gen_key()
    with open(path, "wb") as f:
        f.write(key)

@main.command()
@click.argument("salt-path")
@click.argument("path")
def gen_key_from_password(salt_path, path):
    pw = input("Enter password: ")
    new_key = auth.key_from_password(pw.encode('utf-8'), salt_path)
    with open(path, "wb") as f:
        f.write(new_key)

@main.command()
@click.argument("key1")
@click.argument("key2")
@click.argument("path")
def encrypt_key(key1, key2, path):
    """
    Encrypt key1 with key2
    """
    cipher = auth.get_cipher(key1)
    with open(path, "wb") as f1, open(key2, "rb") as f2:
        f1.write(cipher.encrypt(f2.read()))

@main.command("pickle-service-account-file")
@click.argument("path-in")
@click.argument("key-file")
@click.option("--output-file", default=config.service_account_path)
@click.option("--bucket", default=None)
def pickle_service_account_file(path_in, key_file, output_file, bucket):
    with open(path_in, "r") as f:
        data = json.load(f)
    auth.pickle_service_account_credentials(data, output_file, key_file, bucket)


@main.command("pickle-client-secrets-file")
@click.argument("path-in")
@click.argument("key-file")
def pickle_client_secrets_file(path_in, key_file):
    with open(path_in, "r") as f:
        data = json.load(f)
    auth.pickle_client_secret_file(data, config.client_secrets_path, key_file)


@main.command()
@click.option("--key-file", type=click.Path(exists=False), default=None)
@click.option(
    "--service-account-file",
    type=click.Path(exists=False),
    default=config.service_account_path,
)
@click.option(
    "--user-credentials-file",
    type=click.Path(exists=False),
    default=config.get_user_credentials_path(),
)
@click.option(
    "--client-secret-file",
    type=click.Path(exists=False),
    default=config.client_secrets_path,
)
@click.option("--title", default="GCS Uploader")
@click.option("--with-authentication", is_flag=True)
@click.option("--with-service-account", is_flag=True)
@click.option("--with-bucket-id", is_flag=True)
@click.option("--with-password", is_flag=True)
@click.option("--with-checkboxes", is_flag=True)
@click.option("--dry-run", is_flag=True)
def gui(
    key_file,
    service_account_file,
    user_credentials_file,
    client_secret_file,
    title,
    with_authentication,
    with_service_account,
    with_bucket_id,
    with_checkboxes,
    with_password,
    dry_run,
):
    app = App(
        key=key_file,
        title=title,
        with_authentication=with_authentication,
        with_service_account=with_service_account,
        with_bucket_id=with_bucket_id,
        with_checkboxes=with_checkboxes,
        with_password=with_password,
        dry_run=dry_run,
        service_account_path=service_account_file,
        user_credentials_path=user_credentials_file,
        client_secrets_path=client_secret_file,
    )
    app.run()
