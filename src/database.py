import sqlite3

conn = sqlite3.connect('app_data.db')
# Create cursor object with execute method to perform SQL command
c = conn.cursor()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()


if __name__ == "__main__":
    print("Create database to store app data.")