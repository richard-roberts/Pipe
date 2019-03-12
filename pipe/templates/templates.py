import config


class Template(object):

    def __init__(self):
        self.collection_name = ""
        self.name = ""
        self.function_name = ""
        self.inputs = []
        self.outputs = []
        self.documentation = ""
        self.code = ""

    def setup(self, collection_name, name, inputs, outputs):
        self.collection_name = collection_name
        self.name = name
        self.function_name = name.replace(" ", "_")
        self.inputs = inputs
        self.outputs = outputs
        self.documentation = config.Defaults.Template.new_template_documentation(name)
        self.code = config.Defaults.Template.new_template_code(self.function_name, inputs, outputs)

    def as_json(self):
        return {
            "collection_name": self.collection_name,
            "name": self.name,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "code": self.code,
            "documentation": self.documentation
        }

    def from_json(self, data):
        self.setup(
            data["collection_name"],
            data["name"],
            data["inputs"],
            data["outputs"],
        )
        self.code = data["code"]
        self.documentation = data["documentation"]

    def is_root(self):
        return len(self.inputs) == 0

    def is_leaf(self):
        return len(self.outputs) == 0

    def input_string(self):
        return ", ".join(self.inputs)

    def output_string(self):
        return ", ".join(self.outputs)

    def get_long_name(self):
        return "%s::%s" % (self.collection_name, self.name)


class GraphTemplate(Template):

    def setup(self, collection_name, name, inputs, outputs):
        super(GraphTemplate, self).setup(collection_name, name, inputs, outputs)
        self.code = config.Defaults.Template.graph_execution_template_code(self.function_name, inputs, outputs)
