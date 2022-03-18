from RMLEntity import RMLEntity
from DatabaseManager import DatabaseManager
from RMLParser import RMLParser

# Creates all RMLEntities given the ontology classes and properties loaded and the data loaded
def getRMLEntities(tables, ontoManager, dbManager):
    entities = []
    for x in range(0, len(tables)):
        #Gets columns for a given table
        columns = DatabaseManager.get_table_columns(dbManager, tables[x])
        entity = RMLEntity(tables[x], columns, dbManager, ontoManager)
        #After creating the entity, it is checked if it has any joinConditions given the prooperties assigned to  the entity
        entity.getJoinConditions(tables, dbManager)
        entities.append(entity)
    return entities



def run(ROOT_DIR, data, ontoManager, manager):

    tables = manager.get_tables()

    rmlEntities = getRMLEntities(tables, ontoManager, manager)

    #Calls the RMLParser given the entities loaded (table, properties and correspondence between ontology and database elements)
    RMLParser.RML_Transformation(data['output'], rmlEntities, ontoManager.ontology, data, ROOT_DIR)