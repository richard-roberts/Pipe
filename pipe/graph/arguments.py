import json


class Argument:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.alias = name
        self.edges = {}
        self.default_value = json.dumps(None)
        self.evaluated_value = json.dumps(None)

    def __str__(self):
        return self.pretty()

    def get_node(self):
        return self.node

    def disconnect(self, edge):
        del self.edges[str(edge)]

    def connect(self, edge):
        self.edges[str(edge)] = edge

    def is_connected(self):
        return len(self.edges) > 0

    def set_default_value(self, value):
        self.default_value = value
        if self.evaluated_value is None or self.evaluated_value == json.dumps(None):
            self.set_evaluated_value(self.default_value)

    def reset_default_value(self):
        self.default_value = None

    def get_evaluated_value(self):
        return self.evaluated_value

    def set_input_value(self, value):
        self.evaluated_value = value

    def set_evaluated_value(self, value):
        if value is None or value == json.dumps(None):
            return
        self.evaluated_value = value
        for edge in self.edges.values():
            edge.argument_to.set_input_value(value)

    def has_default_value(self):
        return self.default_value is not None

    def get_connected(self):
        return self.edges.values()

    def pretty(self):
        return "%s.%s" % (self.get_node().template.name, self.name)

    def needs_input(self):
        return self.default_value is None and len(self.edges) == 0

    def code_name(self):
        return "%s_%s_%s" % (self.get_node().template.name, self.name, self.get_node().get_id())

    def as_json(self):
        return {
            "name": self.name,
            "alias": self.alias,
            "default": self.default_value,
            "eval_value": self.evaluated_value
        }

    @staticmethod
    def from_json(node, data):
        arg = Argument(
            node,
            data["name"]
        )
        arg.alias = data["alias"]
        arg.set_default_value(data["default"])
        arg.set_evaluated_value(data["eval_value"])
        return arg
