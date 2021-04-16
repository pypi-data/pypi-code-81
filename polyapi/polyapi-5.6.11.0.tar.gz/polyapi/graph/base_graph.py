#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Описание базового класса, осуществляющего работу с графиками.
"""


class BaseGraph():
    """
    Класс, являющийся общим предком для всех типов графиков. Содержит обобщённые методы работы с графиками.
    """
    def __init__(self, base_bl: 'BusinessLogic', settings: str, grid: str, labels: dict, other: dict,
                common_params: dict, graph_type: str, int_type: int):
        # экземпляр класса BusinessLogic
        self._base_bl = base_bl
        # битмап настроек
        self._settings = settings
        # настройки сетки
        self._grid = grid
        # настройки подписи на графиках
        self._labels = labels
        # прочие настройки, зависящие от графиков
        self._other = other
        # идентификатор OLAP-модуля, идентификатор модуля графиков и конфигцрация OLAP-модуля
        # содержит поля olap_module_id, graph_module_id, olap_config
        self._common_params = common_params
        # тип графика (строковый), используется при формировании общего конфига
        self._graph_type = graph_type
        # целочисленный тип графика, определён Полиматикой в server-codes.json (если не задан, то используется -1)
        self._int_type = int_type
        # название графика
        self._graph_name = other.get('name', False)

    @property
    def base_bl(self) -> 'BusinessLogic':
        return self._base_bl

    @property
    def settings(self) -> str:
        return self._settings

    @property
    def grid(self) -> str:
        return self._grid

    @property
    def labels(self) -> dict:
        return self._labels

    @property
    def other(self) -> dict:
        return self._other

    @property
    def common_params(self) -> dict:
        return self._common_params

    @property
    def graph_type(self) -> str:
        return self._graph_type

    @property
    def int_type(self) -> int:
        return self._int_type

    @property
    def graph_name(self) -> str:
        return self._graph_name

    def _check_frequency_impl(self, check_func: 'def', axis_values: dict, start: int, end: int, step: int):
        """
        Реализация проверки значения частоты подписей по осям. Если проверка не пройдена - сгенерируется исключение.
        :param check_func: проверяющая функция, которая возвращает True, если проверка не пройдена.
        :param axis_values: данные частоты подписей по осям.
        :param start: начало диапазона.
        :param end: конец диапазона.
        :param step: шаг.
        """
        for axis in axis_values:
            axis_value = axis_values.get(axis)
            if not isinstance(axis_value, (int, float)):
                raise ValueError("Axis value must be int or float type!")
            if check_func(axis_value):
                params = [axis, start, end, step]
                raise ValueError("Axis {} frequency must be set in interval [{}, {}] with step {}!".format(*params))

    def check_olap_configuration(self, left_dims_count: int, top_dims_count: int, fact_count: int, marked: bool):
        """
        Сверка текущей конфигурации OLAP-модуля на соответствие заданному типу графика.
        :param left_dims_count: минимальное количество левых размерностей, требующихся для построения графика.
            Т.е. в мультисфере количество левых размерностей должно быть больше или равно заданному значению.
        :param top_dims_count: минимальное количество верхних размерностей, требующихся для построения графика.
            Т.е. в мультисфере количество верхних размерностей должно быть больше или равно заданному значению.
        :param fact_count: минимальное количество фактов, требующихся для построения графика.
            Т.е. в мультисфере количество фактов должно быть больше или равно заданному значению.
        :param marked: должны ли быть отметки фактов (выделения строк) в OLAP-модуле.
            Отметки фактов в обязательном порядке требуются для построения некоторых типов графиков. В этом случае
            значение параметра должно быть True/False.
            Для остальных типов графиков отметка не обязательна - она может как быть, так и не быть (графики построятся
            в любом случае). В этом случае значение параметра должно быть None.
        """
        # olap_config имеет поля: 'top_dim_count', 'left_dim_count', 'fact_count', 'marked'
        olap_config = self.common_params.get('olap_config')
        if olap_config.get('left_dim_count') < left_dims_count or olap_config.get('top_dim_count') < top_dims_count or \
            olap_config.get('fact_count') < fact_count or marked is not None and olap_config.get('marked') != marked:
            raise ValueError('Graph cannot be draw with current OLAP configuration!')

    def get_actual_settings(self, field_names: list) -> dict:
        """
        Преобразование (по типу "0" -> False, "1" -> True) битмапа настроек в реальные настройки графиков.
        :param field_names: названия полей, в которые нужно преобразовать настройки из битмапа.
        :return: словарь, содержащий реальные настройки.
        :example: bitmap="1101", field_names=['arg1', 'arg2', 'arg3', 'arfg4'] ->
            {'arg1': True, 'arg2': True, 'arg3': False, 'arg4': True}
        """
        # если передано неверное число настроек - бросаем ошибку
        if len(self.settings) != len(field_names):
            raise ValueError("Settings length can only equals {} for this graph type!".format(len(field_names)))
        return {field: bool(int(self.settings[i])) for i, field in enumerate(field_names)}

    def check_frequency_axis_5_30_5(self, axis_values: dict):
        """
        Реализация проверки значения частоты подписей по осям.
        Паттерн проверки: значения могут быть от 5 до 30 с шагом 5.
        :param axis_values: данные частоты подписей по осям.
        """
        self._check_frequency_impl(lambda item: item % 5 != 0 or item < 5 or item > 30, axis_values, 5, 30, 5)

    def check_bool(self, value: 'any') -> bool:
        """
        Проверка значения на булевский тип.
        :param value: проверяемое значение.
        """
        return isinstance(value, bool)

    def get_graph_config(self) -> dict:
        """
        Возвращает основную часть настроек графика (то есть ту часть, которая не параметризуется пользователем).
        :return: Основная часть конфигурации графика.
        """
        graph_settings = {
            "plotName": self.graph_type,
            # может размеры окна графиков как-то параметризовать?
            "geometry": {"width": 840, "height": 540},
            "plotData": {
                self.graph_type: {
                    # тут будет прописан конфиг, сформированный на основе настроек, заданных пользователем
                    "config": {
                    },
                    # в этом блоке задаём имя графику; остальное неизвестно, для чего, но нужно
                    "state": {
                        "colors": {
                            "facts": {}
                        },
                        "title": "",
                        "zoom": {
                            "k": 1,
                            "x": 0,
                            "y": 0,
                            "z": 0
                        }
                    },
                    # неизвестно, для чего, но нужно
                    "query": {}
                }
            }
        }
        return graph_settings
