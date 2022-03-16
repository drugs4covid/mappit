from Utils import Utilities
from DatabaseManager import DatabaseManager

class RMLEntity(object):
    def __init__(self, table, columns, db, ontoManager):
        self.table = table
        self.columns = db.get_table_columns(self.table)
        self.onto_class = RMLEntity.correspondenceClass(self, ontoManager.onto_classes)
        self.ID =  RMLEntity.getClassIDTerm(self.onto_class, columns)
        self.onto_properties = RMLEntity.get_class_properties(self, ontoManager.ontology, db)
        self.joinConditions = []
    
    def getClassIDTerm(onto_class, columns):
        dis = 10
        term = ""
        for x in columns:
            name = str(x).replace('_', '').lower()

            try:
                onto_name = onto_class.qname
            except:
                onto_name = onto_class

            auxDis = Utilities.levenshteinDistanceDP(name, onto_name.split(':').pop() + 'id')
            if (name.endswith('id') or name.startswith('id')) and auxDis < dis and auxDis < 2.0:
                dis = auxDis
                term = x
        return term
    
    def correspondenceClass(self, oc_classes):
        dis = 100
        term = ""
        for x in oc_classes:
            term1 = str(self.table).replace('_', '').lower()
            try:
                term2 = x.qname.split(':').pop()
            except:
                term2 = x.split(':').pop()
            auxDis = Utilities.levenshteinDistanceDP(term1, term2)
            if auxDis < dis:
                dis = auxDis
                term = x
        return term

    def get_class_properties(self, ontology, db):
        properties = []
        for col in self.columns:
            term = []
            dis = 0
            for prop in ontology.all_properties:

                columnTerm = str(col).replace('_', '').lower()
                terms = str(col).split('_')
                terms.remove(terms[0])
                lastTerms = ''.join(terms).lower()
                try:
                    propTerm = prop.qname.split(':').pop().lower()
                except:
                    propTerm = prop.split(':').pop().lower()

                auxDis1 = Utilities.jaro_distance(columnTerm, propTerm)
                auxDis2 = Utilities.jaro_distance(lastTerms, propTerm)

                if (auxDis1 > dis):
                    dis = auxDis1
                    term = prop
                elif (auxDis2 > dis and len(lastTerms) > 2):
                    dis = auxDis2
                    term = prop

            IDterm = str(self.ID).replace('_', '').lower()
            if (columnTerm != IDterm):
                columnVal = db.get_column_values(self.table, col)
                properties.append([term, col, columnVal])
        return properties

    def getJoinConditions(self, tables, db):
        for prop in self.onto_properties:
            t, colCor = RMLEntity.checkJoinCondition(self, prop, tables, db)
            if (colCor != ""):
                self.joinConditions.append([prop, t, colCor])
                self.onto_properties.remove(prop)

    def getTableByRange(tables, range):
        dis = 0
        i = 0
        found = False
        table = []
        while(found == False and i < len(tables)):
            dis = Utilities.levenshteinDistanceDP(range, str(tables[i].lower()))
            if (dis <= 1.0):
                table = tables[i]
                found = True
            i+=1
        return table, found


    def getTableColumnCorrespondence(table, prop_name, db):
        tableColumns = db.get_table_columns(table)
        dis = 0
        correspondenceCol = ""
        for col in tableColumns:
            auxDis = Utilities.jaro_distance(prop_name, col)
            if auxDis > dis:
                dis = auxDis
                correspondenceCol = col
        return correspondenceCol

    def checkJoinCondition(self, prop, tables, db):
        i = 0
        foundByRange = False
        t = []
        col = ""
        try:
            ranges = prop[0].ranges
        except:
            ranges = []

        while(foundByRange == False and i < len(ranges)):
            t, foundByRange = RMLEntity.getTableByRange(tables, ranges[i].qname.split(':').pop().lower())

            if(foundByRange and t != self.table):
                name = prop[0].qname.split(':').pop().lower()
                col = RMLEntity.getTableColumnCorrespondence(t, name, db)

            else:
                foundByRange = False
            i+=1
        return t, col





