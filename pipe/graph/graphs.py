
from pipe.graph import nodes
from pipe.graph import edges
from pipe.graph import library


class BasicGraph:

    def __init__(self, lib=None):
        if lib is None:
            self.lib = library.load_interal()
        else:
            self.lib = lib
        self.nodes = {}
        self.edges = []

    def add_node(self, node):
        self.nodes[node.node_id] = node
        return node

    def new_node(self, path, x=0, y=0):
        node = nodes.BasicNode(self.lib, path, x=x, y=y)
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

    def execute(self, current_node):
        # Evaluate toward root first
        for edge in self.edges:
            if edge.node_to == current_node:
                if not edge.node_from.has_output(edge.arg_from):
                    self.execute(edge.node_from)

        # Propagate values in the root-leaf direction
        for edge in self.edges:
            if edge.node_to == current_node:
                value = edge.node_from.read_output(edge.arg_from)
                current_node.set_argument(edge.arg_to, value)

        # Then evaluate current
        current_node.evaluate()

    def execute_by_id(self, id):
        self.execute(self.get_node(id))

    def as_json(self):
        return {
            "library": self.lib.as_json(),
            "nodes": [n.as_json() for n in self.nodes.values()],
            "edges": [e.as_json() for e in self.edges]
        }


def from_json(data):
    lib = library.from_json(data["library"])
    graph = BasicGraph(lib=lib)

    for datum in data["nodes"]: 
        node = nodes.from_json(lib, datum)
        graph.add_node(node)

    for datum in data["edges"]:
        graph.connect_by_id(
            datum["node_id_from"],
            datum["arg_from"],
            datum["node_id_to"],
            datum["arg_to"]
        )

    return graph
