import uuid

import dash
import dash_bootstrap_components as dbc
import numpy as np
import openai
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State

from dashboardai.api import (
    check_string_in_list,
    combine_prompts,
    combine_prompts_graph,
    create_dataframe_definition_prompt,
    create_table_definition_prompt,
    handle_response,
    handle_response_graph,
    send_to_openai,
)
from dashboardai.data import (
    create_sqlite_db,
    get_sqlite_table_info,
    parse_contents,
    query_sqlite_db,
)
from dashboardai.visualizations import generate_table

# load the gapminder data to a dataframe
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

import plotly.graph_objs as go

x = [1, 2, 3, 4, 5]
y = [2, 4, 1, 6, 3]

data = [go.Scatter(x=x, y=y, mode="lines")]

layout = go.Layout(title="My Line Chart")

fig2 = go.Figure(data=data, layout=layout)


# Define a function to convert the contents of an uploaded file to a pandas dataframe


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    [
        dcc.Store(id="memory"),
        dcc.Store(id="table-results"),
        dbc.Row(
            [
                dbc.Col(
                    # file picker component in dcc
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(
                            ["Drag and Drop or ", html.A("Select Files")]
                        ),
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "margin": "10px",
                        },
                        # Allow multiple files to be uploaded
                        multiple=True,
                        # set maximum file size to 100 mb
                        max_size=100000000,
                    )
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        # table component in dash_table
                        html.Div(id="table", children=[generate_table(df)]),
                        dbc.Input(
                            id="chat_input_table",
                            type="text",
                            placeholder="Enter a value...",
                            debounce=True,
                            style={"width": "100%"},
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="graph2", figure=fig2),
                        # text input component in dbc
                        dbc.Input(
                            id="chat_input_graph",
                            type="text",
                            placeholder="Enter a value...",
                            debounce=True,
                            style={"width": "100%"},
                        ),
                    ],
                    width=6,
                ),
            ],
            align="center",
        ),
    ]
)


@app.callback(
    Output("memory", "data"),
    [Input("upload-data", "contents"), State("upload-data", "filename")],
)
def make_sqlite_db(contents, filename):
    print("Upload callback triggered")  # Debug print
    print(f"Contents: {contents is not None}")  # Debug print
    print(f"Filename: {filename}")  # Debug print

    if contents is not None:
        dfs = {
            name.rsplit(".", 1)[0]: parse_contents(content, name).to_dict("records")
            for content, name in zip(contents, filename)
        }
        print(f"Processed dataframes: {list(dfs.keys())}")  # Debug print
        return dfs
    return None  # Add explicit return for when contents is None


@app.callback(
    Output("table", "children"),
    Output("table-results", "data"),
    [Input("chat_input_table", "value"), State("memory", "data")],
)
def update_table(text_input, dfs):
    print("Update table callback triggered")  # Debug print
    print(f"DFs available: {dfs}")  # Debug print

    if dfs is None:
        return html.Div(["No file selected"]), None
    try:
        if text_input == "":
            dfs = [{"name": name, "data": pd.DataFrame(dfs[name])} for name in dfs]
            return generate_table(dfs[0]["data"]), dfs[0]["data"].to_dict("records")
        else:
            engine = create_sqlite_db(
                [{"name": name, "data": pd.DataFrame(dfs[name])} for name in dfs]
            )
            db_schema = get_sqlite_table_info(engine)
            fixed_sql_prompt = create_table_definition_prompt(db_schema)
            prompt = combine_prompts(fixed_sql_prompt, text_input)
            response = send_to_openai(prompt, stop=[";", "#"])
            proposed_query_postprocessed = handle_response(response)
            result = query_sqlite_db(engine, proposed_query_postprocessed)
            return generate_table(result), result.to_dict("records")
    except Exception as e:
        print(f"Error in update_table: {str(e)}")  # Debug print
        return html.Div([f"Error processing data: {str(e)}"]), None


@app.callback(
    Output("graph2", "figure"),
    [Input("chat_input_graph", "value"), State("table-results", "data")],
)
def update_graph(text_input, results):
    if results is None or text_input == "":
        return {}
    else:
        data = pd.DataFrame(results)
        fixed_prompt = create_dataframe_definition_prompt(data)
        prompt = combine_prompts_graph(fixed_prompt, text_input)
        response = send_to_openai(prompt, stop=["fig.show()"])
        # proposed_query_postprocessed = handle_response_graph(response)
        fig = go.Figure()
        print("##################")
        print(prompt)
        print(response["choices"][0]["text"])
        query = response["choices"][0]["text"].replace("fig.show()", "")
        # exec(proposed_query_postprocessed)
        exec(query)
        return fig


if __name__ == "__main__":
    app.run_server(debug=True)
