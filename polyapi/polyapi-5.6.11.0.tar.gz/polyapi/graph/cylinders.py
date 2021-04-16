#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Реализация графика типа "Цилиндры".
"""

from .base_graph import BaseGraph

class Cylinders(BaseGraph):
    """
    Реализация графика типа "Цилиндры".
    """
    def __init__(self, base_bl: 'BusinessLogic', settings: str, grid: str, labels: dict,
                other: dict, common_params: dict):
        super().__init__(base_bl, settings, grid, labels, other, common_params, 'plot-cylinder', -1)

    def _get_settings(self) -> dict:
        """
        Получение актуальных настроек по заданному битмапу.
        :return: {
            'titleShow': <value>,
            'legend': <value>,
            'axis': <value>,
            'axis_notes': <value>,
            'vertical_right_axix': <value>
        }
        """
        return self.get_actual_settings(['titleShow', 'legend', 'axis', 'axis_notes', 'vertical_right_axix'])

    def _get_labels_settings(self) -> dict:
        """
        Получение настроек графика по параметру labels.
        :return: {'OX': <value>, 'OY': <value>, 'short_format': <value>}.
        """
        values_dict = {'OX': self.labels.get('OX', 10), 'OY': self.labels.get('OY', 10)}
        self.check_frequency_axis_5_30_5(values_dict)
        short_format = self.labels.get('short_format', False)
        if not self.check_bool(short_format):
            raise ValueError('Param "short_format" must be bool type!')
        values_dict.update({'short_format': short_format})
        return values_dict

    def _get_other_settings(self) -> dict:
        """
        Получение прочих настроек графика.
        :return: {'hints': <value>, 'ident': <value>, 'ident_value': <value>}.
        """
        hints, ident, ident_value = \
            self.other.get('hints', False), self.other.get('ident', True), self.other.get('ident_value', 1)
        if not self.check_bool(hints):
            raise ValueError('Param "hints" must be bool type!')
        if not self.check_bool(ident):
            raise ValueError('Param "ident" must be bool type!')
        check_func = lambda item: round(item * 100) % 5 != 0 or item < 0 or item > 1
        if check_func(ident_value):
            raise ValueError('Param "ident_value" must be set in interval [0, 1] with step 0.05!')
        return {"hints": hints, "ident": ident, "ident_value": ident_value}

    def draw(self):
        """
        Отрисовка графика. Состоит из нескольких этапов:
        1. Проверка данных для текущего типа графика;
        2. Формирование конфигурации графика;
        3. Выхов команды, отрисовывающей график.
        """
        # проверка данных и получение всех настроек
        self.check_olap_configuration(1, 0, 1, None)
        settings = self._get_settings()
        labels_settings = self._get_labels_settings()
        other_settings = self._get_other_settings()

        # получение базовых настроек и их дополнение на основе заданных пользователем значений
        graph_config = self.get_graph_config().copy()
        base_setting = {
            "titleShow": settings.get('titleShow'),
            "legend": settings.get('legend'),
            "axis": settings.get('axis'),
            "axisNotes": settings.get('axis_notes'),
            "axisPosition": settings.get('vertical_right_axix'),
            "wireShow": self.grid,
            "axisNotesPeriodX": labels_settings.get('OX'),
            "axisNotesPeriodY": labels_settings.get('OY'),
            "axisXShortFormat": labels_settings.get('short_format')
        }
        cylinders_setting = {
            "hints": other_settings.get('hints'),
            "enableIndentation": other_settings.get('ident'),
            "indentation": other_settings.get('ident_value')
        }
        graph_config['plotData'][self.graph_type]['config'].update({
            'base': base_setting,
            'cylinder': cylinders_setting
        })
        graph_config['plotData'][self.graph_type]['state']['title'] = self.graph_name

        # и, наконец, сохраняя настройки, отрисовываем сам график
        self.base_bl.execute_manager_command(
            command_name="user_iface",
            state="save_settings",
            module_id=self.common_params.get('graph_module_id'),
            settings=graph_config
        )
