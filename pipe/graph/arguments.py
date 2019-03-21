class Argument:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.edge = None
        self.default_value = None

    def __str__(self):
        return self.pretty()

    def get_node(self):
        return self.node

    def disconnect(self):
        self.edge = None

    def connect(self, edge):
        self.edge = edge

    def is_connected(self):
        return self.edge is not None

    def set_default_value(self, value):
        self.default_value = value

    def reset_default_value(self):
        self.default_value = None

    def has_default_value(self):
        return self.default_value is not None

    def get_connected(self):
        return self.edge

    def pretty(self):
        return "%s.%s" % (self.get_node().template.name, self.name)

    def needs_input(self):
        return self.default_value is None and self.edge is None

    def code_name(self):
        return "%s_%s_%s" % (self.get_node().template.name, self.name, self.get_node().get_id())

    def as_json(self):
        return {
            "name": self.name,
            "default": self.default_value
        }

    @staticmethod
    def from_json(node, data):
        arg = Argument(
            node,
            data["name"]
        )
        arg.default_value = data["default"]
        return arg
