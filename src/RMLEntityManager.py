from RMLParser import RMLParser
from R2RMLParser import R2RMLParser
from RMLEntityFactory import RMLEntityFactory
from Utils import Utilities


def run(ROOT_DIR, data, ontoManager, manager, equivalences):

    tables = manager.get_tables()

    rmlEntities = RMLEntityFactory.serialize(tables, manager, ontoManager, data['compare_system'],  data['distance_method'], equivalences)
    #Calls the RMLParser given the entities loaded (table, properties and correspondence between ontology and database elements)
    if (data['MapLanguage'] == 'RML'):
        RMLParser.RML_Transformation(data['output'], rmlEntities, ontoManager.ontology, data, ROOT_DIR)
    elif(data['MapLanguage'] == 'R2RML'):
        if(data['Data']['format'] == 'database'):
            R2RMLParser.R2RML_Transformation(data['output'], rmlEntities, ontoManager.ontology, data, ROOT_DIR)
        else:
            print('ERROR: R2RML only works for relational databases, try with RML')
