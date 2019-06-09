
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

    def set_node_position(self, id, x, y):
        node = self.get_node(id)
        node.x = x
        node.y = y

    def connect(self, node_from, arg_from, node_to, arg_to):
        edge = edges.BasicDirectedEdge(
            node_from, arg_from,
            node_to, arg_to
        )
        self.edges.append(edge)
        return edge

    def connect_by_id(self, id_from, arg_from, id_to, arg_to):
        return self.connect(self.get_node(id_from), arg_from, self.get_node(id_to), arg_to)

    def assign_argument(self, id, name, value):
        self.get_node(id).set_argument(name, value)

    def delete_edge(self, edge):
        self.edges.remove(edge)

    def delete_edges(self, edges):
        for edge in edges:
            self.delete_edge(edge)

    def delete_edge_by_match(self, id_from, arg_from, id_to, arg_to):
        edges_to_remove = []
        for edge in self.edges:
            if edge.matches(id_from, arg_from, id_to, arg_to):
                edges_to_remove.append(edge)

        self.delete_edges(edges_to_remove)
        
    def delete_node(self, id):
        node = self.nodes[id]
        del self.nodes[id]

        edges_to_remove = []
        for edge in self.edges:
            for arg in node.template.list_arguments():
                if edge.is_connected_to(id, arg):
                    edges_to_remove.append(edge)
            for out in node.template.list_outputs():
                if edge.is_connected_to(id, out):
                    edges_to_remove.append(edge)

        self.delete_edges(edges_to_remove)

    def replace_template(self, old_template, new_template):
        edges_to_remove = []

        for node in self.nodes.values():
            if node.template == old_template:
                node.replace_template(new_template)

                for edge in self.edges:
                    
                    for arg in old_template.list_arguments():
                        if arg not in new_template.list_arguments():
                            if edge.is_connected_to(node.node_id, arg):
                                edges_to_remove.append(edge)                

                    for out in node.template.list_outputs():
                        if out not in new_template.list_outputs():
                            if edge.is_connected_to(node.node_id, out):
                                edges_to_remove.append(edge)

        edges_to_remove = list(set(edges_to_remove))
        self.delete_edges(edges_to_remove)

    def rename_template(self, old_path, new_path):
        for node in self.nodes.values():
            if node.path == old_path:
                node.path = new_path

    def remove_template(self, template):
        nodes_to_remove = []
        for node in self.nodes.values():
            if node.template == template:
                nodes_to_remove.append(node)
        for node in nodes_to_remove:
            self.delete_node(node.node_id)

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
        return current_node

    def execute_by_id(self, id):
        return self.execute(self.get_node(id))

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
