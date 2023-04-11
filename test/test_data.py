""" tests in pytest for the data module """

import os
import sys

import pandas as pd
import pytest
from sqlalchemy import create_engine

from dashboardai.data import create_sqlite_db, get_sqlite_table_info


def test_create_sqlite_db():
    """test the create_sqlite_db function"""
    # create a list of pandas dataframes
    dataframes = [
        pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}),
        pd.DataFrame({"col1": [5, 6], "col2": [7, 8]}),
    ]
    dataframes[0].name = "table1"
    dataframes[1].name = "table2"
    # create an in memory sqlite database from the dataframes
    engine = create_sqlite_db(dataframes)
    # get the table names from the database
    table_names = engine.table_names()
    # check if the table names are the same as the dataframe names
    assert table_names == ["table1", "table2"]


def test_get_sqlite_table_info():
    """test the get_sqlite_table_info function"""
    # create a list of pandas dataframes
    dataframes = [
        pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}),
        pd.DataFrame({"col1": [5, 6], "col2": [7, 8]}),
    ]
    # create an in memory sqlite database from the dataframes
    dataframes[0].name = "table1"
    dataframes[1].name = "table2"
    engine = create_sqlite_db(dataframes)
    # get the table info from the database
    table_info = get_sqlite_table_info(engine)
    # check if the table info is the same as the dataframe info
    assert table_info == {
        "table1": [
            {"name": "col1", "dtype": "BIGINT"},
            {"name": "col2", "dtype": "BIGINT"},
        ],
        "table2": [
            {"name": "col1", "dtype": "BIGINT"},
            {"name": "col2", "dtype": "BIGINT"},
        ],
    }
