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
            term1 = str(y).split('_', '').pop().lower()
            term2 = x.qname.split(':').pop()
            print("Col: ", term1, "Prop: ", term2)
            auxDis = Utilities.jaro_distance(term1, term2)
            if auxDis > dis:
                dis = auxDis
                term = [x, y]
        cor_properties.append(term)
    return cor_properties

def getClassIDTerm(onto_class, columns):
    dis = 10
    term = ""
    for x in columns:
        name = str(x).replace('_', '').lower()
        auxDis = Utilities.levenshteinDistanceDP(name, onto_class.qname.split(':').pop() + 'id')
        if (name.endswith('id') or name.startswith('id')) and auxDis < dis and auxDis < 2.0:
            dis = auxDis
            term = x
    return term

def get_class_properties(columns, ontology, ID, table, db):
        properties = []
        for col in columns:
            term = []
            dis = 0
            for prop in ontology.all_properties:
                columnTerm = str(col).replace('_', '').lower()
                terms = str(col).split('_')
                terms.remove(terms[0])
                lastTerms = ''.join(terms).lower()
                propTerm = prop.qname.split(':').pop().lower()
                auxDis1 = Utilities.jaro_distance(columnTerm, propTerm)
                auxDis2 = Utilities.jaro_distance(lastTerms, propTerm)
                if (auxDis1 > dis):
                    dis = auxDis1
                    term = prop
                elif (auxDis2 > dis and len(lastTerms) > 3):
                    dis = auxDis2
                    term = prop
            IDterm = str(ID).replace('_', '').lower()
            if (columnTerm != IDterm):
                columnVal = DatabaseManager.get_column_value(db, table, col)
                properties.append([term, col, columnVal])
        return properties

def getRMLEntities(tables, oc_classes, ontology, dbManager):
    entities = []
    for x in range(0, len(tables)):
        columns = DatabaseManager.get_table_columns(dbManager, tables[x][0])
        onto_class = correspondenceClass(oc_classes, tables[x])
        onto_ID = getClassIDTerm(onto_class, columns)
        properties = get_class_properties(columns, ontology, onto_ID, tables[x][0], dbManager)
        #onto_properties = getPropertiesCorrespondence(columns, properties)
        entity = RMLEntity(tables[x], onto_class, properties, onto_ID)
        entity.getJoinConditions(tables, dbManager, onto_ID)
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

    #for x in rmlEntities:
    #    print(x.table)
    #    print(x.onto_class)
    #    print(x.joinConditions)
        #for y in x.onto_properties:
        #    print(y)
        #    for v in y[0].domains:
        #        print("Domain: " + y[0].qname + " " + v.qname)
        #    for v in y[0].ranges:
        #        print("Range: " + y[0].qname + " " + v.qname)


if __name__ == "__main__":
    main()