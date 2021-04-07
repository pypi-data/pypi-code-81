"""Helpers for managing logging to CloudWatch in cubicweb-celerytask workers

Add this module 'cw_celerytask_helpers.cloudwatchlogger' to CELERY_IMPORTS
"""
from __future__ import absolute_import

import logging
from os import getenv
from signal import Signals

import celery
from celery import signals
from watchtower import CloudWatchLogHandler
import boto3


@signals.task_prerun.connect
def setup_logging(conf=None, **kwargs):
    log_group = celery.current_app.conf.get('CUBICWEB_CELERYTASK_LOG_GROUP')
    if not log_group:
        raise RuntimeError(
            "You asked for CloudWatch-based log storage of the task logs "
            "but CUBICWEB_CELERYTASK_LOG_GROUP is not configured. "
            "Please set CUBICWEB_CELERYTASK_LOG_GROUP in your "
            "celery configuration.")
    task_id = kwargs.get('task_id')
    if task_id in ('???', None):
        return
    stream_name = get_stream_name(task_id)
    cloudwatch_endpoint_url = getenv('AWS_CLOUDWATCH_ENDPOINT_URL')
    handler = CloudWatchLogHandler(
        level=logging.DEBUG, log_group=log_group, stream_name=stream_name,
        endpoint_url=cloudwatch_endpoint_url, use_queues=False)
    handler.setFormatter(logging.Formatter(
        fmt="%(levelname)s %(asctime)s %(module)s %(process)d %(message)s\n"))
    logger = logging.getLogger('celery.task')
    logger.addHandler(handler)


@signals.task_postrun.connect
def uninstall_logging(conf=None, **kwargs):
    task_id = kwargs.get('task_id')
    if task_id in ('???', None):
        return
    logger = logging.getLogger('celery.task')
    log_group = celery.current_app.conf.get('CUBICWEB_CELERYTASK_LOG_GROUP')
    delete_stream = bool(celery.current_app.conf.get(
        'CUBICWEB_CELERYTASK_DELETE_LOG_STREAM'))
    stream_name = get_stream_name(task_id)
    for handler in logger.handlers:
        if isinstance(handler, CloudWatchLogHandler):
            logger.removeHandler(handler)
            if delete_stream:
                handler.cwl_client.delete_log_stream(
                    logGroupName=log_group,
                    logStreamName=stream_name)


@signals.task_revoked.connect
def delete_revoked_log_stream(conf=None, **kwargs):
    """executed on main celery process, hence logging handler is destroyed"""
    if 'signum' in kwargs and not isinstance(kwargs['signum'], Signals):
        # workaround for revoked task signal executed twice
        return
    request = kwargs.get('request')
    if not request:
        return
    task_id = request.get('id')
    if task_id in ('???', None):
        return
    delete_stream = bool(celery.current_app.conf.get(
        'CUBICWEB_CELERYTASK_DELETE_LOG_STREAM'))
    if not delete_stream:
        return
    log_group = celery.current_app.conf.get('CUBICWEB_CELERYTASK_LOG_GROUP')
    stream_name = get_stream_name(task_id)
    cloudwatch_endpoint_url = getenv('AWS_CLOUDWATCH_ENDPOINT_URL')
    client = boto3.client('logs', endpoint_url=cloudwatch_endpoint_url)
    client.delete_log_stream(logGroupName=log_group, logStreamName=stream_name)


def get_stream_name(task_id):
    stream_pattern = celery.current_app.conf.get(
        'CUBICWEB_CELERYTASK_STREAM_PATTERN', 'celerytask-%s')
    return stream_pattern % task_id
