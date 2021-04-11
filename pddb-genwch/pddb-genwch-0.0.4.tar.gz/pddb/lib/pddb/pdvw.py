from abc import ABC, abstractmethod
from .pdtbl import *
import pandas as pd


class pdvw(ABC):
    def __init__(self, owner: str = "system", debug: bool = False):
        self.owner = owner
        self.debug = debug
        obj = self.init_obj()
        self._tbl = self.__set_tbl(obj)
        self._cols = obj.get("cols", [])
        self.load()
        pass

    def __set_tbl(self, obj):
        owner = self.owner
        debug = self.debug
        rtn = []
        for t in obj.get("source", []):
            tbl = t.get("tbl")
            tbl.set_owner(owner)
            tbl.set_debug(debug)
            name = t.get("name", type(tbl).__name__)
            join = t.get("join", [])
            rtn.append({"name": name, "tbl": tbl, "join": join})
        return rtn

    @abstractmethod
    def init_obj(self) -> dict:
        pass

    def __conv_args(self, *args, **kwargs) -> list:
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

    def filter(self, *args, **kwargs):
        data = self.__conv_args(*args, **kwargs)
        if data == []:
            df = self._df()
        else:
            df = self._df(filt=data[0])
        return df, [0]

    def upsert(self, *args, **kwargs):
        import copy
        data = self.__conv_args(*args, **kwargs)
        tbl_bk = copy.deepcopy(self._tbl)
        for d in data:
            try:
                rtn = self.update(d)
            except:
                rtn = False
                pass
            if not(rtn):
                rtn = self.insert(d)
            if not(rtn):
                if self.debug:
                    print(f"upsert fail - {d}")
                self._tbl = tbl_bk
                return False
        return True

    def update(self, *args, **kwargs):
        import copy
        data = self.__conv_args(*args, **kwargs)
        tbl_bk = copy.deepcopy(self._tbl)
        for d in data:
            tbl_dt = {}
            for t in self._tbl:
                jcols = t.get("join", [])
                ndt = copy.deepcopy(d)
                tbl = t.get("tbl")
                tname = t.get("name")
                for j in jcols:
                    val = tbl_dt.get(j, None)
                    if val != None:
                        ndt.update({j: val})
                rtn = tbl.update(ndt)
                filt_col = {c: d.get(c) for c in tbl.cols(attr="key")}
                filt, _ = tbl.filter(filt_col)
                for f in tbl.to_dict(filt):
                    tbl_dt = f
                    break
                if not(rtn):
                    if self.debug:
                        print(f"upd {tname} fail - {d}")
                    self._tbl = tbl_bk
                    return False
        return True

    def insert(self, *args, **kwargs):
        import copy
        data = self.__conv_args(*args, **kwargs)
        tbl_bk = copy.deepcopy(self._tbl)
        for d in data:
            for t in self._tbl:
                tbl = t.get("tbl")
                tname = t.get("name")
                rtn = tbl.insert(d)
                if not(rtn):
                    if self.debug:
                        print(f"ins {tname} fail - {d}")
                    self._tbl = tbl_bk
                    return False
        return True

    def _df(self, filt: dict = {}) -> pd.DataFrame:
        fcols = [k for k, v in filt.items()]
        df = pd.DataFrame()
        for t in self._tbl:
            cols = [c.get("col")
                    for c in self._cols if c.get("tbl") == t.get("name")]
            jcols = t.get("join", [])
            cols += jcols
            nfilt = [c for c in cols if c in fcols]
            if filt != {}:
                tfilt = {k: v for k, v in filt.items() if k in nfilt}
                ndf, _ = t.get("tbl").filter(tfilt)
                ndf = ndf[cols]
            else:
                ndf = t.get("tbl")._df[cols]
            if df.empty:
                df = ndf
            else:
                df = pd.merge(df, ndf, on=jcols, how="left")
        return df

    def __repr__(self) -> dict:
        return self._df().to_dict('records')

    def __str__(self) -> str:
        return self._df().to_string()

    def save(self) -> bool:
        for s in self._tbl:
            tbl = s.get("tbl")
            tname = s.get("name")
            if not(tbl.save()):
                if self.debug:
                    print(f"save {tname} fail")
                return False
        return True

    def load(self) -> bool:
        for s in self._tbl:
            tbl = s.get("tbl")
            tname = s.get("name")
            if not(tbl.load()):
                if self.debug:
                    print(f"load {tname} fail")
                return False
        return True
