import os
import json

from pipe.graph import templates


class Library:
    """
    The standard templates are organized in tree-like directory. This
    class loads them from the directory in a way that preserves their hierarchy.
    Each directory represents a "collection" of templates. Each collection contains
    one or more "template sets". Finally, each template set can contain one or more
    template. This hierarchy enables a tree-like presentation for the templates.
    """

    class TemplateSet:

        def __init__(self, name):
            self.name = name
            self.templates = {}

        def __str__(self):
            return "%s [Set]" % self.name

        def pretty(self):
            return "\n\t\t%s\n%s" % (str(self), "\n".join("\t\t\t%s" % str(c) for c in self.templates.values()))

        def add(self, template):
            self.templates[template.name] = template

        def get(self, name):
            return self.templates[name]

    class TemplateCollection:

        def __init__(self, name):
            self.name = name
            self.sets = {}

        def __str__(self):
            return "%s [Collection]" % self.name

        def pretty(self):
            return "\n\t%s\n%s\n" % (str(self), "\n".join(c.pretty() for c in self.sets.values()))

        def add(self, set, template):
            if set not in self.sets.keys():
                self.sets[set] = Library.TemplateSet(set)
            self.sets[set].add(template)

        def get(self, set, name):
            return self.sets[set].get(name)

    def __init__(self):
        self.collections = {}
        self.load_standard_templates()

    def pretty(self):
        return "Library\n%s" % "\n".join(c.pretty() for c in self.collections.values())

    def add(self, collection, template_set, template):
        if collection not in self.collections.keys():
            self.collections[collection] = Library.TemplateCollection(collection)
        self.collections[collection].add(template_set, template)

    def get(self, collection, template_set, name):
        return self.collections[collection].get(template_set, name)

    def load_standard_templates(self):
        template_directory = os.path.join(os.path.dirname(__file__), "..", "templates")

        # Iterate each collection
        for collection_name in os.listdir(template_directory):
            collection_directory = os.path.join(template_directory, collection_name)

            # Iterate each set in directory
            for template_set_filename in os.listdir(collection_directory):
                template_set_path = os.path.join(collection_directory, template_set_filename)
                template_set_name = os.path.splitext(template_set_filename)[0]

                # Open the file
                f = open(template_set_path, "r")
                data = json.loads(f.read())
                f.close()

                # Iterate and create each template in the set
                for datum in data:
                    template = templates.from_json(datum)
                    self.add(
                        collection_name,
                        template_set_name,
                        template
                    )
