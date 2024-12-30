""" tests in pytest for the data module """

import os
import sys

import pandas as pd
import pytest
from sqlalchemy import create_engine, inspect, text

from dashboardai.data import (
    create_sqlite_db,
    get_sqlite_table_info,
    parse_contents,
    query_sqlite_db,
)


@pytest.fixture
def test_data():
    testdata1 = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
    testdata2 = pd.DataFrame({"id": [4, 5], "name": ["David", "Eve"]})
    dataframes = [
        {"name": "table1", "data": testdata1},
        {"name": "table2", "data": testdata2},
    ]
    return dataframes


def test_create_sqlite_db(test_data):
    engine = create_sqlite_db(test_data)
    # Verify that the expected tables were created
    inspector = inspect(engine)
    assert "table1" in inspector.get_table_names()
    assert "table2" in inspector.get_table_names()
    # Verify that the tables contain the expected data
    conn = engine.connect()
    result1 = conn.execute(text("SELECT * FROM table1 ORDER BY id")).fetchall()
    result2 = conn.execute(text("SELECT * FROM table2 ORDER BY id")).fetchall()
    assert result1 == [(1, "Alice"), (2, "Bob"), (3, "Charlie")]
    assert result2 == [(4, "David"), (5, "Eve")]
    # Clean up
    conn.close()


""" tests te get_sqlite_table_info function using the test_data fixture"""


def test_get_sqlite_table_info(test_data):
    engine = create_sqlite_db(test_data)
    table_info = get_sqlite_table_info(engine)
    assert table_info == {
        "table1": [
            {"name": "id", "dtype": "BIGINT"},
            {"name": "name", "dtype": "TEXT"},
        ],
        "table2": [
            {"name": "id", "dtype": "BIGINT"},
            {"name": "name", "dtype": "TEXT"},
        ],
    }


"""test the query_sqlite_db function using the test_data fixture"""


def test_query_sqlite_db(test_data):
    engine = create_sqlite_db(test_data)
    query = "SELECT * FROM table1"
    result = query_sqlite_db(engine, query)
    assert result.equals(test_data[0]["data"])


""" test the parse_contents function, filename is a string and contents is a list of bytes, for csv files
first write a csv file to disk, then read it back in as a list of bytes, then delete the file from disk"""


def test_parse_contents_csv():
    """test the parse_contents function for csv files"""
    test_list = [
        "data:text/csv;base64,Y291bnRyeSxyZWdpb24saW5jb21lLGluY29tZV9sZXZlbCxsaWZlX2V4cCxjbzIsY28yX2NoYW5nZSxwb3B1bGF0aW9uDQpBZmdoYW5pc3RhbixBc2lhLDIuMDMsTGV2ZWwgMSw2Mi43LDAuMjU0LGluY3JlYXNlLDM3LjINCkFsYmFuaWEsRXVyb3BlLDEzLjMsTGV2ZWwgMyw3OC40LDEuNTksaW5jcmVhc2UsMi44OA0KQWxnZXJpYSxBZnJpY2EsMTEuNixMZXZlbCAzLDc2LDMuNjksaW5jcmVhc2UsNDIuMg0KQW5kb3JyYSxFdXJvcGUsNTguMyxMZXZlbCA0LDgyLjEsNi4xMixkZWNyZWFzZSwwLjA3Nw0KQW5nb2xhLEFmcmljYSw2LjkzLExldmVsIDIsNjQuNiwxLjEyLGRlY3JlYXNlLDMwLjgNCkFudGlndWEgYW5kIEJhcmJ1ZGEsQW1lcmljYXMsMjEsTGV2ZWwgMyw3Ni4yLDUuODgsaW5jcmVhc2UsMC4wOTYzDQpBcmdlbnRpbmEsQW1lcmljYXMsMjIuNyxMZXZlbCAzLDc2LjUsNC40MSxkZWNyZWFzZSw0NC40DQo="
    ]
    # call the parse_contents function
    result = parse_contents(test_list[0], "test.csv")
    # check if the result is the same as the dataframe
    assert result.equals(pd.read_csv("test/gapminder.csv"))


def test_parse_contents_xlsx():
    """test the parse_contents function for xlsx files"""
    test_list = [
        "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,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"
    ]
    # call the parse_contents function
    result = parse_contents(test_list[0], "test.xlsx")
    # check if the result is the same as the dataframe
    assert result.equals(pd.read_excel("test/gapminder.xlsx"))
