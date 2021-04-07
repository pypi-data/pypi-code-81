import os
import sys
from argparse import ArgumentParser

from .core.setuptools import get_file_content
from .core.resources.api.dir import Dir, DirRoot
from .core.resources.api.disk import Disk
from .core.resources.api.file import File
from .core.resources.api.file_token import FileToken
from .core.resources.api.upload import Upload, UploadRoot
from .core.config import Config


def _handle_args():
    version = get_file_content(os.path.join(os.path.dirname(__file__), "VERSION"))
    parser = ArgumentParser(description="Share Files WEB UI v{version}".format(version=version))
    parser.add_argument("-o", "--host", dest="host", default="0.0.0.0", type=str, help="APP server host")
    parser.add_argument("-p", "--port", dest="port", default=5000, type=int, help="APP server port")
    parser.add_argument("-d", "--share-directory", dest="share_diretory", type=str, help="Directory where shares are stored.")
    parser.add_argument("-u", "--add-user", dest="add_user", type=str, help="Add admin user in user@password format.")
    parser.add_argument("-r", "--remove-user", dest="remove_user", type=str, help="Remove admin user from users list.")
    parser.add_argument("-l", "--list-users", dest="list_users", default=False, action="store_true", help="List existing admin users")
    parser.add_argument("-t", "--list-tokens", dest="list_tokens", default=False, action="store_true", help="List file tokens into stdout")
    parser.add_argument("-c", "--clear-tokens", dest="clear_tokens", default=False, action="store_true", help="Clear file tokens database")

    args = parser.parse_args()
    args.__setattr__("version", version)

    return args


def run_web(host: str, port: int):
    # configure web server and API
    from .core.resources.web import app
    from flask_restful import Api

    with app.app_context():
        api = Api(app)
        api.add_resource(Dir, "/api/dir/<path:path>")
        api.add_resource(DirRoot, "/api/dir/")
        api.add_resource(Disk, "/api/disk/")
        api.add_resource(File, "/api/file/<path:path>")
        api.add_resource(FileToken, "/api/token/<path:path>")
        api.add_resource(Upload, "/api/upload/<path:path>")
        api.add_resource(UploadRoot, "/api/upload/")
        app.run(host=host, port=port)


def main():
    app_args = _handle_args()

    # config directory handling
    home = os.path.expanduser("~")
    app_config_dir = os.path.join(home, ".fileshare")
    if not os.path.exists(app_config_dir):
        os.makedirs(app_config_dir, exist_ok=True)

    # config
    Config.init(app_args, app_config_dir)

    # handle args
    if app_args.add_user:
        try:
            user: str = app_args.add_user.split("@")[0].strip()
            password: str = app_args.add_user.split("@")[1].strip()
            Config.USERS.add_user(user, password)
            Config.USERS.save_json()
            print(f"Admin user '{user}' added sucessfuly")
            return
        except Exception as ex:
            print(f"ERROR: Unable to parse user@password format: {ex}")
            sys.exit(1)
    elif app_args.remove_user:
        if Config.USERS.remove_user(app_args.remove_user):
            Config.USERS.save_json()
            print(f"User '{app_args.remove_user}' has been removed")
        else:
            print(f"User '{app_args.remove_user}' is not exist")
        return 
    elif app_args.list_users:
        for user in Config.USERS.data.keys():
            print(user)
        return
    elif app_args.list_tokens:
        token_path_list: list = list(Config.FILE_TOKENS.data.keys())
        token_path_list.sort()
        for token_path in token_path_list:
            print(f"{token_path}\t{Config.FILE_TOKENS.data[token_path]}")
        return
    elif app_args.clear_tokens:
        Config.FILE_TOKENS.data = {}
        Config.FILE_TOKENS.save_json()
        print("All tokens has been removed")
        return

    if not app_args.share_diretory:
        print("ERROR: Share directory must be specified")
        sys.exit(1)

    run_web(app_args.host, app_args.port)


if __name__ == '__main__':
    main()
