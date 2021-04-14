from mitosheet.utils import get_column_filter_type
import pandas as pd
import json

def get_column_describe(send, event, wsc):
    """
    Sends back a string that can be parsed to a JSON object that
    contains _all_ the results from the series .describe function
    for the series at column_header in the df at sheet_index.
    """
    sheet_index = event['sheet_index']
    column_header = event['column_header']
    
    series: pd.Series = wsc.dfs[sheet_index][column_header]
    describe = series.describe()

    try:
        describe_obj = {}

        for index, row in describe.iteritems():
            # We turn all the items to strings, as some items are not valid JSON
            # e.g. some wacky numpy datatypes. This allows us to send all of this 
            # to the front-end
            describe_obj[index] = str(row)

        # We fill in some specific values that dont get filled by default
        describe_obj['count: NaN'] = str(series.isna().sum())

        # NOTE: be careful adding things here, as we dont want to destroy performance 
        if get_column_filter_type(series) == 'number':
            describe_obj['median'] = str(series.median())
            describe_obj['sum'] = str(series.sum())

        send({
            'event': 'api_response',
            'id': event['id'],
            'data': json.dumps(describe_obj)
        })
    except:
        # As this is also a non-critical error, we don't want to display an error
        # message in the case of failure, so we just return nothing
        send({
            'event': 'api_response',
            'id': event['id'],
            'data': ''
        })
