import os
import json

from pipe.graph import templates


class Library:

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

    def new(self, path, args, outs, extension, code):
        template = templates.from_data(args, outs, extension, code)
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

