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
            if node is not None: # can be none if failed to find template
                self.nodes[node.get_id()] = node

        self.edges = {}
        for datum in data["edges"]:
            edge = edges.Edge.from_json(self, datum)
            if edge is not None: # can be none if failed to find nodes by id
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
        if globals.TemplateInfo().manager.template_is_graph_execution(template):
            node = nodes.GraphNode(template, position)
        else:
            node = nodes.Node(template, position)
        self.nodes[node.get_id()] = node
        globals.TemplateInfo().manager.create_or_update_graph_template(self)
        return node

    def create_edge(self, argument_from, argument_to):
        edge = edges.Edge(argument_from, argument_to)
        self.edges[edge] = edge
        globals.TemplateInfo().manager.create_or_update_graph_template(self)
        return edge

    def delete_edge(self, edge):
        edge.disconnect()
        del self.edges[edge]
        globals.TemplateInfo().manager.create_or_update_graph_template(self)

    def delete_edges_connected_to_node(self, node):
        edges_copy = [e for e in self.edges.values()]
        for edge in edges_copy:
            if edge.is_connected_to_node(node):
                self.delete_edge(edge)
        globals.TemplateInfo().manager.create_or_update_graph_template(self)

    def delete_node(self, node):
        del self.nodes[node.get_id()]
        self.delete_edges_connected_to_node(node)
        globals.TemplateInfo().manager.create_or_update_graph_template(self)

    def get_node_by_id(self, node_id):
        return self.nodes[node_id]

    def replace_template_a_with_b(self, a, b):
        for node in self.nodes.values():
            if node.template == a:
                for arg in node.inputs.values():
                    if arg.name not in b.inputs and arg.get_connected() is not None:
                        self.delete_edge(arg.get_connected())
                for arg in node.outputs.values():
                    if arg.name not in b.outputs and arg.get_connected() is not None:
                        self.delete_edge(arg.get_connected())
                node.replace_template(b)
                globals.TemplateInfo().manager.create_or_update_graph_template(self)

    def delete_nodes_using_template(self, template):
        nodes_copy = [v for v in self.nodes.values()]
        for node in nodes_copy:
            if node.template == template:
                self.delete_node(node)
        globals.TemplateInfo().manager.create_or_update_graph_template(self)

    def list_inputs_needing_value(self):
        ins = []
        for node in self.nodes.values():
            ins += node.list_inputs_needing_value()
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
                count += 1
        return count

    def number_of_nodes(self):
        return len(self.nodes)

    def number_of_edges(self):
        return len(self.edges)

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
