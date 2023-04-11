import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, dcc, html

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


""" function that takes a string and a list of strings, checks if any string of the list is contained in the string, case insensitive"""


def check_string_in_list(string, list_of_strings):
    """
    This function takes a string and a list of strings, checks if any string of the list is contained in the string, case insensitive.
    :param string: string to check
    :param list_of_strings: list of strings to check
    :return: boolean
    """
    # use the string.lower() method to check if any of the strings in the list are contained in the string, case insensitive
    return any(item.lower() in string.lower() for item in list_of_strings)


def query_sqlite_db(engine, query):
    """
    This function takes a sqlite database and a query string and returns the result of the query as a pandas dataframe.
    :param engine: sqlite database
    :param query: query string
    :return: pandas dataframe
    """
    # use the pandas.read_sql_query() method to execute the query and return the result as a dataframe
    return pd.read_sql_query(query, engine)


def generate_table(dataframe, max_rows=10):
    """
    This function creates an interactive DataTable from a given dataframe, with a maximum of 10 rows.
    It takes the columns in the dataframe and sets them as the columns of the DataTable. It also takes
    the values in the dataframe and converts them into a dictionary format before setting them as the
    data of the DataTable. The maximum number of rows to display can be changed through the max_rows argument.

    :param dataframe: dataframe to convert to DataTable
    :param max_rows: maximum number of rows to display
    :return: DataTable object
    """
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        data=dataframe.to_dict("records"),
        page_size=max_rows,
        style_table={"overflowX": "scroll"},
        filter_action="native",
        sort_action="native",
    )


# Define a function to convert the contents of an uploaded file to a pandas dataframe
def parse_contents(contents, filename):
    """
    This function takes the contents and filename of an uploaded file and returns a pandas dataframe.
    :param contents:
    :param filename:
    :return:
    """
    # Check if file is an Excel file and parse if it is
    if "xlsx" in filename:
        # Assume the Excel file has only one sheet
        df = pd.read_excel(io.BytesIO(contents[0]), sheet_name=0)
    # Check if file is a CSV file and parse if it is
    elif "csv" in filename:
        # Assume the CSV file uses comma delimiter and UTF-8 encoding
        df = pd.read_csv(io.StringIO(contents[0].decode("utf-8")), delimiter=",")
    else:
        # If file is not an Excel or CSV file, return an empty dataframe
        df = pd.DataFrame()

    return df


@app.callback(
    Output("output-data", "children"),
    Input("upload-data", "contents"),
    Input("upload-data", "filename"),
)
def update_output(contents, filename):
    # If no files have been uploaded, return an empty list
    if contents is None:
        return html.Div("No files uploaded.")

    # Parse contents of each uploaded file and store in a list
    df_list = [parse_contents(contents[i], filename[i]) for i in range(len(contents))]

    # Return a list of dataframes as a string representation of tables
    return [
        html.Div(
            [
                html.H5(filename[i]),
                dcc.Table(
                    # Convert dataframe to a list of dictionaries for each row
                    data=df_list[i].to_dict("records"),
                    columns=[{"name": col, "id": col} for col in df_list[i].columns],
                ),
                html.Hr(),
            ]
        )
        for i in range(len(df_list))
    ]


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
