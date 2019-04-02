import json


class Argument:

    def __init__(self, node, template_arg):
        self.node = node
        self.template_arg = template_arg
        self.alias = self.template_arg.name
        self.edges = {}
        if template_arg.has_default():
            self.evaluated_value = self.template_arg.get_default()
        else:
            self.evaluated_value = None

    def __str__(self):
        return self.pretty()

    def get_alias(self):
        return self.alias

    def set_alias(self, alias):
        self.alias = alias

    def get_name(self):
        return self.template_arg.name

    def get_name_with_id(self):
        return "%s_%s" % (self.get_name(), str(self.node))

    def get_name_with_default(self):
        return self.template_arg.get_name_with_default()

    def get_node(self):
        return self.node

    def disconnect(self, edge):
        del self.edges[str(edge)]

    def connect(self, edge):
        self.edges[str(edge)] = edge

    def is_connected(self):
        return len(self.edges) > 0

    def set_default_value(self, value):
        self.template_arg.set_default(value)
        if self.evaluated_value is None or self.evaluated_value == json.dumps(None):
            self.set_evaluated_value(self.template_arg.get_default())

    def reset_default_value(self):
        self.template_arg.set_default(None)

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
        return self.template_arg.has_default()

    def get_default_value(self):
        return self.template_arg.get_default()

    def get_connected(self):
        return list(self.edges.values())

    def get_first_connected(self):
        if len(self.edges) != 1:
            raise ValueError("This is not allowed, must have only one input")
        first_key = list(self.edges.keys())[0]
        return self.edges[first_key]

    def pretty(self):
        return "%s.%s" % (self.get_node().template.name, self.alias)

    def needs_input(self):
        return self.template_arg.get_default() is None and len(self.edges) == 0

    def code_name(self):
        return "%s_%s_%s" % (self.get_node().template.name, self.template_arg.name, self.get_node().get_id())

    def as_json(self):
        return {
            "template_arg": self.template_arg.name,
            "alias": self.alias,
            "eval_value": self.evaluated_value
        }

    @staticmethod
    def from_json(node, data):
        template_arg = node.template.get_arg_by_name(data["template_arg"])
        arg = Argument(
            node,
            template_arg
        )
        arg.alias = data["alias"]
        arg.set_evaluated_value(data["eval_value"])
        return arg
