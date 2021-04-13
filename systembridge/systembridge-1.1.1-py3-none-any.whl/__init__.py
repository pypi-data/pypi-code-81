"""Bridge: Init"""
from systembridge.objects.open.payload import OpenPayload
from aiohttp import ClientResponse
from typing import Any, List, Optional

from .client import BridgeClient
from .objects.audio import Audio
from .objects.audio.delete import AudioDeleteResponse
from .objects.audio.post import AudioPostPayload, AudioPostResponse
from .objects.audio.put import AudioPutPayload, AudioPutResponse
from .objects.base import BridgeBase
from .objects.battery import Battery
from .objects.bluetooth import Bluetooth
from .objects.command.payload import CommandPayload
from .objects.command.response import CommandResponse
from .objects.cpu import Cpu
from .objects.display import Display
from .objects.display.put import DisplayPutPayload
from .objects.filesystem import Filesystem
from .objects.graphics import Graphics
from .objects.information import Information
from .objects.memory import Memory
from .objects.network import Network
from .objects.os import Os
from .objects.processes import Processes
from .objects.system import System
from .objects.video.delete import VideoDeleteResponse
from .objects.video.post import VideoPostPayload, VideoPostResponse
from .objects.video.put import VideoPutResponse

BASE_HEADERS = {"Accept": "application/json"}


class Bridge(BridgeBase):
    """Main class for Bridge."""

    def __init__(self, client: BridgeClient, base_url: str, api_key: str) -> None:
        """Initialize the token manager class."""
        self._client = client
        self._base_url = base_url
        self._api_key = api_key
        self._audio: List[Audio] = []
        self._battery: Battery = {}
        self._bluetooth: Bluetooth = {}
        self._cpu: Cpu = {}
        self._display: Display = {}
        self._filesystem: Filesystem = {}
        self._graphics: Graphics = {}
        self._information: Information = {}
        self._memory: Memory = {}
        self._os: Os = {}
        self._processes: Processes = {}
        self._system: System = {}

    @property
    def audio(self) -> List[Audio]:
        return self._audio

    @property
    def battery(self) -> Battery:
        return self._battery

    @property
    def bluetooth(self) -> Bluetooth:
        return self._bluetooth

    @property
    def cpu(self) -> Cpu:
        return self._cpu

    @property
    def display(self) -> Display:
        return self._display

    @property
    def filesystem(self) -> Filesystem:
        return self._filesystem

    @property
    def graphics(self) -> Graphics:
        return self._graphics

    @property
    def information(self) -> Information:
        return self._information

    @property
    def memory(self) -> Memory:
        return self._memory

    @property
    def network(self) -> Network:
        return self._network

    @property
    def os(self) -> Os:
        return self._os

    @property
    def processes(self) -> Processes:
        return self._processes

    @property
    def system(self) -> System:
        return self._system

    async def async_post(self, path: str, payload: Optional[Any]) -> Any:
        """Generic Delete"""
        response: ClientResponse = await self._client.post(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
            json=payload,
        )
        return await response.json()

    async def async_get(self, path: str) -> Any:
        """Generic get"""
        response: ClientResponse = await self._client.get(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
        )
        return await response.json()

    async def async_post(self, path: str, payload: Any) -> Any:
        """Generic post"""
        response: ClientResponse = await self._client.post(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
            json=payload,
        )
        return await response.json()

    async def async_put(self, path: str, payload: Any) -> Any:
        """Generic put"""
        response: ClientResponse = await self._client.post(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
            json=payload,
        )
        return await response.json()

    async def async_stop_audio_player(self) -> AudioDeleteResponse:
        """Stop audio player"""
        return AudioDeleteResponse(await self.async_delete("/audio"))

    async def async_create_audio_player(
        self, payload: AudioPostPayload
    ) -> AudioPostResponse:
        """Create audio player"""
        return AudioPostResponse(await self.async_post("/audio", payload))

    async def async_get_audio(self) -> List[Audio]:
        """Get audio information"""
        self._audio = [Audio(audio) for audio in await self.async_get("/audio") or []]
        return self._audio

    async def async_update_audio(
        self, id: str, payload: AudioPutPayload
    ) -> AudioPutResponse:
        """Update audio"""
        return AudioPutResponse(await self.async_post(f"/audio/{id}", payload))

    async def async_get_battery(self) -> Battery:
        """Get battery information"""
        self._battery = Battery(await self.async_get("/battery"))
        return self._battery

    async def async_get_bluetooth(self) -> Bluetooth:
        """Get bluetooth information"""
        self._bluetooth = Bluetooth(await self.async_get("/bluetooth"))
        return self._bluetooth

    async def async_send_command(self, payload: CommandPayload) -> CommandResponse:
        """Send command"""
        return CommandResponse(await self.async_post("/command", payload))

    async def async_get_cpu(self) -> Cpu:
        """Get cpu information"""
        self._cpu = Cpu(await self.async_get("/cpu"))
        return self._cpu

    async def async_get_display(self) -> Cpu:
        """Get display information"""
        self._display = Display(await self.async_get("/display"))
        return self._display

    async def async_update_display(
        self, id: str, payload: DisplayPutPayload
    ) -> Display:
        """Update display"""
        return AudioPutResponse(await self.async_post(f"/display/{id}", payload))

    async def async_get_filesystem(self) -> Filesystem:
        """Get filesystem information"""
        self._filesystem = Filesystem(await self.async_get("/filesystem"))
        return self._filesystem

    async def async_get_graphics(self) -> Graphics:
        """Get graphics information"""
        self._graphics = Graphics(await self.async_get("/graphics"))
        return self._graphics

    async def async_get_information(self) -> Information:
        """Get information"""
        self._information = Information(await self.async_get("/information"))
        return self._information

    async def async_get_memory(self) -> Memory:
        """Get memory information"""
        self._memory = Memory(await self.async_get("/memory"))
        return self._memory

    async def async_get_network(self) -> Network:
        """Get network information"""
        self._network = Network(await self.async_get("/network"))
        return self._network

    async def async_open(self, payload: OpenPayload) -> OpenPayload:
        """Send command"""
        return OpenPayload(await self.async_post("/open", payload))

    async def async_get_os(self) -> Os:
        """Get os information"""
        self._os = Os(await self.async_get("/os"))
        return self._os

    async def async_get_processes(self) -> Processes:
        """Get processes information"""
        self._processes = Processes(await self.async_get("/processes"))
        return self._processes

    async def async_get_system(self) -> System:
        """Get system information"""
        self._system = System(await self.async_get("/system"))
        return self._system

    async def async_stop_video_player(self) -> VideoDeleteResponse:
        """Stop video player"""
        return VideoDeleteResponse(await self.async_delete("/video"))

    async def async_create_video_player(
        self, payload: VideoPostPayload
    ) -> VideoPostResponse:
        """Create video player"""
        return VideoPostResponse(await self.async_post("/video", payload))

    async def async_update_video(self, id: str) -> VideoPutResponse:
        """Update video"""
        return VideoPutResponse(await self.async_post(f"/video/{id}"))
