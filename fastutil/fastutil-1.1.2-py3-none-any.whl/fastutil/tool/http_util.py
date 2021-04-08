import json
import time
import traceback

import requests
from loguru import logger
from requests.adapters import HTTPAdapter

request_session = requests.Session()
request_session.mount('http://', HTTPAdapter(max_retries=3))
request_session.mount('https://', HTTPAdapter(max_retries=3))


def get_no_exception(url, use_session=True, return_json=True, **kwargs):
    res = None
    try:
        start_time = time.time()
        if use_session:
            res = request_session.get(url, **kwargs)
        else:
            res = requests.get(url, **kwargs)
        logger.info('url:{},kwargs:{},request cost:{}', url, kwargs, time.time() - start_time)

        if res is None:
            logger.warning('url:{},param:{},status:{},response is None', url, kwargs)
            return None
        if res.status_code != 200:
            logger.warning('url:{},param:{},status:{},result:{}', url, kwargs, res.status_code, res.text)
            return None if return_json else res
        if return_json:
            if not res.text:
                logger.warning('url:{},param:{},result text is None', url, kwargs)
                return None
            return res.json()
        return res
    except requests.RequestException:
        logger.warning('url:{},param:{},request warn:{}', url, kwargs, traceback.format_exc(chain=False))
        return {} if return_json else None
    except json.JSONDecodeError:
        res_text = res.text if res else ''
        logger.warning('url:{},param:{},result:{},decode fail', url, kwargs, res_text)
        return {} if return_json else None


def post_no_exception(url, use_session=True, return_json=True, data=None, json_data=None, **kwargs):
    res = None
    try:
        start_time = time.time()
        if use_session:
            res = request_session.post(url, data=data, json=json_data, **kwargs)
        else:
            res = requests.post(url, data=data, json=json_data, **kwargs)
        data = data if data else json_data
        logger.info('url:{},kwargs:{},data:{},request cost:{}', url, kwargs, data,
                    time.time() - start_time)

        if res is None:
            logger.info('url:{},kwargs:{},data:{},response is None', url, kwargs, data)
            return None
        if res.status_code != 200:
            logger.info('url:{},kwargs:{},data:{},result:{}', url, kwargs, data, res.text)
            return None if return_json else res
        if return_json:
            if not res.text:
                logger.info('url:{},kwargs:{},data:{},result text is None', url, kwargs, data)
                return None
            return res.json()
        return res
    except requests.RequestException:
        logger.info('url:{},kwargs:{},data:{},request warn:{}', url, kwargs, data, traceback.format_exc())
        return {} if return_json else None
    except json.JSONDecodeError:
        res_text = res.text if res else ''
        logger.info('url:{},kwargs:{},data:{},result:{}, decode fail', url, kwargs, data, res_text)
        return {} if return_json else None
