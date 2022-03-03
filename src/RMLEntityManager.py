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

def getRMLEntities(tables, oc_classes, ontology, dbManager):
    entities = []
    for x in range(0, len(tables)):
        columns = DatabaseManager.get_table_columns(dbManager, tables[x][0])
        onto_class = correspondenceClass(oc_classes, tables[x])
        properties = OntologyManager.get_class_properties(ontology, onto_class)
        onto_properties = getPropertiesCorrespondence(columns, properties)
        entities.append(RMLEntity(tables[x], onto_class, onto_properties))
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

    #RMLParser.RML_Transformation('gtfs', rmlEntities, ontology)

    for x in rmlEntities:
        print(x.table)
        print(x.onto_class)
        for y in x.onto_properties:
            print(y[0].printStats())

if __name__ == "__main__":
    main()