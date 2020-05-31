import datetime
import logging
import os
import sqlite3 as db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

db_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'app_data.db'))
db_sql_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'setup_database.sql'))


def init():
    # Initalise the database by setup all the tables
    # like described in the setup script at start up
    with open(db_sql_path) as f, db.connect(db_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.executescript(f.read())
        except db.Error as e:
            logging.error("DB ERROR: %s" % e)
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
    with db.connect(db_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(add_user_query, add_user_data)
        except db.Error as e:
            logging.error("DB ERROR: %s" % e)
            raise
        else:
            conn.commit()

def get_user(user_id):
    with db.connect(db_path) as conn:
        cursor = conn.cursor()
        if user_id is not None:
            cursor.execute("SELECT * FROM users WHERE slack_user_id = ?", (user_id,))
        else:
            cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users
        

if __name__ == "__main__":
    print("Database module")
    init()
    print("Current users:")
    print(get_user(None))