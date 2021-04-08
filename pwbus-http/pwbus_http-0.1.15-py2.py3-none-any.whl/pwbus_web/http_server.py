#!/usr/bin/env python3

# PWBus Server Engine for HTTP
#:
#:  maintainer: fabio.szostak@perfweb.com.br | Fri Nov 15 17:58:07 -03 2019

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import importlib
import json
import traceback

from modules.pwbus_core.commons.logging import *
from modules.pwbus_core.engines.engine_dispatch import EngineDispatch
from modules.pwbus_core.engines.engine_registry_loader import RegistryLoader
from modules.pwbus_core.engines.engine_registry import Registry
from modules.pwbus_core.clients.redis_client import RedisClient


# Load registry
registry = RegistryLoader("/app/etc/pwbus_registry.json")
registry.load()

# Start HTTP Server
pwbus_web = Flask(__name__)
CORS(pwbus_web)

# /pwbus/v1/in
#
#
@pwbus_web.route("/pwbus")
def hello():
    return ("<style>A, P{font-family: Sans-Serif, Arial; font-weight: bold}</style><p><img src='' alt='perfweb - pwbus'></p><p>PWBus Server Engine for HTTP 0.0.1</p><p>Develop by <a href='https://perfweb.com.br'>perfweb.com.br</a></p>")


# /pwbus/v1/request
#
#
@pwbus_web.route("/pwbus/v1/request", methods=['POST'])
def http_in():

    # Pwbus-Channel header
    channel_registry = http_channel('out', request)

    if isinstance(channel_registry, Response):
        return channel_registry

    DEBUG = channel_registry['engine.debug']
    if DEBUG:
        log_debug(
            f'👉 @pwbus_web, http_in - Started from [{request.url}] - remote_address [{request.environ["REMOTE_ADDR"]}]')

    try:
        engine_dispatch = EngineDispatch()
        response_flow = engine_dispatch.route(channel_registry, request)

        if not response_flow:
            log_debug('🟥 @pwbus_web, http_in - Failed on receive request message')
            return http_response({}, {"Pwbus-Status-Code": 500, "Pwbus-Info-Message": "Failed on send request message"})
        else:
            log_debug('@pwbus_web, http_in - Flow in response data', response_flow.getResponse())

            if DEBUG:
                log_debug(f'@pwbus_web, http_in - Flow in header [{response_flow.getHeaders()}]')

            if 'Pwbus-Correlation-Id' in response_flow.getHeaders():
                # Get Client Class dynamically
                resource_type = channel_registry["flow.out.resource_type"].lower()
                module_name = f'modules.pwbus_core.clients.{resource_type}_client'
                class_name = f'{resource_type.capitalize()}Client'
                module = importlib.import_module(module_name)
                class_ = getattr(module, class_name)
                client = class_(
                    host=channel_registry["flow.out.host"] if "flow.out.host" in channel_registry else None,
                    port=channel_registry["flow.out.port"] if "flow.out.port" in channel_registry else None
                )

                response = client.get(
                    channel_registry["flow.out.reply_to"],
                    response_flow.getHeadersEntry('Pwbus-Correlation-Id')
                )

                if not response:
                    log_debug('🙏 @pwbus_web, http_in - Request sent successfully')
                    response_flow.setHeadersEntry('Pwbus-Status-Code', 202)
                    response_flow.setHeadersEntry('Pwbus-Info-Message', "Request sent successfully")
                    return http_response({}, response_flow.getHeaders())
                else:
                    response_flow.setHeadersEntry('Pwbus-Status-Code', 200)

                log_debug_success("@pwbus_web, http_in - Response received successfully")

                return http_response(response, {"Pwbus-Status-Code": 200, "Pwbus-Info-Message": "Request received successfully"})

            else:
                if DEBUG:
                    log_debug('@pwbus_web, http_in - Response data', response_flow.getResponse())
                if DEBUG:
                    log_debug_success('@pwbus_web, http_in - Request sent successfully')
                response_flow.setHeadersEntry('Pwbus-Status-Code', 404)
                return http_response(response_flow.getResponse(), response_flow.getHeaders())

    except:
        traceback.print_exc()


# /pwbus/v1/retry
#
#
@pwbus_web.route("/pwbus/v1/retry", methods=['POST'])
def http_out():
    # Pwbus-Channel header
    channel_registry = http_channel('out', request)
    DEBUG = channel_registry['engine.debug']

    if DEBUG:
        log_debug(
            f'👉 @pwbus_web, http_out - Started from [{request.url}] - remote_address [{request.environ["REMOTE_ADDR"]}]')

    if not 'Pwbus-Correlation-Id' in request.headers:
        log_debug('🟥 @pwbus_web, http_out - Invalid request, Pwbus-Correlation-Id not found')
        return http_response({}, {"Pwbus-Status-Code": 400, "Pwbus-Info-Message": "Invalid request, Pwbus-Correlation-Id not found"})

    # Get Client Class dynamically
    resource_type = channel_registry["flow.out.resource_type"].lower()
    module_name = f'modules.pwbus_core.clients.{resource_type}_client'
    class_name = f'{resource_type.capitalize()}Client'
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
    client = class_(
        host=channel_registry["flow.out.host"] if "flow.out.host" in channel_registry else None,
        port=channel_registry["flow.out.port"] if "flow.out.port" in channel_registry else None
    )

    response = client.get(
        channel_registry["flow.out.reply_to"],
        request.headers['Pwbus-Correlation-Id']
    )

    if not response:
        if DEBUG:
            log_debug('👎 @pwbus_web, http_out - Response not found')
        return http_response({}, {"Pwbus-Status-Code": 202, "Pwbus-Info-Message": "Response not found"})

    if DEBUG:
        log_debug_success("@pwbus_web, http_out - Response received successfully")

    return http_response(response, {"Pwbus-Status-Code": 200})


# /pwbus/v1/update - reload and update registry parameters
#
#
@pwbus_web.route("/pwbus/v1/reload", methods=['GET'])
def registry_reload():
    try:
        registry = RegistryLoader()
        registry.load()
        log_debug_success("@pwbus_web, registry_reload - Registry reloaded successfully")
        return http_response({}, {"Pwbus-Status-Code": 200, "Pwbus-Info-Message": "Registry reload successfully"})
    except:
        log_error("🟥 @pwbus_web, registry_reload - Registry reloaded failed")
        return http_response({}, {"Pwbus-Status-Code": 500, "Pwbus-Info-Message": "Registry reload failed, contact administrator"})

# http_channel - verify and retrieve channel parameters
#


def http_channel(origin, request):
    channel = request.headers['Pwbus-Channel']

    if not channel or channel == '':
        return http_response({}, {"Pwbus-Status-Code": 400, "Pwbus-Info-Message": "Pwbus-Channel is invalid"})

    registry = Registry()
    channel_registry = registry.getChannel(channel)
    if channel_registry is None:
        log_debug(f'🟥 @pwbus_web, http_{origin} - Channel not found in registry')
        return http_response({}, {"Pwbus-Status-Code": 404, "Pwbus-Info-Message": "Pwbus-Channel not found in the registry"})

    if not channel_registry['engine.enabled']:
        log_debug(f'🟥 @pwbus_web, http_{origin} - Unavailable task, channel [{channel}] disabled')
        return http_response({}, {"Pwbus-Status-Code": 503, "Pwbus-Info-Message": "Unavailable task, this channel are disabled"})

    return channel_registry

# http_response - send HTTP response
#


def http_response(response, headers=dict(), status=200, mimetype="application/json", content_type="application/json; charset=utf-8"):
    resp = Response(
        response=json.dumps(response),
        status=status
    )
    if isinstance(headers, dict):
        for name, value in headers.items():
            resp.headers[name] = value

    resp.headers["Content-Type"] = content_type
    resp.headers['Access-Control-Expose-Headers'] = 'Pwbus-Status-Code, Pwbus-Correlation-Id'
    return resp


# /pwbus/v1/fake-client-test @@@@@@@@@@@@@@@@@@@(ONLY FOR TESTS) @@@
#
#
@pwbus_web.route("/pwbus/v1/fake-client-test", methods=['POST'])
def http_fake_client():

    log_debug(
        f'@pwbus_web, http_fake_client - Started from [{request.url}] - remote_address [{request.environ["REMOTE_ADDR"]}]')

    request_data = request.json

    log_message_dump("@pwbus_web, http_fake_client", request_data)

    if request_data and 'Pwbus-Transaction' in request_data:
        if request_data['Pwbus-Transaction'] == 'pwbus.pwbus_test_001':
            response = {"status_code": 200, "message": "PWBus test message received ok"}
            log_debug_success('@pwbus_web, http_fake_client - Success')
        else:
            response = {"status_code": 400, "message": "PWBus test message received but transaction_id invalid"}
            log_debug_success('@pwbus_web, http_fake_client - Success but content is not OK')
    else:
        response = {"status_code": 500, "message": "PWBus test message FAILED"}
        log_debug('@pwbus_web, http_fake_client - Failed')

    return jsonify(response), 200
    #
    # /pwbus/v1/fake-client-test @@@@@@@@@@@@@@@@@@@(ONLY FOR TESTS) @@@


def main():
    pwbus_web.run()


# __main__
#
if __name__ == "__main__":
    main()
