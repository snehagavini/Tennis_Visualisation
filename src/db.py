import sqlite3
from sqlite3 import Error

class db(object):
    """
    sqlite3 database connector
    """
    def __init__(self, database):
        """Creating the database connection to a SQLite database"""
        self.conn = None
        try:
            self.conn = sqlite3.connect(database)
            print(sqlite3.version)
        except Error as e:
            print(e)
        
        return self.conn

    def create_table(self, create_table_sql):
        """
        Create a table from the create_table_sql statement
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """

        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
    
    def insert_data()
