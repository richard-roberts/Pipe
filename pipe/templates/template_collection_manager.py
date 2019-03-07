import os

import globals
from . import template_collection


class TemplateCollectionManager:

    def __init__(self):
        self.collections = {}
        globals.TemplateInfo().set_manager(self)

    def clear(self):
        self.collections = {}

    def new_template(self, collection_name, name, inputs, outputs):
        if collection_name not in self.collections.keys():
            collection = template_collection.TemplateCollection(collection_name)
            self.collections[collection.name] = collection
        collection = self.collections[collection_name]
        collection.create_new_template(name, inputs, outputs)

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

    def get_names(self):
        all_names = []
        for collection in self.collections.values():
            all_names += [("%s::%s" % (collection.name, template_name)) for template_name in collection.get_names()]
        return all_names

    def get_template(self, collection_name, template_name):
        has_collection = collection_name in self.collections.keys()
        if not has_collection:
            return None

        collection = self.collections[collection_name]
        return collection.get_template(template_name)
