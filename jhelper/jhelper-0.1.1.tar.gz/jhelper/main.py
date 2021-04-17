from jhelper.spliter import splite2chunks
import re
import json
from pathlib import Path
from argparse import ArgumentParser
from requests import session
from jhelper.encode import encode_file
from jhelper.decode import JDecoder

BUILD_PATH = "/job/to-inside/build?delay=0sec&Jenkins-Crumb={}"
BASE_URL = "https://192.168.100.66"
REGEX = r'crumb.init\("Jenkins-Crumb", "([a-zA-Z0-9]+)"\)'
REQUEST_PATH = "/job/to-inside/build?delay=0sec"
MAX_SIZE = 8000000


class CrumbGetter:
    def __init__(self, username, password, base_url=BASE_URL):
        self.username = username
        self.password = password
        self.crumb = None
        self.base_url = BASE_URL
        self.session = session()

    def _login(self):
        self.session.post(
            url="https://192.168.100.66/j_acegi_security_check",
            verify=False,
            data={
                "j_username": self.username,
                "j_password": self.password,
                "from": "/",
                "Submit": "登录",
            },
        )

    def _get_crumb(self):
        resp = self.session.get(f"{self.base_url}{REQUEST_PATH}")
        match_pat = re.search(REGEX, resp.text)
        self.crumb = match_pat.group(1)

    def get_crumb(self):
        self._login()
        self._get_crumb()


class ToInsider:
    def __init__(self, session, crumb, encode, base_url=BASE_URL):
        self.session = session
        self.path = BUILD_PATH.format(crumb)
        self.crumb = crumb
        self.encode = encode
        self.base_url = base_url

    def send(self, filelocation):
        with open(filelocation, "rb") as f:
            name, data = encode_file(self.encode, f)
            self.session.post(
                f"{self.base_url}{self.path}",
                files={"file0": (name, data)},
                data=self._build_body(),
            )

    def _build_file(self, fp):
        if not self.encode:
            return (fp.name, fp.read)

    def _build_json_filed(self):
        return {
            "parameter": {"name": "toinside", "file": "file0"},
            "statusCode": "303",
            "redirectTo": ".",
            "Jenkins-Crumb": [
                f"{self.crumb}",
                f"{self.crumb}",
            ],
        }

    def _build_body(self):
        json_field = self._build_json_filed()
        return {
            "name": "toinside",
            "Jenkins-Crumb": f"{self.crumb}",
            "Submit": "开始构建",
            "statusCode": 303,
            "redirectTo": ".",
            "json": json.dumps(json_field),
        }


class UserInfo:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.userinfo = Path.home() / ".jenkins_userinfo"

    def read(self):
        if not self.username or not self.password:
            with open(self.userinfo, "r") as f:
                [self.username, self.password] = f.readlines()
                self.username = self.username.strip()
                self.password = self.password.strip()

    def save(self):
        if self.password and self.username:
            with open(self.userinfo, "w") as f:
                f.write(f"{self.username}\n{self.password}")


def _upload(userinfo, args, filepath=None):
    client = CrumbGetter(userinfo.username, userinfo.password)
    client.get_crumb()

    to_inside = ToInsider(client.session, client.crumb, args.encode)
    if not filepath:
        to_inside.send(args.filepath)
    else:
        to_inside.send(filepath)


def _upload_dir(dirpath, userinfo, args):
    chunks = [chunk for chunk in Path(dirpath).iterdir()]
    chunks.sort(key=lambda x: x.name)
    for chunk in chunks:
        if chunk.name != "fs_manifest.csv":
            _upload(userinfo, args, chunk)


def upload(userinfo, args):
    filepath = Path(args.filepath)
    lstat = filepath.lstat()
    if lstat.st_size > MAX_SIZE:
        chunksdir = splite2chunks(filepath)
        args.encode = True
        _upload_dir(chunksdir.name, userinfo, args)
    else:
        _upload(userinfo, args)


def main():
    parser = ArgumentParser()
    parser.add_argument("--username", help="用户名")
    parser.add_argument("--password", help="密码")
    parser.add_argument("-e", "--encode", help="加密", action="store_true", default=False)
    parser.add_argument("-d", "--decode", help="解密文件")
    parser.add_argument("filepath", help="待上传文件")
    args = parser.parse_args()

    if args.decode:
        jdecoder = JDecoder(args.decode, args.filepath)
        jdecoder.decode()
    else:
        userinfo = UserInfo(args.username, args.password)
        userinfo.read()
        upload(userinfo, args)

        userinfo.save()
