import os
import json

from assembly import assemblers
from . import nodes
from . import edges
import globals


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

    def delete_edge(self, edge):
        edge.disconnect()
        del self.edges[edge]

    def delete_node(self, node):
        del self.nodes[node.get_id()]
        edges_copy = [e for e in self.edges.values()]
        for edge in edges_copy:
            if edge.is_connected_to_node(node):
                self.delete_edge(edge)

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

    def replace_template_a_with_b(self, a, b):
        for node in self.nodes.values():
            if node.template == a:
                node.replace_template(b)

    def delete_nodes_using_template(self, template):
        nodes_copy = [v for v in self.nodes.values()]
        any_nodes_deleted = False
        for node in nodes_copy:
            if node.template == template:
                self.delete_node(node)
                any_nodes_deleted = True

        if any_nodes_deleted:
            globals.TemplateInfo().manager.create_or_update_graph_template(self)

    def disconnected_inputs(self):
        ins = []
        for node in self.nodes.values():
            ins += node.list_disconnected_inputs()
        return ins

    def disconnected_outputs(self):
        ins = []
        for node in self.nodes.values():
            ins += node.list_disconnected_outputs()
        return ins

    def count_uses_of_template(self, template):
        count = 0
        for node in self.nodes.values():
            if node.template == template:
                print("Graph %s is using %s" % (self.name, template.name))
                count += 1
        return count

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
