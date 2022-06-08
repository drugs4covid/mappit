from Utils import Utilities
from RMLEntity import RMLEntity


class RMLEntityFromDB(object):

    #Initialization of the entity. It recieves the correspondent table and columns from the database, the dataManager and the ontoManager

        #Table: table from the database (TriplesMap)
        #Onto_class: A class from the ontology. It depicts the same element as the table from the database
        #ID: Id that identifies each individual by their IRI in the SubjectMap
        #Columns: columns (properties) of the given table
        #Onto_properties: All the properties from the ontology that correspond to the given columns of the table
        #Join Conditions: Properties joined to another properties from another TriplesMap

    def load(tables, db, ontoManager, disMethod, equivalences):

        entities = []
        for x in range(0, len(tables)):
            onto_class = RMLEntityFromDB.correspondenceClass(tables[x], ontoManager.onto_classes, disMethod)
            if(onto_class != ''):
                columns = db.get_table_columns(tables[x])
                ID =  Utilities.getClassIDTerm(onto_class, columns)
                onto_properties, joinConditions = RMLEntityFromDB.get_class_properties(ontoManager, db, columns, tables[x], ID)


                entity = RMLEntity(tables[x], onto_class, ID, joinConditions, onto_properties)
                
                entities.append(entity)
        return entities
    
    #Given the ontology classes, it is checked the one whose name is the most similar to the table assigned to the entity
    def correspondenceClass(table, oc_classes, disMethod):
        dis = 100
        term = ""
        for x in oc_classes:
            term1 = Utilities.replace(table)
            term2 = x.locale
            auxDis = Utilities.distance(term1, term2)
            if auxDis < dis and auxDis < Utilities.threshold(disMethod):
                dis = auxDis
                term = x
        return term

    def rangesToItself(prop, table):
        i = 0
        foundByRange = False
        ranges = prop.ranges


        while(foundByRange == False and i < len(ranges)):
            range = ranges[i]
            if(Utilities.distance(range.locale.split(':').pop().lower(), table.lower()) < 2.0):
                foundByRange = True
            else:
                foundByRange = False
            i+=1

        return foundByRange

    #Given the ontology, it retrieves an array of objects:
    #   - Property Name
    #   - Column Name
    #   - Values of the column in the table
    def get_class_properties(ontoManager, db, columns, table, ID):
        properties = []
        joinConditions = []
        #Each of the columns in the table assigned to the entity are compared to each of the properties of the ontology.
        #This is done by comparing their names using the jaro_distance.
        for col in columns:
            term = []
            dis = 0
            for prop in ontoManager.onto_properties:
                
                #Column Name
                columnTerm = Utilities.replace(col)
                terms = str(col).split('_')
                terms.remove(terms[0])

                #Important terms of the column, this means that, in case that the column contains the name of the column in it's name,
                #for example, shape_distance_travelled, shape is deleted and only distancetravelled is considered 
                lastTerms = ''.join(terms).lower()
                try:
                    propTerm = prop.locale.split(':').pop().lower()
                except:
                    propTerm = prop.split(':').pop().lower()

                #Both terms are compared, the column name and the important terms that have been separated
                auxDis1 = Utilities.distance(columnTerm, propTerm, "jaro")
                auxDis2 = Utilities.distance(lastTerms, propTerm, "jaro")

                # First, it is prefered the complete column name, if it isn't similar, the terms obtained from the column name are
                # checked and the property is selected in case that the important terms are long enough to be reliable (small terms like 'id' might
                # bring a lot of confusion when compared)
                rangesToItself = RMLEntityFromDB.rangesToItself(prop, table)
                if (auxDis1 > dis and rangesToItself == False):
                    dis = auxDis1
                    term = prop
                elif (auxDis2 > dis and len(lastTerms) > 2 and rangesToItself == False):
                    dis = auxDis2
                    term = prop
            #ID columns are ignored and the property is appended to the list
            IDterm = Utilities.replace(ID)
            if (columnTerm != IDterm):
                tables = db.get_tables()
                ###############################comprobar
                if((len(ontoManager.onto_object_properties) > 0 and term in ontoManager.onto_object_properties) or len(ontoManager.onto_object_properties) == 0):
                    t, colCor = RMLEntityFromDB.checkJoinCondition(term, tables, table, db)
                    if (colCor != ""):
                        joinConditions.append([[term, col], t, colCor])
                    else:
                        columnVal = db.get_column_values(table, col)
                        properties.append([term, col, columnVal])
                else: 
                    columnVal = db.get_column_values(table, col)
                    properties.append([term, col, columnVal])
        return properties, joinConditions

    # The range of a given property is compared to each of the tables from the database. If the terms are similar, thhe given table that
    # corresponds to the Parent TriplesMap is assigned.
    def getTableByRange(tables, range):
        dis = 0
        i = 0
        found = False
        table = []
        while(found == False and i < len(tables)):
            dis = Utilities.distance(range, str(tables[i].lower()))
            if (dis <= 1.0):
                table = tables[i]
                found = True
            i+=1
        return table, found

    # For a given table that corresponds to the Parent TriplesMap of the join condition, the name of the property is compared to all the column names
    # of the given table in order to find its correspondence:
    # - parentTriplesMap: table
    # - child: prop_name
    # - parent: column
    def getTableColumnCorrespondence(table, prop_name, db):
        try:
            tableColumns = db.get_table_columns(table)
            dis = 5
            correspondenceCol = ""
            for col in tableColumns:
                auxDis = Utilities.distance(prop_name, col)
                if auxDis < dis:
                    dis = auxDis
                    correspondenceCol = col
            return correspondenceCol
        except: return ""
    
    # Given a property and the total number of tables of the database, first, it is checked if that property refers to another table of
    # the database. If the property and the table names are similar and the property doesn't refer to the table assigned to this entity,
    # it is checked whick of the columns correspond to this property.

    #Returns:
    # [table (Parent TriplesMap), column (rr: parent)]
    def checkJoinCondition(prop, tables, table, db):
        t = []
        col = ""
        name = ""
        i = 0
        foundByRange = False

        try:
            ranges = prop.ranges
        except:
            ranges = []
        # Given the range of the property, it is checked if any of the classes refer to any table to see if there is any join condition
        while(foundByRange == False and i < len(ranges)):
            range = ranges[i]
            t, foundByRange = RMLEntityFromDB.getTableByRange(tables, range.locale.split(':').pop().lower())

            #In case the range of the property corresponds to any table of the database and it isn't their own class, the column is found and
            # assigned
            if(foundByRange and t != table):
                name = prop.locale.split(':').pop().lower()
                col = RMLEntityFromDB.getTableColumnCorrespondence(t, name, db)
            else:
                foundByRange = False
            i+=1
        return name, col





