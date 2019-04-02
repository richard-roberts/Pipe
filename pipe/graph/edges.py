class Edge:

    def __init__(self, argument_from, argument_to):
        self.argument_from = argument_from
        self.argument_to = argument_to
        self.argument_from.connect(self)
        self.argument_to.connect(self)

    def __str__(self):
        return "%s.%s-%s.%s" % (
            self.argument_from.get_node().template.name,
            self.argument_from.template_arg.name,
            self.argument_to.get_node().template.name,
            self.argument_to.template_arg.name
        )

    def as_json(self):
        return {
            "node_id_from": self.argument_from.get_node().get_id(),
            "arg_from_name": self.argument_from.template_arg.name,
            "node_id_to": self.argument_to.get_node().get_id(),
            "arg_to_name": self.argument_to.template_arg.name,
        }

    def disconnect(self):
        self.argument_from.disconnect(self)
        self.argument_to.disconnect(self)

    def is_connected_to_node(self, node):
        matches_from = node == self.argument_from.get_node()
        matches_to = node == self.argument_to.get_node()
        return matches_from or matches_to

    @staticmethod
    def from_json(graph, data):
        try:
            node_from = graph.get_node_by_id(data["node_id_from"])
        except KeyError:
            return None

        try:
            node_to = graph.get_node_by_id(data["node_id_to"])
        except KeyError:
            return None

        argument_from = node_from.get_output_argument_by_name(data["arg_from_name"])

        argument_to = node_to.get_input_argument_by_name(data["arg_to_name"])
        return Edge(argument_from, argument_to)
