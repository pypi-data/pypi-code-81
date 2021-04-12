from enum import Enum


class ActionType(str, Enum):
    """Actions that can be passed to Studio
    """
    ADD_TILESET_TO_MAP = 'map-sdk-add-tileset-top-map'
    ADD_DATASET_TO_MAP = 'map-sdk-add-dataset-to-map'
    REMOVE_DATASET_FROM_MAP = 'map-sdk-remove-dataset-from-map'
    GET_LAYER_TIMELINE_INFO = 'map-sdk-get-layer-timeline-info'
    ADD_LAYER = 'map-sdk-add-layer'
    REMOVE_LAYER = 'map-sdk-remove-layer'
    GET_LAYERS = 'map-sdk-get-layers'
    GET_TIMELINE_INFO = 'map-sdk-get-timeline-info'
    LAYER_ANIMATION_TIME_CHANGED = 'map-sdk-layer-animation-time-changed'
    MAP_INITIALIZED = 'map-sdk-initialized'
    REFRESH_MAP_DATA = 'map-sdk-reload-map-data'
    SET_LAYER_TIMELINE_CONFIG = 'map-sdk-set-layer-timeline-config'
    SET_LAYER_VISIBILITY = 'map-sdk-set-layer-visibility'
    SET_MAP_CONTROL_VISIBILITY = 'map-sdk-set-map-control-visibility'
    SET_THEME = 'map-sdk-set-theme'
    SET_TIMELINE_CONFIG = 'map-sdk-set-timeline-config'
    SET_TIMELINE_INTERVAL = 'map-sdk-set-timeline-interval'
    SET_TIMELINE_SPEED = 'map-sdk-set-timeline-speed'
    SET_VIEW_STATE = 'map-sdk-set-view-state'
    TIMELINE_INTERVAL_CHANGED = 'map-sdk-timeline-interval-changed'
    TOGGLE_TIMELINE_ANIMATION = 'map-sdk-toggle-timeline-animation'
    TOGGLE_TIMELINE_VISIBILITY = 'map-sdk-toggle-timeline-visibility'


class LayerType(str, Enum):
    POINT = 'point'
    ARC = 'arc'
    LINE = 'line'
    GRID = 'grid'
    HEXAGON = 'hexagon'
    GEOJSON = 'geojson'
    CLUSTER = 'cluster'
    ICON = 'icon'
    HEATMAP = 'heatmap'
    HEXAGONID = 'hexagonId'
    _3D = '3D'
    TRIP = 'trip'
    S2 = 's2'
