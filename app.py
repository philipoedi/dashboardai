import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, dcc, html

from dashboardai.visualizations import generate_table

# load the gapminder data to a dataframe
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)


import plotly.graph_objs as go

x = [1, 2, 3, 4, 5]
y = [2, 4, 1, 6, 3]

data = [go.Scatter(x=x, y=y, mode="lines")]

layout = go.Layout(title="My Line Chart")

fig = go.Figure(data=data, layout=layout)


# Define a function to convert the contents of an uploaded file to a pandas dataframe


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    [
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
                        generate_table(df),
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
                        dcc.Graph(id="graph2", figure=fig),
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
if __name__ == "__main__":
    app.run_server(debug=True)
