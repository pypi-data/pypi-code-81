import asyncio
import json
import logging
import time

from pyweatherflowudp.aioudp import open_local_endpoint
from pyweatherflowudp.const import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEVICE_UPDATE_INTERVAL_SECONDS,
    EVENT_AIR_DATA,
    EVENT_HUB_STATUS,
    EVENT_RAPID_WIND,
    EVENT_SKY_DATA,
    EVENT_TEMPEST_DATA,
    PROCESSED_EVENT_EMPTY,
    SOCKET_CHECK_INTERVAL_SECONDS,
    UNIT_SYSTEM_METRIC,
)
from pyweatherflowudp.data import (
    WeatherflowStationStateMachine,
    station_update_from_udp_frames,
)

_LOGGER = logging.getLogger(__name__)


class WeatherFlowListner:
    """Updates device states and attributes."""

    def __init__(
        self, station_id: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, unit_system: str = UNIT_SYSTEM_METRIC
    ):
        self._station_id = station_id
        self._host = host
        self._port = port
        self._unit_system = unit_system

        self._last_device_update_time = 0
        self._last_udpsocket_check = 0
        self._station_state_machine = WeatherflowStationStateMachine()

        self._processed_data = {}
        self.last_update_id = None

        self.udp_connection = None
        self.udp_task = None
        self._udp_subscriptions = []
        self._is_first_update = True
        self._running = True

    async def update(self, force_update=False) -> dict:
        """Updates the status of devices."""

        if self._is_first_update:
            await self._get_device_list()

        await self.async_connect_socket()

        if self.udp_connection:
            _LOGGER.debug("Return data if updated by socket.")
            return self._processed_data

    async def async_connect_socket(self):
        """Connect the UDP Socket."""
        if self.udp_connection is not None:
            return

        if self.udp_task is not None:
            try:
                self.udp_task.cancel()
                self.udp_connection = None
            except Exception:
                _LOGGER.exception("Could not cancel udp_task")
        self.udp_task = asyncio.ensure_future(self._setup_socketreader())

    async def async_disconnect_socket(self):
        """Disconnect the websocket."""
        if self.udp_connection is None:
            return
        self._running = False
        await asyncio.sleep(2)

    async def _get_device_list(self) -> None:
        """Get Initialize the data array."""
        if self._is_first_update:
            self._update_station(self._station_id, PROCESSED_EVENT_EMPTY)
            self._station_state_machine.add(self._station_id, PROCESSED_EVENT_EMPTY)
        self._is_first_update = False

    async def _setup_socketreader(self):
        """Setup the UDP Socket Listner."""
        self.udp_connection = await open_local_endpoint(
            host=self._host, port=self._port
        )

        try:
            while self._running and not self.udp_connection.closed:
                try:
                    data, (host, port) = await self.udp_connection.receive()
                    if data is not None:
                        json_response = json.loads(data.decode("utf-8"))
                        self._process_message(json_response)
                    else:
                        break
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception("Error processing websocket message")
                    return
        finally:
            _LOGGER.debug("Closing connection")
            await self.udp_connection.drain()
            self.udp_connection.close()
            self.udp_connection = None

    def _process_message(self, msg):
        """Process the UDP message."""
        msg_type = msg.get("type")
        if msg_type is not None:
            data_json = {}
            try:
                if msg_type in EVENT_HUB_STATUS:
                    data_json = {
                        "event_type": msg_type,
                        "hub_firmware_revision": msg["firmware_revision"],
                        "hub_uptime": msg["uptime"],
                        "hub_rssi": msg["rssi"],
                    }
                if msg_type in EVENT_RAPID_WIND:
                    obs = msg.get("ob")
                    data_json = {
                        "event_type": msg_type,
                        "time_epoch_rapid_wind": obs[0],
                        "wind_speed": obs[1],
                        "wind_bearing": obs[2],
                    }
                if msg_type in EVENT_SKY_DATA:
                    obs = msg["obs"][0]
                    data_json = {
                        "event_type": msg_type,
                        "time_epoch_sky": obs[0],
                        "illuminance": obs[1],
                        "uv": obs[2],
                        "rain_accumulated": obs[3],
                        "wind_lull": obs[4],
                        "wind_avg": obs[5],
                        "wind_gust": obs[6],
                        "wind_bearing": obs[7],
                        "battery_sky": obs[8],
                        "solar_radiation": obs[10],
                        "local_day_rain_accumulation": obs[11],
                        "precipitation_type": obs[12],
                    }
                if msg_type in EVENT_AIR_DATA:
                    obs = msg["obs"][0]
                    data_json = {
                        "event_type": msg_type,
                        "time_epoch_air": obs[0],
                        "station_pressure": obs[1],
                        "air_temperature": obs[2],
                        "relative_humidity": obs[3],
                        "lightning_strike_count": obs[4],
                        "lightning_strike_avg_distance": obs[5],
                        "battery_air": obs[6],
                    }
                if msg_type in EVENT_TEMPEST_DATA:
                    obs = msg["obs"][0]
                    data_json = {
                        "event_type": msg_type,
                        "time_epoch_tempest": obs[0],
                        "wind_lull": obs[1],
                        "wind_avg": obs[2],
                        "wind_gust": obs[3],
                        "wind_bearing": obs[4],
                        "station_pressure": obs[6],
                        "air_temperature": obs[7],
                        "relative_humidity": obs[8],
                        "illuminance": obs[9],
                        "uv": obs[10],
                        "solar_radiation": obs[11],
                        "local_day_rain_accumulation": obs[12],
                        "precipitation_type": obs[13],
                        "lightning_strike_count": obs[14],
                        "lightning_strike_avg_distance": obs[15],
                        "battery_tempest": obs[16],
                    }
            except Exception as err:
                _LOGGER.debug("Error occured processing data: %s", err)
                return

            # _LOGGER.debug("PROCESSED DATA: %s", data_json)

            if len(data_json) > 0:
                station_id, processed_station = station_update_from_udp_frames(
                    self._station_state_machine, self._station_id, self._unit_system, data_json
                )
                if station_id is None:
                    return

                processed_station.update(data_json)
                self.fire_event(self._station_id, processed_station)
            else:
                _LOGGER.debug("IGNORING TYPE: %s", msg_type)

    def subscribe_udpsocket(self, ws_callback):
        """Subscribe to udpsockets events.

        Returns a callback that will unsubscribe.
        """

        def _unsub_callback():
            self._udp_subscriptions.remove(ws_callback)

        _LOGGER.debug("Adding subscription: %s", ws_callback)
        self._udp_subscriptions.append(ws_callback)
        return _unsub_callback

    def fire_event(self, station_id, processed_event):
        """Callback and event to the subscribers and update data."""
        self._update_station(station_id, processed_event)

        for subscriber in self._udp_subscriptions:
            subscriber({station_id: self._processed_data[station_id]})

    def _update_station(self, station_id, processed_update):
        """Update internal state of a station."""
        self._processed_data.setdefault(station_id, {}).update(processed_update)
