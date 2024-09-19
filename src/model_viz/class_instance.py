class ClassInstance:
    def __init__(self, class_object: object):
        self.class_name: str
        self.inherits_from: list[str] = []
        self.functions: list[str] = []
        self.attributes: list[str] = []

        self.set_attributes(class_object=class_object)

    def set_attributes(self, class_object: object):
        pass
