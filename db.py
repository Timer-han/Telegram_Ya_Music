import sqlite3
from sqlite3 import Error

def create_connection(path: str) -> sqlite3.Connection:
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection: sqlite3.Connection, query: str) -> None:
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

        
        
# connection = create_connection("./users.db")

# create_users_table = """
# CREATE TABLE IF NOT EXISTS users (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   token TEXT NOT NULL
# );
# """

# execute_query(connection, create_users_table)