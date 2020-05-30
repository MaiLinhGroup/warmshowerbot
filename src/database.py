import sqlite3
import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

db_name = 'app_data.db'

def write_praise_data(user_id, user_name):
    pass
    
def add_user(user_id, user_name):
    add_user_query = "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)"
    now = datetime.datetime.now()

    with sqlite3.connect(database=db_name) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(add_user_query, (user_id, user_name, now, now))
        except sqlite3.Error as e:
            logging.error("SQLite ERROR: %s" % e)
            raise
        else:
            conn.commit()


if __name__ == "__main__":
    print("Create database to store app data.")