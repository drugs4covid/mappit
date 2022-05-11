from RMLParser import RMLParser
from RMLEntityFactory import RMLEntityFactory
from Utils import Utilities


def run(ROOT_DIR, data, ontoManager, manager):

    tables = manager.get_tables()

    rmlEntities = RMLEntityFactory.serialize(tables, manager, ontoManager, data['compare_system'])
    if(data['distance_method']):
        Utilities.setDistMethod(data['distance_method'])
    #Calls the RMLParser given the entities loaded (table, properties and correspondence between ontology and database elements)
    RMLParser.RML_Transformation(data['output'], rmlEntities, ontoManager.ontology, data, ROOT_DIR)