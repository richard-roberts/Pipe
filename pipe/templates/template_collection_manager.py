import os

import globals
from . import templates
from . import template_collection


GRAPH_EXE_COLLECTION_NAME = "GraphExecution"


class TemplateCollectionManager:

    def __init__(self):
        self.collections = {}
        self.clear()
        globals.TemplateInfo().set_manager(self)

    def clear(self):
        self.collections = {
            GRAPH_EXE_COLLECTION_NAME: template_collection.TemplateCollection(GRAPH_EXE_COLLECTION_NAME)
        }

    def new_template(self, collection_name, name, inputs, outputs):
        if collection_name not in self.collections.keys():
            collection = template_collection.TemplateCollection(collection_name)
            self.collections[collection.name] = collection
        collection = self.collections[collection_name]
        return collection.create_new_template(
            templates.Template,
            name,
            inputs,
            outputs
        )

    def create_or_update_graph_template(self, graph):
        graph_collection = self.collections[GRAPH_EXE_COLLECTION_NAME]

        if graph_collection.template_exists(graph.name):
            graph_collection.delete_template_by_name(graph.name)

        new_template = graph_collection.create_new_template(
            templates.GraphTemplate,
            graph.name,
            [i.pretty().replace(".", "_") for i in graph.disconnected_inputs()],
            [o.pretty().replace(".", "_") for o in graph.disconnected_outputs()]
        )

        return new_template

    def delete_template(self, template):
        if template.collection_name not in self.collections.keys():
            raise IndexError("No %s collection was found" % template.collection_name)
        collection = self.collections[template.collection_name]
        collection.delete_template(template)
        if collection.is_empty():
            del self.collections[collection.name]

    def delete_template_by_name(self, collection_name, template_name):
        self.delete_template(self.get_template(collection_name, template_name))

    def delete_collection(self, collection):
        del self.collections[collection.name]

    def already_exists(self, collection_name, template_name):
        has_collection = collection_name in self.collections.keys()
        if not has_collection:
            return False

        collection = self.collections[collection_name]
        return collection.template_exists(template_name)

    def import_collection(self, filepath):
        name = os.path.splitext(os.path.basename(filepath))[0]
        collection = template_collection.TemplateCollection(name)
        collection.import_from_filepath(filepath)
        self.collections[collection.name] = collection
        return collection

    def import_collections(self, directory):
        filepaths = []
        for filename in [f for f in os.listdir(directory) if f.endswith(".json")]:
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                filepaths.append(filepath)

        for filepath in filepaths:
            self.import_collection(filepath)

    def export_collections(self, directory):
        for collection in self.collections.values():
            collection.export_to_directory(directory)

    def assemble_collections(self, directory):
        for collection in self.collections.values():
            collection.assemble_to_directory(directory)

    def get_collection_names(self):
        return [collection.name for collection in self.collections.values()]

    def get_dictionary(self):
        collections_dict = {}
        for key in self.collections.keys():
            collections_dict[key] = []

        for key in self.collections.keys():
            for name in self.collections[key].get_names():
                collections_dict[key].append(name)

        return collections_dict

    def get_template(self, collection_name, template_name):
        has_collection = collection_name in self.collections.keys()
        if not has_collection:
            return None

        collection = self.collections[collection_name]
        return collection.get_template(template_name)
