import mysql.connector
from DataManagement import DataManagement


class DatabaseManager(DataManagement):

    #Connects to the database given the host, user, password and name of the database
    # The tables are saved in the following nested dictionary:
    # tables{
    #   tableName :
    #   columns {
    #   columName: columnValues ([val1, val2, val3..., val20])
    #   }
    # }
    def __init__(self, data):

        self.host = data['host']
        self.user = data['user']
        self.password = data['password']
        self.charset = 'utf8mb4'
        self.database = data['database']
        self.tables = dict()

        try:
            self.connection = mysql.connector.connect(host= self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.database,
                                    charset=self.charset)

            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.connection.cursor()
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()
                print("You're connected to database: ", record)

                self.cursor.execute("show tables;")
                tables = self.cursor.fetchall()

                #Loads all tables from the database
                for t in tables:
                    sql_select_Query = "select * from " + t[0]
                    self.cursor.execute(sql_select_Query)
                    self.cursor.fetchall()
                    columnNames = self.cursor.column_names
                    columnDict = dict()

                    #For each column in  the table, it is saves a dictionary of columns, whith their respective name and a list of a maximum of 20 values
                    # from the column. In case that there isn't any values in the column, the sample value assigned is a string: ["term"]
                    for c in columnNames:
                        sql_select_Query = "select " + c + " from " + t[0] + " LIMIT 20"
                        self.cursor.execute(sql_select_Query)
                        values = self.cursor.fetchall()
                        if(len(values) > 0):
                            columnDict.update({c : values})
                        else:
                            columnDict.update({c : ["term"]})
                            
                    self.tables.update({t[0] : columnDict})
                self.cursor.close()
                self.connection.close()
                    
        except:
            print("Error while connecting to MySQL")

    # Returns all the tables from the databse
    def get_tables(self):
        return list(self.tables.keys())
    # Returns all the columns given a the name of a table
    def get_table_columns(self, table):
        return list(self.tables[table].keys())
    # Returns all the values of the given column of a given table
    def get_column_values(self, table, column):
        return list(self.tables[table][column])