from abc import ABC, abstractclassmethod, abstractmethod
import pandas as pd
from pandas import DataFrame
import pickle
import os

from pydantic.main import BaseModel
from typing import Optional, Dict, List
from enum import Enum

from grilled.common.note import Result
from grilled.common.logger import LoggingLogger


logger = LoggingLogger()

class Filepaths(BaseModel):
    csv: Optional[Dict[str, str]]
    excel: Optional[Dict[str, str]]
    pickle: Optional[Dict[str, str]]


class Directories(BaseModel):
    input: str
    persistent: str
    output: str
    note: str

class File(BaseModel):
    variable_name: str
    file_name: str

class FileType(Enum):
    csv = "csv"
    excel = "excel"
    pickle = "pickle"


class Files(BaseModel):
    input: Optional[Dict[FileType, List[File]]]
    persistent: Optional[Dict[FileType, List[File]]]
    result: Optional[Dict[FileType, List[File]]]


class BaseAlgorithm(ABC):
    __nickname__: str = "not defined"

    def __init__(
        self, 
        hyperparameter: dict = {},
        process_params: dict = {}, 
        input_filepaths: Filepaths = Filepaths(),
        persistent_filepaths: Filepaths = Filepaths(),
        result_filepaths: Filepaths = Filepaths() 
    ) -> None: 
        super().__init__()
        self.process_params = process_params
        self.hyperparameter = hyperparameter
        self.process_params = process_params
        self.input_filepaths = input_filepaths
        self.persistent_filepaths = persistent_filepaths
        self.result_filepaths = result_filepaths

    def __load_input_file(self) -> None:
        if self.input_filepaths is None:
            return
        for file_type, value in self.input_filepaths.dict().items():
            if value == None:
                continue
            # 加载 csv 文件
            elif file_type == "csv":
                for variable_name, filepath in value.items():
                    setattr(self, variable_name, pd.read_csv(filepath, encoding="GB2312"))
            # 加载 excel 文件
            elif file_type == "excel":
                for variable_name, filepath in value.items():
                    setattr(self, variable_name, pd.read_excel(filepath))
            # 加载 pickle 文件
            elif file_type == "pickle":
                for variable_name, filepath in value.items():
                    with open(filepath, "rb") as fr:
                        setattr(self, variable_name, pickle.load(fr))

    def __load_persistent_file(self) -> None:
        if self.persistent_filepaths is None:
            return
        for file_type, value in self.persistent_filepaths.dict().items():
            if value == None:
                continue
            # 加载 csv 文件
            elif file_type == "csv":
                for variable_name, filepath in value.items():
                    setattr(self, variable_name, pd.read_csv(filepath, encoding="GB2312"))
            # 加载 excel 文件
            elif file_type == "excel":
                for variable_name, filepath in value.items():
                    setattr(self, variable_name, pd.read_excel(filepath))
            # 加载 pickle 文件
            elif file_type == "pickle":
                for variable_name, filepath in value.items():
                    if not os.path.exists(filepath):
                        return setattr(self, variable_name, None)
                    with open(filepath, "rb") as fr:
                        setattr(self, variable_name, pickle.load(fr))

    def load(self) -> None:
        self.__load_input_file()
        self.__load_persistent_file()
        logger.info(f"[{self.__nickname__}] load finished.")

    def __output_result_file(self) -> None:
        if self.result_filepaths is None:
            return
        for file_type, value in self.result_filepaths.dict().items():
            if value == None:
                continue
            # 导出 csv 文件
            elif file_type == "csv":
                for variable_name, filepath in value.items():
                    data:DataFrame = getattr(self, variable_name)
                    data.to_csv()
            # 导出 excel 文件
            elif file_type == "excel":
                for variable_name, filepath in value.items():
                    data:DataFrame = getattr(self, variable_name)
                    data.to_excel()
            # 导出 pickle 文件
            elif file_type == "pickle":
                for variable_name, filepath in value.items():
                    data:dict = getattr(self, variable_name)
                    with open(filepath, "wb") as fw:
                        pickle.dump(data, fw)

    def __output_persistent_file(self) -> None:
        if self.persistent_filepaths is None:
            return
        for file_type, value in self.persistent_filepaths.dict().items():
            if value == None:
                continue
            # 导出 csv 文件
            elif file_type == "csv":
                for variable_name, filepath in value.items():
                    data:DataFrame = getattr(self, variable_name)
                    data.to_csv()
            # 导出 excel 文件
            elif file_type == "excel":
                for variable_name, filepath in value.items():
                    data:DataFrame = getattr(self, variable_name)
                    data.to_excel()
            # 导出 pickle 文件
            elif file_type == "pickle":
                for variable_name, filepath in value.items():
                    data:dict = getattr(self, variable_name)
                    with open(filepath, "wb") as fw:
                        pickle.dump(data, fw)

    def output(self) -> None:
        self.__output_result_file()
        self.__output_persistent_file()
        logger.info(f"[{self.__nickname__}] output finished.")

    @abstractmethod
    def preprocessing(self) -> None:
        logger.info(f"[{self.__nickname__}] preprocessing finished.")

    @abstractmethod
    def algorithm(self) -> Result:
        logger.info(f"[{self.__nickname__}] algorithm finished.")

    def run(self) -> None:
        self.load()
        self.preprocessing()
        self.algorithm()
        self.output()


class AlgorithmDevelopmentManager:
    __nickname__ = "👮‍ Algorithm Manager"

    root_path = os.getcwd()
    directories = Directories(
        input=os.getenv("INPUT_PATH"),
        persistent=os.getenv("PERSISTENT_PATH"),
        output=os.getenv("RESULT_PATH"),
        note=os.getenv("NOTE_PATH")
    )
    
    files: Optional[Files] = None

    input_filepaths: Optional[Filepaths] = None
    result_filepaths: Optional[Filepaths] = None
    persistent_filepaths: Optional[Filepaths] = None

    @classmethod
    def __generate_filepaths(cls, dictionary_type, files):
        filepaths = {"csv": {}, "excel": {}, "pickle": {}}
        for file_type, file_match in files.items():
            if file_type == FileType.csv:
                for file in file_match:
                    filepath = os.path.join(cls.root_path, getattr(cls.directories, dictionary_type), file.file_name)
                    filepaths["csv"].update({file.variable_name: filepath})
            elif file_type == FileType.excel:
                for file in file_match:
                    filepath = os.path.join(cls.root_path, getattr(cls.directories, dictionary_type), file.file_name)
                    filepaths["excel"].update({file.variable_name: filepath})
            elif file_type == FileType.pickle:
                for file in file_match:
                    filepath = os.path.join(cls.root_path, getattr(cls.directories, dictionary_type), file.file_name)
                    filepaths["pickle"].update({file.variable_name: filepath})
        return filepaths

    @classmethod
    def __generate_input_filepaths(cls):
        for dictionary_type, files in cls.files:
            if files == None:
                continue
            if dictionary_type == "input":
                input_filepaths = cls.__generate_filepaths(dictionary_type=dictionary_type, files=files)
                cls.input_filepaths = Filepaths(**input_filepaths)
                break

    @classmethod
    def __generate_result_filepaths(cls):
        for dictionary_type, files in cls.files:
            if files == None:
                continue
            if dictionary_type == "output":
                result_filepaths = cls.__generate_filepaths(dictionary_type=dictionary_type, files=files)
                cls.result_filepaths = Filepaths(**result_filepaths)
                break
    
    @classmethod
    def __generate_persistent_filepaths(cls):
        for dictionary_type, files in cls.files:
            if files == None:
                continue
            if dictionary_type == "persistent":
                persistent_filepaths = cls.__generate_filepaths(dictionary_type=dictionary_type, files=files)
                cls.persistent_filepaths = Filepaths(**persistent_filepaths)
                break

    @classmethod
    def initialize(cls):
        if cls.files != None:
            cls.__generate_input_filepaths()
            cls.__generate_result_filepaths()
            cls.__generate_persistent_filepaths()
        logger.info(f"[{cls.__nickname__}] initialize finished.")

    @abstractclassmethod
    def run_algorithm(cls):
        """
        👇👇👇 YOU SHOULD write algorithm like this 👇👇👇 
        class Algorithm(BaseAlgorithm):
            def preprocessing(self) -> None:
                return super().preprocessing()
            
            def algorithm(self) -> dict:
                return super().algorithm()

        algorithm = Algorithm()
        algorithm.run()
        """
        logger.info(f"[{cls.__nickname__}] algorithm finished.")
    
    @classmethod
    def run(cls):
        cls.initialize()
        cls.run_algorithm()
    