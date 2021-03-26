import os
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_table import DataTable
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

# QUERY
query_layout = dbc.Card([
        html.H4("Query"),
        dbc.FormGroup([
                dbc.Label("Source File", id='source-file-value'),
                dcc.Dropdown(
                    id="source-file-dropdown",
                    options=get_source_files(),
                    value=None
                )
            ]
        ),
        dbc.FormGroup([
                dbc.Label("Trap Number", id="trap-num-value"),
                dcc.Dropdown(
                    id="trap-num-dropdown",
                    options=[],
                    value=None
                )
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Time Number", id="time-num-value"),
                dcc.Dropdown(
                    id="time-num-dropdown",
                    options=[],
                    value=None
                )
            ]
        ),
        html.Button('Query', id='query-button', n_clicks=0),
        # Shared
        html.Div(id="yolo-csv", style={"display": "none"}),
        html.Div(id="yolo-query", style={"display": "none"})
    ],
    body=True,
)

# PLOT
plot_layout = dcc.Graph(id="graph-1", figure=go.Figure(), responsive=True, style={"height": "100%", "width": "100%"})

# RAW
raw_layout = dbc.Col([
                    html.H4("Raw Data"),
                    DataTable(id="raw-table",
                              style_table={
                                  "overflowY": "auto",
                                  "overflowX": "auto",
                                  "height": "50vh",
                                },
                              style_data_conditional=[
                                   {
                                       'if': {'row_index': 'odd'},
                                       'backgroundColor': 'rgb(248, 248, 248)'
                                   }
                               ],
                              style_header={
                                   'backgroundColor': 'rgb(230, 230, 230)',
                                   'fontWeight': 'bold'
                               }
                              )])


# INFO
info_1 = dbc.Card([
            dbc.CardBody([
                html.H4("Total Branch Count", className="card-title"),
                html.P("Info1", className="card-text")
            ]),
    ],
    style={},
)

info_2 = dbc.Card([
            dbc.CardBody([
                html.H4("Main Branch Count", className="card-title"),
                html.P("Info2", className="card-text")
            ]),
    ],
    style={},
)

info_3 = dbc.Card([
            dbc.CardBody([
                html.H4("Longest Main Branch", className="card-title"),
                html.P("Info3", className="card-text")
            ]),
    ],
    style={},
)

info_4 = dbc.Card([
            dbc.CardBody([
                html.H4("Shortest Main Branch", className="card-title"),
                html.P("Info4", className="card-text")
            ]),
    ],
    style={},
)

info_5 = dbc.Card([
            dbc.CardBody([
                html.H4("Possible Errors", className="card-title"),
                html.P("Info5", className="card-text")
            ]),
    ],
    style={},
)

info_layout = [dbc.Col(info_1, width="auto"), dbc.Col(info_2, width="auto"), dbc.Col(info_3, width="auto"),
               dbc.Col(info_4, width="auto"), dbc.Col(info_5, width="auto")]


layout = [
    dbc.Container([
            html.H1("Cell Family Tree Analysis and Visualization"),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Row(query_layout,
                            style={'background-color': 'white'},
                            justify="center",
                            align="center"
                            ),
                    dbc.Row(raw_layout,
                            style={'background-color': 'white'},
                            justify="center",
                            align="center"),
                    ],
                    width=3),
                dbc.Col([
                    dbc.Row(plot_layout,
                            style={'background-color': 'white'},
                            className="h-75"),
                    dbc.Row(info_layout,
                            style={'background-color': 'white'},
                            className="h-25")
                    ],
                    width=True)
                    ],
                    style={'background-color': 'white'},
                    className="h-100")
    ],
     fluid=True,
     style={"height": "90vh"})
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
@app.callback([Output('graph-1', 'figure'),
               Output('raw-table', 'columns'),
               Output('raw-table', 'data')
               ],
              [Input('query-button', 'n_clicks')],
              [State('source-file-dropdown', 'value'),
               State('trap-num-dropdown', 'value'),
               State('time-num-dropdown', 'value')])
def click_query(click, source_file_value, trap_value, time_value):

    if source_file_value and trap_value and time_value:
        fig, query_df = run_query(source_file_value, trap_value, time_value)
        dt_columns = [{"name": i, "id": i} for i in query_df.columns],
        dt_rows = query_df.to_dict('records'),
        return [fig, dt_columns[0], dt_rows[0]]

    return [go.Figure(), [], []]


if __name__ == '__main__':

    app.run_server(debug=True)