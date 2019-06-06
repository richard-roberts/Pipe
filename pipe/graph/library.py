import os
import json

from pipe.graph import templates


class Library:

    internal_filepath = os.path.abspath(__file__)[:-2] + "json"

    def __init__(self):
        self.templates = {}

    def is_valid_path(self, path):
        return path in self.templates.keys()

    def add(self, path, template):
        if self.is_valid_path(path):
            raise ValueError(
                f"There is already a template saved under `{path}` (use `replace` instead)"
            )
        self.templates[path] = template

    def new_basic_template(self, path, args, outs, extension, code):
        template = templates.from_data(args, outs, extension, code)
        self.add(path, template)
        return template

    def new_file_template(self, path, filepath):
        template = templates.FileTemplate(filepath)
        self.add(path, template)
        return template
    
    def replace(self, path, template):
        if not self.is_valid_path(path):
            raise ValueError(
                f"There is no template saved under `{path}` (use `add` instead)"
            )
        self.templates[path] = template

    def remove(self, path):
        if not self.is_valid_path(path):
            raise ValueError(f"There is no template saved under `{path}`")
        del self.templates[path]

    def move(self, old_path, new_path):
        if not self.is_valid_path(old_path):
            raise ValueError(
                f"There is no template saved under `{old_path}`"
            )
        if self.is_valid_path(new_path):
            raise ValueError(
                f"There is already a template saved under `{new_path}`"
            )
        self.add(new_path, self.get(old_path))
        self.remove(old_path)

    def get(self, path):
        return self.templates[path]

    def list_templates(self):
        return list(self.templates.keys())

    def as_json(self):
        data = {}
        for key in self.templates.keys():
            data[key] = self.templates[key].as_json()
        return data

    def update_interal(self, pretty=True):
        if pretty:
            content = json.dumps(
                self.as_json(),
                sort_keys=True, indent=4, separators=(',', ': ')
            )
        else:
            content = json.dumps(self.as_json())

        f = open(Library.internal_filepath, "w")
        f.write(content)
        f.close()


def from_json(data):
    l = Library()
    for path in data.keys():
        template_json = data[path]
        template = templates.from_json(template_json)
        l.add(path, template)
    return l

def load_interal():
    f = open(Library.internal_filepath, "r")
    data = json.loads(f.read())
    f.close()
    return from_json(data)
