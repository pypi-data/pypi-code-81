from itsimodels.core.base_models import BaseModel, ChildModel
from itsimodels.core.compat import string_types
from itsimodels.core.fields import (
    BoolField,
    DictField,
    ForeignKey,
    ForeignKeyList,
    ListField,
    NumberField,
    StringField,
    TypeField
)


KPI_SUMMARY_RE = r'`get_full_itsi_summary_kpi\((.+)\)`'


KV_STORE_KEY_RE = r'splunk-enterprise-kvstore://(.+)'

'''
Sample urls with object key embedded (one in the middle, one at the end):
Notice Id could belong to multiple types of objects. in below example, 
one is 'savedHomeView', the other is 'service'

/en-US/app/itsi/homeview?savedHomeViewId=46eef7d0-3b25-11eb-9a4b-020df9a76f18&earliest=$global_time.earliest$&latest=$global_time.latest$

/app/itsi/homeview?view=standard&viewType=service_topology&earliest=-12h&latest=now&serviceId=3f4706e8-109e-4af1-9a69-4eab5696c648
'''
EVENT_HANDLER_OPTION_URL_RE = r'id=([\w-]+?)(?=&|$)'

class ValuedModel(ChildModel):

    def to_dict(self, *args, **kwargs):
        obj = super(ValuedModel, self).to_dict(*args, **kwargs)

        # Remove any null values to conform with the UI visualization library
        data = {key: value for key, value in obj.items() if
                value or (type(value) in (int, float, bool) and value is not None)}

        return data


class DataSourceMeta(ChildModel):
    kpi_id = ForeignKey('itsimodels.service.Kpi', alias='kpiID')

    service_id = ForeignKey('itsimodels.service.Service', alias='serviceID')


class DataSourceOptions(ValuedModel):
    data = DictField()

    # NOTE:
    # glass table --> definition --> data_sources --> options --> query
    # the regex is not complete. ids may have to be manually fixed
    query = ForeignKey('itsimodels.service.Kpi', key_regex=KPI_SUMMARY_RE)


class DataSource(ValuedModel):
    meta = TypeField(DataSourceMeta)

    name = StringField()

    options = TypeField(DataSourceOptions)

    primary = StringField()

    type = StringField()


class DefinitionInput(ChildModel):
    options = DictField()

    title = StringField()

    type = StringField()


class LayoutImage(ChildModel):
    size_type = StringField(alias='sizeType')

    src = ForeignKey('itsimodels.glass_table_image.GlassTableImage', key_regex=KV_STORE_KEY_RE)

    x = NumberField()

    y = NumberField()


class LayoutOptions(ValuedModel):
    background_color = StringField(alias='backgroundColor')

    background_image = TypeField(LayoutImage, alias='backgroundImage')

    display = StringField()

    height = NumberField()

    show_title_and_description = BoolField(alias='showTitleAndDescription')

    width = NumberField()


class StructureItem(ChildModel):
    # references one of the visualizations id within the
    # glass table definition
    item = StringField()

    position = DictField()

    type = StringField()


class Layout(ChildModel):
    global_inputs = ListField(string_types, alias='globalInputs')

    options = TypeField(LayoutOptions)

    structure = ListField(StructureItem)

    type = StringField()


class VisualizationOptions(ValuedModel):
    background_color = StringField(alias='backgroundColor')

    color = StringField()

    color_mode = StringField(alias='colorMode')

    content = StringField()

    fill = StringField()

    font_family = StringField(alias='fontFamily')

    font_size = NumberField(alias='fontSize')

    font_weight = StringField(alias='fontWeight')

    icon = ForeignKey('itsimodels.glass_table_icon.GlassTableIcon', key_regex=KV_STORE_KEY_RE)

    major_color = StringField(alias='majorColor')

    number_precision = NumberField(alias='numberPrecision')

    preserve_aspect_ratio = BoolField(alias='preserveAspectRatio')

    rx = NumberField()

    ry = NumberField()

    show_trend_indicator = BoolField(alias='showTrendIndicator')

    show_spark_line = BoolField(alias='showSparkline')

    show_spark_line_tooltip = BoolField(alias='showSparklineTooltip')

    show_value = BoolField(alias='showValue')

    spark_line_display = StringField(alias='sparklineDisplay')

    spark_line_position = StringField(alias='sparklinePosition')

    spark_line_stroke_color = StringField(alias='sparklineStrokeColor')

    src = ForeignKey('itsimodels.glass_table_image.GlassTableImage', key_regex=KV_STORE_KEY_RE)

    stroke = StringField()

    stroke_width = NumberField(alias='strokeWidth')

    text_color = StringField(alias='textColor')

    trend_display_mode = StringField(alias='trendDisplayMode')

    unit = StringField()

    unit_position = StringField(alias='unitPosition')

    width = NumberField()


class EventHandlerOption(ValuedModel):
    key = StringField()

    newTab = BoolField()

    type = StringField()

    # None refers because we want to check all types of objects for key
    # mapping. It is because the object key embeded could belong to different
    # types, not just one (see example above regarding EVENT_HANDLER_OPTION_URL_RE
    url = ForeignKey(refers=None, key_regex=EVENT_HANDLER_OPTION_URL_RE)


class EventHandlers(ChildModel):
    options = TypeField(EventHandlerOption)

    type = StringField()


class Visualization(ValuedModel):
    data_sources = DictField(alias='dataSources')

    encoding = DictField()

    event_handlers = ListField(EventHandlers, alias='eventHandlers')

    options = TypeField(VisualizationOptions)

    # references visualization ids within glass table def
    primary = StringField()

    title = StringField()

    type = StringField()


class Definition(ChildModel):
    data_sources = DictField(DataSource, alias='dataSources')

    defaults = DictField()

    description = StringField()

    inputs = DictField(DefinitionInput)

    layout = TypeField(Layout)

    title = StringField()

    visualizations = DictField(Visualization)


class GlassTable(BaseModel):
    key = StringField(required=True, alias='_key')

    title = StringField(required=True)

    definition = TypeField(Definition)

    description = StringField(default='')

    gt_version = StringField(default='beta')

    # interactable = BoolField()

    latest = StringField(default='now')

    latest_label = StringField(default='Now')

    swap_service_ids = ForeignKeyList('itsimodels.service.Service')

    selected_swap_service_id = ForeignKey('itsimodels.service.Service')

    template_selected_service_id = ForeignKey('itsimodels.service.Service', alias='templateSelectedServiceId')

    template_swappable_service_ids = ForeignKeyList('itsimodels.service.Service', alias='templateSwappableServiceIds')

