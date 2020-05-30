import datetime
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

db_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'app_data.db'))
db_sql_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'setup_database.sql'))


def init():
    with open(db_sql_path) as f, sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.executescript(f.read())
        except sqlite3.Error as e:
            logging.error("SQLite ERROR: %s" % e)
            raise
        else:
            conn.commit()

def write_praise_data(user_id, user_name):
    pass
    
def add_user(user_id, user_name):
    add_user_query = """INSERT OR IGNORE INTO users 
                        (id,slack_user_id,slack_user_name) 
                        VALUES (?, ?, ?)"""
    
    add_user_data = [None, user_id, user_name]

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(add_user_query, add_user_data)
        except sqlite3.Error as e:
            logging.error("SQLite ERROR: %s" % e)
            raise
        else:
            conn.commit()


if __name__ == "__main__":
    print("Create database to store app data.")