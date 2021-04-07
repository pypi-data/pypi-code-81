"""
snapsheets.core
"""

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pendulum
import toml
from icecream import ic


@dataclass
class Config:
    confd: str = "."
    saved: str = "."

    def get_fnames(self, pattern: str) -> List[Path]:
        p = Path(self.confd)
        fnames = sorted(p.glob(pattern))
        return fnames

    def load_yaml(self) -> Dict[Any, Any]:
        config: Dict[Any, Any] = {}
        fnames = self.get_fnames("*.yml")
        n = len(fnames)
        ic("Loaded YAML files: ", n)
        for fname in fnames:
            with open(fname) as f:
                c = yaml.safe_load(f)
                config.update(c)
        return config

    def load_toml(self) -> Dict[Any, Any]:
        config: Dict[Any, Any] = {}
        fnames = self.get_fnames("*.toml")
        n = len(fnames)
        ic("Loaded TOML files: ", n)
        for fname in fnames:
            c = toml.load(fname)
            config.update(c)
        return config

    def load_config(self) -> Dict[Any, Any]:
        config: Dict[Any, Any] = {}
        c = self.load_yaml()
        config.update(c)
        c = self.load_toml()
        config.update(c)
        self.config = config

        return config

    def sections(self) -> List[str]:
        return sorted(self.config.keys())

    def volumes(self) -> Optional[str]:
        return self.config.get("volumes")

    def options(self) -> Optional[str]:
        return self.config.get("options")

    def datefmt(self) -> Optional[str]:
        return self.config.get("datefmt")

    def sheets(self) -> Any:
        return self.config.get("sheets")

    def sheet_names(self) -> Any:
        sheets = self.sheets()
        names = sorted(sheets.keys())
        return names

    def sheet(self, name: str) -> Any:
        sheets = self.sheets()
        return sheets.get(name)


@dataclass
class Sheet(Config):
    url: Union[str, Optional[str]] = None
    key: Optional[str] = None
    gid: Optional[str] = None
    fmt: str = "xlsx"
    desc: Optional[str] = None
    fname: Optional[str] = "snapshot"
    datefmt: Optional[str] = "%Y%m%dT%H%M%S"

    def __post_init__(self) -> None:
        self.set_savef()

        if self.url is not None:
            self.set_key_gid_from_url()
        else:
            msg = f"URL : {self.url} / key : {self.key}"
            ic(msg)
        return

    def set_savef(self) -> None:
        fmt = f".{self.fmt}"
        fname = Path(self.fname)
        self.savef = Path(self.saved) / fname.with_suffix(fmt)
        return

    def set_key_gid_from_url(self) -> None:
        url = self.url
        if url.startswith("https://"):
            self.key = url.split("/")[-2]
            self.gid = url.split("#")[-1].split("=")[1]
        else:
            self.key = self.url
            self.gid = None
        return

    def info(self) -> None:
        ic(self.confd)
        ic(self.saved)
        ic(self.url)
        ic(self.key)
        ic(self.gid)
        ic(self.fmt)
        ic(self.desc)
        ic(self.fname)
        ic(self.savef)
        ic(self.export_url())
        return

    def load(self, sheet: Dict[str, Any]) -> None:
        self.url = sheet.get("url")
        self.desc = sheet.get("desc")
        self.gid = sheet.get("gid")
        self.fmt = sheet.get("format")
        self.fname = sheet.get("stem")
        self.datefmt = sheet.get("datefmt")
        return

    def export_url(self):
        if self.key is None:
            self.set_key_gid_from_url()
            msg = f"Got key from URL : {self.url}"
            ic(msg)

        self.check_fmt()
        fmt = self.fmt
        key = self.key
        gid = self.gid
        path = f"https://docs.google.com/spreadsheets/d/{key}/export"
        query = f"format={fmt}"
        if not str(gid) == "None":
            query += f"&gid={gid}"
        url = f"{path}?{query}"
        return url

    def check_fmt(self):
        fmt = self.fmt
        ok = ["xlsx", "ods", "csv", "tsv"]
        if fmt not in ok:
            msg = f"{fmt} is a wrong format. Select from {ok}. ... Exit."
            ic(msg)
            sys.exit()

    def download(self) -> str:
        url = self.export_url()
        savef = str(self.savef)
        cmd = ["wget", "--quiet", "-O", savef, url]
        cmd = [str(c) for c in cmd if c]
        subprocess.run(cmd)
        print(f"🚀 {savef}")
        return savef

    def backup(self) -> str:
        datefmt = self.datefmt
        now = pendulum.now().strftime(datefmt)

        fmt = f".{self.fmt}"
        fname = Path(f"{now}_{self.fname}")
        movef = Path(self.saved) / fname.with_suffix(fmt)

        savef = str(self.savef)
        movef = str(movef)
        shutil.move(savef, movef)
        print(f"🚚 {movef}")
        return movef

    def snapshot(self):
        print(f"📝 {self.desc}")
        self.download()
        movef = self.backup()
        return movef


@dataclass
class Book(Sheet):
    def __post_init__(self) -> None:
        self.check_fmt()
        if self.url is not None:
            self.set_key_gid_from_url()
        else:
            msg = f"URL : {self.url} / key : {self.key}"
            ic(msg)
        self.gid = None
        self.set_savef()

    def check_fmt(self):
        fmt = self.fmt
        ok = ["xlsx", "ods"]
        if fmt not in ok:
            msg = f"{fmt} is a wrong format. Select from {ok}. ... Exit."
            ic(msg)
            sys.exit()
