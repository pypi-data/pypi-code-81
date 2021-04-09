import unittest
from bffacilities.socketserver import TcpSocketServer, SocketClient, logger
from bffacilities.utils import changeLoggerLevel
import logging
changeLoggerLevel(logger, logging.DEBUG)
import time
import threading
import asyncio
async def createClient(id):
    client = SocketClient.createTcpClient(("127.0.0.1", 54134))
    try:
        client.connect()
        data = f"{{'name': '{id}'}}"
        while True:
            client.sock.send(data.encode())
            await asyncio.sleep(2) 
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        print("exception:", e)
    print("Client Done ", id)
async def main():
    tasks = []
    for i in range(3):
        tasks.append(createClient(i))
    await asyncio.gather(*tasks)
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

