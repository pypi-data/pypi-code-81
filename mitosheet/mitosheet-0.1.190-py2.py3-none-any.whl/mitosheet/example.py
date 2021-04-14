#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Main file containing the mito widget.
"""
from mitosheet.utils import get_new_step_id
from mitosheet.api import API
from mitosheet.mito_analytics import log, log_event_processed, log_recent_error
import pandas as pd

from ipywidgets import DOMWidget
import traitlets as t

from mitosheet._frontend import module_name, module_version
from mitosheet.errors import EditError, get_recent_traceback_as_list
from mitosheet.save_utils import (
    read_and_upgrade_analysis, 
    write_analysis,
    saved_analysis_names_json
)

from mitosheet.widget_state_container import WidgetStateContainer
from mitosheet.profiling import timeit

from mitosheet.user.user import is_local_deployment, should_upgrade_mitosheet

class MitoWidget(DOMWidget):
    """
        The MitoWidget holds all of the backend state for the Mito extension, and syncs
        the state with the frontend widget. 
    """
    _model_name = t.Unicode('ExampleModel').tag(sync=True)
    _model_module = t.Unicode(module_name).tag(sync=True)
    _model_module_version = t.Unicode(module_version).tag(sync=True)
    _view_name = t.Unicode('ExampleView').tag(sync=True)
    _view_module = t.Unicode(module_name).tag(sync=True)
    _view_module_version = t.Unicode(module_version).tag(sync=True)

    is_local_deployment = t.Bool(True).tag(sync=True)
    analysis_name = t.Unicode('').tag(sync=True)
    curr_step_idx = t.Int(0).tag(sync=True)
    sheet_json = t.Unicode('').tag(sync=True)
    code_json = t.Unicode('').tag(sync=True)
    df_names_json = t.Unicode('').tag(sync=True)
    df_shape_json = t.Unicode('').tag(sync=True)
    saved_analysis_names_json = t.Unicode('').tag(sync=True)
    column_spreadsheet_code_json = t.Unicode('').tag(sync=True)
    column_filters_json = t.Unicode('').tag(sync=True)
    column_type_json = t.Unicode('').tag(sync=True)
    has_rendered = t.Bool(True).tag(sync=True)
    user_email = t.Unicode('').tag(sync=True)
    step_data_list_json = t.Unicode('').tag(sync=True)
    should_upgrade_mitosheet = t.Bool(False).tag(sync=True)

    def __init__(self, *args, **kwargs):
        """
        Takes a list of dataframes and strings that are paths to CSV files
        passed through *args.
        """
        # Call the DOMWidget constructor to set up the widget properly
        super(MitoWidget, self).__init__()

        # Set if this is a local deployment
        self.is_local_deployment = is_local_deployment()

        # Mark if it is time for the user to update
        self.should_upgrade_mitosheet = should_upgrade_mitosheet()
            
        # Set up the state container to hold private widget state
        self.widget_state_container = WidgetStateContainer(args)
        
        # When the widget is first created, it has not been rendered on the frontend yet,
        # but after it is rendered once, this is set to False. This helps us detect 
        # when we are rendering for the first time vs. refreshing the sheet
        self.has_rendered = False

        # Set up starting shared state variables
        self.update_shared_state_variables()

        # Set up message handler
        self.on_msg(self.receive_message)

        # And the api
        self.api = API(self.widget_state_container, self.send)

    def update_shared_state_variables(self):
        """
        Helper function for updating all the variables that are shared
        between the backend and the frontend through trailets.
        """
        self.sheet_json = self.widget_state_container.sheet_json
        self.curr_step_idx = self.widget_state_container.curr_step_idx
        self.column_spreadsheet_code_json = self.widget_state_container.column_spreadsheet_code_json
        self.code_json = self.widget_state_container.code_json
        self.df_names_json = self.widget_state_container.df_names_json
        self.df_shape_json = self.widget_state_container.df_shape_json
        self.analysis_name = self.widget_state_container.analysis_name
        self.saved_analysis_names_json = saved_analysis_names_json()
        self.column_filters_json = self.widget_state_container.column_filters_json
        self.column_type_json = self.widget_state_container.column_type_json
        self.user_email = self.widget_state_container.user_email
        self.step_data_list_json = self.widget_state_container.step_data_list_json

    def handle_edit_event(self, event):
        """
        Handles an edit_event. Per the spec, an edit_event
        updates both the sheet and the codeblock, and as such
        the sheet is re-evaluated and the code for the codeblock
        is re-transpiled.

        Useful for any event that changes the state of both the sheet
        and the codeblock!
        """
        # First, we send this new edit to the evaluator
        self.widget_state_container.handle_edit_event(event)

        # We update the state variables 
        self.update_shared_state_variables()

        # Also, write the analysis to a file!
        write_analysis(self.widget_state_container)

        # Tell the front-end to render the new sheet and new code
        self.send({"event": "update_sheet"})
        self.send({"event": "update_code"})


    def handle_update_event(self, event):
        """
        This event is not the user editing the sheet, but rather information
        that has been collected from the frontend (after render) that is being
        passed back.

        For example:
        - Names of the dataframes
        - Name of an existing analysis
        """
        # If this is just a message to notify the backend that we have rendered, set and return
        if event['type'] == 'has_rendered_update':
            self.has_rendered = True
            return

        self.widget_state_container.handle_update_event(event)

        # Update all state variables
        self.update_shared_state_variables()

        # Also, write the analysis to a file!
        write_analysis(self.widget_state_container)

        # Tell the front-end to render the new sheet and new code
        self.send({"event": "update_sheet"})
        self.send({"event": "update_code"})

    def receive_message(self, widget, content, buffers=None):
        """
        Handles all incoming messages from the JS widget. There are two main
        types of events:

        1. edit_event: any event that updates the state of the sheet and the
        code block at once. Leads to reevaluation, and a re-transpile.

        2. update_event: any event that isn't caused by an edit, but instead
        other types of new data coming from the frontend (e.g. the df names 
        or some existing steps).

        3. A log_event is just an event that should get logged on the backend.
        """
        event = content

        try:
            if event['event'] == 'edit_event':
                self.handle_edit_event(event)
            elif event['event'] == 'update_event':
                self.handle_update_event(event)
            elif event['event'] == 'api_call':
                self.api.process_new_api_call(event)
                return 
            
            # NOTE: we don't need to case on log_event above because it always gets
            # passed to this function, and thus is logged. However, we do not log
            # api calls, as they are just noise.
            log_event_processed(event, self.widget_state_container)
        except EditError as e:
            print(get_recent_traceback_as_list())
            print(e)
            
            # Log processing this event failed
            log_event_processed(event, self.widget_state_container, failed=True, edit_error=e)

            # Report it to the user, and then return
            self.send({
                'event': 'edit_error',
                'type': e.type_,
                'header': e.header,
                'to_fix': e.to_fix
            })
        except:
            print(get_recent_traceback_as_list())
            # We log that processing failed, but have no edit error
            log_event_processed(event, self.widget_state_container, failed=True)
            # Report it to the user, and then return
            self.send({
                'event': 'edit_error',
                'type': 'execution_error',
                'header': 'Execution Error',
                'to_fix': 'Sorry, there was an error during executing this code.'
            })

def sheet(
        *args, 
        saved_analysis_name=None
    ) -> MitoWidget:
    """
    Renders a Mito sheet. If no arguments are passed, renders an empty sheet. Otherwise, renders
    any dataframes that are passed. Errors if any given arguments are not dataframes or paths to
    CSV files that can be read in as dataframes.

    If running this function just prints text that looks like `MitoWidget(...`, then you need to 
    install the JupyterLab extension manager by running:

    jupyter labextension install @jupyter-widgets/jupyterlab-manager@2;

    Run this command in the terminal where you installed Mito. It should take 5-10 minutes to complete.

    Then, restart your JupyterLab instance, and refresh your browser. Mito should now render.

    NOTE: if you have any issues with installation, please book a demo at https://hubs.ly/H0FL1920
    """
    args = list(args)

    # We first validate all the parameters as either dataframes or strings
    for arg in args:
        if not isinstance(arg, pd.DataFrame) and not isinstance(arg, str):
            error_message = f'Invalid argument passed to sheet: {arg}. Please pass all dataframes or paths to CSV files.'
            log('mitosheet_sheet_call_failed', {'error': error_message})
            raise ValueError(error_message)

    # We log that personal data has been used if they pass a dataframe
    # that is not tutorial data, or if they pass a path to a file
    if len(args) > 0 and isinstance(args[0], pd.DataFrame) and args[0].columns.tolist() != ['Zip', 'City', 'State', 'Ticket_Office']:
        log('used_personal_data')    

    # We error if the saved analysis does not exist
    if saved_analysis_name is not None and read_and_upgrade_analysis(saved_analysis_name) is None:
        log(
            'mitosheet_sheet_call_failed', 
            {'error': f'There is no saved analysis with the name {saved_analysis_name}.'}
        )
        raise ValueError(f'There is no saved analysis with the name {saved_analysis_name}.')

    try:
        # We pass in the dataframes directly to the widget
        widget = MitoWidget(*args) 
    except:
        # We log the error
        log_recent_error('mitosheet_sheet_call_failed')
        # And then bubble it to the user
        raise

    # Then, we log that the call was successful, along with all of it's params
    log(
        'mitosheet_sheet_call',
        dict(
            **{
                'param_saved_analysis_name': saved_analysis_name
            },
            **{
                # NOTE: analysis name is the UUID that mito saves the analysis under
                'wsc_analysis_name': widget.widget_state_container.analysis_name,
            },
            **{
                'param_num_args': len(args),
                'params_num_str_args': len([arg for arg in args if isinstance(arg, str)]),
                'params_num_df_args': len([arg for arg in args if isinstance(arg, pd.DataFrame)]),
            }
        )
    )
    
    # If an analysis is passed, we pass this to the widget
    if saved_analysis_name is not None:
        widget.receive_message(widget, {
            'event': 'update_event',
            'type': 'replay_analysis_update',
            'analysis_name': saved_analysis_name,
            'import_summaries': None,
            'clear_existing_analysis': False
        })

    return widget
