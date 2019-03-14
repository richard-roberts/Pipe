import os
import shutil
import pathlib
import subprocess

from graph import graph_manager
from templates import template_collection_manager


class PipeBackend:

    def __init__(self):
        self.graphs = graph_manager.GraphManager()
        self.templates = template_collection_manager.TemplateCollectionManager()

    def clear(self):
        self.graphs.clear()
        self.templates.clear()

    def open_project(self, project_directory):
        templates_directory = os.path.join(project_directory, "templates")
        graphs_directory = os.path.join(project_directory, "graphs")
        self.clear()
        self.templates.import_collections(templates_directory)
        self.graphs.import_graphs(graphs_directory)

    def save_project(self, project_directory):
        shutil.rmtree(project_directory)
        templates_directory = os.path.join(project_directory, "templates")
        graphs_directory = os.path.join(project_directory, "graphs")
        if not os.path.exists(templates_directory):
            os.makedirs(templates_directory)
        if not os.path.exists(graphs_directory):
            os.makedirs(graphs_directory)
        self.templates.export_collections(templates_directory)
        self.graphs.export_graphs(graphs_directory)

    def assemble_project(self, project_directory):
        templates_directory = os.path.join(project_directory, "templates")
        graphs_directory = project_directory
        if not os.path.exists(templates_directory):
            os.makedirs(templates_directory)
            pathlib.Path(os.path.join(templates_directory, "__init__.py")).touch()
        if not os.path.exists(graphs_directory):
            os.makedirs(graphs_directory)
        self.templates.assemble_collections(templates_directory)
        self.graphs.assemble_graphs(graphs_directory)

    def list_graphs(self):
        return self.graphs.graphs.values()

    def execute(self, graph, command_line_args_str):
        temporary = "./tmp"
        self.templates.create_or_update_graph_template(graph)
        self.assemble_project(temporary)
        command = 'python ./tmp/%s.py %s' % (graph.name, command_line_args_str)

        try:
            result = subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            shutil.rmtree(temporary)
            raise ValueError(str(e))

        shutil.rmtree(temporary)
        return result.decode("utf-8") if result else False
