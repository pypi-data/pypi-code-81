#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Описание интерфейсного класса для взаимодействия с внешними вызовами.
"""
from ..common import GRAPH_ID
from .lines import Lines
from .cylinders import Cylinders
from .cumulative_cylinders import CumulativeCylinders


class Graph():
    """Класс, реализующий методы для взаимодействия пользователя с графиками"""
    def __init__(self, base_bl: 'BusinessLogic', graph_type: [int, str], settings: str, grid: int,
                labels: dict, other: dict, current_id: str):
        # экземпляр класса BusinessLogic
        self._base_bl = base_bl
        # тип графика (в виде строки); если заданного пользователем типа не существует - будет сгенерирована ошибка;
        # общий параметр для всех типов графиков
        self._graph_type = self._get_graph_type(graph_type)
        self._check_implemented()
        # битмап настроек; конкретные настройки для каждого типа графика извлекаются непосредственно в соотв. классах
        settings = settings or self._get_default_settings()
        self._check_setting_bitmap(settings)
        self._settings = settings
        # настройки сетки; общий параметр для всех типов графиков
        self._grid = self._get_grid(grid)
        # настройки подписи на графиках;
        # конкретные настройки для каждого типа графика извлекаются непосредственно в соотв. классах
        self._labels = labels
        # прочие настройки; конкретные настройки для каждого типа графика извлекаются непосредственно в соотв. классах
        self._other = other
        # идентификатор мультисферы (если график создаётся) или идентификатор графика (если график изменяется)
        self._current_id = current_id

    def _get_graph_type(self, graph_type: [int, str]) -> str:
        """
        Проверка типа графика. Возвращает тип графика в виде строки.
        """
        int_type_map = {
            1: 'lines',
            2: 'cylinders',
            3: 'cumulative_cylinders',
            4: 'area',
            5: 'cumulative_area',
            6: 'pies',
            7: 'radar',
            8: 'circles',
            9: 'circles_series',
            10: 'balls',
            11: 'pools',
            12: '3d_pool',
            13: 'corridor',
            14: 'surface',
            15: 'graph',
            16: 'sankey',
            17: 'chord',
            18: 'point',
            19: 'point_series'
        }
        if isinstance(graph_type, int):
            if graph_type not in int_type_map:
                raise ValueError('Graph type "{}" does not exists!'.format(graph_type))
            return int_type_map.get(graph_type)
        elif isinstance(graph_type, str):
            if graph_type not in list(int_type_map.values()):
                raise ValueError('Graph type "{}" does not exists!'.format(graph_type))
            return graph_type
        else:
            raise ValueError('Param "g_type" must be string or int!')

    def _check_implemented(self):
        """
        Временная проверка, показывающая, реализован ли на данный момент указанный тип графика.
        Будет удалено, когда будут реализованы все 19 типов графиков.
        """
        implemented_graphs = ['lines', 'cylinders', 'cumulative_cylinders']
        if self._graph_type not in implemented_graphs:
            raise ValueError('Type "{}" of graph is not yet implemented!'.format(self._graph_type))

    def _get_graph_instance(self) -> 'Graph instance':
        """
        Возвращает необходимый класс в зависимости от типа графика.
        """
        class_map = {
            'lines': Lines,
            'cylinders': Cylinders,
            'cumulative_cylinders': CumulativeCylinders,
            'area': None,
            'cumulative_area': None,
            'pies': None,
            'radar': None,
            'circles': None,
            'circles_series': None,
            'balls': None,
            'pools': None,
            '3d_pool': None,
            'corridor': None,
            'surface': None,
            'graph': None,
            'sankey': None,
            'chord': None,
            'point': None,
            'point_series': None
        }
        return class_map.get(self._graph_type)

    def _get_default_settings(self) -> str:
        """
        Возвращает настройки графиков по-умолчанию в зависимости от типа графика.
        """
        settings_map = {
            'lines': "11110",
            'cylinders': "11110",
            'cumulative_cylinders': "11110",
            'area': "11110",
            'cumulative_area': "11110",
            'pies': "111",
            'radar': "1111",
            'circles': "11110",
            'circles_series': "11110",
            'balls': "1111",
            'pools': "11110",
            '3d_pool': "1111",
            'corridor': "11110",
            'surface': "111",
            'graph': "11",
            'sankey': "1",
            'chord': "11",
            'point': "11110",
            'point_series': "11110"
        }
        return settings_map.get(self._graph_type)

    def _check_setting_bitmap(self, settings_bitmap: str):
        """
        Проверка правильности задания настроек.
        """
        try:
            int(settings_bitmap, 2)
        except ValueError:
            raise ValueError("Settings string can only contain 0 or 1!")

    def _get_grid(self, grid: int) -> str:
        """
        Получение значения сетки (если это поддерживается заданным типом графика).
        """
        # для указанных типов графиков не нужно задавать значение сетки - пропускаем их
        # пропустить параметр означает не отобразить его в итоговой конфигурации графика
        not_grid_graph_types = ['pies', 'radar', 'balls', '3d_pool', 'surface', 'graph', 'sankey', 'chord']
        if self._graph_type in not_grid_graph_types:
            return str()

        # проверка значения
        if not isinstance(grid, int):
            raise ValueError("Grids values can only be Integers")

        # интерпретируем значение для использования в графиках
        grids = {
            0: "all",  # Все линии
            1: "h",    # Горизонтальные линии
            2: "v",    # Вертикальные линии
            3: "none"  # Без сетки
        }
        if grid not in grids:
            raise ValueError("Grid value can be only in interval [0, 3]!")
        return grids.get(grid)

    def _get_olap_module_config(self, module_id: str) -> dict:
        """
        Получение конфигурации заданного OLAP-модуля.
        :param module_id: идентификатор OLAP-модуля.
        :return: конфигурация в виде {'top_dim_count': <>, 'left_dim_count': <>, 'fact_count': <>, 'marked': <>}.
        """
        config = {'top_dim_count': 0, 'left_dim_count': 0, 'fact_count': 0, 'marked': False}

        # т.к. заданный пользователем OLAP-модуль может отличаться от текущего активного OLAP-модуля,
        # то делаем временную подмену для получения актуальных данных
        old_ms_module_id = self._base_bl.multisphere_module_id
        self._base_bl._set_multisphere_module_id(module_id)
        result = self._base_bl.get_multisphere_data()
        self._base_bl._set_multisphere_module_id(old_ms_module_id)

        # данные по размерностям обоих уровней
        for item in result.get('dimensions'):
            position = item.get('position')
            if position == 1:
                config['left_dim_count'] += 1
            if position == 2:
                config['top_dim_count'] += 1

        # данные по фактам
        for item in result.get('facts'):
            if item.get('visible'):
                config['fact_count'] += 1

        # данные по меткам (в данном случае неважно, сколько их; важно, чтобы была хотя бы одна)
        mark_result = self._base_bl.execute_olap_command(
            command_name="view", state="get", from_col=0, from_row=0, num_col=100, num_row=100)
        mark_result_data = self._base_bl.h.parse_result(mark_result, 'left')
        for item in mark_result_data:
            if len(item) > 0 and item[0].get('flags', 0) != 0:
                config['marked'] = True
                break
        return config

    def create(self) -> str:
        """
        Создание нового графика с заданными параметрами.
        """
        # получаем идентификатор слоя и OLAP-модуля
        layer_id, olap_module_id = self._base_bl._find_olap_module(self._current_id)
        if not olap_module_id:
            if self._current_id:
                error_msg = 'OLAP module "{}" not found!'.format(self._current_id)
            else:
                error_msg = 'OLAP module not exists!'
            raise ValueError(error_msg)

        # создаём новое окно, сохраняем идентификатор модуля графиков
        res = self._base_bl.execute_manager_command(
            command_name="user_iface",
            state="create_module",
            module_id=olap_module_id,
            module_type=GRAPH_ID,
            layer_id=layer_id,
            after_module_id=olap_module_id
        )
        graph_module_uuid = self._base_bl.h.parse_result(res, 'module_desc', 'uuid')

        # запаковываем в словарь все необходимые данные, в т.ч. конфигурацию OLAP-модуля
        common_params = {
            'olap_module_id': olap_module_id,
            'graph_module_id': graph_module_uuid,
            'olap_config': self._get_olap_module_config(olap_module_id)
        }

        # отрисовываем график на созданном окне
        graph = self._get_graph_instance()
        try:
            graph(self._base_bl, self._settings, self._grid, self._labels, self._other, common_params).draw()
        except Exception as ex:
            # если не удалось отрисовать график с заданными параметрами - закрываем созданное окно графиков
            self._base_bl.execute_manager_command(
                command_name='user_iface', state='close_module', module_id=graph_module_uuid)
            raise
        return graph_module_uuid

    def update(self) -> str:
        """
        Изменение уже существующего графика по заданным параметрам.
        """
        # проверка, существует ли график с заданным идентификатором
        layer_id, graph_module_id = self._base_bl._find_graph_module(self._current_id)
        if not graph_module_id:
            if self._current_id:
                error_msg = 'Graph "{}" not found!'.format(self._current_id)
            else:
                error_msg = 'Graph module not exists!'
            raise ValueError(error_msg)

        # получаем идентификатор OLAP-модуля, на основе которого построен график
        layer_settings = self._base_bl.execute_manager_command(
            command_name="user_layer", state="get_layer", layer_id=layer_id)
        layer_modules = self._base_bl.h.parse_result(
            result=layer_settings, key="layer", nested_key="module_descs") or list()
        olap_module_id = str()
        for module in layer_modules:
            if module.get('uuid') == graph_module_id:
                olap_module_id = module.get('parent')
                break
        if not olap_module_id:
            raise ValueError('OLAP module for graph "{}" not found!'.format(graph_module_id))

        # запаковываем в словарь все необходимые данные, в т.ч. конфигурацию OLAP-модуля
        common_params = {
            'olap_module_id': olap_module_id,
            'graph_module_id': graph_module_id,
            'olap_config': self._get_olap_module_config(olap_module_id)
        }

        # отрисовываем график на созданном окне
        graph = self._get_graph_instance()
        try:
            graph(self._base_bl, self._settings, self._grid, self._labels, self._other, common_params).draw()
        except Exception as ex:
            # если не удалось отрисовать график с заданными параметрами - закрывать созданное окно графиков не нужно,
            # т.к. оно уже было создано ранее (не в этом методе)
            raise
        return graph_module_id
