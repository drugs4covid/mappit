from DatabaseManager import DatabaseManager
from OntologyManager import OntologyManager
import RMLEntityManager
import json
import os
import sys

def loadProperties(propertiesFile):
        with open(propertiesFile) as json_file:
            data = json.load(json_file)
            json_file.close()
        return data

def appendAdditionalProperties(data, properties):
    for x in data['properties']:
        properties.append(x['name'])

def appendAdditionalClasses(data, classes):
    for x in data['classes']:
        classes.append(x['name'])

def getTypeManager(data):
    manager = []
    try:
        manager = DatabaseManager(data)
    except:
        print("Error with Data on properties file")
    return manager

def main():
    
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    data = loadProperties(ROOT_DIR + '/properties/' + sys.argv[1])

    ontoManager = OntologyManager(data['main_ontology'])
    dataManager = getTypeManager(data['Data'])

    ontology = ontoManager.ontology

    appendAdditionalProperties(data, ontology.all_properties)
    appendAdditionalClasses(data, ontology.all_classes)

    RMLEntityManager.run(ROOT_DIR, data, ontoManager, dataManager)

if __name__ == "__main__":
    main()
