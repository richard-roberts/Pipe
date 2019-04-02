import os

import globals
from . import graphs


class GraphManager:

    def __init__(self):
        self.graphs = {}
        globals.GraphInfo().set_manager(self)

    def clear(self):
        self.graphs = {}

    def new_graph(self, name):
        graph = graphs.Graph()
        graph.name = name
        self.graphs[graph.name] = graph
        globals.TemplateInfo().manager.create_or_update_graph_template(graph)
        return graph

    def import_graph(self, filepath):
        graph = graphs.Graph()
        graph.import_from_filepath(filepath)
        self.graphs[graph.name] = graph
        globals.TemplateInfo().manager.create_or_update_graph_template(graph)
        return graph

    def import_graphs(self, directory):
        filepaths = []
        for filename in [f for f in os.listdir(directory) if f.endswith(".json")]:
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                filepaths.append(filepath)

        for filepath in filepaths:
            self.import_graph(filepath)

    def export_graphs(self, directory):
        for graph in self.graphs.values():
            graph.export_to_directory(directory)

    def assemble_graphs(self, directory):
        for graph in self.graphs.values():
            graph.assemble_to_directory(directory)

    def rename_graph(self, old_name, new_name):
        self.graphs[new_name] = self.graphs.pop(old_name)
        self.graphs[new_name].name = new_name
        globals.TemplateInfo().manager.rename_graph_execution(old_name, new_name)

    def delete_graph(self, name):
        del self.graphs[name]
        globals.TemplateInfo().manager.remove_graph_execution(name)

    def get_names(self):
        return [graph.name for graph in self.graphs.values()]

    def already_exists(self, name):
        return name in self.get_names()

    def get_by_name(self, name):
        return self.graphs[name]

    def replace_template_a_with_b(self, a, b):
        found = False
        for graph in self.graphs.values():
            found_in_graph = graph.replace_template_a_with_b(a, b)
            if found_in_graph:
                found = True
        return found

    def delete_any_nodes_using_template(self, template):
        for graph in self.graphs.values():
            graph.delete_nodes_using_template(template)

    def assemble_templates_for_graph(self, graph_name):
        self.graphs[graph_name].assemble_template()

    def count_uses_of_template(self, template):
        count = 0
        for graph in self.graphs.values():
            n = graph.count_uses_of_template(template)
            count += n
        return count
