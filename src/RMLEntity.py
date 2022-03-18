from Utils import Utilities
from DatabaseManager import DatabaseManager

class RMLEntity(object):

    #Different characters that are replaced from the columns and tables from the database
    charsToReplace = ['-', '_', '*', '|', '^', '+', '`']

    #Initialization of the entity. It recieves the correspondent table and columns from the database, the dataManager and the ontoManager

        #Table: table from the database (TriplesMap)
        #Onto_class: A class from the ontology. It depicts the same element as the table from the database
        #ID: Id that identifies each individual by their IRI in the SubjectMap
        #Columns: columns (properties) of the given table
        #Onto_properties: All the properties from the ontology that correspond to the given columns of the table
        #Join Conditions: Properties joined to another properties from another TriplesMap

    def __init__(self, table, columns, db, ontoManager):
        self.table = table
        self.columns = db.get_table_columns(self.table)
        self.onto_class = RMLEntity.correspondenceClass(self, ontoManager.onto_classes)
        self.ID =  RMLEntity.getClassIDTerm(self.onto_class, columns)
        self.onto_properties = RMLEntity.get_class_properties(self, ontoManager.ontology, db)
        self.joinConditions = []
    
    #Method that eliminates all the separators from the given term. 
    def replace (s):
        name = str(s)
        for c in RMLEntity.charsToReplace:
            name = name.replace(c, '')
        return name.lower()

    #By using the LevenshteinDistance, the id of the class given all the columns is detected. 
    def getClassIDTerm(onto_class, columns):
        dis = 10
        term = ""
        for x in columns:
            name = RMLEntity.replace(x)
            try:
                onto_name = onto_class.qname
            except:
                onto_name = onto_class
            #The name of the class in the ontology is compared to the column. 'id' is added to the class name in order to get the
            #id in the columsn more efficiently
            auxDis = Utilities.levenshteinDistanceDP(name, onto_name.split(':').pop() + 'id')
            #The column is checked in order to see if it is actually an id and the distance is checked to be lower than 2.0, which means
            #that only two replacements must be done in order to have both strings to be the same. This is done in order to see that the column is 
            #actually the class id and not a reference to another table
            if (name.endswith('id') or name.startswith('id')) and auxDis < dis and auxDis < 2.0:
                dis = auxDis
                term = x
        return term
    
    #Given the ontology classes, it is checked the one whose name is the most similar to the table assigned to the entity
    def correspondenceClass(self, oc_classes):
        dis = 100
        term = ""
        for x in oc_classes:
            term1 = RMLEntity.replace(self.table)
            try:
                term2 = x.qname.split(':').pop()
            except:
                term2 = x.split(':').pop()
            auxDis = Utilities.levenshteinDistanceDP(term1, term2)
            if auxDis < dis:
                dis = auxDis
                term = x
        return term

    #Given the ontology, it retrieves an array of objects:
    #   - Property Name
    #   - Column Name
    #   - Values of the column in the table
    def get_class_properties(self, ontology, db):
        properties = []
        #Each of the columns in the table assigned to the entity are compared to each of the properties of the ontology.
        #This is done by comparing their names using the jaro_distance.
        for col in self.columns:
            term = []
            dis = 0
            for prop in ontology.all_properties:
                
                #Column Name
                columnTerm = RMLEntity.replace(col)
                terms = str(col).split('_')
                terms.remove(terms[0])

                #Important terms of the column, this means that, in case that the column contains the name of the column in it's name,
                #for example, shape_distance_travelled, shape is deleted and only distancetravelled is considered 
                lastTerms = ''.join(terms).lower()
                try:
                    propTerm = prop.qname.split(':').pop().lower()
                except:
                    propTerm = prop.split(':').pop().lower()

                #Both terms are compared, the column name and the important terms that have been separated
                auxDis1 = Utilities.jaro_distance(columnTerm, propTerm)
                auxDis2 = Utilities.jaro_distance(lastTerms, propTerm)

                # First, it is prefered the complete column name, if it isn't similar, the terms obtained from the column name are
                # checked and the property is selected in case that the important terms are long enough to be reliable (small terms like 'id' might
                # bring a lot of confusion when compared)
                if (auxDis1 > dis):
                    dis = auxDis1
                    term = prop
                elif (auxDis2 > dis and len(lastTerms) > 2):
                    dis = auxDis2
                    term = prop
            #ID columns are ignored and the property is appended to the list
            IDterm = RMLEntity.replace(self.ID)
            if (columnTerm != IDterm):
                columnVal = db.get_column_values(self.table, col)
                properties.append([term, col, columnVal])
        return properties

    # For each property assigned to the entity (class), it is checked if any table has a column that is referred by the property.
    def getJoinConditions(self, tables, db):
        for prop in self.onto_properties:
            t, colCor = RMLEntity.checkJoinCondition(self, prop, tables, db)
            if (colCor != ""):
                self.joinConditions.append([prop, t, colCor])
                self.onto_properties.remove(prop)

    # The range of a given property is compared to each of the tables from the database. If the terms are similar, thhe given table that
    # corresponds to the Parent TriplesMap is assigned.
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

    # For a given table that corresponds to the Parent TriplesMap of the join condition, the name of the property is compared to all the column names
    # of the given table in order to find its correspondence:
    # - parentTriplesMap: table
    # - child: prop_name
    # - parent: column
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
    
    # Given a property and the total number of tables of the database, first, it is checked if that property refers to another table of
    # the database. If the property and the table names are similar and the property doesn't refer to the table assigned to this entity,
    # it is checked whick of the columns correspond to this property.

    #Returns:
    # [table (Parent TriplesMap), column (rr: parent)]
    def checkJoinCondition(self, prop, tables, db):
        i = 0
        foundByRange = False
        t = []
        col = ""
        try:
            ranges = prop[0].ranges
        except:
            ranges = []
        # Given the range of the property, it is checked if any of the classes refer to any table to see if there is any join condition
        while(foundByRange == False and i < len(ranges)):
            t, foundByRange = RMLEntity.getTableByRange(tables, ranges[i].qname.split(':').pop().lower())

            #In case the range of the property corresponds to any table of the database and it isn't their own class, the column is found and
            # assigned
            if(foundByRange and t != self.table):
                name = prop[0].qname.split(':').pop().lower()
                col = RMLEntity.getTableColumnCorrespondence(t, name, db)

            else:
                foundByRange = False
            i+=1
        return t, col





