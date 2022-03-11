import pandas as pd
import json
import sys
import os
from Utils import Utilities

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
    
    def LogicalSource(table, SQLversion):
        level = 8
        print (" "*level, "rml:logicalSource [")
        print (" "*(2*level), "rml:source " + '"' + "<#DB_source>" + '";')
        print (" "*(2*level), "rr:sqlVersion " + '"' + SQLversion + '";')
        print (" "*(2*level), "rr:tableName " + '"' + table[0] + '";')
        print (" "*level, "];")
        
    def TripleMap(subject):
        level = 8
        print ("<#" + subject[0] + "> a rr:TriplesMap;")
        RMLParser.LogicalSource(subject, "SQL2008")
        
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

    def PredicateObjectMap(property, column, onto_class, base, last):
        level = 8
        print (" "*level, "rr:predicateObjectMap [")
        print (" "*(2*level), "rr:predicate " + '<' + property.uri + '>;')
        print (" "*(2*level), "rr:objectMap " + '[ rr:column ' + '"' + column + '"; ' + "rr:datatype " + "xsd:string" + "; ];")
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
                last = (len(x.onto_properties) == 0)
                RMLParser.TripleMap(x.table)
                RMLParser.SubjectMap(x.onto_class, x.ID, base, last)
                v = 0
                for y in x.onto_properties:
                    last = (v == len(x.onto_properties) - 1)
                    RMLParser.PredicateObjectMap(y[0], y[1], x.onto_class, base, last)
                    v += 1
            sys.stdout = original_stdout
            fw.close()
