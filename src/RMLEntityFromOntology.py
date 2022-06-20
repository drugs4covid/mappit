from concurrent.futures import ThreadPoolExecutor
from Utils import Utilities
from RMLEntity import RMLEntity
import rdflib
import concurrent
class RMLEntityFromOntology(object):

    def load(tables, db, ontoManager, disMethod, equivalences):

        #self.ID =  RMLEntity.getClassIDTerm(self.onto_class, self.columns)
        classes = ontoManager.onto_classes
        classesDict = dict()
        tableAuxDict = dict()
        entities = []

        for y in classes:
            clasNames = getParents(y)
            clasNames.append(y)

            onto_properties = []
            onto_class = []
            joinConditions = []
            dis = 100
            totalDisFromProp = 0
            name = ""
            tableSelected = ""
            
            if (y not in tableAuxDict.keys()):
                for x in range(0, len(tables)):
                    #Gets columns for a given table
                    columns = db.get_table_columns(tables[x])
                    name, dis, auxProperties, auxObjectProperties, totalDisProperties, changed = correspondenceClass(tables[x], columns, clasNames, dis, name, classesDict, db, disMethod, equivalences)
                    if (changed and totalDisProperties >= totalDisFromProp):
                        totalDisFromProp = totalDisProperties
                        onto_class = y
                        tableSelected = tables[x]
                        onto_properties = auxProperties
                        joinConditions = auxObjectProperties

                if (dis < Utilities.threshold(disMethod)):
                    classesDict.update({y : name})
                    tableAuxDict.update({y.locale : tableSelected})
                    id = Utilities.getClassIDTerm(y, db.get_table_columns(tableSelected))
                    if(id == ''):
                        id = name
                    tableJoinConditions = getNotFoundJoinConditions(y, tables, joinConditions, disMethod, db, equivalences)
                    entity = RMLEntity(tableSelected, onto_class, id, joinConditions, onto_properties)
                    #After creating the entity, it is checked if it has any joinConditions given the prooperties assigned to  the entity
                    #entity.getJoinConditions(tables, dbManager)
                    entities.append(entity)

                    for tjc in tableJoinConditions:
                        entity = RMLEntity(tjc[0], tjc[1], tjc[2], tjc[3], [], True)
                        entities.append(entity)
        

        for x in list(classesDict):
            if classesDict[x] == '':
                del classesDict[x]
        updateJoinConditions(entities, tableAuxDict, db, disMethod)
        return entities

    #Given the ontology classes, it is checked the one whose name is the most similar to the table assigned to the entity
def correspondenceClass(table, columns, oc_classes, lastDis, term, classesDict, db, disMethod, equivalences):

    changed = False
    
    term1 = Utilities.replace(table)

    dis1 = 100
    propCount = 0
    prop = []
    objProp = []
    for c in oc_classes:
        label = c.bestLabel()
        locale = c.locale

        if (label in equivalences.keys()):
            term2 = equivalences[label]
        elif (locale in equivalences.keys()):
            term2 = equivalences[locale]
        else: term2 = label.lower()


        auxDis1 = Utilities.distance(term1, term2)
        bestCol = ""
        dis2 =  100
        
        #bestCol, dis2 = compareColumns(columns, term2, disMethod, dis2, classesDict, oc_classes[-1])

        #if (dis2 + 2 < dis1 and dis2 < lastDis):
        #    term = bestCol
        #    lastDis = dis2
        #    changed = True

        auxProp, auxObjProp, auxTotalDis = getProperties(columns, c, db, table, disMethod)
        for x in auxProp:
            prop.append(x)
        for x in auxObjProp:
            objProp.append(x)
    

        if (auxDis1 <= lastDis and auxDis1 < Utilities.threshold(disMethod) and auxTotalDis >= propCount): 
            term = table
            dis1 = auxDis1
            lastDis = dis1
            changed = True
            propCount = auxTotalDis

        
    return term, lastDis, prop, objProp, propCount, changed

def compareColumns(columns, term, disMethod, dis, classesDict, o_class):
    bestCol = ''
    dis = 100
    for column in columns:
        auxDis2 = Utilities.distance(Utilities.replace(column), term, disMethod)
        if auxDis2 < dis:
            if (column in classesDict.values()):
                classesDict.update({o_class : column})
            dis = auxDis2
            bestCol = column
    return bestCol, dis

def getProperties(columns, oc_class, db, table, disMethod):
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
            propTerm = Utilities.replace(x.bestLabel())

            #Both terms are compared, the column name and the important terms that have been separated
            auxDis1 = Utilities.distance(columnTerm, propTerm, disMethod)
            auxDis2 = Utilities.distance(lastTerms, propTerm, disMethod)
            if((auxDis1 < auxDis and auxDis1 < Utilities.threshold(disMethod)) or (auxDis2 < auxDis and auxDis2 < Utilities.threshold(disMethod))):
                if(x.rdftype ==  rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#ObjectProperty')):
                    propObjData.append([x, y])
                else:
                    propData = [x, y, db.get_column_values(table, y)]
                auxDis = min(auxDis1, auxDis2)

        if(x.rdftype_qname == 'owl:InverseFunctionalProperty'):
            id = Utilities.getClassIDTerm(x, columns)
            if(id != ''):
                propObjData.append([x, id])
            else:
                for c in columns:
                    dis = 100
                    auxDis = Utilities.distance(c, x.bestLabel(), 'lcs')
                    if (auxDis < dis):
                        id = c
                        dis = auxDis
                propObjData.append([x, id])
        if (propData != []):
            properties.append(propData)

        if (propObjData != []):
            correspondenceRange = createJoinConditions(x, propObjData, disMethod)                 
            if(correspondenceRange != []):
                objectProperties.append(correspondenceRange)

    totalDis = len(properties) + len(objectProperties)
    return properties, objectProperties, totalDis

def getNotFoundJoinConditions(o_class, tables, joinconditions, disMethod, db, equivalences):
    jc = []
    for i in joinconditions:
        jc.append(i[0][0])
    notFound = [i for i in o_class.domain_of if i.rdftype ==  rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#ObjectProperty') and i not in jc]

    jcTables = []
    for possibleJCTables in notFound:
        dis = 200
        tableFound = ""

        #Find best suitable table that may connect this property to other classes
        if(len(possibleJCTables.ranges) > 0):
            
            label = possibleJCTables.bestLabel()
            locale = possibleJCTables.locale

            if (label in equivalences.keys()):
                nameProp = equivalences[label]
            elif (locale in equivalences.keys()):
                nameProp = equivalences[locale]
            else: nameProp = label

            nameProp = Utilities.replace(nameProp)
            for t in range(0, len(tables)):
                auxDis = Utilities.distance(nameProp, tables[t], disMethod)
                if (auxDis < dis and auxDis < Utilities.threshold(disMethod)):
                    dis = auxDis
                    tableFound = tables[t]

            nameRange = Utilities.replace(possibleJCTables.ranges[0].locale)
            nameDomain = Utilities.replace(possibleJCTables.domains[0].locale)
            disTarget = 200
            disID = 200
            childColumn = ""
            parentColumn = ""
            
            if (tableFound != ''):
                for c in db.get_table_columns(tableFound):
                    nameColumn = Utilities.replace(c)

                    #Find child column
                    auxDis = Utilities.distance(nameRange, nameColumn, disMethod)
                    if(auxDis < disTarget):
                        childColumn = c
                        disTarget = auxDis

                    #Find parent column
                    auxDis = Utilities.distance(nameDomain, nameColumn, disMethod)
                    if(auxDis < disID):
                        parentColumn = c
                        disID = auxDis

                if(parentColumn != '' and childColumn != ''):
                    for r in possibleJCTables.ranges:
                        rangeParentClasses = getParents(r)
                        rangeChildrenClasses = getChildren(r)

                        rangeclasses = []
                        for x in rangeParentClasses:
                            rangeclasses.append(x)
                        for x in rangeChildrenClasses:
                            rangeclasses.append(x)
                        rangeclasses.append(r)

                        jcFound = []
                        for x in rangeclasses:
                            t = x.locale
                            jcFound.append([[possibleJCTables, childColumn], t, ""])
                        jcTables.append([tableFound, o_class, parentColumn, jcFound])
    return jcTables



def createJoinConditions(prop, propertiesData, disMethod):
    correspondenceRange = []
    for r in prop.ranges:
        rangeDis = 30
        for s in propertiesData:
            if (s[0].rdftype_qname == 'owl:InverseFunctionalProperty'):
                correspondenceRange = [s, r.locale, ""]
            else:
                name = Utilities.replace(s[1])
                rangeDisAux = Utilities.distance(Utilities.replace(r.bestLabel()), name, disMethod)
                correspondenceRange = [s, r.locale, ""]
                if(rangeDis > rangeDisAux):
                    rangeDis = rangeDisAux
                    correspondenceRange = [s, r.locale, s[1]]
    return correspondenceRange

def updateJoinConditions(entities, tableDict, db, disMethod):
    for e in entities:
            for jc in e.joinConditions:
                try:
                    dis = 100
                    if(jc[0][0].rdftype_qname != 'owl:InverseFunctionalProperty'):
                        columns = db.get_table_columns(tableDict[jc[1]])
                        for c in columns:
                            auxDis1 = Utilities.distance(c, jc[1], disMethod)
                            if(auxDis1 < dis):
                                dis = auxDis1
                                id = Utilities.getClassIDTerm(jc[0][0], columns)
                                if (id != ''):
                                    jc[2] = id
                                else:
                                    jc[2] = c
                    else:
                        columns = db.get_table_columns(tableDict[jc[1]])
                        for c in columns:
                            auxDis1 = Utilities.distance(c, jc[0][0].locale, 'lcs')
                            auxDis2 = Utilities.distance(c, e.onto_class.locale, 'lcs')
                            if(auxDis1 < dis and auxDis1 < Utilities.threshold('lcs')):
                                dis = auxDis1
                                jc[2] = c
                            if(auxDis2 < dis and auxDis2 < Utilities.threshold('lcs')):
                                dis = auxDis2
                                jc[2] = c

                        id = Utilities.getClassIDTerm(jc[1], columns)
                        if (id != '' and jc[2] == ''):
                            jc[2] = id


                except: e.joinConditions.remove(jc)

def getKeyByValue(dict, value):
    key_list = list(dict.keys())
    val_list = list(dict.values()) 
    # one-liner
    return (list(dict.keys())[list(dict.values()).index(value)])

def getParents(c):
    totalPar = []
    actPar = c._parents
    while(actPar != []):
        totalPar.append(actPar[-1])
        actPar = actPar[0]._parents
    return totalPar

def getChildren(c):
    totalChildren = []
    actPar = c._children
    while(actPar != []):
        totalChildren.append(actPar[-1])
        actPar = actPar[0]._children
    return totalChildren

def getSuperParent(c):
    try:
        return getParents(c)[-1]
    except: 
        return c

    

    