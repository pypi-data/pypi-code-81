import asyncio
import json
import logging
from logging import ERROR
from pprint import pprint
from threading import Thread
from . import http_server
import refinitiv.dataplatform as rdp
from . import websocket_server

websocket_server_address = ('127.0.0.1', 9001)
http_server_address = ('127.0.0.1', 10015)

http_t = None
ws_server_inst = None
http_server_inst = None

monkey_patch = None


def run(host, port, config=None):
    global monkey_patch

    monkey_patch = rdp.core.PlatformSession._get_rdp_url_root
    rdp.core.PlatformSession._get_rdp_url_root = lambda: u'http://{}:{}'.format(*http_server_address)

    try:
        monkey_patch = rdp.core.PlatformSession._get_rdp_url_root
        rdp.core.PlatformSession._get_rdp_url_root = lambda: u'http://{}:{}'.format(*http_server_address)

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(run_async(host, port, config))
        finally:
            loop.close()

    except Exception as e:
        if config:
            config['error'] = e


async def run_async(host, port, config=None):
    global http_t, ws_server_inst, http_server_inst

    config = config or {}
    #
    #
    ws_server_inst = websocket_server.SimpleWebSocketServer(
        host,
        port,
        websocket_server.StreamingWebSocketDataSet,
        config=config
        )
    ws_server_inst.set_scenario(config.get('socket_scenario', ''))

    task = asyncio.create_task(ws_server_inst.serveforever())

    #
    #
    if config.get("run_http_server"):
        http_server_inst = http_server.RdpHttpServer(
            http_server_address,
            mock_server_data_filename='mock_server_search_data_set.json'
            )
        http_server_inst.set_scenario(config.get('http_scenario', ''))

        http_t = Thread(target=http_server_inst.serve_forever)
        http_t.start()

    config['ready'] = True
    await asyncio.gather(task)


def set_scenario(ws_scenario="", http_scenario=""):
    if ws_scenario:
        ws_server_inst.set_scenario(ws_scenario)

    if http_server_inst:
        http_server_inst.set_scenario(http_scenario)


def stop():
    global http_t, ws_server_inst, http_server_inst, monkey_patch

    if monkey_patch:
        rdp.core.PlatformSession._get_rdp_url_root = monkey_patch
        monkey_patch = None

    ws_server_inst.close()
    http_server_inst and http_server_inst.shutdown()

    http_t and http_t.join()


if __name__ == '__main__':
    with open('./fields.json') as f:
        json_data = json.loads(f.read())

    logging.basicConfig(format="%(levelname)s %(message)s", level=ERROR)

    config_type = 'large_100'

    pprint("Start serve, config:")

    cfg = None
    for c in json_data:
        if c.get('type') == config_type:
            cfg = c

    cfg['update_response_number'] = 1
    cfg['socket_scenario'] = 'streaming_prices'
    cfg['http_scenario'] = 'simple_lookup'
    cfg['is_mock_data_item'] = True
    cfg['data_filename'] = './streaming_pricing_data.json'

    pprint(cfg)
    pprint(f'fields len={len(cfg.get("fields", {}).values())}')
    pprint(f'websocket_server_address={websocket_server_address}')
    run(*websocket_server_address, cfg)
