import os
from difflib import SequenceMatcher

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
        self.import_collections("./pipe/templates/standard_collections")

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
        if GRAPH_EXE_COLLECTION_NAME not in self.collections.keys():
            self.collections[GRAPH_EXE_COLLECTION_NAME] = template_collection.TemplateCollection(GRAPH_EXE_COLLECTION_NAME)

        graph_collection = self.collections[GRAPH_EXE_COLLECTION_NAME]
        old_template = None

        if graph_collection.template_exists(graph.name):
            old_template = graph_collection.get_template(graph.name)
            graph_collection.delete_template_by_name(graph.name)

        new_template = graph_collection.create_new_template(
            templates.GraphTemplate,
            graph.name,
            graph.list_inputs_needing_value(),
            graph.disconnected_outputs()
        )

        if old_template is not None:
            globals.GraphInfo().manager.replace_template_a_with_b(old_template, new_template)

        return new_template

    def template_is_graph_execution(self, template):
        # This can be called before any graph executors are created
        if GRAPH_EXE_COLLECTION_NAME not in self.collections.keys():
            return False
        return self.collections[GRAPH_EXE_COLLECTION_NAME].template_exists(template.name)

    def is_graph_execution_name(self, name):
        return name == GRAPH_EXE_COLLECTION_NAME

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

    def get_most_similar_and_map_of_similar_template(self, name):
        similar_templates = {}
        most_similar_name = ""
        most_similar_value = 0.0
        for collection in self.collections.values():
            for template_name in collection.get_names():
                similarity = SequenceMatcher(None, template_name, name).ratio()
                if similarity > 0.3:
                    if similarity > most_similar_value:
                        most_similar_value = similarity
                        most_similar_name = "%s::%s" % (collection.name, template_name)
                    if collection.name not in similar_templates.keys():
                        similar_templates[collection.name] = [template_name]
                    else:
                        similar_templates[collection.name].append(template_name)
        return most_similar_name, similar_templates

    def graph_template_already_exists(self, template_name):
        return self.collections[GRAPH_EXE_COLLECTION_NAME].template_exists(template_name)

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
        return self.collections[collection_name].get_template(template_name)

    def rename_graph_execution(self, old_name, new_name):
        self.collections[GRAPH_EXE_COLLECTION_NAME].rename_template_by_name(old_name, new_name)

    def remove_graph_execution(self, name):
        self.collections[GRAPH_EXE_COLLECTION_NAME].delete_template_by_name(name)

