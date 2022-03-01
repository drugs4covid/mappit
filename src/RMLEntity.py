class RMLEntity(object):
    def __init__(self, table, onto_class, class_properties):
        self.onto_class = onto_class
        self.onto_properties = class_properties
        self.table = table