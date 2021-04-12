import sys
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .enums import ActionType, LayerType

# Literal is included in the stdlib as of Python 3.8
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


class CamelCaseBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

        @staticmethod
        def to_camel_case(snake_str: str) -> str:
            """Convert snake_case string to camelCase
            https://stackoverflow.com/a/19053800
            """
            components = snake_str.split('_')
            # We capitalize the first letter of each component except the first one
            # with the 'title' method and join them together.
            return components[0] + ''.join(x.title() for x in components[1:])

        alias_generator = to_camel_case


# TODO: do we expose this class at all?
# class MapOptions(BaseModel):
#     mapUrl: Optional[str]
#     mapUUID: Optional[UUID]
#     appendToId: Optional[str]
#     id: Optional[str]
#     embed: Optional[bool]
#     onLoad: Optional[() => void]
#     onTimelineIntervalChange: Optional[(currentTimeInterval: List[float>) => void]
#     onLayerTimelineTimeChange: Optional[(currentTime: float) => void]
#     appendToDocument: bool
#     width: float
#     height: float

# class MapInstance(BaseModel):
#     iframe: HTMLCanvasElement


class Layer(CamelCaseBaseModel):
    label: str
    id: str
    is_visible: bool


class ViewState(CamelCaseBaseModel):
    longitude: float
    latitude: float
    # TODO: From looking at the SDK implementation, this should be Optional?
    zoom: Optional[float] = None


class TimelineInfo(CamelCaseBaseModel):
    data_id: List[str]
    domain: List[float]
    is_visible: bool
    enlarged_histogram: List[Any]
    histogram: List[Any]
    value: List[float]
    speed: float
    step: float
    is_animating: bool


class TimeInterval(CamelCaseBaseModel):
    start_time: float
    end_time: float


class TimelineConfig(CamelCaseBaseModel):
    idx: str
    current_time_interval: Optional[TimeInterval]
    is_visible: Optional[bool]
    is_animating: Optional[bool]
    speed: Optional[float]
    timezone: Optional[str]
    time_format: Optional[str]


class LayerTimelineInfo(CamelCaseBaseModel):
    current_time: float
    default_time_format: str
    domain: List[float]
    duration: float
    is_visible: bool
    is_animating: bool
    speed: float
    time_format: str
    time_steps: Any
    timezone: str


class LayerTimelineConfig(CamelCaseBaseModel):
    current_time: Optional[float]
    is_visible: Optional[bool]
    is_animating: Optional[bool]
    speed: Optional[float]
    timezone: Optional[str]
    time_format: Optional[str]


TilesetType = Literal['vector-tile', 'raster-tile']


class VectorMeta(CamelCaseBaseModel):
    data_url: str
    metadata_url: str


class RasterMeta(CamelCaseBaseModel):
    data_url: str
    metadata_url: str


class Tileset(CamelCaseBaseModel):
    name: str
    type: TilesetType
    meta: Union[VectorMeta, RasterMeta]


class LayerConfig(CamelCaseBaseModel):
    data_id: str
    columns: Dict[str, Any]
    is_visible: Optional[bool]
    vis_config: Optional[Dict[str, Any]]
    color_field: Optional[Dict[str, Any]]
    color_scale: Optional[Dict[str, Any]]
    color_ui: Optional[Dict[str, Any]] = Field(alias='colorUI')


class LayerSpec(CamelCaseBaseModel):
    label: Optional[str]
    id: str
    type: LayerType
    config: LayerConfig
    visual_channels: Optional[Dict[str, Any]]


class AddDatasetResponse(BaseModel):
    status: Literal['ok', 'fail']
    message: Optional[str]


class RemoveDatasetResponse(BaseModel):
    status: Literal['ok', 'fail']
    message: Optional[str]


class Action(CamelCaseBaseModel):
    type: ActionType
    message_id: UUID = Field(default_factory=uuid4)

    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        """Custom dict encoding to put keys within `data` key

        Only top level keys should be type, data, and messageId
        """
        # Export by alias by default, but don't change by_alias=False
        if 'by_alias' not in kwargs.keys():
            kwargs['by_alias'] = True

        # Remove None values by default
        if 'exclude_none' not in kwargs.keys():
            kwargs['exclude_none'] = True

        # Use default superclass dict serialization
        d = super().dict(**kwargs)

        # Make sure the data key doesn't exist yet
        assert d.get('data') == None, 'data key already exists'

        d['data'] = {}

        # Keys that should stay at the top level
        top_level_json_keys = ['type', 'messageId', 'data']

        # Set all keys within the data key, but not recursively
        inner_keys = set(d.keys()).difference(top_level_json_keys)
        for key in inner_keys:
            d['data'][key] = d.pop(key)

        return d

    def json(self, **kwargs: Any) -> str:
        """Custom json encoding to put keys within `data` key

        Only top level keys should be type, data, and messageId
        """
        # Export by alias by default, but don't change by_alias=False
        if 'separators' not in kwargs.keys():
            kwargs['separators'] = (',', ':')

        # Export by alias by default, but don't change by_alias=False
        if 'by_alias' not in kwargs.keys():
            kwargs['by_alias'] = True

        # Remove None values by default
        if 'exclude_none' not in kwargs.keys():
            kwargs['exclude_none'] = True

        return super().json(**kwargs)


class SetViewState(Action):
    type: ActionType = ActionType.SET_VIEW_STATE
    view_state: ViewState


class GetLayers(Action):
    type: ActionType = ActionType.GET_LAYERS


class SetLayerVisibility(Action):
    type: ActionType = ActionType.SET_LAYER_VISIBILITY
    layer_id: str
    is_visible: bool


class SetTheme(Action):
    type: ActionType = ActionType.SET_THEME
    theme: Literal['light', 'dark']


class GetTimelineInfo(Action):
    type: ActionType = ActionType.GET_TIMELINE_INFO
    idx: str


class ToggleTimelineAnimation(Action):
    type: ActionType = ActionType.TOGGLE_TIMELINE_ANIMATION
    idx: str


class ToggleTimelineVisibility(Action):
    type: ActionType = ActionType.TOGGLE_TIMELINE_VISIBILITY
    idx: str


class SetTimelineInterval(Action):
    type: ActionType = ActionType.SET_TIMELINE_INTERVAL
    idx: str
    start_time: float
    end_time: float


class SetTimelineAnimationSpeed(Action):
    type: ActionType = ActionType.SET_TIMELINE_SPEED
    idx: str
    speed: float


class SetTimelineConfig(Action):
    type: ActionType = ActionType.SET_TIMELINE_CONFIG
    config: TimelineConfig


class RefreshMapData(Action):
    type: ActionType = ActionType.REFRESH_MAP_DATA


class GetLayerTimelineInfo(Action):
    type: ActionType = ActionType.GET_LAYER_TIMELINE_INFO


class SetLayerTimelineConfig(Action):
    type: ActionType = ActionType.SET_LAYER_TIMELINE_CONFIG
    config: LayerTimelineConfig


class AddTileset(Action):
    type: ActionType = ActionType.ADD_TILESET_TO_MAP
    tileset: Tileset


class AddDataset(Action):
    type: ActionType = ActionType.ADD_DATASET_TO_MAP
    uuid: UUID


class RemoveDataset(Action):
    type: ActionType = ActionType.REMOVE_DATASET_FROM_MAP
    uuid: UUID


class AddLayer(Action):
    type: ActionType = ActionType.ADD_LAYER
    layer: LayerSpec


class RemoveLayer(Action):
    type: ActionType = ActionType.REMOVE_LAYER
    id: str
