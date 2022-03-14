from Utils import Utilities
class RMLEntity(object):
    def __init__(self, table, onto_class, class_properties, idName):
        self.onto_class = onto_class
        self.onto_properties = class_properties
        self.table = table
        self.ID =  idName
        self.joinConditions = []
    
    def getJoinConditions(self, tables, db, ID):
        for prop in self.onto_properties:
            t, colCor = RMLEntity.checkJoinCondition(self, prop, tables, db, ID)
            if (colCor != ""):
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
                #print("Checking: ", i, "Table: ", table[0].lower())
                dis = Utilities.levenshteinDistanceDP(i, str(table[0].lower()))
                #print("DIS: ", dis)
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

    def getTableByRange(tables, range):
        dis = 0
        i = 0
        found = False
        table = []
        while(found == False and i < len(tables)):
            dis = Utilities.levenshteinDistanceDP(range, str(tables[i][0].lower()))
            if (dis <= 1.0):
                table = tables[i]
                found = True
            i+=1
        return table, found

    #def getTableByID(tables)

    def getTableColumnCorrespondence(table, prop_name, db):
        tableColumns = db.get_table_columns(table[0])
        dis = 0
        correspondenceCol = ""
        for col in tableColumns:
            auxDis = Utilities.jaro_distance(prop_name, col)
            if auxDis > dis:
                dis = auxDis
                correspondenceCol = col
        return correspondenceCol

    def checkJoinCondition(self, prop, tables, db, ID):
        ranges = prop[0].ranges
        print(prop[1])
        i = 0
        foundByRange = False
        foundByID = False
        t = []
        col = ""
        while(foundByRange == False and i < len(ranges)):
            t, foundByRange = RMLEntity.getTableByRange(tables, ranges[i].qname.split(':').pop().lower())
            #if(foundByRange == False):

            if(foundByRange and t != self.table):
                name = prop[0].qname.split(':').pop().lower()
                col = RMLEntity.getTableColumnCorrespondence(t, name, db)
                #print("Property: ", name, "Col: ", col)
            else:
                foundByRange = False
                foundByID = False
            i+=1
        return t, col
        #rangeTable = RMLEntity.getTableByRange(tables=les, )




