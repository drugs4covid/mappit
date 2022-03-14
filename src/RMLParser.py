import pandas as pd
import json
import sys
import os
from Utils import Utilities
from DatabaseManager import DatabaseManager

class RMLParser(object):

    def loadProperties(propertiesFile):
        with open(propertiesFile) as json_file:
            data = json.load(json_file)
            json_file.close()
        return data

    def writeProperties(output, data, properties, fw):
        for x in data['list_prefixes']:
            print("@prefix " + x['prefix'] + ": <" + x['URI'] + "> .")
        for x in properties:
            print("@prefix " + x[0] + ": <" + x[1] + "> .")
        #print('@base ' + properties['base']['URI'])
            
    def getBase(properties):
        return properties['base']['URI']
    
    def TripleMap(entity, base):
        last = (len(entity.onto_properties) == 0 and len(entity.joinConditions) == 0)
        level = 8
        print ("<#" + entity.table[0] + "> a rr:TriplesMap;")
        RMLParser.LogicalSource(entity.table)
        RMLParser.SubjectMap(entity.onto_class, entity.ID, base, last)
        v = 0
        for y in entity.onto_properties:
            last = (v == len(entity.onto_properties) - 1 and len(entity.joinConditions) == 0)
            RMLParser.PredicateObjectMap(y[0], y[1], y[2], last)
            v += 1
        v = 0
        for j in entity.joinConditions:
            last = (v == len(entity.joinConditions) - 1)
            RMLParser.JoinCondition(j, last)
            v += 1
        
    def LogicalSource(table):
        level = 8
        print (" "*level, "rml:logicalSource [")
        print (" "*(2*level), "rml:source " + '"' + "<#DB_source>" + '";')
        print (" "*(2*level), "rr:tableName " + '"' + table[0] + '";')
        print (" "*level, "];")
        
    def SubjectMap(onto_class, onto_id, base, last):
        level = 8
        print (" "*level, "rr:subjectMap [")
        print (" "*(2*level), "rr:template " + '"' + base + onto_class.qname.split(':').pop() + '/{' + onto_id +'}' + '";')
        print (" "*(2*level), "rr:termType " + 'rr:IRI;')
        print (" "*(2*level), "rr:class " + onto_class.qname + ';')
        endpoint = ";"
        if (last == True):
            endpoint = "."
        print (" "*level, "]" + endpoint)

    def PredicateObjectMap(property, column, value, last):
        level = 8
        print (" "*level, "rr:predicateObjectMap [")
        print (" "*(2*level), "rr:predicate " + '<' + property.uri + '>;')
        print (" "*(2*level), "rr:objectMap " + '[ rr:column ' + '"' + column + '"; ' + "rr:datatype " + Utilities.infereType(value[0]) + "; ];")
        endpoint = ";"
        if (last == True):
            endpoint = "."
        print (" "*level, "]" + endpoint)

    def JoinCondition(joinCondition, last):
        level = 8
        print (" "*level, "rr:predicateObjectMap [")
        print (" "*(2*level), "rr:predicate " + '<' + joinCondition[0][0].uri + '>;')
        print (" "*(2*level), "rr:objectMap " + '[')
        print (" "*(3*level), "a rr:RefObjectMap;")
        print (" "*(3*level), "rr:parentTriplesMap " + "<#" + joinCondition[1][0] + ">;")
        print (" "*(3*level), "rr:joinCondition " + '[')
        print (" "*(4*level), "rr:child " + '"' + joinCondition[0][1] + '";')
        print (" "*(4*level), "rr:parent " + '"' + joinCondition[2] + '";')
        print (" "*(3*level), '];')
        print (" "*(2*level), '];')
        endpoint = ";"
        if (last == True):
            endpoint = "."
        print (" "*level, "]" + endpoint)

    def deleteFileContent(file):
        file = open("outputs/" + file,"r+")
        file.truncate(0)
        file.close()


    def RML_Transformation(output, rmlEntities, ontology, propertiesFile):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        data = RMLParser.loadProperties(ROOT_DIR + "/properties/" + propertiesFile)
        base = RMLParser.getBase(data)
        with open(ROOT_DIR + "/outputs/" + output, 'w') as fw:
            original_stdout = sys.stdout
            sys.stdout = fw
            RMLParser.writeProperties(ROOT_DIR + "/outputs/" + output, data, ontology.namespaces, fw)
            print ('@base <' + base + "> .")
            for x in rmlEntities:
                RMLParser.TripleMap(x, base)
            sys.stdout = original_stdout
            fw.close()
