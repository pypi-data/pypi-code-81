import websockets
import asyncio
import uuid
import json

class WebSocket:
    WEBSOCKET_ENDPOINT = 'ws://api.upbit.com/websocket/v1'

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.__connect())

    async def __connect(self):
        async with websockets.connect(self.WEBSOCKET_ENDPOINT) as conn:
            self.__conn = conn
            await self.on_connect()
            while True:
                try:
                    data = await self.__conn.recv()
                except websockets.ConnectionClosed:
                    await self.on_disconnect()
                    break
                data_json = json.loads(data)
                await self.on_response(data_json)

    async def send_ping(self):
        await self.__conn.ping()

    async def send_field(self, ticket: str = str(uuid.uuid4()), type_fields: list[dict] = [{'type': 'ticker', 'codes': ['KRW-BTC']}], format: str = 'DEFAULT'):
        field = [
            {
                'ticket': ticket
            },
            {
                'format': format
            }
        ]

        for type_field in type_fields:
            field.append(type_field)

        field_str = json.dumps(field)
        await self.__conn.send(field_str)

    async def on_connect(self):
        pass

    async def on_disconnect(self):
        pass

    async def on_response(self, response: dict):
        pass
