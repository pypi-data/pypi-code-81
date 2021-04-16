import abc
from typing import Iterable, Optional, Mapping, NamedTuple, Iterator, List, Dict, Union
import io

import pandas as pd
import requests

from dirba.models.abc import BinaryPredict, CategoryId, CategoryName


class Row(NamedTuple):
    x: Mapping
    y: List[BinaryPredict]


class AbstractDataset(abc.ABC):
    def __init__(self, dataset_path: str, feature_cols: Dict[CategoryName, CategoryId],
                 labels: Optional[Iterable[str]] = None):
        self.labels = labels
        if feature_cols is None:
            raise ValueError("Feature columns should be specified")
        self.feature_cols = feature_cols
        self.dataset_path = dataset_path
        self._dataset: pd.DataFrame = self.load(dataset_path)

    @staticmethod
    @abc.abstractmethod
    def load(dataset_path: str, labels: Optional[Iterable[str]] = None) -> pd.DataFrame:
        pass

    @abc.abstractmethod
    def features(self) -> Iterable[Row]:
        pass

    def size(self) -> int:
        return len(self._dataset)


class CSVDataset(AbstractDataset):
    def features(self) -> Iterator[Row]:
        for index, values in self._dataset.iterrows():
            yield Row(x=values.drop(columns=self.feature_cols),
                      y=[BinaryPredict(category=class_id, score=values[col])
                         for col, class_id in self.feature_cols.items()])

    @staticmethod
    def load(dataset_path: str, labels: Optional[Iterable[str]] = None):
        header = 'infer' if not labels else [i for i in labels]
        return pd.read_csv(dataset_path, header=header)


class ProhibitedTexValidationDataset(CSVDataset):
    """
    Валидационный датасет с запрещёнными материалами
    """
    url = 'https://cloud.uriit.ru/index.php/s/NtoSfKaQaDOFeE7/download'

    def __init__(self):
        feature_cols = {'is_legal': -1,
                        'is_drug': 25,
                        'is_extremism': 14,
                        'is_terrorism': 15,
                        'is_porn': 19,
                        'is_gaming': 23}
        super().__init__(self.url, feature_cols)

    def load(self, dataset_path: str, labels: Optional[Iterable[str]] = None):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise ConnectionError("Unable to download dataset")

        buffer = io.BytesIO(response.content)
        header = 'infer' if not labels else [i for i in labels]
        return pd.read_csv(buffer, header=header)


if __name__ == '__main__':
    dataset = ProhibitedTexValidationDataset()
    for i in dataset.features():
        print(i.y)
        break
