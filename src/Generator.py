import sqlite3
import pandas as pd

conn = sqlite3.connect('test_database')
query = open('/examples/datasets/sql/1/mysql_schema.sql', 'r')
df = pd.read_sql_query(query.read(),connection)
print(df)
query.close()
