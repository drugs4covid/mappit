import mysql.connector


class DatabaseManager(object):
    def __init__(self, database, user, password, host = 'localhost', charset='utf8mb4'):
            self.host = host
            self.user = user
            self.password = password
            self.charset = charset
            self.database = database
            try:
                self.connection = mysql.connector.connect(host='localhost',
                                     user='root',
                                     password='gtfs',
                                     database='gtfs',
                                     charset='utf8mb4')

                if self.connection.is_connected():
                        db_Info = self.connection.get_server_info()
                        print("Connected to MySQL Server version ", db_Info)
                        self.cursor = self.connection.cursor()
                        self.cursor.execute("select database();")
                        record = self.cursor.fetchone()
                        print("You're connected to database: ", record)
            except:
                print("Error while connecting to MySQL")

    def get_tables(self):
        self.cursor.execute("show tables;")
        myresult = self.cursor.fetchall()
        return myresult

    def get_table_columns(self, table):
        sql_select_Query = "select * from " + table
        self.cursor.execute(sql_select_Query)
        # get all records
        records = self.cursor.fetchall()
        return self.cursor.column_names