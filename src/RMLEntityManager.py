from RMLEntity import RMLEntity
from DatabaseManager import DatabaseManager
from OntologyManager import OntologyManager
from Utils import Utilities
from RMLParser import RMLParser

def correspondenceClass(oc_classes, table):
    dis = 100
    term = ""
    for x in oc_classes:
        term1 = str(table).replace('_', '').lower()
        term2 = x.qname.split(':').pop()
        auxDis = Utilities.levenshteinDistanceDP(term1, term2)
        if auxDis < dis:
            dis = auxDis
            term = x
    return term

def getPropertiesCorrespondence(columns, properties):
    cor_properties = []
    for x in properties:
        dis = 0
        term = []
        for y in columns:
            term1 = str(y).replace('_', '').lower()
            term2 = x.qname.split(':').pop()
            auxDis = Utilities.jaro_distance(term1, term2)
            if auxDis > dis:
                dis = auxDis
                term = [x, y]
        cor_properties.append(term)
    return cor_properties

def getClassIDTerm(onto_class, columns):
    dis = 0
    term = ""
    for x in columns:
        name = str(x).replace('_', '').lower()
        auxDis = Utilities.jaro_distance(name, onto_class.qname.split(':').pop() + 'id')
        if (name.endswith('id') or name.startswith('id')) and auxDis > dis:
            dis = auxDis
            term = x
    return term

def get_class_properties(columns, ontology):
        properties = []
        for col in columns:
            term = []
            dis = 0
            for prop in ontology.all_properties:
                columnTerm = str(col).replace('_', '').lower()
                propTerm = prop.qname.split(':').pop().lower()
                auxDis = Utilities.jaro_distance(columnTerm, propTerm)
                if (auxDis > dis):
                    dis = auxDis
                    term = prop
            properties.append([term, col])
        return properties

def get_joinconditions(tables, entities):
    joins = []

def getRMLEntities(tables, oc_classes, ontology, dbManager):
    entities = []
    for x in range(0, len(tables)):
        columns = DatabaseManager.get_table_columns(dbManager, tables[x][0])
        onto_class = correspondenceClass(oc_classes, tables[x])
        properties = get_class_properties(columns, ontology)
        #onto_properties = getPropertiesCorrespondence(columns, properties)
        onto_ID = getClassIDTerm(onto_class, columns)
        entity = RMLEntity(tables[x], onto_class, properties, onto_ID)
        entity.getJoinConditions(tables, dbManager)
        entities.append(entity)
    return entities


def main():
    ontoManager = OntologyManager('http://vocab.gtfs.org/terms#')
    dbManager = DatabaseManager('gtfs', 'root', 'gtfs')
    #print(ontoManager.onto_classes)

    ontology = ontoManager.ontology
    onto_classes = ontoManager.onto_classes
    tables = dbManager.get_tables()
    #print(tables[0][0])

    rmlEntities = getRMLEntities(tables, ontoManager.onto_classes, ontoManager.ontology, dbManager)

    RMLParser.RML_Transformation('gtfs.ttl', rmlEntities, ontology, 'properties.json')

    for x in rmlEntities:
        print(x.table)
        print(x.onto_class)
        for y in x.joinConditions:
            print(y)
    #        for v in y[0].domains:
    #            print("Domain: " + y[0].qname + " " + v.qname)
    #        for v in y[0].ranges:
    #            print("Range: " + y[0].qname + " " + v.qname)


if __name__ == "__main__":
    main()