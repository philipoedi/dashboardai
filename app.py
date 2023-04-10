import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, dcc, html
from sqlalchemy import create_engine

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


def create_sqlite_db(dataframes):
    """
    This function takes a list of pandas dataframes and turns them into an inmemory sqlite database.
    It uses the pandas.to_sql() method to create a table for each dataframe in the list. The table name
    is the same as the dataframe name. The index of the dataframe is not saved in the database.

    :param dataframes: list of pandas dataframes
    :return: sqlite database
    """
    # create an in memory sqlite database
    engine = create_engine("sqlite:///:memory:")
    # loop through the dataframes and save them to the database
    for dataframe in dataframes:
        dataframe.to_sql(dataframe.name, engine, index=False)
    return engine


""" function that returns the tables, their column names and datatypes of the sqlite in-memory database, the table names are dictory keys and the column names and datatypes are the values as tuples"""


def get_sqlite_table_info(engine):
    """
    This function returns the tables, their column names and datatypes of the sqlite in-memory database.
    The table names are dictory keys and the column names and datatypes are the values as tuples.

    :param engine: sqlite database
    :return: dictionary with table names as keys and column names and datatypes as values
    """
    # get the table names from the database
    table_names = engine.table_names()
    # create an empty dictionary to store the table info
    table_info = {}
    # loop through the table names
    for table in table_names:
        # get the column names and datatypes of the table
        table_info[table] = engine.execute(f"PRAGMA table_info({table})").fetchall()
    return table_info


""" function that takes a string and a list of strings, checks if any string of the list is contained in the string, case insensitive"""


def check_string_in_list(string, list_of_strings):
    """
    This function takes a string and a list of strings, checks if any string of the list is contained in the string, case insensitive.

    :param string: string to check
    :param list_of_strings: list of strings to check
    :return: boolean
    """
    # loop through the list of strings
    for item in list_of_strings:
        # check if the string is contained in the item, case insensitive
        if item.lower() in string.lower():
            return True
    return False


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
