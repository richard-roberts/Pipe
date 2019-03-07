import os
import json

from . import templates


class TemplateCollection:

    def __init__(self, name):
        self.name = name
        self.templates = {}

    def as_json(self):
        data = {}
        for template in self.templates.values():
            data[template.name] = template.as_json()

        return {
            "name": self.name,
            "templates": data
        }

    def get_names(self):
        return [template.name for template in self.templates.values()]

    def template_exists(self, name):
        return name in self.get_names()

    def get_template(self, name):
        return self.templates[name]

    def create_new_template(self, name, inputs, outputs):
        template = templates.Template()
        template.setup(self.name, name, inputs, outputs)
        self.templates[template.name] = template
        return template

    def from_json(self, data):
        self.name = data["name"]
        self.templates = {}
        for datum in data["templates"].values():
            template = templates.Template()
            template.from_json(datum)
            self.templates[template.name] = template

    def import_from_filepath(self, filepath):
        with open(filepath) as stream:
            string = stream.read()
            data = json.loads(string)
            self.from_json(data)

    def export_to_filepath(self, filepath):
        filepath = os.path.join(filepath)
        with open(filepath, 'w') as stream:
            string = json.dumps(self.as_json(), sort_keys=True, indent=4, separators=(',', ': '))
            stream.write(string)

    def export_to_directory(self, directory):
        filepath = os.path.join(directory, "%s.json" % self.name)
        self.export_to_filepath(filepath)
