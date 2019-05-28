
from pipe.graph import nodes
from pipe.graph import edges
from pipe.graph import library


class BasicGraph:

    def __init__(self):
        self.lib = library.Library()
        self.nodes = {}
        self.edges = []

    def add_node(self, node):
        self.nodes[node.node_id] = node
        return node

    def new_node(self, path):
        node = nodes.BasicNode(self.lib, path)
        self.nodes[id(node)] = node
        return node

    def list_nodes(self):
        return [n.as_json() for n in self.nodes.values()]
    
    def list_edges(self):
        return [e.as_json() for e in self.edges]

    def get_node(self, id):
        if id not in self.nodes.keys():
            raise KeyError("No known node with id=%s" % str(id))
        return self.nodes[id]

    def connect(self, node_from, arg_from, node_to, arg_to):
        edge = edges.BasicDirectedEdge(
            node_from, arg_from,
            node_to, arg_to
        )
        self.edges.append(edge)

    def connect_by_id(self, id_from, arg_from, id_to, arg_to):
        self.connect(self.get_node(id_from), arg_from, self.get_node(id_to), arg_to)

    def assign_argument(self, id, name, value):
        self.get_node(id).set_argument(name, value)

    def execute_to_root(self, current_node):
        # Evaluate toward root first
        for edge in self.edges:
            if edge.node_to == current_node:
                if not edge.node_from.has_output(edge.arg_from):
                    self.execute_to_root(edge.node_from)

        # Propagate values in the root-leaf direction
        for edge in self.edges:
            if edge.node_to == current_node:
                value = edge.node_from.read_output(edge.arg_from)
                current_node.set_argument(edge.arg_to, value)

        # Then evaluate current
        current_node.evaluate()
