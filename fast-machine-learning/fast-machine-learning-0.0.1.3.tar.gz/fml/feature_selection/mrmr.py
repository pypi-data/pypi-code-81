
from pathlib import Path
import numpy as np, sys, pandas as pd
from subprocess import Popen, PIPE
self_file_dir_path = Path(__file__).parent.resolve()
self_tmp_dir_path = Path(self_file_dir_path, "tmp")
self_exec_dir_papth = Path(self_file_dir_path, "exec")
self_tmp_path = Path(self_tmp_dir_path, "tmp.csv")
import platform
if platform.system() == "Windows":
    self_exec_path = Path(self_exec_dir_papth, "mrmr.exe")
else:
    self_exec_path = Path(self_exec_dir_papth, "mrmr")

class MRMR(object):
    """
    MRMR class
    """
    def __init__(self, method="penglab"):
        self.method = method
        self.feature_mrmr = None
        self.feature_index = None
        self.feature_importance = None

    def fit(self, X, Y):
        if self.method == "penglab":
            self.feature_mrmr = self.penglab(X, Y)
        return self
    
    def penglab(self, X, Y):
        dataset = np.concatenate([Y.reshape(-1, 1), X], axis=1)
        dataset = pd.DataFrame(dataset)
        dataset.to_csv(self_tmp_path, index=None)
        cmd = f"{str(self_exec_path)} -i {str(self_tmp_path)} -t 1"
        out = Popen(cmd, stdout=PIPE)
        load_f = False
        feature_mrmr = []
        out = out.stdout.readlines()
        for o in out:
            t = o.decode()
            if t == "\r\n" and load_f:
                load_f = False
            if load_f:
                t = t.split("\r\n")[0].split(" ")
                feature_mrmr.append([t[2], t[6]])
            if t == "*** mRMR features *** \r\n":
                load_f = True
        feature_mrmr.pop(0)
        feature_mrmr = np.array(feature_mrmr, dtype=float)
        feature_mrmr[:, 0] -= 1
        self_tmp_path.unlink()
        return feature_mrmr

