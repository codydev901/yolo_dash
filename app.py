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

# HEADER
header_layout = dbc.Row([
            dbc.Col([
                html.H1("Cell Family Tree Analysis and Visualization", style={"color": "#ffffff"})
                ],
                width=True),
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardImg(src=app.get_asset_url('rd2021.png'), top=True, className='align-self-center'),
                        ],
                        style={"height": "30%", "width": "30%", "background-color": "#10366C", "margin-right": "2rem"}, outline=False
                    ),
                    dbc.Card([
                        dbc.CardImg(src=app.get_asset_url('utc2021.png'), top=True, className='align-self-center'),
                        ],
                        style={"height": "30%", "width": "30%", "background-color": "#10366C", "margin-right": "3rem"}, outline=False
                    )
                ],
                justify="end")
            ],
            width=3),
        ],
        justify="end",
        align="center",
        style={"padding-top": "1rem", "background-color": "#10366C"}

)


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
                    DataTable(id="raw-table",
                              style_table={
                                  "overflowY": "auto",
                                  "overflowX": "auto",
                                  "height": "48vh",
                                  "width": "auto"
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
                              )],
                     style={"padding-top": "1rem"}
                     )

# INFO
info_1 = dbc.Card([
            dbc.CardBody([
                html.H4("Total Branch Count", className="card-title"),
                html.P(id="info_t_b_c", className="card-text", children="")
            ]),
    ],
    style={},
)

info_2 = dbc.Card([
            dbc.CardBody([
                html.H4("Main Branch Count", className="card-title"),
                html.P(id="info_m_b_c", className="card-text", children="")
            ]),
    ],
    style={},
)

info_3 = dbc.Card([
            dbc.CardBody([
                html.H4("Longest Main Branch", className="card-title"),
                html.P(id="info_l_m_b", className="card-text", children="")
            ]),
    ],
    style={},
)

info_4 = dbc.Card([
            dbc.CardBody([
                html.H4("Shortest Main Branch", className="card-title"),
                html.P(id="info_s_m_b", className="card-text", children="")
            ]),
    ],
    style={},
)

# info_5 = dbc.Card([
#             dbc.CardBody([
#                 html.H4("Possible Errors", className="card-title"),
#                 html.P(id="info_p_e", className="card-text", children="")
#             ]),
#     ],
#     style={},
# )

info_layout = [dbc.Col(info_1), dbc.Col(info_2,), dbc.Col(info_3),
               dbc.Col(info_4)]

# Footers
# footer_layout = dbc.Row([
#     html.H6("Updated: 03-30-21 - Under Active Development", style={"color": "#ffffff"})
#     ],
#     style={"background-color": "#10366C", "margin-top": "1rem"},
#     align="end")

layout = [
    dbc.Container([
            header_layout,
            dbc.Row([
                dbc.Col([
                    dbc.Row(query_layout,
                            style={'background-color': '#10366C'},
                            justify="center",
                            align="center"
                            ),
                    dbc.Row(raw_layout,
                            style={'background-color': '#10366C'},
                            justify="center",
                            align="center"),
                    ],
                    width=3, style={"margin-right": "1rem"}),
                dbc.Col([
                    dbc.Row(plot_layout,
                            style={'background-color': '#10366C'},
                            className="h-75"
                            ),
                    dbc.Row(info_layout,
                            style={'background-color': '#10366C'},
                            className="h-25",
                            justify="around",
                            align="center"
                            )
                    ],
                    width=True)
                    ],
                    style={'background-color': "#10366C", "margin-right": "0rem", "margin-top": "1rem"},
                    ),
    ],
     fluid=True,
     style={"background-color": "#10366C", "margin-left": "1rem", "margin-bottom": "1rem"})
    ]

app.layout = html.Div(layout, style={"background-color": "#10366C", "display": "inline-flex"})


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
               Output('raw-table', 'data'),
               Output('info_t_b_c', 'children'),
               Output('info_m_b_c', 'children'),
               Output('info_l_m_b', 'children'),
               Output('info_s_m_b', 'children')
               ],
              [Input('query-button', 'n_clicks')],
              [State('source-file-dropdown', 'value'),
               State('trap-num-dropdown', 'value'),
               State('time-num-dropdown', 'value')])
def click_query(click, source_file_value, trap_value, time_value):

    if source_file_value and trap_value and time_value:
        fig, query_df, web_info = run_query(source_file_value, trap_value, time_value)
        dt_columns = [{"name": i, "id": i} for i in query_df.columns],
        dt_rows = query_df.to_dict('records'),
        return [fig,
                dt_columns[0],
                dt_rows[0],
                web_info["total_branch_count"],
                web_info["main_branch_count"],
                web_info["longest_main_branch_count"],
                web_info["shortest_main_branch_count"],
                ]

    temp_fig = go.Figure()
    temp_fig.layout.yaxis["showticklabels"] = False
    temp_fig.layout.xaxis["title"] = "Time Num"

    return [temp_fig, [], [], "", "", "", ""]


if __name__ == '__main__':

    app.run_server(debug=False)
