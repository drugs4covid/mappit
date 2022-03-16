from abc import ABC, abstractmethod

class DataManagement(ABC):

    @abstractmethod
    def __init__(self, dataInitialization):
        pass

    @abstractmethod
    def get_tables(self):
        pass

    @abstractmethod
    def get_table_columns(self, table):
        pass

    @abstractmethod
    def get_column_values(self, table, column):
        pass