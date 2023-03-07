from OntologyManager import OntologyManager
from DataManager import DataManager
import RMLEntityManager
import json
import os
import argparse

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

def loadEquivalences(data):
    equivalenceDict = dict()
    try:
        for x in data['list_equivalence']:
            equivalenceDict.update({x['entity'] : x['equivalence']})
    except: pass
    return equivalenceDict



#The properties, ontology and database are loaded. Then, all the information is given to the RMLEntityManager to create the entities
# and parse the data into the document.
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(dest="prop", help="Properties file")
    args = parser.parse_args()

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    #data = loadProperties(ROOT_DIR + '/properties/properties-cmt_structured.json')
    #data = loadProperties(os.path.join(ROOT_DIR, args.prop))
    data = loadProperties(args.prop)

    ontoManager = OntologyManager(ROOT_DIR, data['main_ontology'])

    for x in ontoManager.onto_classes:
        print(x.bestLabel())

    equivalences = loadEquivalences(data)

    dataManager = DataManager()
    dataManager.serialize(data['Data'])


    RMLEntityManager.run(ROOT_DIR, data, ontoManager, dataManager, equivalences)

if __name__ == "__main__":
    main()
