import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn

def write_praise_data(cursor, user_id, user_name):
    pass
    


def check_db_for_user(cursor, user_id, user_name):
    try:
        cursor.execute("SELECT * FROM user WHERE user_id=?", user_id)
        exists = cursor.fetchall()
        if not exists:
            cursor.execute("INSERT INTO user(user_id, user_name) VALUES (?,?)", user_id, user_name)
        return True
    except sqlite3.Error as e:
        print(e)
        return False



if __name__ == "__main__":
    print("Create database to store app data.")