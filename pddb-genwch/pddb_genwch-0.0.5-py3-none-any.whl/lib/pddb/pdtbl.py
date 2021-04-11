from abc import ABC, abstractmethod
import pandas as pd
from .columns import Column
from enum import Enum


class ACL(Enum):
    PUBLIC = 0
    SHARED = 1
    PRIVATE = 2


class pdtbl(ABC):
    def __init__(self, owner: str = "system", debug: bool = False):
        self.set_debug(debug)
        (obj, path, acl) = self.init_obj()
        obj = self.__set_sys_obj(obj)
        self._obj = self.__obj2col(obj)
        self._model = self.__obj2mod(self._obj)
        self._df = self.init_df(cols=[o.name for o in self._obj])
        self.__upddtm()
        self.set_owner(owner)
        self._path = path
        self._acl = acl
        self.load()
        pass

    def __obj2mod(self, obj: dict):
        from pydantic import create_model
        from typing import Optional
        fields = {}
        for o in obj:
            name = o.get("name")
            type = o.get("type", str)
            if o.get("optional", False):
                type = Optional[type]
                default = None
                if self.debug:
                    print(name, "optional", type)
            else:
                default = ...
            fields[name] = (type, default)
        model = create_model(self.__class__.__name__, **fields)
        return model
        # pass

    def set_owner(self, owner: str):
        self.owner = owner

    def set_debug(self, debug: bool):
        self.debug = debug

    def __set_sys_obj(self, obj: dict) -> dict:
        from datetime import datetime
        obj.update({"cre_dtm": {"type": datetime, "curdtm": True, "ignupd": True},
                    "cre_by": {"type": str, "owner": True, "ignupd": True},
                    "upd_dtm": {"type": datetime, "curdtm": True},
                    "upd_by": {"type": str, "owner": True}})
        return obj

    def cols(self, attr: str = None) -> list:
        if attr == None:
            return [o.name for o in self._obj]
        return [o.name for o in self._obj if o.get(attr, False)]

    def __upddtm(self) -> bool:
        from datetime import datetime
        self.datetime = datetime.now()
        return True

    def __obj2col(self, obj: dict) -> list:
        cnt = 0
        rtn = []
        for k, v in obj.items():
            if isinstance(v, type):
                v = {"type": v}
            v.update({"name": k, "iloc": cnt})
            rtn.append(self.__set_col(v))
            cnt += 1
        return rtn

    def __set_col(self, *args, **kwargs) -> Column:
        return Column(*args, **kwargs)

    @abstractmethod
    def init_obj(self) -> dict:
        pass

    def init_df(self, cols: list = []) -> pd.DataFrame:
        cols = self.cols() if cols == [] else cols
        return pd.DataFrame(columns=cols)

    def __conv_args(self, *args, **kwargs) -> dict:
        rtn = []
        for a in args:
            rtn = [a] if isinstance(a, dict) else a
            break
        if rtn == []:
            rtn = [kwargs]
        if kwargs != {}:
            nrtn = []
            for r in rtn:
                r.update(kwargs)
                nrtn.append(r)
            rtn = nrtn
        return rtn

    def check_require(self, data: dict) -> bool:
        for r in self.cols(attr="require"):
            if data.get(r, None) == None:
                return False
        return True

    def __set_uuid(self, data: dict) -> dict:
        import uuid
        for g in self.cols(attr="uuid"):
            if data.get(g, None) == None or data.get(g, None) == "":
                data.update({g: str(uuid.uuid4())})
        return data

    def __set_md5(self, data: dict) -> dict:
        import hashlib
        for g in self.cols(attr="md5"):
            val = data.get(g, None)
            if val != None:
                data.update({g: hashlib.md5(val.encode()).hexdigest()})
        return data

    def __set_genrun(self, data: dict) -> dict:
        for g in self.cols(attr="genrun"):
            if data.get(g, None) == None or data.get(g, None) == "":
                obj = [o for o in self._obj if o.get("name") == g][0]
                nmask = obj.get("genrun_pattern").split("!!")
                genpat = nmask[1].split("-")
                if genpat[0] == "cnt":
                    cnt = len(self._df)+1
                    runnum = str(cnt).zfill(int(genpat[1]))
                    val = "{}{}{}".format(nmask[0], runnum, nmask[2])
                else:
                    val = None
                data.update({g: val})
        return data

    def __set_now(self, data: dict) -> dict:
        for g in self.cols(attr="curdtm"):
            val = data.get(g, None)
            if val == None:
                data.update({g: self.datetime})
        return data

    def __set_owner(self, data: dict) -> dict:
        for g in self.cols(attr="owner"):
            val = data.get(g, None)
            if val == None:
                data.update({g: self.owner})
        return data

    def count(self) -> int:
        return len(self._df)

    def __prepare_data(self, *args, **kwargs) -> list:
        data = self.__conv_args(*args, **kwargs)
        rtn = []
        for d in data:
            if d.get("__gen_uuid", True):
                d = self.__set_uuid(data=d)
            if d.get("__mask_md5", True):
                d = self.__set_md5(data=d)
            if d.get("__genrun", True):
                d = self.__set_genrun(data=d)
            if d.get("__cur_dtm", True):
                d = self.__set_now(data=d)
                d = self.__set_owner(data=d)
            for o in self._obj:
                d[o.get("name")] = d.get(o.get("name"), o.get("default", None))
            newd = {k: v for k, v in d.items() if k in self.cols()}
            rtn.append(newd)
        return rtn

    def filter(self, filtcond: dict, filtowner=False) -> (list, int):
        df = self._df
        filt = filtcond.copy()
        if filtowner:
            filt.update({"upd_by": self.owner})
        filtcol = [k for k, v in filt.items()]
        for d in self.__prepare_data(filt):
            data = d
            break
        filt = {k: v for k, v in data.items() if k in filtcol}
        if self.debug:
            print(f"filter - {self.to_dict(df)}, {filt}")
        for k, v in filt.items():
            df = df[df[k] == v]
        if df.empty:
            return (pd.DataFrame(), [])
        return (df, df.index.to_list())

    def select(self, filtcond: dict) -> (list):
        filtowner = self.check_acl(issel=True)
        df, _ = self.filter(filtcond=filtcond, filtowner=filtowner)
        return df

    def upsert(self, *args, **kwargs) -> (bool, list):
        if kwargs.get("__upddtm", True):
            self.__upddtm()
        kwargs.update({"__upddtm": False})
        data = self.__prepare_data(*args, **kwargs)
        df = self._df
        for d in data:
            key = {k: v for k, v in d.items() if k in self.cols(attr="key")}
            filt, idx = self.filter(key)
            if idx == []:
                if self.debug:
                    print(f"upsert(ins) - {d}")
                df = df.append(d, ignore_index=True)
            else:
                if self.debug:
                    print(f"upsert(upd) - {d}")
                filtowner = self.check_acl(isupd=True)
                filt, idx = self.filter(key, filtowner=filtowner)
                if idx == []:
                    return False, None
                else:
                    for k, v in d.items():
                        if k not in self.cols(attr="key") and k not in self.cols(attr="uuid") and k not in self.cols(attr="ignupd"):
                            upd = pd.Series({i: v for i in idx})
                            df[k].update(upd)
        self._df = df
        return True, data

    def check_acl(self, isupd=False, issel=False) -> bool:
        filtowner = True if self.owner != "system" else False
        if self._acl == ACL.PUBLIC:
            filtowner = False
        if not(isupd):
            if self._acl == ACL.SHARED:
                filtowner = False
        if not(issel):
            if self._acl == ACL.PRIVATE:
                filtowner = False
        return filtowner

    def update(self, *args, **kwargs) -> (bool, list):
        if kwargs.get("__upddtm", True):
            self.__upddtm()
        data = self.__prepare_data(*args, **kwargs)
        df = self._df
        for d in data:
            key = {k: v for k, v in d.items() if k in self.cols(attr="key")}
            filtowner = self.check_acl(isupd=True)
            filt, idx = self.filter(key, filtowner=filtowner)
            if idx != []:
                if self.debug:
                    print(f"update - {d}")
                for k, v in d.items():
                    if k not in self.cols(attr="key") and k not in self.cols(attr="uuid") and k not in self.cols(attr="ignupd"):
                        upd = pd.Series({i: v for i in idx})
                        df[k].update(upd)
            else:
                return False, None
        self._df = df
        return True, data

    def insert(self, *args, **kwargs) -> (bool, list):
        if kwargs.get("__upddtm", True):
            self.__upddtm()
        data = self.__prepare_data(*args, **kwargs)
        df = self._df
        for d in data:
            key = {k: v for k, v in d.items() if k in self.cols(attr="key")}
            filt, idx = self.filter(key)
            if idx == []:
                if self.debug:
                    print(f"insert - {d}")
                df = df.append(d, ignore_index=True)
            else:
                return False, None
        self._df = df
        return True, data

    def __repr__(self) -> dict:
        return self._df.to_dict("records")

    def to_dict(self, df: pd.DataFrame = pd.DataFrame()) -> dict:
        df = self._df if df.empty else df
        return df.to_dict("records")

    def __str__(self) -> str:
        return self._df.to_string()

    def save(self, path: str = None) -> bool:
        path = self._path if path == None else path
        try:
            self._df.to_parquet(path=path, compression='gzip')
        except:
            return False
        return True

    def load(self, path: str = None) -> bool:
        path = self._path if path == None else path
        try:
            self._df = pd.read_parquet(path=path)
        except:
            return False
        return True
