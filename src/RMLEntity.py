class RMLEntity(object):
    def __init__(self, table, o_class, ID, joinConditions, o_prop):
        self.table = table
        self.onto_class = o_class
        self.ID =  ID
        self.joinConditions = joinConditions
        self.onto_properties = o_prop