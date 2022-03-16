from RMLEntity import RMLEntity
from DatabaseManager import DatabaseManager
from OntologyManager import OntologyManager
from RMLParser import RMLParser
import os

def getRMLEntities(tables, ontoManager, dbManager):
    entities = []
    for x in range(0, len(tables)):
        columns = DatabaseManager.get_table_columns(dbManager, tables[x])
        entity = RMLEntity(tables[x], columns, dbManager, ontoManager)
        entity.getJoinConditions(tables, dbManager)
        entities.append(entity)
    return entities



def run(ROOT_DIR, data, ontoManager, manager):

    tables = manager.get_tables()

    rmlEntities = getRMLEntities(tables, ontoManager, manager)

    RMLParser.RML_Transformation(data['output'], rmlEntities, ontoManager.ontology, data, ROOT_DIR)