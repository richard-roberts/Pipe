
from pipe.graph import edges


class BasicGraph:

    def __init__(self):
        self.edges = []

    def connect(self, node_from, arg_from, node_to, arg_to):
        edge = edges.BasicDirectedEdge(
            node_from, arg_from,
            node_to, arg_to
        )
        self.edges.append(edge)

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

