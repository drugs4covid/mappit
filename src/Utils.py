from decimal import Decimal
import numbers
from unicodedata import decimal
import numpy as numpy
import datetime

def levenshteinDistanceDP(str1, str2):
    distances = numpy.zeros((len(str1) + 1, len(str2) + 1))

    for t1 in range(len(str1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(str2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(str1) + 1):
        for t2 in range(1, len(str2) + 1):
            if (str1[t1-1] == str2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1
    return distances[len(str1)][len(str2)]
    
#min(1, 1 - abs(t1-t2)/len(str1))

def string_distance(str1, str2):
    distances = numpy.zeros(len(str1))
    streak = 0
    for x in range(0, len(str1)):
        for y in range(x, len(str2)):
            char1 = str1[x].lower()
            char2 = str2[y].lower()
            if char1 == char2:
                val = min(1, 1 - abs(x-y)/(max(len(str1), len(str2))))
                #print(val)
                if distances[x] < val:
                    distances[x] = val + streak
                if val == 1:
                    streak += 0.1
                    break
    #print(distances)
    return numpy.sum(distances)/(max(len(str1), len(str2)))

def jaccard_distance(str1, str2):
    intersection = len(list(set(str1).intersection(str2)))
    union = (len(str1) + len(str2)) - intersection
    return 1-(float(intersection) / union)

def jaro_distance(str1,str2):
    if (str1==str2):
        return 1.0

    len1=len(str1)
    len2=len(str2)

    if (len1==0 or len2==0):
        return 0.0

    max_dist=(max(len1, len2)//2)-1

    match=0

    hash_str1=[0]*len1
    hash_str2=[0]*len2

    for i in range(len1):
        for j in range(max(1,i-max_dist),min(len2, i+max_dist+1)):
            if (str1[i]==str2[j] and hash_str2[j]==0):
                hash_str1[i]==1
                hash_str2[j]==1
                match+=1
                break

    if (match==0):
        return 0.0

    t=0
    point=0

    for i in range(len1):
        if (hash_str1[i]):
            while (hash_str2[point]==0):
                point+=1
            if (str1[i]!=str2[point]):
                point+=1
                t+=1
            else:
                point+=1
            # global t
            t/=2

    return 1-((match/len1+match/len2+(match-t)/match)/3.0)


def lcs(st1, st2):
    ans = 0
    for a in range(len(st1)):
            for b in range(len(st2)):
                k = 0
                while ((a + k) < len(st1) and (b + k) < len(st2)
            and st1[a + k] == st2[b + k]):
                    k = k + 1

                ans = max(ans, k)
    if(ans != 0):
        return 1/ans
    else: return 1



class Utilities:
    def __init__(self):
        self.distMethod = "levehnstein"

    def setDistMethod(self, method = "levehnstein"):
        self.distMethod = method

    def distance(str1, str2, method = "levehnstein"):
        if method == "levehnstein":
            return levenshteinDistanceDP(str1, str2)
        elif method == "jaccard":
            return jaccard_distance(str1, str2)
        elif method == "jaro":
            return jaro_distance(str1, str2)
        elif method == "lcs":
            return lcs(str1, str2)
    def threshold(method):
        if method == "levehnstein":
            return 10
        elif method == "jaccard":
            return 0.6
        elif method == "jaro":
            return 0.5
        elif method == "lcs":
            return 0.4
    def isBoolean(column):
        val = []
        i = 0
        while(len(val) < 3 and i < len(column)):
            if(len(val) < 2):
                val.append(column[i])
            else:
                same = True
                j = 0
                while (same == True and j < len(val)):
                    if(val[j] != column[i]):
                        val.append(column[i])
                        same = False
                    else:
                        j+=1
            i+=1
        return (len(val) == 2 and i == len(column))

    #Method that eliminates all the separators from the given term. 
    def replace (s):
        name = str(s)
        #Different characters that are replaced from the columns and tables from the database
        charsToReplace = ['-', '_', '*', '|', '^', '+', '`']
        for c in charsToReplace:
            name = name.replace(c, '')

        if (name[-1] == 's'):
            ''.join(name[-1])
        return name.lower()

    def switchType(column):
        field_type = {
            'DECIMAL' : "xsd:decimal" ,
            'TINY' : "xsd:double",
            'SHORT' : "xsd:short",
            'LONG' : "xsd:long",
            'FLOAT' : "xsd:float",
            'FLOAT64' : "xsd:float",
            'DOUBLE' : "xsd:double",
            'NULL' : "xsd:string",
            'TIMESTAMP' : "xsd:datetime",
            'LONGLONG' : "xsd:long",
            'INT24' : "xsd:integer",
            'INT64' : "xsd:integer",
            'DATE' : "xsd:date",
            'TIME' : "xsd:time",
            'DATETIME' : "xsd:datetime",
            'YEAR' : "xsd:year",
            'NEWDATE' : "xsd:date",
            'VARCHAR' : "xsd:string",
            'BIT' : "xsd:string", 
            'NEWDECIMAL' : "xsd:decimal",
            'INTERVAL' : "xsd:duration",
            'SET' : "xsd:string",
            'TINY_BLOB' : "xsd:double",
            'MEDIUM_BLOB' : "xsd:string",
            'LONG_BLOB' : "xsd:string",
            'BLOB' : "xsd:string",
            'VAR_STRING' : "xsd:string",
            'STRING' : "xsd:string",
            'OBJECT' : "xsd:string",
            'GEOMETRY' : "xsd:string",
            'BOOL' : "xsd:bool",
            'object' : "xsd:string",
            'int64' : "xsd:integer",
            'float64' : "xsd:float",
            'bool' : "xsd:bool",
            'datetime64' : "xsd:date",
            'character varying' : "xsd:string",
            'integer' : "xsd:integer",
            'date' : "xsd:date"}
        return field_type[column]

    
    def infereType(column):
        try:
            return Utilities.switchType(column)
        except:
            return "xsd:string"

    def getKeyByValue(dict, value):
        # one-liner
        return (list(dict.keys())[list(dict.values()).index(value)])

    #By using the LevenshteinDistance, the id of the class given all the columns is detected. 
    def getClassIDTerm(onto_class, columns):
        dis = 10
        term = ""
        for x in columns:
            name = Utilities.replace(x)
            try:
                onto_name = onto_class.locale
            except:
                onto_name = onto_class
            #The name of the class in the ontology is compared to the column. 'id' is added to the class name in order to get the
            #id in the columsn more efficiently
            auxDis = Utilities.distance(name, onto_name.split(':').pop() + 'id')
            #The column is checked in order to see if it is actually an id and the distance is checked to be lower than 2.0, which means
            #that only two replacements must be done in order to have both strings to be the same. This is done in order to see that the column is 
            #actually the class id and not a reference to another table
            if (name.lower() == 'id' or (name.endswith('id') or name.startswith('id')) and auxDis < dis and auxDis < 5.0):
                dis = auxDis
                term = x
        return term
        
