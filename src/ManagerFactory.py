import mysql.connector
from mysql.connector import FieldType
import glob
import os
import pandas as pd
class ManagerFactory:

    def serialize(data):
        serializer = get_serializer(data['format'])
        return serializer(data)

def get_serializer(format):
    if format.lower() == 'database':
        return _serialize_to_DB
    elif format.lower() == 'dump_database':
        return _serialize_to_dump_DB
    elif format.lower() == 'csv':
        return _serialize_to_CSV
    elif format.lower() == 'json':
        return _serialize_to_JSON
    elif format.lower() == 'xls':
        return _serialize_to_XLS
    else:
        raise ValueError(format)

def _serialize_to_dump_DB(data):
    tables_dict = dict()
    file = ""
    sql = ""
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
    with open(ROOT_DIR + "/Inputs/" + data['file'], 'r', encoding='utf-8') as f:
        for chunk in iter(lambda: f.read(1024), ''):
            sql += chunk
    #file = open(data['file'])

    cnx = mysql.connector.connect(user='u', password='p', host='h', database='d')
    cursor = cnx.cursor()
    try:
        cursor.execute(sql, multi = True)
    except:
        l = 1000
        o = 0

    tables = cursor.fetchall()
    for t in tables:
        sql_select_Query = "select * from " + t[0]
        cursor.execute(sql_select_Query)
        cursor.fetchall()
        columnNames = cursor.column_names
        columnDict = dict()

        #For each column in  the table, it is saves a dictionary of columns, whith their respective name and a list of a maximum of 20 values
        # from the column. In case that there isn't any values in the column, the sample value assigned is a string: ["term"]
        for c in columnNames:
            #sql_select_Query = "select " + c + " from " + t[0] + "WHERE emp_no = %s", (123,)
            cursor.execute("select " + c + " from " + t[0])
            desc = cursor.description
            val = FieldType.get_info(desc[0][1])
            columnDict.update({c : val})

        tables_dict.update({t[0] : columnDict})
    cursor.close()
    return tables_dict
    cnx.close()
def _serialize_to_DB(data):
    tables_dict = dict()
    try:
        connection = mysql.connector.connect(
                                host= data['host'],
                                port=data['port'],
                                user=data['user'],
                                password=data['password'],
                                database=data['database'],
                                charset='utf8mb4')

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            cursor.execute("show tables;")
            tables = cursor.fetchall()

            #Loads all tables from the database
            for t in tables:
                sql_select_Query = "select * from " + t[0]
                cursor.execute(sql_select_Query)
                cursor.fetchall()
                columnNames = cursor.column_names
                columnDict = dict()

                #For each column in  the table, it is saves a dictionary of columns, whith their respective name and a list of a maximum of 20 values
                # from the column. In case that there isn't any values in the column, the sample value assigned is a string: ["term"]
                for c in columnNames:
                    #sql_select_Query = "select " + c + " from " + t[0] + "WHERE emp_no = %s", (123,)
                    cursor.execute("select " + c + " from " + t[0])
                    desc = cursor.description
                    val = FieldType.get_info(desc[0][1])
                    columnDict.update({c : val})
                        
                tables_dict.update({t[0] : columnDict})
            cursor.close()
            connection.close()
        return tables_dict
            
    except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

def _serialize_to_CSV(data):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
    try:
        files = glob.glob(ROOT_DIR + "/Inputs/" + data['folder'] + "/*.csv")
    except:
        try:
            files = glob.glob(data['folder'] + "/*.csv")
        except:
            print("Loding error: Incorrect path.")
    return loadDF(files, data)

def _serialize_to_XLS(data):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
    try:
        files = glob.glob(ROOT_DIR + "/Inputs/" + data['folder'] + "/*.xls")
    except:
        try:
            files = glob.glob(data['folder'] + "/*.csv")
        except:
            print("Loding error: Incorrect path.")
    return loadDF(files, data)

def _serialize_to_JSON(data):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
    try:
        files = glob.glob(ROOT_DIR + "/Inputs/" + data['folder'] + "/*.json")
    except:
        try:
            files = glob.glob(data['folder'] + "/*.csv")
        except:
            print("Loding error: Incorrect path.")
    return loadDF(files, data)

def loadDF(files, data):
    tables_dict = dict()
    for f in files:
        fileName = os.path.basename(f)
        fileName = fileName.split('.')[0].lower()
        if (data['format'].lower() == 'csv'):
            df = pd.read_csv(f, sep= data['separator'])
        elif (data['format'].lower() == 'json'):
            df = pd.read_json(f)
        elif (data['format'].lower() == 'xls'):
            df = pd.read_excel(f, engine='openpyxl')
        columnDict = dict()
        i = 0
        for c in df.columns:
            val = ""
            if (df[c].dtype == 'object'):
                val = "STRING"
            elif (df[c].dtype == 'int64'):
                val = "INT64"
            elif (df[c].dtype == 'datetime64[ns]'):
                val = "DATETIME"
            elif (df[c].dtype == 'float64'):
                val = "FLOAT"
            elif (df[c].dtype == 'bool'):
                val = "BOOL"
            columnDict.update({c : val})
            i+=1
        tables_dict.update({fileName : columnDict})
    return tables_dict