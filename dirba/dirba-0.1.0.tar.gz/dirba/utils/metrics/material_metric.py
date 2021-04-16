from typing import Optional, Union

from prometheus_client import Counter

from .abc import AbstractMetric


class MaterialMetric(AbstractMetric):
    """
    Обёртка над метрикой для упрощённого взаимодействия
    """

    def name(self) -> str:
        return 'elements_processed'

    _default_labels = [
        'category',
        'category_name',
        'model_name',
        'model_version',
        'content_type',
        'query_category',
        'query_category_name'
    ]
    _registered_labels = []

    def __init__(self):
        self._metric: Optional[Counter] = None

        self._value_cache = dict()

    def register_labels(self, *labels):
        """
        Добавление новых label'ов для метрики.

        Добавление label'ов должно происходить **ДО** старта приложения
        :param labels: список label'ов, которые будут дополнять метрику
        :raises KeyError: при невозможности добавления новых label'ов
        """
        if self._metric:
            raise KeyError("Unable to set labels after metric is started")

        self._registered_labels.extend(labels)

    def add_label_values(self, **values):
        """
        Добавление значений для метрик. Данный процесс должен происходить при каждой обработке материала
        :param values: набор пар "название label'а -> значение"
        :raises ValueError: если были указаны не все зарегистрированные значения
        """
        if set(values.keys()) == set(self._registered_labels):
            self._value_cache.update(values)
        else:
            raise ValueError(f"You should specify all registered labels: {', '.join(self._registered_labels)}")

    def _set_default_values(self, **values):
        """
        Выставление значений для метрик по умолчанию.

        Это служебная функция, которую не должен вызывать пользователь
        :param values: перечень значений
        """
        self._value_cache.update(values)

    def _inc(self, value: Union[int, float] = 1):
        """
        Увеличение значения счётчика.

        Это служебная функция, которую не должен вызывать пользователь
        :param value: значения для инкремента
        :return:
        """
        if self._metric is None:
            self._metric = Counter(self.name(),
                                   'Кол-во материалов обработанных моделью',
                                   [*self._default_labels, *self._registered_labels])
        self._metric.labels(**self._value_cache).inc(value)

    def _reset(self):
        """
        Сброс значений кэша значений

        Это служебная функция, которую не должен вызывать пользователь
        :return:
        """
        self._value_cache.clear()
