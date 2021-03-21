import os
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from helpers.selection import get_source_files, load_source_file, get_valid_trap_num_from_children

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
        options=get_source_files(),
        value=None
    ),

    # Shared
    html.Div(id="yolo-csv", style={"display": "none"})

])


@app.callback(dash.dependencies.Output('yolo-csv', 'children'), [dash.dependencies.Input('source-file-dropdown', 'value')])
def load_csv_data(value):
    if value:
        yolo_csv = load_source_file(value).to_json()
        return yolo_csv


@app.callback(dash.dependencies.Output('source-file-value', 'children'), [dash.dependencies.Input('yolo-csv', 'children')])
def source_file_value(children):
    return "Loaded Source File" if children else "Select Source File"


@app.callback(dash.dependencies.Output('trap-num-dropdown', 'options'), [dash.dependencies.Input('yolo-csv', 'children')])
def trap_num_options(children):
    if children:
        return get_valid_trap_num_from_children(children)

    return []


@app.callback(dash.dependencies.Output('trap-num-value', 'children'), [dash.dependencies.Input('trap-num-dropdown', 'value')])
def source_file_value(value):
    return "Trap Num Selected" if value else "Select Trap Num"






if __name__ == '__main__':

    app.run_server(debug=True)