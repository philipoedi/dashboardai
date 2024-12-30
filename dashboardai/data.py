import base64
import io

import pandas as pd
from dash import html
from sqlalchemy import create_engine, inspect, text


def create_sqlite_db(dataframes):
    """
    This function takes a list dicts with keys name (the table name) and data (pandas dataframes) and turns them into an inmemory sqlite database.
    It uses the pandas.to_sql() method to create a table for each dataframe in the list. The index of the dataframe is not saved in the database.

    :param dataframes: list of pandas dataframes
    :return: sqlite database
    """
    # create an in memory sqlite database
    engine = create_engine("sqlite:///:memory:")
    # loop through the dataframes and save them to the database
    for df in dataframes:
        df["data"].to_sql(df["name"], engine, index=False)
    return engine


def get_sqlite_table_info(engine):
    """
    This function returns the tables, their column names and datatypes of the sqlite in-memory database.
    The table names are dictionary keys and the column names and datatypes are the values as tuples.

    :param engine: sqlite database
    :return: dictionary with table names as keys and column names and datatypes as values
    """
    # get the table names from the database using inspector
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    # create an empty dictionary to store the table info
    table_info = {}

    # Create a connection to execute queries
    with engine.connect() as conn:
        # loop through the table names
        for table in table_names:
            # get the column names and datatypes of the table
            table_info[table] = [
                {"name": tup[1], "dtype": tup[2]}
                for tup in conn.execute(text(f"PRAGMA table_info({table})")).fetchall()
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
    print(f"Parsing file: {filename}")  # Debug print
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            print(f"Successfully parsed CSV with columns: {df.columns}")  # Debug print
            return df
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            return df
        else:
            print(f"Unsupported file type: {filename}")  # Debug print
            return None
    except Exception as e:
        print(f"Error parsing file: {str(e)}")  # Debug print
        return html.Div(["There was an error processing this file."])


def create_duckdb(dataframes):
    """
    This function takes a list of pandas dataframes and turns them into an in-memory DuckDB database.
    It uses the pandas.to_sql() method to create a table for each dataframe in the list. The table name
    is the same as the dataframe name. The index of the dataframe is not saved in the database.
     :param dataframes: list of pandas dataframes
    :return: DuckDB database
    """
    # create an in memory DuckDB database
    con = duckdb.connect(":memory:")
    # loop through the dataframes and save them to the database
    for dataframe in dataframes:
        dataframe.to_sql(dataframe.name, con, index=False)
    return con


def get_duckdb_table_info(con):
    """
    This function returns the tables, their column names and datatypes of the DuckDB in-memory database.
    The table names are dictionary keys and the column names and datatypes are the values as tuples.
     :param con: DuckDB database
    :return: dictionary with table names as keys and column names and datatypes as values
    """
    # get the table names from the database
    table_names = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    # create an empty dictionary to store the table info
    table_info = {}
    # loop through the table names
    for table in table_names:
        # get the column names and datatypes of the table
        table_info[table[0]] = [
            {"name": column[0], "dtype": column[1]}
            for column in con.execute(f"PRAGMA table_info('{table[0]}')").fetchall()
        ]
    return table_info
