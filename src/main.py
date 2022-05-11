from OntologyManager import OntologyManager
from DataManager import DataManager
import RMLEntityManager
import json
import os
import sys

#Loads the properties file
def loadProperties(propertiesFile):
        with open(propertiesFile) as json_file:
            data = json.load(json_file)
            json_file.close()
        return data

#If there are any properties that aren't loaded by ontospy, loads additional properties declared in the properties file
def appendAdditionalProperties(data, properties):
    for x in data['properties']:
        properties.append(x['name'])

#If there are any classes that aren't loaded by ontospy, loads additional classes declared in the properties file
def appendAdditionalClasses(data, classes):
    for x in data['classes']:
        classes.append(x['name'])

#Loads additional ontologies
def loadAdditionalOntologies(data, ontology):
    for x in data['ontologies']:
        addOnto = OntologyManager(x['URI'])
        for c in addOnto.ontology.all_classes:
            ontology.all_classes.append(c)
        for p in addOnto.ontology.all_properties:
            ontology.all_properties.append(p)


#The properties, ontology and database are loaded. Then, all the information is given to the RMLEntityManager to create the entities
# and parse the data into the document.
def main():
    
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    data = loadProperties(ROOT_DIR + '/properties/properties_sfo.json')

    ontoManager = OntologyManager(ROOT_DIR, data['main_ontology'])

    dataManager = DataManager()
    dataManager.serialize(data['Data'])

    RMLEntityManager.run(ROOT_DIR, data, ontoManager, dataManager)

if __name__ == "__main__":
    main()
