class BasicDirectedEdge:

    def __init__(self, node_from, arg_from_name, node_to, arg_to_name):
        self.node_from = node_from
        self.arg_from = arg_from_name
        self.node_to = node_to
        self.arg_to = arg_to_name

    def output_connected_to(self, node, argument_name):
        return self.node_to == node and self.arg_to == argument_name

    def node_from_matches_id(self, node_id):
        return self.node_from.node_id == node_id

    def node_to_matches_id(self, node_id):
        return self.node_to.node_id == node_id

    def arg_from_matches(self, name):
        return self.arg_from == name

    def arg_to_matches(self, name):
        return self.arg_to == name

    def is_connected_to(self, node_id, name):
        from_matches = self.node_from_matches_id(node_id) and self.arg_from_matches(name)
        to_matches = self.node_to_matches_id(node_id) and self.arg_to_matches(name)
        return from_matches or to_matches

    def matches(self, node_from_id, arg_from, node_to_id, arg_to):
        nodes_match = self.node_from_matches_id(node_from_id) and self.node_to_matches_id(node_to_id)
        vars_match = self.arg_from_matches(arg_from) and self.arg_to_matches(arg_to)
        print(nodes_match, vars_match)
        return nodes_match and vars_match

    def as_json(self):
        return {
            "node_id_from" : self.node_from.node_id,
            "arg_from" : self.arg_from,
            "node_id_to" : self.node_to.node_id,
            "arg_to" : self.arg_to
        }

