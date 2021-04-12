import json
from asyncio import Future
from typing import Any, Callable, Dict, List, Optional, Type, Union
from uuid import UUID

from deprecated import deprecated
from ipywidgets import DOMWidget, Widget
from pydantic import BaseModel
from traitlets import Int, Unicode

from . import models
from ._frontend import module_name, module_version
from .models import Action


class UnfoldedMap(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('UnfoldedMapModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('UnfoldedMapView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode('Hello from Jupyter').tag(sync=True)

    # TODO: support all of MapOptions arguments?
    mapUrl = Unicode('').tag(sync=True)
    mapUUID = Unicode('').tag(sync=True)
    # TODO: JS Map SDK doesn't yet support 100%
    # width = Any("100%").tag(sync=True)
    height = Int(600).tag(sync=True)

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        # Register callback for receiving messages
        self.on_msg(self._receive_message)

        # Mapping from message id to related future
        self.futures: Dict[str, Dict] = {}

    def _send_message(self, message: Action) -> None:
        """Send message to JS

        TODO: should this optionally poll for a response synchronously?
        TODO: update to handle sending binary buffers
        """
        # In order to properly serialize the Pydantic model to a dict, this
        # serializes to JSON and then loads it back as a dict. Currently,
        # exporting a Pydantic model to a dict does not make the contained
        # objects serializable. (https://stackoverflow.com/q/65622045). This
        # means that later calling `json.dumps` on this dict will fail.
        # On the other hand, ipywidgets requires dict input so it can do its own
        # JSON serialization.
        # https://github.com/jupyter-widgets/ipywidgets/blob/24628f006c8a468994eba7a6e964fe619c992267/ipywidgets/widgets/widget.py#L516-L526
        msg = json.loads(message.json())
        self.send(msg)
        # print('sent message:', msg)

    def _create_future(
            self, message: Action, response_callback: Callable) -> Future:
        future: Future = Future()
        self.futures[str(message.message_id)] = {
            'future': future,
            'response_callback': response_callback}
        return future

    # TODO: check type of `buffers`
    def _receive_message(
            self, widget: Widget, content: Dict, buffers: List[bytes]) -> None:
        """Receive message from JS
        """
        # pylint:disable=unused-argument
        message_id = content['messageId']
        data = content['data']
        self.received_message = content

        future_ref = self.futures.pop(message_id)
        response_callback = future_ref['response_callback']
        self.future_ref = future_ref
        future_ref['future'].set_result(response_callback(data))

    # TODO generic typing?
    # TODO: error responses have a data object of type {message: '...'}
    @staticmethod
    def _create_iterable_response_callback(
        response_class: Type[BaseModel]
    ) -> Callable[[List[Dict]], List[BaseModel]]:
        def response_callback(resp: List[Dict]) -> List[BaseModel]:
            if resp:
                try:
                    return [response_class(**item) for item in resp]
                except:
                    pass

            return []

        return response_callback

    # TODO generic typing?
    @staticmethod
    def _create_response_callback(
        response_class: Type[BaseModel]
    ) -> Callable[[Dict], Optional[BaseModel]]:
        def response_callback(resp: Dict) -> Optional[BaseModel]:
            if resp:
                try:
                    return response_class(**resp)
                except:
                    pass

            # TODO: what to return as default?
            return None

        return response_callback

    @staticmethod
    def get_map_url(map_uuid: Union[UUID, str]) -> str:
        """Get the full URL for the published map

        Args:
            map_uuid - Universally unique identifier (UUID) for the published map

        Returns:
            (string): Full URL for the published map
        """
        return f'https://studio.unfolded.ai/public/{map_uuid}'

    # TODO: return future types
    def set_view_state(self, view_state: models.ViewState) -> Future:
        """Set the map view state

        Args:
            view_state: ViewState model instance or dict with `longitude`, `latitude`, and `zoom` keys.
        """
        action = models.SetViewState(view_state=view_state)
        self._send_message(action)
        response_callback = self._create_response_callback(models.ViewState)
        return self._create_future(action, response_callback)

    def get_layers(self) -> Future:
        """Get all layers for the provided map instance
        """
        action = models.GetLayers()
        self._send_message(action)
        response_callback = self._create_iterable_response_callback(
            models.Layer)
        return self._create_future(action, response_callback)

    def set_layer_visibility(self, layer_id: str, is_visible: bool) -> Future:
        """Set visibility of specified layer

        Args:
            layer_id: layer id
            is_visible: If True, make layer visible, else hide the layer
        """
        action = models.SetLayerVisibility(
            layer_id=layer_id, is_visible=is_visible)
        self._send_message(action)
        response_callback = self._create_response_callback(models.Layer)
        return self._create_future(action, response_callback)

    def set_theme(self, theme: str) -> None:
        """Set the map theme to 'light' or 'dark'

        Args:
            theme: theme name, either 'light' or 'dark'
        """
        action = models.SetTheme(theme=theme)
        self._send_message(action)

    def get_timeline_info(self, idx: str) -> Future:
        """Get information object for the timeline filter

        Args:
            idx: Index of the timeline filter
        """
        action = models.GetTimelineInfo(idx=idx)
        self._send_message(action)
        response_callback = self._create_response_callback(models.TimelineInfo)
        return self._create_future(action, response_callback)

    @deprecated(reason="Use `setTimelineConfig` instead")
    def toggle_timeline_animation(self, idx: str) -> None:
        """Toggle timeline filter animation

        Args:
            idx: Index of the timeline filter
        """
        action = models.ToggleTimelineAnimation(idx=idx)
        self._send_message(action)

    @deprecated(reason="Use `setTimelineConfig` instead")
    def toggle_timeline_visibility(self, idx: str) -> None:
        """Toggle timeline filter visibility

        Args:
            idx: Index of the timeline filter
        """
        action = models.ToggleTimelineVisibility(idx=idx)
        self._send_message(action)

    @deprecated(reason="Use `setTimelineConfig` instead")
    def set_timeline_interval(
            self, idx: str, start_time: float, end_time: float) -> None:
        """Set current timeline filter interval

        Args:
            idx: Index of the timeline filter
            start_time: Unix Time in milliseconds for the start of the interval
            end_time: Unix Time in milliseconds for the end of the interval
        """
        action = models.SetTimelineInterval(
            idx=idx, start_time=start_time, end_time=end_time)
        self._send_message(action)

    @deprecated(reason="Use `setTimelineConfig` instead")
    def set_timeline_animation_speed(self, idx: str, speed: float) -> None:
        """Set current time filter animation speed

        Args:
            idx: Index of the timeline filter
            speed: speed multiplier
        """
        action = models.SetTimelineAnimationSpeed(idx=idx, speed=speed)
        self._send_message(action)

    def set_timeline_config(self, config: models.TimelineConfig) -> None:
        """Set timeline configuration

        Args:
            config: Timeline configuration object
        """
        action = models.SetTimelineConfig(config=config)
        self._send_message(action)

    def refresh_map_data(self) -> None:
        """Refresh map data sources
        """
        action = models.RefreshMapData()
        self._send_message(action)

    def get_layer_timeline_info(self) -> Future:
        """Get information object for the layer timeline control
        """
        action = models.GetLayerTimelineInfo()
        self._send_message(action)
        response_callback = self._create_response_callback(
            models.LayerTimelineInfo)
        return self._create_future(action, response_callback)

    def set_layer_timeline_config(
            self, config: models.LayerTimelineConfig) -> Future:
        """Set layer timeline configuration

        Args:
            config: Layer timeline configuration object
        """
        action = models.SetLayerTimelineConfig(config=config)
        self._send_message(action)
        response_callback = self._create_response_callback(
            models.LayerTimelineConfig)
        return self._create_future(action, response_callback)

    def _add_tileset(self, tileset: models.Tileset) -> None:
        """Create a new tileset

        Args:
            tileset: tileset configuration
        """
        action = models.AddTileset(tileset=tileset)
        self._send_message(action)

    def add_dataset(self, uuid: Union[str, UUID]) -> Future:
        """Add a dataset to the map.

        Args:
            uuid: Dataset UUID

        Inputs:
        - map
        - id - Dataset id
        """
        action = models.AddDataset(uuid=uuid)
        self._send_message(action)
        response_callback = self._create_response_callback(
            models.AddDatasetResponse)
        return self._create_future(action, response_callback)

    def remove_dataset(self, uuid: Union[str, UUID]) -> Future:
        """Remove the dataset with the specified UUID from the map.

        Args:
            uuid: Dataset UUID
        """
        action = models.RemoveDataset(uuid=uuid)
        self._send_message(action)
        response_callback = self._create_response_callback(
            models.RemoveDatasetResponse)
        return self._create_future(action, response_callback)

    def add_layer(self, layer: models.LayerSpec) -> None:
        """Add a layer to the map

        Args:
            layer: Layer configuration
        """
        action = models.AddLayer(layer=layer)
        self._send_message(action)

    def remove_layer(self, layer_id: str) -> None:
        """Remove layer from the map

        Args:
            id: Layer id
        """
        action = models.RemoveLayer(id=layer_id)
        self._send_message(action)
