import pandas as pd
import json
import sys
import os

class RMLParser(object):

    def loadProperties(outputFile, propertiesFile):
        with open('properties/' + propertiesFile) as json_file:
            data = json.load(json_file)
            json_file.close()
        return data

    def writeProperties(output, properties, fw):
            for x in properties:
                print("@prefix " + x[0] + ": <" + x[1] + ">")
            #print('@base ' + properties['base']['URI'])

    def LogicalSource(table, SQLversion):
        level = 8
        print (" "*level, "rml:logicalSource [")
        print (" "*(2*level), "rml:source: " + '"' + "<#DB_source>" + '";')
        print (" "*(2*level), "rr:sqlVersion " + '"' + SQLversion + '";')
        print (" "*(2*level), "rr:tableName: " + '"' + table[0] + '";')
        print (" "*level, "];")
        
    def TripleMap(subject):
        level = 8
        print ("<" + subject[0] + ">")
        print (" "*level, "a rr:TriplesMap;")
        #print ("\n")
        RMLParser.LogicalSource(subject, "SQL2008")
        
    def SubjectMap(onto_class):
        level = 8
        print (" "*level, "rr:subjectMap [")
        print (" "*(2*level), "rr:template: " + '"' + onto_class.uri + '";')
        print (" "*(2*level), "rr:termType: " + '"rr:IRI";')
        print (" "*(2*level), "rr:class: " + '"' + onto_class.qname + '";')
        print (" "*level, "];")

    def PredicateObjectMap(property, column):
        level = 8
        print (" "*level, "rr:predicateObjectMap [")
        print (" "*(2*level), "rr:predicate: " + '"' + property.uri + '";')
        print (" "*(2*level), "rr:objectMap: " + '[ rr:column ' + '"' + column + '"; ' + "rr:datatype " + property.rdftype + "; ];")
        print (" "*level, "];")

    def deleteFileContent(file):
        file = open("outputs/" + file,"r+")
        file.truncate(0)
        file.close()
    #def RMLTable(oc, table):

    def RML_Transformation(output, rmlEntities, ontology):
        #data = loadProperties(output, properties)
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        with open(ROOT_DIR + "/outputs/" + output, 'w') as fw:
            original_stdout = sys.stdout
            sys.stdout = fw
            RMLParser.writeProperties(ROOT_DIR + "/outputs/" + output, ontology.namespaces, fw)
            for x in rmlEntities:
                RMLParser.TripleMap(x.table)
                RMLParser.SubjectMap(x.onto_class)
                for y in x.onto_properties:
                    RMLParser.PredicateObjectMap(y[0], y[1])
            sys.stdout = original_stdout
            fw.close()
