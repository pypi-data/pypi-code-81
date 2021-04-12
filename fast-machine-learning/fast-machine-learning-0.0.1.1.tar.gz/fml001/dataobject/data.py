from collections.abc import Iterable
import numpy as np, os, platform
from ..utils import check_is_1D, check_not_2D

class Data(object):

    def __init__(self):
        self.data = None
        self.target_mask = None
        self.feature_mask = None
        self.feature_names = None
        self.target_names = None
        self.sample_indexes = None

    def from_dataframe(self, dataframe, target_indexes=0):
        """
        dataframe: dataframe
        """
        
        self.data = dataframe.values
        self.target_mask = np.zeros([self.data.shape[1]], dtype=bool)
        self.feature_mask = np.ones([self.data.shape[1]], dtype=bool)
        target_indexes = self.check_target_indexes(target_indexes)
        self.target_mask[target_indexes] = ~self.target_mask[target_indexes]
        self.feature_mask[self.target_mask] = ~self.feature_mask[self.target_mask]

        self.sample_indexes = np.array(dataframe.index)
        self.feature_names = dataframe.columns[self.feature_mask]
        self.target_names = dataframe.columns[self.target_mask]
        self.check_names_is_str_or_list()
        return self

    def from_numpy(self, X=None, Y=None, target_indexes=0, feature_names=None, target_names=None, *argv):
        """
        X: 2D ndarray
        Y: 1D or 2D ndarray
        *argv: [X, Y]
        """
        if check_not_2D(X): assert("X must be 2D")
        
        if Y is None and isinstance(X, np.ndarray) and target_indexes is not None:
            self.data = X
            target_indexes = self.check_target_indexes(target_indexes)
        elif X is None and Y is None:
            X, Y = argv[0:3]
            if check_is_1D(Y): Y = Y.reshape(-1, 1)
            if X.shape[0] != Y.shape[0]: assert("X and Y length not equal")
            self.data = np.concatenate([Y, X], axis=1)
            target_indexes = np.array(range(Y.shape[1]))
        elif isinstance(X, np.ndarray) and isinstance(Y, np.ndarray):
            if check_is_1D(Y): Y = Y.reshape(-1, 1)
            if X.shape[0] != Y.shape[0]: assert("X and Y length not equal")
            self.data = np.concatenate([Y, X], axis=1)
            target_indexes = np.array(range(Y.shape[1]))
        else:
            assert("You must pass Y or non-zero target_indexes.")
        
        self.target_mask = np.zeros([self.data.shape[1]], dtype=bool)
        self.feature_mask = np.ones([self.data.shape[1]], dtype=bool)
        
        self.target_mask[target_indexes] = ~self.target_mask[target_indexes]
        self.feature_mask[self.target_mask] = ~self.feature_mask[self.target_mask]
        
        self.sample_indexes = np.array(range(self.data.shape[0]))
        if feature_names is None: 
            self.feature_names = np.array(range(self.data.shape[1]))[self.feature_mask]
        else:
            self.feature_names = feature_names
        if target_names is None:
            self.target_names = np.array(range(self.data.shape[1]))[self.target_mask]
        else:
            self.target_names = target_names
        self.check_names_is_str_or_list()
        return self
    
    @property
    def targets(self):
        return self.data[:, self.target_mask]
    def _target(self, target_index=0):
        return self.targets[:, target_index]
    @property
    def target(self, target_index=0):
        return self.targets[:, target_index]
    @property
    def features(self):
        return self.data[:, self.feature_mask]
    
    @property
    def Ys(self):
        return self.targets
    @property
    def Y(self, target_index=0):
        return self.target
    @property
    def X(self):
        return self.features
    
    def to_csv(self, path):
        with open(path, "w") as f:
            first_line = ["index"] + self.target_names.astype(str).tolist() + self.feature_names.astype(str).tolist()
            f.writelines(f"{','.join(first_line)}\n")
            for index, dataline in zip(self.sample_indexes, self.data):
                f.writelines(f"{','.join([str(index)]+dataline.astype(str).tolist())}\n")
        return None
    
    def to_txt(self, path):
        with open(path, "w") as f:
            first_line = ["index"] + self.target_names.astype(str).tolist() + self.feature_names.astype(str).tolist()
            first_line = '\t'.join(first_line)
            f.writelines(f"{first_line}\n")
            for index, dataline in zip(self.sample_indexes, self.data):
                dataline = '\t'.join([str(index)] + dataline.astype(str).tolist())
                f.writelines(f"{dataline}\n")
        return None
    
    def check_target_indexes(self, target_indexes):
        if isinstance(target_indexes, Iterable):
            target_indexes = np.array(target_indexes).reshape(-1, )
        if isinstance(target_indexes, (int, float, )):
            target_indexes = np.array(int(target_indexes))
        else:
            assert("target_indexes must be int, float or iterable(int or float)")
        return target_indexes
    
    def to_df(self):
        try:
            from pandas import DataFrame
        except:
            assert("to_df needs additional pkg pandas")
        return DataFrame(self.data, columns=self.target_names.tolist()+self.feature_names.tolist(), index=self.sample_indexes)
    
    def check_names_is_str_or_list(self):
        if isinstance(self.target_names, (str, list,)):
            self.target_names = np.array(self.target_names).reshape(-1, )
        if isinstance(self.feature_names, (str, list,)):
            self.feature_names = np.array(self.feature_names).reshape(-1, )


class ReadData:
    
    def __init__(self, filepath, target_indexes=0):
        self.filepath = filepath
        self.read_data(target_indexes)
    
    @property
    def ext(self):
        return os.path.splitext(self.filepath)[-1]
    
    def read_data(self, target_indexes):
        if self.ext in ['.xlsx', '.xls']:
            try:
                from pandas import read_excel
            except:
                assert("to_df needs additional pkg pandas")
            df = read_excel(self.filepath, index_col=0)
            self.data = Data().from_dataframe(df, target_indexes)
        elif self.ext in ['.txt', '.csv']:
            if platform.system() == "Windows":
                system_line_spliter = "\n"
            else:
                system_line_spliter = "\r\n"
            if self.ext == ".txt":
                spliter = "\t"
            else:
                spliter = ","
            with open(self.filepath, "r") as f:
                if f.readable():
                    row_list = []
                    for index, line in enumerate(f.readlines()):
                        row = [cell for cell in line.split(system_line_spliter)[0].split(spliter)]
                        if index == 0:
                            columns = row
                        else:
                            row_list.append(row)
                    row_array = np.array(row_list)
                    self.data = Data().from_numpy(X=row_array[:,1:], target_indexes=target_indexes, feature_names=columns[2:], target_names=columns[1])
                else:
                    raise Exception("Unreadable file: {self.filepath}")
        else:
            raise Exception("need txt or csv")
        return self.data
    
    def __call__(self):
        return self.data
