from RMLEntityFromDB import RMLEntityFromDB
from RMLEntityFromOntology import RMLEntityFromOntology

class RMLEntityFactory:
    def serialize(tables, db, ontoManager, format, disMethod, equivalences):
        serializer = get_serializer(format)
        return serializer(tables, db, ontoManager, disMethod, equivalences)

def get_serializer(format):
    if format.lower() == 'database':
        return _serialize_from_DB
    elif format.lower() == 'ontology':
        return _serialize_from_ontology
    else:
        raise ValueError(format)

def _serialize_from_DB(tables, db, ontoManager, disMethod, equivalences):
    entities = RMLEntityFromDB.load(tables, db, ontoManager, disMethod, equivalences)
    return entities

def _serialize_from_ontology(tables, db, ontoManager, disMethod, equivalences):
    entities = RMLEntityFromOntology.load(tables, db, ontoManager, disMethod, equivalences)
    return entities