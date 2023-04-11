""" tests in pytest for the visualizations module"""

import pandas as pd
from dash import dash_table

from dashboardai.visualizations import generate_table


def test_generate_table():
    """test the generate_table function"""
    # create a pandas dataframe
    dataframe = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    # create a dash table from the dataframe
    table = generate_table(dataframe)
    # check if the table is a dash table
    assert isinstance(table, dash_table.DataTable)
    # check if the table has the correct columns
    assert table.columns == [
        {"name": "col1", "id": "col1"},
        {"name": "col2", "id": "col2"},
    ]
    # check if the table has the correct data
    assert table.data == [{"col1": 1, "col2": 3}, {"col1": 2, "col2": 4}]
    # check if the table has the correct page size
    assert table.page_size == 10
    # check if the table has the correct style
    assert table.style_table == {"overflowX": "scroll"}
    # check if the table has the correct filter action
    assert table.filter_action == "native"
    # check if the table has the correct sort action
    assert table.sort_action == "native"
