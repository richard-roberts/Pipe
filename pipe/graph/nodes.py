class BasicNode:

    def __init__(self, template):
        self.template = template
        self.arguments = {}
        self.outputs = {}

    def __str__(self):
        return self.template.get_name()

    def list_arguments(self):
        return self.template.list_arguments()

    def evaluate(self):
        self.outputs = {}
        result = self.template.execute(argument_data=self.arguments)
        for key in result.keys():
            value = result[key]
            self.outputs[key] = value

    def set_argument(self, key, value):
        self.arguments[key] = value

    def read_output(self, key):
        return self.outputs[key]

    def has_output(self, key):
        return key in self.outputs.keys()
