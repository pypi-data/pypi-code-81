from abc import ABC, abstractmethod
from typing import Union


class AbstractMetric(ABC):
    """
    Базовый класс для внедрения метрик в механизмы работы runner'a и модели
    """
    # перечень обязательных метрик, прокидываемых на уровне runner'a
    _default_labels = []
    # перечень дополнительных метрик, которые могут быть добавлены для детализации работы модели
    _registered_labels = []

    @abstractmethod
    def register_labels(self, *labels):
        """
        Добавление новых label'ов для метрики.

        Добавление label'ов должно происходить **ДО** старта приложения
        :param labels: список label'ов, которые будут дополнять метрику
        :raises KeyError: при невозможности добавления новых label'ов
        """

    @abstractmethod
    def add_label_values(self, **values):
        """
        Добавление значений для метрик. Данный процесс должен происходить при каждой обработке материала
        :param values: набор пар "название label'а -> значение"
        :raises ValueError: если были указаны не все зарегистрированные значения
        """

    @abstractmethod
    def _set_default_values(self, **values):
        """
        Выставление значений для метрик по умолчанию.

        Это служебная функция, которую не должен вызывать пользователь
        :param values: перечень значений
        """

    @abstractmethod
    def _inc(self, value: Union[int, float] = 1):
        """
        Увеличение значения счётчика.

        Это служебная функция, которую не должен вызывать пользователь
        :param value: значения для инкремента
        :return:
        """

    @abstractmethod
    def _reset(self):
        """
        Сброс значений кэша значений

        Это служебная функция, которую не должен вызывать пользователь
        :return:
        """

    @abstractmethod
    def name(self) -> str:
        """
        Название метрики
        :return:
        """
        pass


class MetricMock(AbstractMetric):
    def name(self) -> str:
        return 'mock'

    def register_labels(self, *labels):
        pass

    def add_label_values(self, **values):
        pass

    def _set_default_values(self, **values):
        pass

    def _inc(self, value: Union[int, float] = 1):
        pass

    def _reset(self):
        pass
