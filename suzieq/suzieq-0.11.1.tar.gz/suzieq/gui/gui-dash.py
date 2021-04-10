import dash
import dash_table
from dash.dependencies import Input, Output
import dash_html_components as html
import pandas as pd
from suzieq.sqobjects.routes import RoutesObj
from suzieq.sqobjects.lldp import LldpObj

df = RoutesObj().get(namespace='ibgp-evpn')
df['prefix'] = df.prefix.astype(str)

app = dash.Dash('suzieq')
app.layout = html.Div([
    dash_table.DataTable(
        id='routes',
        columns=[{"name": i, "id": i, "selectable": True} for i in df.columns],
        data=df.to_dict('records'),
        column_selectable="multi",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        filter_action="native",
        selected_columns=[],
        selected_rows=[],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    ),
    html.Div(id="routes-container")
])


@app.callback(
    Output('routes', 'style_data_conditional'),
    [Input('routes', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


if __name__ == '__main__':
    app.run_server(debug=True)
