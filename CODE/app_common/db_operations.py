
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import mysql.connector

def export_to_sql(df):
    db_user = 'root'
    db_password = '12345678'
    db_host = 'localhost' 
    db_name = 'stocks'

    engine_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"

    try:
        engine = sqlalchemy.create_engine(engine_url)
        df.to_sql(name='stocks_data', con= engine, if_exists='replace', index=False)
    except Exception as e:
        print(f"Exception has thrown as below: \n {e} ")



def create_db_objects():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678"
        )

        cursor = connection.cursor()
        # create db
        cursor.execute("CREATE DATABASE IF NOT EXISTS stocks;")

        # create table
        create_stocks_table = '''create table IF NOT EXISTS stocks_data 
        ( 
        ticker nvarchar(100), day DATETIME, month nvarchar(10),
        open float, close float, high float,low float, volume float

        ) '''

        cursor.execute("USE stocks")
        cursor.execute(create_stocks_table)

        connection.commit()
        print('Database  Tables created successfully')
    except Exception as e:
        print(f"Exception thrown \n {e}")

def get_table_data(mySQLcursor, table_name):
    query = f"SELECT * FROM {table_name}"
    mySQLcursor.execute(query)
    db_data = mySQLcursor.fetchall()
    return db_data

def get_query_data(mySQLcursor, query):
    mySQLcursor.execute(query)
    db_data = mySQLcursor.fetchall()
    return db_data

def get_db_data():
    db_name = "stocks"
    table_name = "stocks_data"

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database=db_name
    )

    mySQLcursor = connection.cursor()

    stocks_data = get_table_data(mySQLcursor, table_name)
    column_names = [ 'ticker', 'day', 'month', 'open', 'close', 'high', 'low', 'volume']
    stocks_df = pd.DataFrame(stocks_data, columns=column_names)
    return stocks_df