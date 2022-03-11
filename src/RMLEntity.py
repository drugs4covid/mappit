from Utils import Utilities
class RMLEntity(object):
    def __init__(self, table, onto_class, class_properties, idName):
        self.onto_class = onto_class
        self.onto_properties = class_properties
        self.table = table
        self.ID =  idName
        self.joinConditions = []
    
    def getJoinConditions(self, tables, db):
        for t in tables:
            for prop in self.onto_properties:
                colCor = RMLEntity.checkTableCorrespondenceByColumn(prop, t, db)
                if (self.table != t and colCor != ""):
                    self.joinConditions.append([prop, t, colCor])
                    self.onto_properties.remove(prop)

    def checkTableCorrespondenceByColumn(prop, table, db):
        found = False
        count = 0
        importantTerms = ""
        correspondenceCol = ""
        propTerms = prop[1].split('_')
        while (found == False and count < len(propTerms)):
            for i in propTerms:
                print("Checking: ", i, "Table: ", table[0].lower())
                dis = Utilities.levenshteinDistanceDP(i, str(table[0].lower()))
                print("DIS: ", dis)
                if (dis <= 1.0):
                    found = True
                    propTerms.remove(i)
                    importantTerms = ''.join(map(str, propTerms))
                count += 1
        if found:
            tableColumns = db.get_table_columns(table[0])
            dis = 0
            for col in tableColumns:
                auxDis = Utilities.jaro_distance(importantTerms, col)
                if auxDis > dis:
                    dis = auxDis
                    correspondenceCol = col
        return correspondenceCol




