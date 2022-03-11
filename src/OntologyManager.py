import ontospy

class OntologyManager(object):


    def loadOntology(uri):
        return ontospy.Ontospy(uri, verbose=True, hide_implicit_preds=True, hide_implicit_types=True)

    def get_onto_classes(ontology):
        classes = []
        for x in ontology.all_classes:
            classes.append(x)
        return classes

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

    def get_onto_properties(ontology, classes):
        properties = []
        for x in classes:
            properties_class = OntologyManager.get_class_properties(ontology, x)
            if len(properties_class) != 0:
                properties.append(properties_class)
        return properties

    #def get_JoinConditions()

    def __init__(self, uri):
        self.onto_uri = uri
        self.ontology = OntologyManager.loadOntology(uri)
        self.onto_classes =OntologyManager.get_onto_classes(self.ontology)
        self.onto_properties = OntologyManager.get_onto_properties(self.ontology, self.onto_classes)