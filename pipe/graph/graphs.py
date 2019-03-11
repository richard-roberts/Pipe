import os
import json

from assembly import assemblers
from . import nodes
from . import edges


class Graph:

    def __init__(self):
        self.name = ""
        self.nodes = {}
        self.edges = {}

    def from_json(self, data):
        self.name = data["name"]
        self.nodes = {}
        for datum in data["nodes"]:
            node = nodes.Node.from_json(datum)
            self.nodes[node.get_id()] = node
        self.edges = {}
        for datum in data["edges"]:
            edge = edges.Edge.from_json(self, datum)
            self.edges[edge] = edge

    def import_from_filepath(self, filepath):
        with open(filepath) as stream:
            string = stream.read()
            data = json.loads(string)
            self.from_json(data)

    def export_to_filepath(self, filepath):
        filepath = os.path.join(filepath)
        with open(filepath, 'w') as stream:
            string = json.dumps(
                self.as_json(),
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
            stream.write(string)

    def export_to_directory(self, directory):
        filepath = os.path.join(directory, self.name + ".json")
        self.export_to_filepath(filepath)

    def assemble_to_filepath(self, filepath):
        with open(filepath, 'w') as stream:
            stream.write(assemblers.Assembler.assemble_graph(self))

    def assemble_to_directory(self, directory):
        filepath = os.path.join(directory, self.name + ".py")
        self.assemble_to_filepath(filepath)

    def create_node(self, template, position):
        node = nodes.Node(template, position)
        self.nodes[node.get_id()] = node
        return node

    def create_edge(self, argument_from, argument_to):
        edge = edges.Edge(argument_from, argument_to)
        self.edges[edge] = edge
        return edge

    def delete_node(self, node):
        del self.nodes[node.get_id()]

    def delete_edge(self, edge):
        edge.disconnect()
        del self.edges[edge]

    def get_node_by_id(self, node_id):
        return self.nodes[node_id]

    def get_edge_by_argument_from(self, node, argument):
        for edge in self.edges.values():
            if edge.argument_from == argument and edge.argument_from.get_node() == node:
                return edge

    def get_edge_by_argument_to(self, node, argument):
        for edge in self.edges.values():
            if edge.argument_to == argument and edge.argument_to.get_node() == node:
                return edge

    def as_json(self):
        node_data = []
        for node in self.nodes.values():
            node_data.append(node.as_json())

        edge_data = []
        for edge in self.edges.values():
            edge_data.append(edge.as_json())

        return {
            "name": self.name,
            "nodes": node_data,
            "edges": edge_data
        }
