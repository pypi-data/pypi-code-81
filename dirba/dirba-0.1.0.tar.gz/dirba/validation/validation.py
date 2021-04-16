import logging
from typing import Iterable, Type, Dict, List, Tuple, Union, Any, Set
import warnings

import pydantic

from dirba.models.abc import AbstractModel, BinaryPredict, Predict, CategoryId
from dirba.validation.dataset import AbstractDataset
from dirba.validation.metrics import AbstractMetric, AISSearchTextMetric

Name = str
Metric = Union[float, Dict[Any, float]]


class ValidationResult(pydantic.BaseModel):
    size: int
    metrics_scores: Dict[Name, Metric]


class Validator:
    """
    Класс для валидации работы моделей
    """
    logger = logging.getLogger('validator')

    def __init__(self, dataset: AbstractDataset, model: AbstractModel, metrics_classes: Iterable[Type[AISSearchTextMetric]]):
        self.metrics_classes = metrics_classes
        self.model = model
        self.dataset = dataset

    def _fix_missing_categories(self, row: List[Predict], categories: Set[CategoryId], is_binary=False) -> List[Union[Predict, BinaryPredict]]:
        """
        Исправляет кол-во оценок по категориям в списке ответов от модели или списке из реальных ответов набора данных.
        """
        pure_row = list(filter(lambda predict: predict.category in categories, row))
        if len(pure_row) != len(categories):
            self.logger.debug(f'Found predict and true values mismatch in row {row}')
            missing_categories = categories.symmetric_difference(set(predict.category for predict in pure_row))
            for category in missing_categories:
                pure_row.append(Predict(category=category, score=0) if not is_binary else BinaryPredict(category=category, score=0))
        return pure_row

    def _append_missing(self, true_values: List[List[BinaryPredict]], predicted_values: List[List[Predict]]) -> \
            Tuple[List[List[BinaryPredict]], List[List[Predict]]]:
        """
        Выправляет данные, устанавливая одинаковое кол-во категорий в реальных и предстказанных значениях.
        """
        if len(true_values) != len(predicted_values):
            raise ValueError('Look like a huge mistake. Count of true values should be equal to predicted')

        most_fully_row = max(true_values, key=lambda x: len(x))
        full_categories: Set[CategoryId] = {i.category for i in most_fully_row}

        true_processed = []
        predicted_processed = []
        for index in range(len(true_values)):
            true_row = true_values[index]
            predicted_row = predicted_values[index]

            true_row_filled = self._fix_missing_categories(true_row, categories=full_categories, is_binary=True)
            predict_row_filled = self._fix_missing_categories(predicted_row, categories=full_categories)

            ordered_true = sorted(true_row_filled, key=lambda predict: predict.category)
            ordered_predicted = sorted(predict_row_filled, key=lambda predict: predict.category)
            true_processed.append(ordered_true)
            predicted_processed.append(ordered_predicted)
        return true_processed, predicted_processed

    def produce(self) -> Dict[Name, Metric]:
        """
        Прогоняет набор данных по модели и составляет метрики по результатам работы
        :return:
        """
        y_true = []
        y_predicted = []

        for row in self.dataset.features():
            model_result = self.model(row.x)

            y_true.append(row.y)
            y_predicted.append(model_result)

        y_true, y_predicted = self._append_missing(y_true, y_predicted)
        results = {}
        for MetricClass in self.metrics_classes:
            metric = MetricClass(y_true, y_predicted)
            results[metric.name] = metric.evaluate()

        return results

    def result(self) -> ValidationResult:
        """
        Собирает результат работы модели
        :return:
        """
        metrics = self.produce()
        return ValidationResult(size=self.dataset.size(), metrics_scores=metrics)

    def describe(self):
        """
        Выводит результат работы модели в консоль
        :return:
        """
        validation_result = self.result()
        print('-------------------------------------------------------')
        print(f'Running validation on {validation_result.size} values')
        print(*[f'{name.capitalize()}: {score}' for name, score in
                validation_result.metrics_scores.items()], sep='\n')
        print('-------------------------------------------------------')
