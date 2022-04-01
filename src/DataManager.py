from ManagerFactory import ManagerFactory as mf

class DataManager():
    def __init__(self):
        self.tables = dict()
        
    def serialize(self, data):
        self.tables = mf.serialize(data)


        # Returns all the tables from the databse
    def get_tables(self):
        return list(self.tables.keys())
    # Returns all the columns given a the name of a table
    def get_table_columns(self, table):
        return list(self.tables[table].keys())
    # Returns all the values of the given column of a given table
    def get_column_values(self, table, column):
        return self.tables[table][column]