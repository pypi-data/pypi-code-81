import asyncio
from rich.progress import (
    Progress, 
    BarColumn, 
    TimeRemainingColumn, 
    TimeElapsedColumn, 
    TaskID
)
import numpy as np
from typing import List
import json
import errno
import logging


class Reader:
    def __init__(self, filename: str):
        self.filename  = filename

    def read(self, progress: Progress, task_id: TaskID) -> List[np.array]:
        result_list = []
        stream = open(self.filename, mode="r")
        matrix = []
        start  = False
        progress.start_task(task_id)
        while (line := stream.readline()):
            if "START" in line:
                start = True
            elif "END" in line:
                start = False
                if len(matrix) == 1:
                    matrix = matrix[0]
                result_list.append(np.array(matrix))
                matrix = []
                progress.update(task_id, advance=1)
            
            if start and not "START" in line:
                row = [float(x) for x in line.split()]
                if row:
                    matrix.append(row)

        return result_list
    
    @staticmethod
    def read_files(files: List[str], json_info:str) -> List[np.array]:
        tasks = []
        args = [
            "[progress.description]{task.description}",
            BarColumn(), 
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            TimeElapsedColumn()
        ]
        result = []
        with Progress(*args) as progress, open(json_info, mode="r") as stream:
            json_dict = json.load(stream)
            
            for f in files:

                # Take the number of matrices for filename
                key = f.split("/")[-1].split(".")[0]

                # The key must be inside the info_file
                if not key in json_dict:
                    raise KeyError((key,))

                mnumb = json_dict[key]
                task_id = progress.add_task("[yellow]Getting matrix from {} ...".format(f.split("/")[-1]), total=mnumb)
                reader = Reader(f)
                result_matrix = reader.read(progress, task_id)
                result += result_matrix
        
        return result