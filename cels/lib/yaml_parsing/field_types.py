class TaggedScalar(str):
    def __new__(cls, value, tag):
        obj = str.__new__(cls, value)
        obj.tag = tag
        return obj


class TaggedSequence(list):
    def __init__(self, value, tag):
        super().__init__(value)
        self.tag = tag


class TaggedMapping(dict):
    def __init__(self, value, tag):
        super().__init__(value)
        self.tag = tag
