import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file, isolation_level=None)

    except Error as e:
        print(e)
    return conn;


def insert_attendance(conn, identity):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = '''INSERT INTO attendance (id,name,date_in,time_in,time_out) values (?,?,?,?,?)'''
    # print(sql)

    cur = conn.cursor()
    cur.execute(sql, identity)
    conn.commit()
    # print('insertion completed')
    return cur.lastrowid

# if __name__ == '__main__':
#     create_connection(r"attendance.db")