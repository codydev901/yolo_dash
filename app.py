import os
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from helpers.selection import get_source_files, load_source_file, get_trap_nums, get_time_nums, run_query

"""
layout = [
    dbc.Container([
            dbc.Row([
                dbc.Col(html.Div("Row 1 Col1"),
                        style={'background-color': 'green'},
                        width=3),
                dbc.Col(html.Div("Row 1 Col2"),
                        style={'background-color': 'yellow'},
                        width=True)
                     ],
                    style={'background-color': 'blue'},
                    className="h-100")
    ],
     fluid=True,
     style={"height": "100vh"})
    ]
"""

# Dash Stuff
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

query_layout = html.Div([
    # Title
    html.H2('Yolo CSV Tree Visualization'),

    # Source File
    html.Div(id='source-file-value'),
    dcc.Dropdown(
        id="source-file-dropdown",
        options=get_source_files(),
        value=None
    ),

    # Trap Num
    html.Div(id='trap-num-value'),
    dcc.Dropdown(
        id="trap-num-dropdown",
        options=[],
        value=None
    ),

    # Time Num
    html.Div(id='time-num-value'),
    dcc.Dropdown(
        id="time-num-dropdown",
        options=[],
        value=None
    ),

    # Query
    html.Button('Query', id='query-button', n_clicks=0),

    # Shared
    html.Div(id="yolo-csv", style={"display": "none"}),
    html.Div(id="yolo-query", style={"display": "none"})

])

plot_layout = dcc.Graph(id="graph-1", figure=go.Figure(), responsive=True, style={"height": "100%", "width": "100%"})

layout = [
    dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Row(query_layout,
                            style={'background-color': 'red'},
                            className="h-50"),
                    dbc.Row(html.Div("RAW"),
                            style={'background-color': 'yellow'},
                            className="h-50"),
                    ],
                    width=3),
                dbc.Col([
                    dbc.Row(plot_layout,
                            style={'background-color': 'orange'},
                            className="h-75"),
                    dbc.Row(html.Div("INFO"),
                            style={'background-color': 'pink'},
                            className="h-25")
                    ],
                    width=True)
                    ],
                    style={'background-color': 'blue'},
                    className="h-100")
    ],
     fluid=True,
     style={"height": "100vh"})
    ]

app.layout = html.Div(layout)


# Source File
@app.callback([Output('yolo-csv', 'children')],
              [Input('source-file-dropdown', 'value')])
def get_source_file_options(value):
    if value:
        yolo_csv = load_source_file(value).to_initial_json()
        return [yolo_csv]
    return [[]]


@app.callback([Output('source-file-value', 'children')],
              [Input('yolo-csv', 'children')])
def set_source_file_value(children):
    return ["Loaded Source File"] if children else ["Select Source File"]


# Trap Num
@app.callback([Output('trap-num-dropdown', 'options')],
              [Input('yolo-csv', 'children')])
def get_trap_num_options(children):
    if children:
        return [get_trap_nums(yolo_csv_c=children)]

    return [[]]


@app.callback([Output('trap-num-value', 'children')],
              [Input('trap-num-dropdown', 'value')])
def set_trap_num_value(value):
    print("Trap Num Value", value)
    return ["Trap Num Selected"] if value else ["Select Trap Num"]


# Time Num
@app.callback([Output('time-num-dropdown', 'options')],
              [Input('yolo-csv', 'children'), Input('trap-num-dropdown', 'value')])
def get_time_num_options(children, value):

    if children and value:
        return [get_time_nums(yolo_csv_c=children, trap_num=value)]

    return [[]]


@app.callback([Output('time-num-value', 'children')],
              [Input('time-num-dropdown', 'value')])
def set_time_num_value(value):
    print("Time Num Value", value)
    return ["Time Num Selected"] if value else ["Select Time Num"]


# Query
@app.callback([Output('graph-1', 'figure')],
              [Input('query-button', 'n_clicks')],
              [State('source-file-dropdown', 'value'),
               State('trap-num-dropdown', 'value'),
               State('time-num-dropdown', 'value')])
def click_query(click, source_file_value, trap_value, time_value):

    if source_file_value and trap_value and time_value:
        return [run_query(source_file_value, trap_value, time_value)]

    return [go.Figure()]


if __name__ == '__main__':

    app.run_server(debug=True)