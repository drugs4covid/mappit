import ontospy

class OntologyManager(object):


    #Uses the ontospy library to load the ontology given its uri or file
    def loadOntology(UriOrFile):
        return ontospy.Ontospy(UriOrFile, verbose=True, hide_implicit_preds=True, hide_implicit_types=True)

    #Returns all the classes loaded by ontospy for a given ontology
    def get_onto_classes(ontology):
        classes = []
        for x in ontology.all_classes:
            classes.append(x)
        return classes
    
    #For a given class, given all properties of the ontology, it checks for only those that refer to this class in their range or domain.
    #Actually this method is not used because it doesn't retrieve all the properties for a given class
    def get_class_properties(ontology, o_class):
        properties = []
        total_prop = []
        for x in ontology.all_properties:
            for y in x.ranges:
                if y.qname == o_class.qname:
                    properties.append(x)
            for y in x.domains:
                if y.qname == o_class.qname:
                    properties.append(x)
        total_prop.append([o_class, properties])
        return properties
    
     #For a given class, given all properties of the ontology, it checks for only those that refer to this class in their range or domain.
    #Actually this method is not used because it doesn't retrieve all the properties for a given class
    def get_onto_properties(ontology, classes):
        properties = []
        for x in classes:
            properties_class = OntologyManager.get_class_properties(ontology, x)
            if len(properties_class) != 0:
                properties.append(properties_class)
        return properties

    def __init__(self, uri):
        self.onto_uri = uri
        self.ontology = OntologyManager.loadOntology(uri)
        self.onto_classes = OntologyManager.get_onto_classes(self.ontology)
        self.onto_properties = OntologyManager.get_onto_properties(self.ontology, self.onto_classes)