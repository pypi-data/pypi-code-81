import argparse
import random 
import numpy as np 
from dataclasses import asdict
from rich.progress import (
    Progress,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TaskID
)
import os
import os.path as osp
from typing import Union, List, Dict, Tuple, Any
from copy import deepcopy
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor

from ..config.config import Configuration


class MatrixType:
    SQUARED        = 0
    SUP_TRIANGULAR = 1
    INF_TRIANGULAR = 2
    DIAGONAL       = 3
    IDENTITY       = 4
    NULL           = 5
    COLUMN         = 6
    VECTOR         = 7
    RECTANGULAR    = 8
    A_DIAGONAL     = 9


class MatrixGen:
    def __init__(self, **kargs):
        self.ncols: np.int64 = kargs['ncols']
        self.nrows: np.int64 = kargs['nrows']
        self.mtype: np.int64 = kargs['mtype']
        self.mnumb: np.int64 = kargs['mnumb']

        self.current_matrix  = 0

    def __str__(self) -> str:
        return f"MatrixGen.{self.mnumb}(" + ", ".join([f"{k}: {v}" for k, v in self.__dict__.items()]) + ")"

    def __iter__(self): 
        return self

    def __next__(self) -> np.array:
        if self.current_matrix < self.mnumb:
            self.current_matrix += 1
            return self.create_matrix()
            
        raise StopIteration(f"Created {self.mnumb} matrix ...")

    def __len__(self) -> np.int64:
        return self.mnumb

    def get_random(self) -> np.float64:
        return random.random() * random.randint(1, 100)

    def create_matrix(self) -> np.array:
        # If I want to get a squared matrix 
        if self.ncols == self.nrows and self.mtype == MatrixType.SQUARED: return self.create_squared()

        # Otherwise
        return_mx = {
            MatrixType.SUP_TRIANGULAR: self.create_sup_triangular,
            MatrixType.INF_TRIANGULAR: self.create_inf_triangular,
            MatrixType.DIAGONAL      : self.create_diagonal,
            MatrixType.IDENTITY      : self.create_identity,
            MatrixType.NULL          : self.create_null,
            MatrixType.COLUMN        : self.create_column,
            MatrixType.VECTOR        : self.create_row,
            MatrixType.RECTANGULAR   : self.create_rect,
            MatrixType.A_DIAGONAL    : self.create_adiagonal
        }
        return return_mx[self.mtype]()

    def create_simple(self) -> np.array:
        return np.array(
            [self.get_random() for _ in range(self.ncols * self.nrows)]
        ).reshape(self.nrows, self.ncols)

    def create_squared(self) -> np.array:
        return self.create_simple()

    def create_sup_triangular(self) -> np.array:
        assert self.ncols == self.nrows, "A triangular matrix must have #rows == #columns (is a squared one!!!)"
        return np.array(
            [self.get_random() if j >= i else 0.0 for i in range(self.nrows) for j in range(self.ncols)]
        ).reshape(self.nrows, self.ncols)

    def create_inf_triangular(self) -> np.array:
        assert self.ncols == self.nrows, "A triangular matrix must have #rows == #columns (is a squared one!!!)"
        return np.array(
            [self.get_random() if j <= i else 0.0 for i in range(self.nrows) for j in range(self.ncols)]
        ).reshape(self.nrows, self.ncols)

    def create_diagonal(self) -> np.array:
        assert self.ncols == self.nrows, "A diagonal matrix must have #rows == #columns (is a squared one!!!)"
        return np.diag([self.get_random() for _ in range(self.ncols)])

    def create_identity(self) -> np.array:
        assert self.ncols == self.nrows, "The identity matrix must have #rows == #columns (is a squared one!!!)"
        return np.identity(self.ncols)

    def create_null(self) -> np.array:
        return np.zeros((self.nrows, self.ncols))

    def create_column(self) -> np.array:
        # Return a matrix with one column
        return np.array([self.get_random() for _ in range(self.nrows)]).reshape(-1, 1)

    def create_row(self) -> np.array:
        return np.array([self.get_random() for _ in range(self.ncols)])

    def create_rect(self) -> np.array:
        assert self.ncols != self.nrows, "Number of rows == #columns, use -t=0 to get a squared matrix"
        return self.create_simple()

    def create_adiagonal(self) -> np.array:
        assert self.ncols == self.nrows, "A diagonal matrix must have #rows == #columns (is a squared one!!!)"
        return np.fliplr(self.create_diagonal())

    @staticmethod
    def get_matrices(configuration: Dict[Any, Any], info_file: Union[str, None], progress: Progress, task_id: TaskID) -> Union[None, List[np.array]]:
        # Trasform Configuration object into a dict
        asdict_conf = configuration
        mgen        = MatrixGen(**asdict_conf)
        miter       = iter(mgen)

        # Iter and get all the matrices
        matrix_list = []
        matrix_stri = ""
        progress.start_task(task_id)
        for matrix in miter:
            matrix_list.append(matrix) # However fill the list
            printable, max_len = MatrixGen.printable_matrix(matrix)
            matrix_stri += "START\n" + printable + "END" + ("\n" + "-"*max_len + "\n") # Create also the string
            progress.update(task_id, advance=1)
        
        if asdict_conf['savem']:
            mode = "x" if not osp.isfile(asdict_conf['nfile']) else "w"
            with open(asdict_conf['nfile'], mode=mode) as stream:
                stream.write(matrix_stri)

            # Save new matrix number into the info json file
            with open(info_file, mode="r") as json_info:
                info_dict = json.load(json_info)
                filename  = asdict_conf['nfile'].split("/")[-1].split(".")[0]
                info_dict[filename] = asdict_conf['mnumb']

            with open(info_file, mode="w") as stream:
                json.dump(info_dict, stream)
            
            return 
        
        return matrix_list

    @staticmethod
    def save_matrices_from_configurations(configurations: Dict[str, List[Configuration]], info_file:str) -> Tuple[
        Dict[str, List[Configuration]],
        List[str]
    ]:
        confi_dict_cp = deepcopy(configurations)
        files         = []
        progress      = Progress(
            "[progress.description]{task.description}",
            BarColumn(), 
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            TimeElapsedColumn()
        )

        with progress, ThreadPoolExecutor() as pool:
            for k_conf, config in configurations.items():

                for c in config:
                    if c.savem:
                        confi_dict_cp[k_conf].remove(c)
                        c_dict  = asdict(c)
                        task_id = progress.add_task(f"[yellow]Creating matrices for {c_dict['name']} ...", total=c_dict['mnumb'])
                        pool.submit(MatrixGen.get_matrices, c_dict, info_file, progress, task_id)
                        files.append(c.nfile)

                if not confi_dict_cp[k_conf]:
                    confi_dict_cp.pop(k_conf)

        return confi_dict_cp, files

    @staticmethod
    def get_matrix_from_configuration(configurations: Dict[str, List[Configuration]]) -> List[np.array]:
        results = []
        args = [
            "[progress.description]{task.description}",
            BarColumn(), 
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            TimeElapsedColumn()
        ]

        with Progress(*args) as progress:
            for _, v in configurations.items():
                for config in v:
                    config_dict = asdict(config)
                    task_id     = progress.add_task(f"[yellow]Creating matrices for {config_dict['name']} ...", total=config_dict['mnumb'])
                    matrices    = MatrixGen.get_matrices(config_dict, None, progress, task_id)
                    results    += matrices

        return results

    @staticmethod
    def printable_matrix(M: np.array) -> None:
        tot_str = ""
        # If M is a vector matrix
        if len(M.shape) == 1:
            tot_str = " ".join([f"{x}" for x in M]) + "\n"
            return tot_str, len(tot_str) - 1
        
        # Otherwise
        max_len = 0
        for i in range(M.shape[0]):
            parz = ""
            for j in range(M.shape[1]):
                parz += "%.6f " % (M[i][j])
            tot_str += parz + "\n"
            if (new_len := len(parz)) > max_len:
                max_len = new_len
        
        return tot_str, max_len
