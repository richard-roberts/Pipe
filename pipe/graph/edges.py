class BasicDirectedEdge:

    def __init__(self, node_from, arg_from_name, node_to, arg_to_name):
        self.node_from = node_from
        self.arg_from = arg_from_name
        self.node_to = node_to
        self.arg_to = arg_to_name

    def output_connected_to(self, node, argument_name):
        return self.node_to == node and self.arg_to == argument_name

    def as_json(self):
        return {
            "node_id_from" : id(self.node_from),
            "arg_from" : self.arg_from,
            "node_id_to" : id(self.node_to),
            "arg_to" : self.arg_to
        }

