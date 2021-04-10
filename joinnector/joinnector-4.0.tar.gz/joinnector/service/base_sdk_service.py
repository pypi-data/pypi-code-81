# pylint: disable=dangerous-default-value
# pylint: disable=line-too-long

import base64
import uuid

from joinnector.wrapper.request_wrapper import request_wrapper

from joinnector.helper.collection_helper import CollectioHelper
from joinnector.helper.constant_helper import ConstantHelper


class BaseSDKService(object):
    def __init__(self, name):
        self.name = name

    def get_infos(self, endpoint):
        apimapopts = ConstantHelper.get_setting_constant().API_MAP.get(self.name)

        base_url = ConstantHelper.get_setting_constant().API_PROD_BASE_URL if request_wrapper.get_wrapper(
        ).mode is "prod" else ConstantHelper.get_setting_constant().API_DEV_BASE_URL

        url = CollectioHelper.process_key_join(value=[base_url, "/api/open", endpoint], separator="")
        headers = { **ConstantHelper.get_setting_constant().API_BASE_HEADER}
        params = {}

        return request_wrapper.get_wrapper().process_axios_get(
            url=url, headers=headers, params=params)

    def create(self, payload, action="create"):
        apimapopts = ConstantHelper.get_setting_constant().API_MAP.get(self.name)

        base_url = ConstantHelper.get_setting_constant().API_PROD_BASE_URL if request_wrapper.get_wrapper(
        ).mode is "prod" else ConstantHelper.get_setting_constant().API_DEV_BASE_URL

        url = CollectioHelper.process_key_join(value=[base_url, apimapopts.get(
            action).get("prefix"), apimapopts.get(action).get("endpoint")], separator="")
        headers = { **ConstantHelper.get_setting_constant().API_BASE_HEADER}
        params = {}
        attributes = payload

        token = "%(name)s:%(pass)s" % {
            "name": request_wrapper.get_wrapper().key, "pass": request_wrapper.get_wrapper().secret}
        headers.update({"authorization": "Basic " +
                        base64.b64encode(token.encode("utf-8")).decode('ascii')})

        headers.update(
            {"x-apikey": request_wrapper.get_wrapper().key})

        return request_wrapper.get_wrapper().process_axios_post(
            url=url, headers=headers, params=params, data=attributes)

    def get(self, by_id, action="get"):
        apimapopts = ConstantHelper.get_setting_constant().API_MAP.get(self.name)

        base_url = ConstantHelper.get_setting_constant().API_PROD_BASE_URL if request_wrapper.get_wrapper(
        ).mode is "prod" else ConstantHelper.get_setting_constant().API_DEV_BASE_URL

        url = CollectioHelper.process_key_join(value=[base_url, apimapopts.get(action).get(
            "prefix"), apimapopts.get(action).get("endpoint")], separator="").replace("{id}", by_id)
        headers = { **ConstantHelper.get_setting_constant().API_BASE_HEADER}

        token = "%(name)s:%(pass)s" % {
            "name": request_wrapper.get_wrapper().key, "pass": request_wrapper.get_wrapper().secret}
        headers.update({"authorization": "Basic " +
                        base64.b64encode(token.encode("utf-8")).decode('ascii')})

        headers.update(
            {"x-apikey": request_wrapper.get_wrapper().key})

        return request_wrapper.get_wrapper().process_axios_get(
            url=url, headers=headers, params={})

    def get_by(self, by_key, by_value, swap_id=None, action="get"):
        apimapopts = ConstantHelper.get_setting_constant().API_MAP.get(self.name)

        base_url = ConstantHelper.get_setting_constant().API_PROD_BASE_URL if request_wrapper.get_wrapper(
        ).mode is "prod" else ConstantHelper.get_setting_constant().API_DEV_BASE_URL

        url = CollectioHelper.process_key_join(value=[base_url, apimapopts.get(action).get(
            "prefix"), apimapopts.get(action).get("endpoint")], separator="").replace("{id}", str(uuid.uuid4()))
        headers = { **ConstantHelper.get_setting_constant().API_BASE_HEADER}
        params = {}

        params.update({by_key: by_value})
        if swap_id is not None:
            params.update({"swap_id": swap_id})

        token = "%(name)s:%(pass)s" % {
            "name": request_wrapper.get_wrapper().key, "pass": request_wrapper.get_wrapper().secret}
        headers.update({"authorization": "Basic " +
                        base64.b64encode(token.encode("utf-8")).decode('ascii')})

        headers.update(
            {"x-apikey": request_wrapper.get_wrapper().key})

        headers.update(
            {"content-type": "application/x-www-form-urlencoded"})

        return request_wrapper.get_wrapper().process_axios_get(
            url=url, headers=headers, params=params)

    def save(self, by_id, payload, action="save"):
        apimapopts = ConstantHelper.get_setting_constant().API_MAP.get(self.name)

        base_url = ConstantHelper.get_setting_constant().API_PROD_BASE_URL if request_wrapper.get_wrapper(
        ).mode is "prod" else ConstantHelper.get_setting_constant().API_DEV_BASE_URL

        url = CollectioHelper.process_key_join(value=[base_url, apimapopts.get(action).get(
            "prefix"), apimapopts.get(action).get("endpoint")], separator="").replace("{id}", by_id)
        headers = { **ConstantHelper.get_setting_constant().API_BASE_HEADER}
        attributes = payload

        token = "%(name)s:%(pass)s" % {
            "name": request_wrapper.get_wrapper().key, "pass": request_wrapper.get_wrapper().secret}
        headers.update({"authorization": "Basic " +
                        base64.b64encode(token.encode("utf-8")).decode('ascii')})

        headers.update(
            {"x-apikey": request_wrapper.get_wrapper().key})

        return request_wrapper.get_wrapper().process_axios_put(
            url=url, headers=headers, params={}, data=attributes)

    def delete(self, by_id, action="get"):
        apimapopts = ConstantHelper.get_setting_constant().API_MAP.get(self.name)

        base_url = ConstantHelper.get_setting_constant().API_PROD_BASE_URL if request_wrapper.get_wrapper(
        ).mode is "prod" else ConstantHelper.get_setting_constant().API_DEV_BASE_URL

        url = CollectioHelper.process_key_join(value=[base_url, apimapopts.get(action).get(
            "prefix"), apimapopts.get(action).get("endpoint")], separator="").replace("{id}", by_id)
        headers = { **ConstantHelper.get_setting_constant().API_BASE_HEADER}

        token = "%(name)s:%(pass)s" % {
            "name": request_wrapper.get_wrapper().key, "pass": request_wrapper.get_wrapper().secret}
        headers.update({"authorization": "Basic " +
                        base64.b64encode(token.encode("utf-8")).decode('ascii')})

        headers.update(
            {"x-apikey": request_wrapper.get_wrapper().key})

        return request_wrapper.get_wrapper().process_axios_delete(
            url=url, headers=headers, params={})

    def fetch(self, by_filter={}, action="fetch"):

        apimapopts = ConstantHelper.get_setting_constant().API_MAP.get(self.name)

        base_url = ConstantHelper.get_setting_constant().API_PROD_BASE_URL if request_wrapper.get_wrapper(
        ).mode is "prod" else ConstantHelper.get_setting_constant().API_DEV_BASE_URL

        url = CollectioHelper.process_key_join(value=[base_url, apimapopts.get(
            action).get("prefix"), apimapopts.get(action).get("endpoint")], separator="")
        headers = { **ConstantHelper.get_setting_constant().API_BASE_HEADER}
        params = { "page": 1, "limit": 20, **by_filter }

        token = "%(name)s:%(pass)s" % {
            "name": request_wrapper.get_wrapper().key, "pass": request_wrapper.get_wrapper().secret}
        headers.update({"authorization": "Basic " +
                        base64.b64encode(token.encode("utf-8")).decode('ascii')})

        headers.update(
            {"x-apikey": request_wrapper.get_wrapper().key})

        return request_wrapper.get_wrapper().process_axios_get(
            url=url, headers=headers, params=params)
