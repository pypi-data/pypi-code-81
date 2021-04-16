# coding: utf-8

__all__ = ['StreamingWebSocket', 'StreamingWebSocketDataSet']

import json
import logging
import random
import time

import zope.event

from .websocket_server import WebSocket, SimpleWebSocketServer


def response_to_json_str(response):
    fields = response.get('Fields')
    if fields:
        fields['Timestamp'] = time.time()
    return json.dumps([response])


class StreamingWebSocket(WebSocket):

    def __init__(self, server, sock, address, config):
        super().__init__(server, sock, address)
        self.config = config or {}
        self.update_response_number = self.config.get("update_response_number", 1) - 1
        if self.update_response_number < 0:
            self.update_response_number = 0
        self.fields = self.config.get("fields")
        self.update_message = None
        server_data = SimpleWebSocketServer.get_server_data()
        scenario = SimpleWebSocketServer.get_scenario()
        self.scenario_data = server_data.get(scenario)

    def get_data_from_scenario(self, item_name):
        data = self.scenario_data.get(item_name)

        if not data and not self.config.get('is_mock_data_item'):
            return None
        elif data and self.config.get('is_mock_data_item'):
            return self.scenario_data.get('__mock__')
        elif not data and self.config.get('is_mock_data_item'):
            return self.scenario_data.get('__mock__')

        return data

    def handleMessage(self):
        request = json.loads(self.data)
        request_domain = request.get("Domain")

        if request_domain == 'Login':
            self.process_login_request(request)

        elif request_domain is None or request_domain == 'MarketPrice':
            request_type = request.get("Type")

            if request_type is None:
                self.process_refresh_request(request)
                self.process_subscribe_request(request)
            elif request_type == "Close":
                self.process_close_request(request)

    def process_login_request(self, request):
        login_response = self.scenario_data.get("login_response")
        login_response["ID"] = request.get('ID')
        self.sendMessage(response_to_json_str(login_response))

    def process_refresh_request(self, request):
        logging.info(f'---> request = {request}')

        request_id = request.get('ID')

        request_key = request.get('Key')
        name_ = request_key.get('Name')
        service = request_key.get('Service')
        scenario_data_item = self.get_data_from_scenario(name_)

        if not scenario_data_item:
            logging.warning(f"[WARN] process_refresh_request: {name_} item doesn't have in scenario data.")
            return

        refresh_response = scenario_data_item.get("refresh_response", {})

        if self.fields:
            refresh_response['Fields'] = self.fields

        refresh_response["ID"] = request_id

        if "Key" in refresh_response:
            key = refresh_response.get("Key")

            if "Name" in key:
                key["Name"] = name_

            if "Service" in key:
                key["Service"] = service

        logging.info(f'<--- refresh_response = {refresh_response}')
        self.sendMessage(response_to_json_str(refresh_response))

    def process_subscribe_request(self, request):
        request_id = request.get('ID')

        request_key = request.get('Key')
        name_ = request_key.get('Name')
        service = request_key.get('Service')

        request_response = self.scenario_data.get("request_response")
        request_response["ID"] = request_id

        if "Key" in request_response:
            key = request_response.get("Key")

            if "Name" in key:
                key["Name"] = name_

            if "Service" in key:
                key["Service"] = service

        if "Fields" in request_response:
            fields = request_response.get("Fields")

            if "ACVOL_1" in fields:
                fields["ACVOL_1"] = random.randint(10000, 100000)

            if "ASK" in fields:
                fields["ASK"] = random.randint(-100, 100)

            if "ASKSIZE" in fields:
                fields["ASKSIZE"] = random.randint(1, 100)

            if "BID" in fields:
                fields["BID"] = random.randint(-100, 100)

            if "BIDSIZE" in fields:
                fields["BIDSIZE"] = random.randint(1, 100)

            if "VOLUME" in fields:
                fields["VOLUME"] = random.randint(100, 1000)

        self.sendMessage(response_to_json_str(request_response))

        if "Fields" in request_response:
            # prepare next message to be sent within a timer
            update_message = self.scenario_data.get("update_message")
            update_message["ID"] = request_id
            key = update_message.get('Key')
            key['Name'] = name_
            key['Service'] = service

    def process_update_request(self, websocket, response):
        for _ in range(0, 2):
            time.sleep(2)
            fields = response.get('Fields')
            fields['VOLUME'] = random.randint(10000, 100000)
            fields['ACVOL_1'] += fields['VOLUME']
            fields['ASK'] = random.randint(-100, 100)
            fields['ASKSIZE'] = random.randint(1, 100)
            fields['BID'] = random.randint(-100, 100)
            fields['BIDSIZE'] = random.randint(1, 100)
            fields['Timestamp'] = time.time()
            response['Type'] = 'Update'
            response['UpdateType'] = 'Quote'

            websocket.sendMessage(response_to_json_str(response))

    def process_close_request(self, response):
        logging.info(f'<--- close_response = {response}')
        self.closed = True


class StreamingWebSocketDataSet(StreamingWebSocket):
    """ this is a class designed for streaming data set via web socket """

    def process_login_request(self, request):
        login_response = self.scenario_data.get("login_response")
        login_response["ID"] = request.get('ID')
        logging.info(f'---> request = {request}')
        logging.info(f'<--- login_response = {login_response}')
        self.sendMessage(response_to_json_str(login_response))

    def process_subscribe_request(self, request):
        logging.info(f'---> request = {request}')

        id_ = request.get('ID')
        request_key = request.get('Key')
        name_ = request_key.get('Name')
        service = request_key.get('Service')
        scenario_data_item = self.get_data_from_scenario(name_)

        if not scenario_data_item:
            logging.warning(f"[WARN] process_subscribe_request: {name_} item doesn't have in scenario data.")
            return

        request_response = scenario_data_item.get("request_response")

        if self.fields:
            request_response['Fields'] = self.fields

        request_response["ID"] = id_

        if "Key" in request_response:
            key = request_response["Key"]

            if "Name" in key:
                key["Name"] = name_

            if "Service" in key:
                key["Service"] = service

        logging.info(f'<--- subscribe_response = {request_response}')
        self.sendMessage(response_to_json_str(request_response))

        if "Fields" in request_response:
            update_message = scenario_data_item.get("update_message")

            if self.fields:
                update_message['Fields'] = self.fields

            update_message["ID"] = id_
            key = update_message.get('Key')
            key['Name'] = name_
            key['Service'] = service

            self.update_message = update_message
            zope.event.subscribers.append(self._on_sent_event_handler)

    def _on_sent_event_handler(self, event):
        if not event == 'sent':
            return

        if self.update_response_number == 0 or self.closed:
            zope.event.subscribers.remove(self._on_sent_event_handler)
            return

        self.update_response_number -= 1
        self.process_update_request(self, self.update_message)

    def process_update_request(self, websocket, response):
        if not self.closed:
            logging.info(f'<--- update_response = {response}')
            websocket.sendMessage(response_to_json_str(response))
