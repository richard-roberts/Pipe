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
        return graph

    def import_graph(self, filepath):
        graph = graphs.Graph()
        graph.import_from_filepath(filepath)
        self.graphs[graph.name] = graph
        return graph

    def import_graphs(self, directory):
        filepaths = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                filepaths.append(filepath)

        for filepath in filepaths:
            self.import_graph(filepath)

    def export_graphs(self, directory):
        for graph in self.graphs.values():
            graph.export_to_directory(directory)

    def get_names(self):
        return [graph.name for graph in self.graphs.values()]

    def already_exists(self, name):
        return name in self.get_names()

    def get_by_name(self, name):
        return self.graphs[name]
