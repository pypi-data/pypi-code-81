import abc
from typing import Iterable, List, Dict

from dirba.models.abc import BinaryPredict, Predict, CategoryId
from sklearn import metrics

from dirba.validation.utils import multi_categorical_to_single

FeatureClass = str
Probability = float


class AbstractMetric(abc.ABC):

    def __init__(self, features_true: Iterable, features_predicted: Iterable):
        self.features_true = features_true
        self.features_predicted = features_predicted

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplementedError("Override property before use")

    @abc.abstractmethod
    def evaluate(self) -> float:
        """
        Подсчитывает общую метрику для всех классов в совокупности
        :return:
        """
        pass


class AISSearchTextMetric(AbstractMetric, abc.ABC):
    """
    Метрики связанные с текстами в АИС Поиск.

    Работают с мультикатегориальными вероятностными оценками, т.е.
    Принимают на вход оценки моеделей вида [0.5,0,0.2]
    и реальные значения категорий для материала в виде [1,0,0] на каждый материал.

    Текущие категории (с маппингом к категориям в системе)
    'is_legal': -1,
    'is_drug': 25,
    'is_extremism': 14,
    'is_terrorism': 15,
    'is_porn': 19,
    'is_gaming': 23
    """
    features_true: List[List[BinaryPredict]]
    features_predicted: List[List[Predict]]

    def __init__(self, features_true: List[List[BinaryPredict]], features_predicted: List[List[Predict]]):
        super().__init__(features_true, features_predicted)


class AISMetricSingle(AISSearchTextMetric, abc.ABC):
    """
    Для этой оценки значения переводятся из оценок по всем классам в оценку по 1 классу, для этого
    из массива оценок по классам [Predict(category=-1,score=0.7),Predict(category=25,score=0.9)]
    будет взята оценка, имеющая максимальное значение.
    В резульатате массив оценок для каждого матаериала будет приведён к категории, имеющей максимальную оценку
    [[Predict(category=-1,score=0.7),Predict(category=25,score=0.9)],[Predict(category=-1,score=0.6),Predict(category=25,score=0.2)]] ->
    [25,-1]
    """

    features_true: List[CategoryId]
    features_predicted: List[CategoryId]

    def __init__(self, features_true: List[List[BinaryPredict]], features_predicted: List[List[Predict]]):
        super().__init__(features_true, features_predicted)
        true_processed, predicted_processed = multi_categorical_to_single(features_true, features_predicted)
        self.features_true = true_processed
        self.features_predicted = predicted_processed


class PrecisionAISTextMetricMultiCategorical(AISSearchTextMetric):

    def evaluate(self) -> float:
        true_values = [[i.score for i in row] for row in self.features_true]
        predicted_values = [[i.score for i in row] for row in self.features_predicted]
        return metrics.label_ranking_average_precision_score(true_values, predicted_values)

    @property
    def name(self):
        return 'precision_multi_categorical'


class PrecisionAISTextPerClass(AISMetricSingle):

    @property
    def name(self):
        return 'precision_per_class'

    def evaluate(self) -> Dict[CategoryId, float]:
        categories = set(self.features_true)
        precision_per_label = {}
        for category in categories:
            precision = metrics.precision_score(self.features_true, self.features_predicted, labels=[category], average='micro')
            precision_per_label[category] = precision
        return precision_per_label



class RecallAISTextPerClass(AISSearchTextMetric):

    @property
    def name(self):
        return 'recall_per_class'

    def evaluate(self) -> Dict[CategoryId, float]:
        # TODO вынести общие с recall функции
        if len(self.features_true) == 0:
            raise ValueError("Empty true values from dataset")
        categories = set(map(lambda predict: predict.category, self.features_true[0]))
        recall_per_label = {}

        for category in categories:
            true_values_per_category = []
            predicted_values_per_category = []

            for index in range(len(self.features_true)):
                true_per_category = list(filter(lambda predict: predict.category == category, self.features_true[index]))[0]
                predicted_per_category = list(filter(lambda predict: predict.category == category, self.features_predicted[index]))[0]
                true_values_per_category.append(true_per_category.category)
                predicted_values_per_category.append(predicted_per_category.category if predicted_per_category.score >= 0.7 else -322)

            precision = metrics.recall_score(true_values_per_category, predicted_values_per_category, average='micro')
            recall_per_label[category] = precision
        return recall_per_label


class PrecisionAISTextMetricSingle(AISMetricSingle):
    """
    Precision оценка по попаданию в 1 категорию.
    """

    def evaluate(self) -> float:
        return metrics.precision_score(self.features_true, self.features_predicted, average='micro')

    @property
    def name(self):
        return 'precision_single'


class RecallAISTextMetricSingle(AISMetricSingle):
    """
    Recall оценка по попаданию в 1 категорию.
    """

    def evaluate(self) -> float:
        return metrics.recall_score(self.features_true, self.features_predicted, average='micro')

    @property
    def name(self):
        return 'recall_single'
