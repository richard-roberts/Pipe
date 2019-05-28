class BasicNode:

    def __init__(self, library, path, node_id=None):
        self.path = path
        self.node_id = node_id if node_id is not None else id(self)
        self.template = library.get(self.path)
        self.arguments = {}
        self.outputs = {}

    def __str__(self):
        return self.template.get_name()

    def list_arguments(self):
        return self.template.list_arguments()

    def evaluate(self):
        result = self.template.execute(self.arguments)
        for key in result.keys():
            value = result[key]
            self.outputs[key] = value

    def set_argument(self, key, value):
        self.arguments[key] = value

    def read_output(self, key):
        return self.outputs[key]

    def has_output(self, key):
        return key in self.outputs.keys()
