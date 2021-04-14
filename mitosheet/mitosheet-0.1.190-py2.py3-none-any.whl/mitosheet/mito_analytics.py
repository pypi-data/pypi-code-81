#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Mito currently collects logs on basic user interactions with the app, 
so that we can improve the tool.

However, _we collect no logs that contain personal user data_. No private
data is taken from the users computer, as can be verified by this app.

Our general approach to logging can be understood as:
0. Log no information about the data users use in Mito. Not a drop!
1. Users are identified by a single random ID that we generate on the client-side, 
   here. We store this in the ~/.mito/user.json file, and we use it as the permanent
   ID for all users.
2. All logging is on the backend. This avoids us worrying about blockers or needing
   to associate with ad-tech at all.
3. We generate a single log event for a single action taken by the user. That means that if
   the user takes an action that causes an error, the error is logged _with_ that action.

   This appears to be good practice, as it allows us to associate what actions are taken
   with their result very effectively!
"""
from mitosheet.utils import get_random_id
from mitosheet.parser import parse_formula

import analytics
# Write key taken from segement.com
analytics.write_key = '6I7ptc5wcIGC4WZ0N1t0NXvvAbjRGUgX' 

import pandas as pd
import sys
import getpass

from mitosheet.user.user_utils import get_user_field
from mitosheet._version import __version__
from mitosheet.errors import get_recent_traceback_as_list


# When we anonymize, we use some combination of these words
# to construct new private words
valid_words = ['cat', 'dog', 'hat', 'time', 'person', 'year', 'way', 'thing', 'man', 'world', 'life', 'born', 'part', 'child', 'eye', 'woman', 'place', 'work', 'fall', 'case', 'point', 'company', 'number', 'group', 'problem', 'fact']

# We use the same salt to anonymize_words, and we read
# this salt in once the function is called for the first
# time, to make sure it's initialized properly
salt = None
def anonymize_word(word):
    """
    Helper function that turns a column header into
    a totally anonymous version of the column header,
    as to not leak _any_ user data
    """
    # We make sure that the salt is read in after the entire
    # app has been initalized, so that we don't have to read
    # from the file all the time
    global salt
    if salt is None:
        salt = get_user_field('user_salt')

    word = str(word)

    # We select three indexes from the valid_words list, and concatenate them
    index_one = int(hash(salt + word + '0')) % len(valid_words)
    index_two = int(hash(salt + word + '1')) % len(valid_words)
    index_three = int(hash(salt + word + '2')) % len(valid_words)

    return valid_words[index_one] + valid_words[index_two] + valid_words[index_three]


def anonymize_formula(formula):
    """
    Helper function that anonymizes formula to 
    make sure that no private data is included in it.
    """
    # We just input a random address, as we don't use it
    _, _, dependencies = parse_formula(formula, 'A', throw_errors=False)
    
    for dependency in dependencies:
        formula = formula.replace(dependency, anonymize_word(dependency))
    
    return formula


def log(log_event, params=None):
    """
    Helper function that logs an event with the
    given parameters.
    """
    if params is None:
        params = {}

    # Private params are where we _make sure_ that no private
    # user data leaves the users machine. We replace any potentially
    # private params with non-private versions of them
    private_params = {}
    for key, value in params.items():
        # We take any of the items that contain private user data, and we anonymize them
        if ('column_header' in key \
            or 'df_name' in key \
            or 'dataframe_name' in key \
            or 'analysis_name' in key \
            or 'merge_key' in key ) \
            and 'index' not in key:
            private_params[key] = anonymize_word(value)
        elif 'formula' in key:
            # We make sure to remove any private references from a formula
            private_params[key] = anonymize_formula(value)
        elif 'file_names' in key:
            # Just count the number of files, instead of keeping their names
            private_params[key] = len(value)
        elif 'rows' in key or 'columns' in key or 'selected_columns' in key:
            # We anonymize all of the column headers in any list
            private_params[key] = [anonymize_word(v) for v in value]
        elif 'values' in key:
            # for pivot params, we anonymize the column headers
            # and keep the agg functions
            private_params[key] = {anonymize_word(k): v for k, v in value.items()}
        elif 'filters' in key:
            # For filters, we just count the number of filters that they have
            private_params[key] = len(value)
        elif 'import_summaries' in key:
            if value is not None:
                # For import summaries, we also just take the length of them
                private_params[key] = len(value)
            else:
                private_params[key] = value

        else:
            private_params[key] = value

    analytics.track(
        get_user_field('static_user_id'), 
        log_event, 
        private_params
    )


def identify():
    """
    Helper function for identifying a user. We just take
    their python version, mito version, and email.
    """
    static_user_id = get_user_field('static_user_id')
    user_email = get_user_field('user_email')

    analytics.identify(static_user_id, {
        'python_version': sys.version_info,
        'mito_version': __version__,
        'email': user_email,
        'user': getpass.getuser(),
    })


def log_recent_error(log_event=None):
    """
    A helper function for logging the most recent error that has occured.

    log_event defaults to an execution_error_log_event
    """
    if log_event is None:
        log_event = 'execution_error_log_event'

    # We get the error, see more here: https://wiki.python.org/moin/HandlingExceptions
    e = sys.exc_info()[0]

    # If we have some other error, we just report this as an execution error
    log(
        log_event, 
        {
            'header': 'Execution Error', 
            'to_fix': 'Sorry, there was an error during executing this code.',
            'error': str(e),
            'traceback': get_recent_traceback_as_list()
        }
    )


def log_event_processed(event, widget_state_container, failed=False, edit_error=None):
    """
    Helper function for logging when an event is processed
    by the widget state container. 

    Does it's best to fill in helpful meta-data for interpreting the event
    including the state of the widget_state_container _after_ the step
    was applied.

    NOTE: if processing the event fails, then failed should be True. If there was an
    edit error that was thrown during the processing of the event, then edit_error
    should be set to that error.
    """
    try:
        # First, we get all the params of the event, and append them with _params_
        event_properties = {
            'params_' + key: value for key, value in event.items()
        }

        # We also get some metadata about the widget state container at this state
        wsc_properties = {
            # NOTE: analysis name is the UUID that mito saves the analysis under
            'wsc_analysis_name': widget_state_container.analysis_name,
            'wsc_curr_step_idx': widget_state_container.curr_step_idx,
            'wsc_curr_step_type': widget_state_container.curr_step['step_type'],
        }

        # Python properties, just for helpful data about the system
        python_properties = {
            'version_python': sys.version_info,
            'version_mito': __version__ 
        }

        # We also check there is an edit_error, and if there is, then we add the error logs
        if edit_error is not None:
            error_properties = {
                'error_type': edit_error.type_,
                'error_header': edit_error.header,
                'error_to_fix': edit_error.to_fix,
                'error_traceback': get_recent_traceback_as_list(),
            }
        elif failed:
            # Otherwise, if there is no edit_error, and we still failed, then we must have
            # gotten an execution error
            error_properties = {
                'error_type': 'execution_error',
                'error_header': 'Execution Error',
                'error_traceback': get_recent_traceback_as_list(),
            }
        else:
            error_properties = {}

        # We choose to log the event type, as it is the best high-level item for our logs
        # and we append a _failed if the event failed in doing this.
        log_event = event['type'] + ('_failed' if failed else '')

        log(
            log_event, 
            dict(
                **python_properties,
                **event_properties,
                **wsc_properties,
                **error_properties
            )
        )
    except:
        # We don't want logging to ever brick the application, so if the logging fails
        # we just log simple information about the event. This should never occur, but it
        # is just a precaution - some defensive programming so to speak
        log(
            event['type'],
            event
        )
