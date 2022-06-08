import pandas as pd
import sys
from Utils import Utilities

class RMLParser(object):

    #Writes all prefixes given the ontology and the additional prefixes declared in the json data file
    def writePrefixes(output, data, properties):
        print ("@prefix rr: <http://www.w3.org/ns/r2rml#>.")
        print("@prefix rml: <http://semweb.mmlab.be/ns/rml#>.")
        print("@prefix ql: <http://semweb.mmlab.be/ns/ql#>.")
        print("@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.")
        print("@prefix " + data['base']['prefix'] + ": " + "<" + data['base']['URI'] + ">.")
        #for x in data['list_prefixes']:
        #    print("@prefix " + x['prefix'] + ": <" + x['URI'] + "> .")
        for x in properties:
            print("@prefix " + x[0] + ": <" + x[1] + "> .")
    
    # Returns tha base uri declared in the json data file
    def getBase(properties):
        return properties['base']['URI'], properties['base']['prefix']
    

    def TripleMap(entity, base, prefix, data, ROOT_DIR):
        last = (len(entity.onto_properties) == 0 and len(entity.joinConditions) == 0)
        level = 8
        print ("<#" + entity.onto_class.locale + "> a rr:TriplesMap;")
        if (data['format'] != 'database'):
            dir =  ROOT_DIR + "/Inputs/" + data['folder']
        else:
            dir = ""
        RMLParser.LogicalSource(entity.table, data['format'], dir)
        RMLParser.SubjectMap(entity.onto_class, entity.ID, base, prefix, last)
        v = 0
        for y in entity.onto_properties:
            last = (v == len(entity.onto_properties) - 1 and len(entity.joinConditions) == 0)
            RMLParser.PredicateObjectMap(y[0], y[1], y[2], last, prefix)
            v += 1
        v = 0
        for j in entity.joinConditions:
            last = (v == len(entity.joinConditions) - 1)
            RMLParser.JoinCondition(j, last, prefix)
            v += 1
        
    def LogicalSource(table, format, dir):
        level = 8
        print (" "*level, "rml:logicalSource [")
        if (format == 'database'):
            print (" "*(2*level), "rml:source " + '"' + "<#DB_source>" + '";')
            print (" "*(2*level), "rr:tableName " + '"' + table + '";')
        elif (format == 'csv'):
             print (" "*(2*level), "rml:source " + '"' + dir + table + '.csv" ;')
             print (" "*(2*level), "rml:referenceFormulation ql:CSV")
        elif (format == 'json'):
            print (" "*(2*level), "rml:source " + '"' + dir + table + '.json" ;')
            print (" "*(2*level), "rml:referenceFormulation ql:JSONPath ;")
            print (" "*(2*level), "rml:iterator " + '"$.' + table + '[*]"')
        print (" "*level, "];")
        
    def SubjectMap(onto_class, onto_id, base, prefix, last):
        level = 8
        try:
            name = onto_class.qname
        except: name = onto_class
        print (" "*level, "rr:subjectMap [")
        print (" "*(2*level), "rr:template " + '"' + base + name.split(':').pop() + '/{' + onto_id +'}' + '";')
        print (" "*(2*level), "rr:termType " + 'rr:IRI;')
        print (" "*(2*level), "rr:class " + onto_class.qname)
        endpoint = ";"
        if (last == True):
            endpoint = "."
        print (" "*level, "]" + endpoint)

    def PredicateObjectMap(property, column, values, last, prefix):
        level = 8
        print (" "*level, "rr:predicateObjectMap [")
        try:
            print (" "*(2*level), "rr:predicate "  + property.qname + ";")
        except:
            print (" "*(2*level), "rr:predicate " + property + ";")
        print (" "*(2*level), "rr:objectMap " + '[ rml:reference ' + '"' + column + '"; ' + "rr:datatype " + Utilities.infereType(values) + "];")
        endpoint = ";"
        if (last == True):
            endpoint = "."
        print (" "*level, "]" + endpoint)

    def JoinCondition(joinCondition, last, prefix):
        level = 8
        print (" "*level, "rr:predicateObjectMap [")
        print (" "*(2*level), "rr:predicateMap " + '[')
        print (" "*(3*level), "a rr:PredicateMap;")
        print (" "*(3*level), "rr:constant "  +joinCondition[0][0].qname + ';')
        print (" "*(2*level), '];')
        print (" "*(2*level), "rr:objectMap " + '[')
        print (" "*(3*level), "a rr:RefObjectMap;")
        print (" "*(3*level), "rr:parentTriplesMap " + "<#" + joinCondition[1] + ">;")
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


    def RML_Transformation(output, rmlEntities, ontology, data, ROOT_DIR):
        base, prefix = RMLParser.getBase(data)
        with open(ROOT_DIR + "/outputs/" + output, 'w') as fw:
            original_stdout = sys.stdout
            sys.stdout = fw
            RMLParser.writePrefixes(ROOT_DIR + "/outputs/" + output, data, ontology.namespaces)
            print ('@base <' + base + "> .")
            for x in rmlEntities:
                RMLParser.TripleMap(x, base, prefix, data['Data'], ROOT_DIR)
            sys.stdout = original_stdout
            fw.close()
