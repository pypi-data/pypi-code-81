import websockets
import asyncio
import json


class Eye:

    def __init__(self, port, on_open, on_message, on_error, on_close):

        self.on_open = on_open
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close

        start_server = websockets.serve(self.connection, '0.0.0.0', port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def connection(self, ws, path):

        await self.on_open(ws)

        while True:

            try:

                resp = await ws.recv()
                msg = json.loads(resp)
                await self.on_message(ws, msg)


            except websockets.exceptions.ConnectionClosedError as err:
                await self.on_error(ws, err)
                break

            except websockets.exceptions.ConnectionClosedOK as err:
                await self.on_error(ws, err)
                break

            except Exception as err:
                await self.on_error(ws, err)

        await self.on_close(ws)
