'''_1516.py

DynamicCustomReportItem
'''


from mastapy._internal import constructor
from mastapy.utility.report import (
    _1497, _1480, _1485, _1486,
    _1487, _1488, _1489, _1490,
    _1492, _1493, _1494, _1495,
    _1496, _1498, _1500, _1501,
    _1504, _1505, _1506, _1508,
    _1509, _1510, _1511, _1513,
    _1514
)
from mastapy.shafts import _20
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical import _961
from mastapy.utility_gui.charts import _1575, _1576
from mastapy.bearings.bearing_results import (
    _1648, _1649, _1652, _1660
)
from mastapy.system_model.analyses_and_results.system_deflections.reporting import _2515
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4048
from mastapy.system_model.analyses_and_results.modal_analyses.reporting import _4893, _4897
from mastapy._internal.python_net import python_net_import

_DYNAMIC_CUSTOM_REPORT_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'DynamicCustomReportItem')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicCustomReportItem',)


class DynamicCustomReportItem(_1505.CustomReportNameableItem):
    '''DynamicCustomReportItem

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_CUSTOM_REPORT_ITEM

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicCustomReportItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_main_report_item(self) -> 'bool':
        '''bool: 'IsMainReportItem' is the original name of this property.'''

        return self.wrapped.IsMainReportItem

    @is_main_report_item.setter
    def is_main_report_item(self, value: 'bool'):
        self.wrapped.IsMainReportItem = bool(value) if value else False

    @property
    def inner_item(self) -> '_1497.CustomReportItem':
        '''CustomReportItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1497.CustomReportItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_shaft_damage_results_table_and_chart(self) -> '_20.ShaftDamageResultsTableAndChart':
        '''ShaftDamageResultsTableAndChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _20.ShaftDamageResultsTableAndChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ShaftDamageResultsTableAndChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_cylindrical_gear_table_with_mg_charts(self) -> '_961.CylindricalGearTableWithMGCharts':
        '''CylindricalGearTableWithMGCharts: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _961.CylindricalGearTableWithMGCharts.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CylindricalGearTableWithMGCharts. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_ad_hoc_custom_table(self) -> '_1480.AdHocCustomTable':
        '''AdHocCustomTable: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1480.AdHocCustomTable.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to AdHocCustomTable. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_chart(self) -> '_1485.CustomChart':
        '''CustomChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1485.CustomChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_graphic(self) -> '_1486.CustomGraphic':
        '''CustomGraphic: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1486.CustomGraphic.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomGraphic. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_image(self) -> '_1487.CustomImage':
        '''CustomImage: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1487.CustomImage.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomImage. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report(self) -> '_1488.CustomReport':
        '''CustomReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1488.CustomReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_cad_drawing(self) -> '_1489.CustomReportCadDrawing':
        '''CustomReportCadDrawing: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1489.CustomReportCadDrawing.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportCadDrawing. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_chart(self) -> '_1490.CustomReportChart':
        '''CustomReportChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1490.CustomReportChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_column(self) -> '_1492.CustomReportColumn':
        '''CustomReportColumn: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1492.CustomReportColumn.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportColumn. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_columns(self) -> '_1493.CustomReportColumns':
        '''CustomReportColumns: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1493.CustomReportColumns.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportColumns. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_definition_item(self) -> '_1494.CustomReportDefinitionItem':
        '''CustomReportDefinitionItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1494.CustomReportDefinitionItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportDefinitionItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_horizontal_line(self) -> '_1495.CustomReportHorizontalLine':
        '''CustomReportHorizontalLine: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1495.CustomReportHorizontalLine.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportHorizontalLine. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_html_item(self) -> '_1496.CustomReportHtmlItem':
        '''CustomReportHtmlItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1496.CustomReportHtmlItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportHtmlItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_item_container(self) -> '_1498.CustomReportItemContainer':
        '''CustomReportItemContainer: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1498.CustomReportItemContainer.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainer. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_item_container_collection_base(self) -> '_1500.CustomReportItemContainerCollectionBase':
        '''CustomReportItemContainerCollectionBase: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1500.CustomReportItemContainerCollectionBase.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainerCollectionBase. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_item_container_collection_item(self) -> '_1501.CustomReportItemContainerCollectionItem':
        '''CustomReportItemContainerCollectionItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1501.CustomReportItemContainerCollectionItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainerCollectionItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_multi_property_item_base(self) -> '_1504.CustomReportMultiPropertyItemBase':
        '''CustomReportMultiPropertyItemBase: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1504.CustomReportMultiPropertyItemBase.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportMultiPropertyItemBase. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_nameable_item(self) -> '_1505.CustomReportNameableItem':
        '''CustomReportNameableItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1505.CustomReportNameableItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportNameableItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_named_item(self) -> '_1506.CustomReportNamedItem':
        '''CustomReportNamedItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1506.CustomReportNamedItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportNamedItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_status_item(self) -> '_1508.CustomReportStatusItem':
        '''CustomReportStatusItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1508.CustomReportStatusItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportStatusItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_tab(self) -> '_1509.CustomReportTab':
        '''CustomReportTab: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1509.CustomReportTab.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportTab. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_tabs(self) -> '_1510.CustomReportTabs':
        '''CustomReportTabs: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1510.CustomReportTabs.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportTabs. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_text(self) -> '_1511.CustomReportText':
        '''CustomReportText: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1511.CustomReportText.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportText. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_sub_report(self) -> '_1513.CustomSubReport':
        '''CustomSubReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1513.CustomSubReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomSubReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_table(self) -> '_1514.CustomTable':
        '''CustomTable: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1514.CustomTable.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomTable. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_dynamic_custom_report_item(self) -> 'DynamicCustomReportItem':
        '''DynamicCustomReportItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if DynamicCustomReportItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to DynamicCustomReportItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_line_chart(self) -> '_1575.CustomLineChart':
        '''CustomLineChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1575.CustomLineChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomLineChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_table_and_chart(self) -> '_1576.CustomTableAndChart':
        '''CustomTableAndChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1576.CustomTableAndChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomTableAndChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_loaded_ball_element_chart_reporter(self) -> '_1648.LoadedBallElementChartReporter':
        '''LoadedBallElementChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1648.LoadedBallElementChartReporter.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedBallElementChartReporter. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_loaded_bearing_chart_reporter(self) -> '_1649.LoadedBearingChartReporter':
        '''LoadedBearingChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1649.LoadedBearingChartReporter.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedBearingChartReporter. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_loaded_bearing_temperature_chart(self) -> '_1652.LoadedBearingTemperatureChart':
        '''LoadedBearingTemperatureChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1652.LoadedBearingTemperatureChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedBearingTemperatureChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_loaded_roller_element_chart_reporter(self) -> '_1660.LoadedRollerElementChartReporter':
        '''LoadedRollerElementChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1660.LoadedRollerElementChartReporter.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedRollerElementChartReporter. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_shaft_system_deflection_sections_report(self) -> '_2515.ShaftSystemDeflectionSectionsReport':
        '''ShaftSystemDeflectionSectionsReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2515.ShaftSystemDeflectionSectionsReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ShaftSystemDeflectionSectionsReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_parametric_study_histogram(self) -> '_4048.ParametricStudyHistogram':
        '''ParametricStudyHistogram: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4048.ParametricStudyHistogram.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ParametricStudyHistogram. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_campbell_diagram_report(self) -> '_4893.CampbellDiagramReport':
        '''CampbellDiagramReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4893.CampbellDiagramReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CampbellDiagramReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_per_mode_results_report(self) -> '_4897.PerModeResultsReport':
        '''PerModeResultsReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4897.PerModeResultsReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to PerModeResultsReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None
