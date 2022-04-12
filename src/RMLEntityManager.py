from RMLParser import RMLParser
from RMLEntityFactory import RMLEntityFactory


def run(ROOT_DIR, data, ontoManager, manager):

    tables = manager.get_tables()

    rmlEntities = RMLEntityFactory.serialize(tables, manager, ontoManager, 'ontology')

    #Calls the RMLParser given the entities loaded (table, properties and correspondence between ontology and database elements)
    RMLParser.RML_Transformation(data['output'], rmlEntities, ontoManager.ontology, data, ROOT_DIR)