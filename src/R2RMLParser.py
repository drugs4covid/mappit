import pandas as pd
import sys
from Utils import Utilities

class R2RMLParser(object):

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
    

    def TripleMap(entity, base):
        last = (len(entity.onto_properties) == 0 and len(entity.joinConditions) == 0)
        level = 8
        if (not entity.JCFromTable):
            print ("<#" + entity.onto_class.locale + ">")
        else:
            print ("<#" + entity.joinConditions[0][0][0].locale + ">")
        R2RMLParser.LogicalTable(entity.table)
        R2RMLParser.SubjectMap(entity.onto_class, entity.ID, base, last)
        v = 0
        for y in entity.onto_properties:
            last = (v == len(entity.onto_properties) - 1 and len(entity.joinConditions) == 0)
            R2RMLParser.PredicateObjectMap(y[0], y[1], last)
            v += 1
        v = 0
        for j in entity.joinConditions:
            last = (v == len(entity.joinConditions) - 1)
            R2RMLParser.JoinCondition(j, last)
            v += 1
        
    def LogicalTable(table):
        level = 8
        print (" "*level, "rr:logicalTable [ " + "rr:tableName " + '"' + table + '"' + "];")
        
    def SubjectMap(onto_class, onto_id, base, last):
        level = 8
        try:
            name = onto_class.locale
        except: name = onto_class
        print (" "*level, "rr:subjectMap [")
        print (" "*(2*level), "rr:template " + '"' + base + name.split(':').pop() + '/{' + onto_id + '}' + '";')
        print (" "*(2*level), "rr:class " + onto_class.qname)
        endpoint = ";"
        if (last == True):
            endpoint = "."
        print (" "*level, "]" + endpoint)

    def PredicateObjectMap(property, column, last):
        level = 8
        print (" "*level, "rr:predicateObjectMap [")
        print (" "*(2*level), "rr:predicate "  + property.qname + ";")
        print (" "*(2*level), "rr:objectMap " + '[ rr:column ' + '"' + column + '"' + "];")
        endpoint = ";"
        if (last == True):
            endpoint = "."
        print (" "*level, "]" + endpoint)

    def JoinCondition(joinCondition, last):
        try:
            level = 8
            print (" "*level, "rr:predicateObjectMap [")
            print (" "*(2*level), "rr:predicate " + joinCondition[0][0].qname + ';')
            print (" "*(2*level), "rr:objectMap " + '[')
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
        except: pass

    def deleteFileContent(file):
        file = open("outputs/" + file,"r+")
        file.truncate(0)
        file.close()


    def R2RML_Transformation(output, rmlEntities, ontology, data, ROOT_DIR):
        base, prefix = R2RMLParser.getBase(data)
        with open(ROOT_DIR + "/outputs/" + output, 'w') as fw:
            original_stdout = sys.stdout
            sys.stdout = fw
            R2RMLParser.writePrefixes(ROOT_DIR + "/outputs/" + output, data, ontology.namespaces)
            print ('@base <' + base + "> .")
            for x in rmlEntities:
                R2RMLParser.TripleMap(x, base)
            sys.stdout = original_stdout
            fw.close()
