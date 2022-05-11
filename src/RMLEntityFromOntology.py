from html import entities
from Utils import Utilities
from RMLEntity import RMLEntity
import rdflib
class RMLEntityFromOntology(object):

    def load(tables, db, ontoManager):

        #self.ID =  RMLEntity.getClassIDTerm(self.onto_class, self.columns)

        classes = ontoManager.onto_classes
        classesDict = dict()
        tableAuxDict = dict()
        entities = []

        for y in classes:
            dis = 100
            totalDisFromProp = 100
            name = ""
            for x in range(0, len(tables)):
                #Gets columns for a given table
                columns = db.get_table_columns(tables[x])
                name, dis, auxProperties, auxObjectProperties, totalDisProperties, changed = correspondenceClass(tables[x], columns, y, dis, name, classes, classesDict, db)
                if (changed and totalDisProperties <= totalDisFromProp):
                    totalDisFromProp = totalDisProperties
                    onto_class = y
                    table = tables[x]
                    onto_properties = auxProperties
                    joinConditions = auxObjectProperties
            if (dis < 10):
                classesDict.update({y : name})
                tableAuxDict.update({y.locale : table})
                entity = RMLEntity(table, onto_class, name, joinConditions, onto_properties)
                #After creating the entity, it is checked if it has any joinConditions given the prooperties assigned to  the entity
        #        entity.getJoinConditions(tables, dbManager)
                entities.append(entity)
        for x in list(classesDict):
            if classesDict[x] == '':
                del classesDict[x]
        updateJoinConditions(entities, tableAuxDict, db)
        return entities

    #Given the ontology classes, it is checked the one whose name is the most similar to the table assigned to the entity
def correspondenceClass(table, columns, oc_class, lastDis, term, classes, classesDict, db):
    term1 = Utilities.replace(table)
    try:
        term2 = oc_class.locale
    except:
        term2 = oc_class.split(':').pop()
    changed = False
    dis1 = Utilities.distance(term1, term2)
    bestCol = ""
    dis2 =  100
    for y in columns:
        auxDis2 = Utilities.distance(y, term2)
        if auxDis2 < dis2:
            if (y not in classesDict.values()):
                dis2 = auxDis2
                bestCol = y
            else:
                old_class = getKeyByValue(classesDict, y)
                oldDis = Utilities.distance(old_class.locale, y)
                if auxDis2 < oldDis:
                    classesDict.update({old_class : ""})
                    classesDict.update({oc_class : y})
                    classes.append(old_class)
                    dis2 = auxDis2
                    bestCol = y
                else: pass
    prop = []
    objProp = []
    totalDis = 100

    if (dis2 < dis1 and dis2 < lastDis):
        term = bestCol
        lastDis = dis2
        changed = True
    elif (dis1 < lastDis and table not in classesDict.values()): 
        term = table
        lastDis = dis1
        changed = True

    if(changed):
        prop, objProp, totalDis = getProperties(columns, oc_class, db, table)
        
    return term, lastDis, prop, objProp, totalDis, changed


def getProperties(columns, oc_class, db, table):
    properties = []
    objectProperties = []
    totalDis = 0
    for x in oc_class.domain_of:
        auxDis = 5
        propData = []
        propObjData = []
        for y in columns:
            #Column Name
            columnTerm = Utilities.replace(y)
            terms = str(y).split('_')
            terms.remove(terms[0])
            lastTerms = ''.join(terms).lower()
            try:
                propTerm = x.locale.split(':').pop().lower()
            except:
                propTerm = x.split(':').pop().lower()

            #Both terms are compared, the column name and the important terms that have been separated
            auxDis1 = Utilities.distance(columnTerm, propTerm)
            auxDis2 = Utilities.distance(lastTerms, propTerm)
            if(auxDis1 < auxDis or auxDis2 < auxDis):
                if(x.rdftype ==  rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#ObjectProperty')):
                    propObjData.append([x, y])
                else:
                    propData = [x, y, db.get_column_values(table, y)]
                auxDis = min(auxDis1, auxDis2)
        if (propData != []):
            properties.append(propData)
        if (propObjData != []):
            for r in x.ranges:
                rangeDis = 30
                correspondenceRange = []
                for s in propObjData:
                    rangeDisAux = Utilities.distance(r.locale, s[1])
                    if(rangeDis > rangeDisAux):
                        rangeDis = rangeDisAux
                        correspondenceRange = [s, r.locale, s[1]]
            if(correspondenceRange != []):
                objectProperties.append(correspondenceRange)
        totalDis += auxDis
    return properties, objectProperties, totalDis

def updateJoinConditions(entities, tableDict, db):
    for e in entities:
        for jc in e.joinConditions:
            dis = 100
            columns = db.get_table_columns(tableDict[jc[1]])
            prop = jc[0][1]
            for c in columns:
                auxDis1 = Utilities.distance(c, prop)
                auxDis2 = Utilities.distance(c, jc[1])
                if(auxDis1 < dis and auxDis1 < auxDis2):
                    dis = auxDis1
                    jc[2] = c
                elif(auxDis2 < dis and auxDis2 < auxDis1):
                    dis = auxDis2
                    jc[2] = c

def getKeyByValue(dict, value):
    key_list = list(dict.keys())
    val_list = list(dict.values()) 
    # one-liner
    return (list(dict.keys())[list(dict.values()).index(value)])