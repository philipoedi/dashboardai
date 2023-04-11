import pandas as pd
from dash import dash_table


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
