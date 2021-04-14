#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import json
import uuid 
from copy import deepcopy
import pandas as pd
from typing import List


from mitosheet.steps.column_steps.set_column_formula import SET_COLUMN_FORMULA_EVENT, SET_COLUMN_FORMULA_STEP_TYPE
from mitosheet.steps.filter import execute_filter_column
from mitosheet.steps import EVENT_TYPE_TO_STEP, STEP_TYPE_TO_STEP
from mitosheet.updates import UPDATES
from mitosheet.steps.initalize import execute_initialize_step
from mitosheet.preprocessing import PREPROCESS_STEPS
from mitosheet.utils import dfs_to_json
from mitosheet.transpiler.transpile import transpile
from mitosheet.user.user_utils import get_user_field


class WidgetStateContainer():
    """
    Holds the state of the steps, which represents operations that
    have been performed on the input dataframes. 
    """

    def __init__(self, args):
        """
        When initalizing the Widget State Container, we also do preprocessing
        of the arguments that were passed to the mitosheet. 

        All preprocessing can be found in mitosheet/preprocessing, and each of 
        the transformations are applied before the data is considered imported.
        """
        # We just randomly generate analysis names. 
        # We append a UUID to note that this is not an analysis the user has saved.
        self.analysis_name = 'UUID-' + str(uuid.uuid4())

        # The args are a tuple of dataframes or strings, and we start by making them
        # into a list, and making copies of them for safe keeping
        self.original_args = [
            arg.copy(deep=True) if isinstance(arg, pd.DataFrame) else deepcopy(arg) for arg in args
        ]

        # Then, we go through the process of actually preprocessing the args
        for PREPROCESS_STEP in PREPROCESS_STEPS:
            args = PREPROCESS_STEP['execute'](args)

        # Then we initialize the first initalize step
        self.steps = []
        # We display the state that exists after the curr_step_idx is applied,
        # which means you can never see before the initalize step
        self.curr_step_idx = 0

        execute_initialize_step(self, args)


    @property
    def curr_step(self):
        """
        Returns the current step object as a property of the object,
        so reference it with self.curr_step
        """
        return self.steps[self.curr_step_idx]

    @property
    def num_sheets(self):
        """
        Duh. :)
        """
        return len(self.steps[self.curr_step_idx]['dfs'])

    @property
    def dfs(self) -> List[pd.DataFrame]:
        return self.steps[self.curr_step_idx]['dfs']

    @property
    def df_names_json(self):
        """
        A JSON object containing the names of the dataframes
        """
        return json.dumps({'df_names': self.curr_step['df_names']})

    @property
    def sheet_json(self):
        """
        sheet_json contains a serialized representation of the data
        frames that is then fed into the ag-grid in the front-end. 

        NOTE: we only display the _first_ 2,000 rows of the dataframe
        for speed reasons. This results in way less data getting 
        passed around
        """
        return dfs_to_json(self.curr_step['dfs'])
    
    @property
    def df_shape_json(self):
        """
        Returns the df shape (rows, columns) of each dataframe in the 
        current step!
        """
        return json.dumps([
            {'rows': df.shape[0], 'cols': df.shape[1]}
            for df in self.curr_step['dfs']
        ])

    @property
    def column_spreadsheet_code_json(self):
        """
        column_spreadsheet_code_json is a list of all the spreadsheet
        formulas that users have used, for each sheet they have. 
        """
        return json.dumps(self.curr_step['column_spreadsheet_code'])

    @property
    def code_json(self):
        """
        This code json string is sent to the front-end and is what
        ends up getting displayed in the codeblock. 
        """
        return json.dumps(transpile(self))

    @property
    def column_filters_json(self):
        """
        This column_filters list is used by the front end to display
        the filtered icons in the UI
        """
        return json.dumps(self.curr_step['column_filters'])
    
    @property
    def column_type_json(self):
        """
        Returns a list of JSON objects that hold the type of each
        data in each column.
        """
        return json.dumps(self.curr_step['column_type'])

    @property
    def user_email(self):
        """
        Returns the user_email from user.json
        """
        return get_user_field('user_email')

    
    @property
    def step_data_list_json(self):
        """
        Returns a list of step data
        """
        step_data_list = []
        for index, step in enumerate(self.steps):
            STEP_OBJ = STEP_TYPE_TO_STEP[step['step_type']]
            params = {key: value for key, value in step.items() if key in STEP_OBJ['params']}
            step_data_list.append({
                'step_id': step['step_id'],
                'step_idx': index,
                'step_type': step['step_type'],
                'step_display_name': STEP_OBJ['step_display_name'],
                'step_description': STEP_OBJ['describe'](
                    df_names=step['df_names'],
                    **params,
                )
            })

        return json.dumps(step_data_list)

    def edit_event_should_overwrite_curr_step(self, edit_event):
        """
        We overwrite the step if the step_ids are shared between the curr step
        and the edit event, or if if it is an set formula event that is setting 
        the formula of a column that was updated the last step
        """
        overwrite_formula_step = self.curr_step['step_type'] == SET_COLUMN_FORMULA_STEP_TYPE \
                and edit_event['type'] == SET_COLUMN_FORMULA_EVENT \
                and self.curr_step['sheet_index'] == edit_event['sheet_index'] \
                and self.curr_step['column_header'] == edit_event['column_header']

        return self.curr_step['step_id'] == edit_event['step_id'] or overwrite_formula_step

    def handle_edit_event(self, edit_event):
        """
        Updates the widget state with a new step that was created
        by the edit_event. Each edit_event creates at most one step. 

        If there is an error in the creation of the new step, this
        function will delete the new, invalid step.
        """
        # NOTE: We ignore any edit if we are in a historical state, for now. This is a result
        # of the fact that we don't allow previous editing currently
        if self.curr_step_idx != len(self.steps) - 1:
            return

        try:
            curr_step = self.steps[-1]

            overwrite = self.edit_event_should_overwrite_curr_step(edit_event)

            if overwrite:
                # If we are overwriting the event, then we set the current
                # step back 1 from the actual current step, so that we start
                # from the correct state
                curr_step = self.steps[-2]             

            step_obj = EVENT_TYPE_TO_STEP[edit_event['type']]

            # Saturate the event
            if step_obj['saturate'] is not None:
                step_obj['saturate'](curr_step, edit_event)

            # Get the params for this event
            params = {key: value for key, value in edit_event.items() if key in step_obj['params']}
            # If it's filter, we need to do a lot of extra work
            # so we sent it into the execute function directly
            if step_obj['step_type'] == 'filter_column':
                execute_filter_column(
                    self,
                    **params
                )
                self.curr_step_idx = len(self.steps) - 1
                # If we made a new step, save the step id of this step
                if 'step_id' not in self.curr_step:
                    self.curr_step['step_id'] = edit_event['step_id']
                return 
            
            # Actually get the new step
            new_step = step_obj['execute'](curr_step, **params)

            # If the new step is None, we dont do anything with it, otherwise we
            # add it to the steps
            if new_step is not None:
                # Save the parameters in the new step
                for key, value in params.items():
                    new_step[key] = value
                
                # Furthermore, we save the step_id
                new_step['step_id'] = edit_event['step_id']

                # Finially, we append this step in the correct location to the steps
                if not overwrite:
                    self.steps.append(new_step)
                else:
                    self.steps[-1] = new_step
            
            # and then update the index of the current step
            self.curr_step_idx = len(self.steps) - 1
        except:

            # We bubble the error up if it occurs
            # https://stackoverflow.com/questions/6593922/letting-an-exception-to-bubble-up
            raise


    def handle_update_event(self, update_event):
        """
        Handles any event that isn't caused by an edit, but instead
        other types of new data coming from the frontend (e.g. the df names 
        or some existing steps).
        """
        for update in UPDATES:
            if update_event['type'] == update['event_type']:
                # Get the params for this event
                params = {key: value for key, value in update_event.items() if key in update['params']}
                # Actually execute this event
                update['execute'](self, **params)
                # And then return
                return

        raise Exception(f'{update_event} is not an update event!')        


    def _delete_curr_step(self):
        """
        Deletes the current step and rolls back a step!
        """
        self.steps.pop()

    


    