from html import entities
from Utils import Utilities
from RMLEntity import RMLEntity
import rdflib
class RMLEntityFromOntology(object):

    def load(tables, db, ontoManager):

        #self.ID =  RMLEntity.getClassIDTerm(self.onto_class, self.columns)

        classes = ontoManager.onto_classes
        classesDict = dict()
        entities = []

        for y in classes:
            dis = 100
            totalDisFromProp = 100
            name = ""
            for x in range(0, len(tables)):
                #Gets columns for a given table
                columns = db.get_table_columns(tables[x])
                name, dis, auxProperties, auxObjectProperties, totalDisProperties = correspondenceClass(tables[x], columns, y, dis, name, classes, classesDict)
                if (totalDisProperties < totalDisFromProp):
                    totalDisFromProp = totalDisProperties
                    onto_class = y
                    table = tables[x]
                    onto_properties = auxProperties
                    joinConditions = auxObjectProperties
            if (dis < 12):
                classesDict.update({y : name})
            entity = RMLEntity(table, onto_class, "", joinConditions, onto_properties)
            #After creating the entity, it is checked if it has any joinConditions given the prooperties assigned to  the entity
    #        entity.getJoinConditions(tables, dbManager)
            entities.append(entity)
        for x in list(classesDict):
            if classesDict[x] == '':
                del classesDict[x]
        return entities

    #Given the ontology classes, it is checked the one whose name is the most similar to the table assigned to the entity
def correspondenceClass(table, columns, oc_class, lastDis, term, classes, classesDict):
    term1 = Utilities.replace(table)
    try:
        term2 = oc_class.locale
    except:
        term2 = oc_class.split(':').pop()
    dis1 = Utilities.levenshteinDistanceDP(term1, term2)
    bestCol = ""
    dis2 =  100
    for y in columns:
        auxDis2 = Utilities.levenshteinDistanceDP(y, term2)
        if auxDis2 < dis2:
            if (y not in classesDict.values()):
                dis2 = auxDis2
                bestCol = y
            else:
                old_class = getKeyByValue(classesDict, y)
                oldDis = Utilities.levenshteinDistanceDP(old_class.locale, y)
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
    elif (dis1 < lastDis and table not in classesDict.values()): 
        term = table
        lastDis = dis1
    tableReturned = ""
    if(term != ""):
        prop, objProp, totalDis = getProperties(columns, oc_class)
        
    return term, lastDis, prop, objProp, totalDis


def getProperties(columns, oc_class):
    properties = []
    objectProperties = []
    totalDis = 0
    for x in oc_class.domain_of:
        auxDis = 100
        print("Name: ", x.locale, "Type: ", x.rdftype)
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
            auxDis1 = Utilities.levenshteinDistanceDP(columnTerm, propTerm)
            auxDis2 = Utilities.levenshteinDistanceDP(lastTerms, propTerm)
            if(auxDis1 < auxDis or auxDis2 < auxDis):
                if(x.rdftype ==  rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#ObjectProperty')):
                    propObjData = [x, y]
                else:
                    propData = [x, y, "string"]
                auxDis = min(auxDis1, auxDis2)
        if (propData != []):
            properties.append(propData)
        if (propObjData != []):
            for r in x.ranges:
                objectProperties.append([propObjData, r.locale, propObjData[1]])
        totalDis += auxDis
    return properties, objectProperties, totalDis

def getKeyByValue(dict, value):
    key_list = list(dict.keys())
    val_list = list(dict.values()) 
    # one-liner
    return (list(dict.keys())[list(dict.values()).index(value)])