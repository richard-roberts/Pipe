import os
import json

from assembly import assemblers
from . import templates
import globals


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

    def create_new_template(self, clazz, name, inputs, outputs):
        template = clazz()
        template.setup(self.name, name, inputs, outputs)
        self.templates[template.name] = template
        return template

    def delete_template(self, template):
        if template.name not in self.templates.keys():
            raise IndexError("No template named %s in %s collection" % (template.name, self.name))
        del self.templates[template.name]
        if len(self.templates) == 0:
            globals.TemplateInfo().manager.delete_collection(self)

    def delete_template_by_name(self, name):
        self.delete_template(self.get_template(name))

    def rename_template_by_name(self, old_name, new_name):
        self.templates[new_name] = self.templates.pop(old_name)
        self.templates[new_name].name = new_name

    def is_empty(self):
        return len(self.templates)

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

    def assemble_to_filepath(self, filepath):
        with open(filepath, 'w') as stream:
            stream.write(assemblers.Assembler.assemble_collection(self))

    def assemble_to_directory(self, directory):
        filepath = os.path.join(directory, self.name + ".py")
        self.assemble_to_filepath(filepath)
