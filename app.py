import os
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from helpers.selection import get_source_files, load_source_file, get_trap_nums, get_time_nums, run_query

# Dash Stuff
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Layout
app.layout = html.Div([
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

    # Run Graph/Tree Button
    html.Button('Query', id='query-button', n_clicks=0),

    # Shared
    html.Div(id="yolo-csv", style={"display": "none"}),
    html.Div(id="yolo-query", style={"display": "none"})

])


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
@app.callback([Output('yolo-query', 'children')],
              [Input('query-button', 'n_clicks')],
              [State('source-file-dropdown', 'value'),
               State('trap-num-dropdown', 'value'),
               State('time-num-dropdown', 'value')])
def click_query(click, source_file_value, trap_value, time_value):

    if source_file_value and trap_value and time_value:
        return [run_query(source_file_value, trap_value, time_value)]

    return [[]]


if __name__ == '__main__':

    app.run_server(debug=True)
