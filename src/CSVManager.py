from DataManagement import DataManagement
import glob
import os
import pandas as pd
class CSVManager(DataManagement):
    def __init__(self, data):
        self.folder = data['folder']
        self.separator = data['separator']
        self.tables = dict()

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

        files = glob.glob(ROOT_DIR + "/inputs/" + self.folder + "/*.csv")
        for f in files:
            fileName = os.path.basename(f)
            fileName = fileName.split('.')[0].lower()
            df = pd.read_csv(f, sep=self.separator)
            print (df.columns)
            #with open(f, newline='') as csvfile:
            #    reader = csv.DictReader(csvfile)
            #    dict_csv = dict(list(reader)[0])
            #    print(dict_csv)

    # Returns all the tables from the databse
    def get_tables(self):
        return list(self.tables.keys())
    # Returns all the columns given a the name of a table
    def get_table_columns(self, table):
        return list(self.tables[table].keys())
    # Returns all the values of the given column of a given table
    def get_column_values(self, table, column):
        return self.tables[table][column]
