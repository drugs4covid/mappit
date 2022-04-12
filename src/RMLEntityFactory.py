from html import entities
from RMLEntityFromDB import RMLEntityFromDB
from RMLEntityFromOntology import RMLEntityFromOntology

class RMLEntityFactory:
    def serialize(tables, db, ontoManager, format):
        serializer = get_serializer(format)
        return serializer(tables, db, ontoManager)

def get_serializer(format):
    if format.lower() == 'database':
        return _serialize_from_DB
    elif format.lower() == 'ontology':
        return _serialize_from_ontology
    else:
        raise ValueError(format)

def _serialize_from_DB(tables, db, ontoManager):
    entities = RMLEntityFromDB.load(tables, db, ontoManager)
    return entities

def _serialize_from_ontology(tables, db, ontoManager):
    entities = RMLEntityFromOntology.load(tables, db, ontoManager)
    return entities