#!/usr/bin/env python3
import collections
import datetime as dt
import functools
import inspect
import json
import logging
import os
import pprint as pp
import sys
import threading

import dcyd
from . import gcp
from dcyd.utils import (
    base64_pickle,
    generate_uid,
    get_project_id,
)

instance_id = generate_uid()
project_id = get_project_id()


def log_entry(*, payload: dict):
    '''
    Write a dictionary with the underlying logging infrastructure.
    '''
    if type(payload) is not dict:
        logging.getLogger(__name__).error(f"payload should be a dict but is a {type(payload)}; payload={pp.pprint(payload)}")
        return  # TODO: find out if there is any other action we can do
    return gcp.log_struct(record=payload)


def collect_runtime_data() -> dict:
    '''
    Adding runtime data to a payload
    '''
    return {
        'client_name': 'dcyd',
        'client_version': dcyd.__version__,
        'client_language': 'python',
        'protocol_name': 'client-log',
        'protocol_version': '2.0',
        'project_id': project_id,
        'instance_id': instance_id,
        'process_id': str(os.getpid()),
        'thread_id': str(threading.get_ident()),
    }


def collect_function_data(*, function: callable, function_signature: inspect.Signature = None) -> dict:
    '''
    Collect function information
    '''
    function_signature = function_signature or inspect.signature(function)  # In case function_signature is not provided
    return {
        'function': {
            'function_name': function.__name__,
            'function_qualname': function.__qualname__,
            'function_module': function.__module__,
            'function_sourcefile': inspect.getsourcefile(function),
            'function_parameters': {
                k: str(v.kind) for k, v in function_signature.parameters.items()
            }
        },
    }


def serialize_objects(*, objects: dict) -> tuple:
    errors = []
    serialized_data = {}
    for k, v in objects.items():
        serialized_data[k], success = base64_pickle(v)
        if not success:
            errors.append(k)
    return serialized_data, errors


def bind_function_arguments(*, signature, args, kwargs):
    ba = signature.bind(*args, **kwargs)
    ba.apply_defaults()
    return ba.arguments


def apply_transformers(*, transformers: dict, values: collections.OrderedDict):
    transformed_values = collections.OrderedDict({})
    for key, value in values.items():
        if key in transformers:
            transformer = transformers[key]
            transformed_values[key] = transformer(value)
        else:
            transformed_values[key] = value
    return transformed_values


def construct_request_payload(
        *,
        function_signature: inspect.Signature,
        args,
        kwargs,
        request_id: str = None,
        request_timestamp: str = None,
        transformers: dict = {},
) -> dict:
    error_dict = {}
    bound_args = bind_function_arguments(signature=function_signature, args=args, kwargs=kwargs)
    transformed_values = apply_transformers(transformers=transformers or {}, values=bound_args)
    serialized_request_data, arg_errors = serialize_objects(objects=transformed_values)
    if arg_errors:
        error_dict['request_data'] = arg_errors

    request_payload = {
        'event_type': 'request',
        'request': {
            'request_id': request_id or generate_uid(),
            'request_timestamp': request_timestamp or dt.datetime.utcnow().isoformat(),
            'request_data': serialized_request_data,
        },
    }
    if error_dict:
        request_payload['request']['serialization_errors'] = error_dict

    return request_payload


def construct_response_payload(
        *,
        response_value,
        response_timestamp: str = None,
        transformer: callable = None,
) -> dict:
    transformed_value = response_value
    if callable(transformer):
        transformed_value = apply_transformers(transformers={'return': transformer}, values={'return': response_value})['return']
    serialized_response, response_errors = serialize_objects(objects={'response_value': transformed_value})
    serialized_response = serialized_response['response_value']

    response_payload = {
        'event_type': 'response',
        'response': {
            'response_timestamp': response_timestamp or dt.datetime.utcnow().isoformat(),
            'response_data': serialized_response
        }
    }
    if response_errors:
        response_payload['response']['serialization_errors'] = {'response_data': response_errors}
    return response_payload


def monitor(function=None, *_ignore_args, transformers: dict = {}, return_transformer: callable = None, **_ignore_kwargs):
    """Decorate a client's function."""
    def decorate(function: callable):
        function_signature = inspect.signature(function)
        function_data = collect_function_data(function=function, function_signature=function_signature)

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            runtime_data = collect_runtime_data()

            # Log call of client's function
            request_id = generate_uid()
            request_timestamp = dt.datetime.utcnow().isoformat()
            request_payload = construct_request_payload(
                function_signature=function_signature,
                args=args,
                kwargs=kwargs,
                request_id=request_id,
                request_timestamp=request_timestamp,
                transformers=transformers,
            )
            request_payload.update(function_data)
            request_payload.update(runtime_data)
            log_entry(payload=request_payload)

            # Call client's function
            response = function(*args, **kwargs)

            # Log response of client's function
            response_timestamp = dt.datetime.utcnow().isoformat()
            response_payload = construct_response_payload(
                response_value=response,
                response_timestamp=response_timestamp,
                transformer=return_transformer,
            )
            response_payload.update(function_data)
            response_payload.update(runtime_data)
            response_payload.update({'request': request_payload['request']})
            log_entry(payload=response_payload)

            # Pass along the function clientall response
            return response
        return wrapper
    if function:
        return decorate(function)
    return decorate
