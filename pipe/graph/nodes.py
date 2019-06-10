class BasicNode:

    def __init__(self, library, path, node_id=None, x=0, y=0):
        self.path = path
        self.node_id = node_id if node_id is not None else id(self)
        self.x = x
        self.y = y
        self.template = library.get(self.path)
        self.arguments = {}
        self.outputs = {}

    def __str__(self):
        return self.template.get_name()

    def replace_template(self, new_template):
        old_template = self.template

        args = {}
        for arg in old_template.list_arguments():
            if arg in new_template.list_arguments():
                args[arg] = self.arguments[arg]

        
        outs = {}
        for out in old_template.list_outputs():
            if out in new_template.list_outputs():
                outs[out] = self.outputs[out]

        self.arguments = args
        self.outputs = outs
        self.template = new_template

    def list_arguments(self):
        return self.template.list_arguments()

    def evaluate(self):
        self.outputs = {}
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

    def as_json(self):
        return {
            "path": self.path,
            "id": self.node_id,
            "args": self.arguments,
            "outs": self.outputs,
            "x": self.x,
            "y": self.y,
        }

def from_json(library, data):
    node = BasicNode(
        library,
        data["path"],
        node_id=data["id"],
        x=data["x"],
        y=data["y"]
    )
    node.arguments = data["args"]
    node.outputs = data["outs"]
    return node
