import io

import pandas as pd
from sqlalchemy import create_engine


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
        table_info[table] = [
            {"name": tup[1], "dtype": tup[2]}
            for tup in engine.execute(f"PRAGMA table_info({table})").fetchall()
        ]
    return table_info


def query_sqlite_db(engine, query):
    """
    This function takes a sqlite database and a query string and returns the result of the query as a pandas dataframe.
    :param engine: sqlite database
    :param query: query string
    :return: pandas dataframe
    """
    # use the pandas.read_sql_query() method to execute the query and return the result as a dataframe
    return pd.read_sql_query(query, engine)


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
