#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains handlers for the Mito API
"""
from mitosheet.mito_analytics import log_event_processed
import os
from queue import Queue
from threading import Thread
from pathlib import Path

from mitosheet.api.get_column_dtype import get_column_dtype
from mitosheet.api.get_column_summary_graph import get_column_summary_graph
from mitosheet.api.get_saved_analysis_description import get_saved_analysis_description
from mitosheet.api.get_column_describe import get_column_describe
from mitosheet.steps.import_steps.raw_python_import import RAW_PYTHON_IMPORT_STEP_TYPE
from mitosheet.steps.import_steps.simple_import import SIMPLE_IMPORT_STEP_TYPE
from mitosheet.save_utils import read_analysis

# As the column summary statistics tab does three calls, we defaulted to this max
MAX_QUEUED_API_CALLS = 3


class API():
    """
    The API provides a wrapper around a thread that responds to API calls.

    Some notes:
    -   We allow at most MAX_QUEUED_API_CALLS API calls to be in the queue, which practically
        Stops a backlog of calls from building up.
    -   All API calls should only be reads. This stops us from having to worry 
        about most concurrency issues
    -   Note that printing inside of a thread does not work properly! 
        See here: https://stackoverflow.com/questions/18234469/python-multithreaded-print-statements-delayed-until-all-threads-complete-executi
    """
    def __init__(self, wsc, send):
        self.api_queue = Queue(MAX_QUEUED_API_CALLS)
        # Note that we make the thread a daemon thread, which practically means that when
        # The process that starts this thread terminate, our API will terminate as well.
        self.thread = Thread(target=handle_api_event_thread, args=(self.api_queue, wsc, send), daemon=True)
        self.thread.start()

    def process_new_api_call(self, event):
        """
        We privilege new API calls over old calls, and evict the old ones 
        if the API queue is full.

        Because we are using a queue, only events that have not been started 
        being processed will get removed.
        """        
        if self.api_queue.full():
            self.api_queue.get()
        self.api_queue.put(event)


def handle_api_event_thread(queue, wsc, send):
    """
    This is the worker thread function, that actually is 
    responsible for handling at the API call events.

    It lives forever, and just handles events as it 
    receives them from the queue
    """
    while True:
        # Note that this blocks when there is nothing in the queue,
        # and waits till there is something there - so no infinite 
        # loop as it is waiting!
        event = queue.get()
        # We place the API handling inside of a try catch, 
        # because otherwise if an error is thrown, then the entire thread crashes, 
        # and then the API never works again
        try:
            handle_api_event(send, event, wsc)
        except:
            # Log in error if it occurs
            log_event_processed(event, wsc, failed=True)


def get_filenames_with_suffix(suffix):
    """
    Returns all the file names in the current folder that end with the given
    suffix, sorted from most-recently created to the oldest.
    """
    # We sort them by creation time, to get the most recent files, as the user
    # is more likely to want these
    filenames = sorted(Path('.').iterdir(), key=os.path.getmtime)
    filenames.reverse()
    return [str(filename) for filename in filenames if filename.suffix == suffix]


def handle_datafiles(send, event):
    """
    Handles a `datafiles` api call, and returns all the csv files
    in the current folder.
    """
    csv_files = get_filenames_with_suffix('.csv')
    # TODO: also get the XLSX files, when we can import them
    send({
        'event': 'api_response',
        'id': event['id'],
        'data': csv_files
    })

def handle_import_summary(send, event):
    """
    Handle import summary is a route that, given the name of an analysis, will
    return the parameters to import steps over the course of the analysis. 

    The data we return is in the format:
    {
        "1": {
            "file_names": ["file123.csv"]
        }, 
        "3": {
            "python_code": "import pandas as ...",
            "new_df_names": ["df1"]
        }
    }
    which is a mapping from raw import steps to the files that they import.
    """
    analysis_name = event['analysis_name']
    # NOTE: we don't upgrade, as this happens when you actually choose to replay an analysis
    analysis = read_analysis(analysis_name)

    imports_only = dict()
    if analysis is not None:
        for step_idx, step in analysis['steps'].items():
            if step['step_type'] == SIMPLE_IMPORT_STEP_TYPE:
                imports_only[step_idx] = dict()
                imports_only[step_idx]['step_type'] = SIMPLE_IMPORT_STEP_TYPE
                imports_only[step_idx]['file_names'] = step['file_names']
            elif step['step_type'] == RAW_PYTHON_IMPORT_STEP_TYPE:
                imports_only[step_idx] = dict()
                imports_only[step_idx]['step_type'] = RAW_PYTHON_IMPORT_STEP_TYPE
                imports_only[step_idx]['python_code'] = step['python_code']
                imports_only[step_idx]['new_df_names'] = step['new_df_names']

    send({
        'event': 'api_response',
        'id': event['id'],
        'data': imports_only
    })


def get_dataframe_as_csv(send, event, wsc):
    """
    Sends a dataframe as a CSV string
    """
    sheet_index = event['sheet_index']
    df = wsc.dfs[sheet_index]

    send({
        'event': 'api_response',
        'id': event['id'],
        'data': df.to_csv(index=False)
    })


def handle_api_event(send, event, wsc):
    """
    Handler for all API calls. Note that any response to the
    API must return the same ID that the incoming message contains,
    so that the frontend knows how to match the responses.
    """    
    # And then handle it
    if event['type'] == 'datafiles':
        handle_datafiles(send, event)
    elif event['type'] == 'import_summary':
        handle_import_summary(send, event)
    elif event['type'] == 'get_dataframe_as_csv':
        get_dataframe_as_csv(send, event, wsc)
    elif event['type'] == 'get_column_summary_graph':
        get_column_summary_graph(send, event, wsc)
    elif event['type'] == 'get_column_describe':
        get_column_describe(send, event, wsc)
    elif event['type'] == 'get_column_dtype':
        get_column_dtype(send, event, wsc)
    elif event['type'] == 'get_saved_analysis_description':
        get_saved_analysis_description(send, event, wsc)
    else:
        raise Exception(f'Event: {event} is not a valid API call')