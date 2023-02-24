import sqlite3
from security import DB_NAME


def db_request(req, *params):
    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    return [conn, cur.execute(req, *params)]


def setup_db():
    try:
        db_request("""
            CREATE TABLE users(
                id INTEGER PRIMARY KEY,
                username text
            )
        """)

    except Exception as e:
        print(e)

    try:
        db_request("""
            CREATE TABLE operators(
                id INTEGER PRIMARY KEY,
                status text,
                client_id text 
            )
        """)
    except Exception as e:
        print(e)
