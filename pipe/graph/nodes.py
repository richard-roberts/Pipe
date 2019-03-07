import itertools

import globals
from . import arguments


class Node:
    node_ids = itertools.count(0)

    def __init__(self, template, position, node_id=None):
        self.node_id = next(self.node_ids) if node_id is None else node_id
        self.template = template
        self.position = position

        self.inputs = {}
        for name in self.template.inputs:
            arg = arguments.Argument(self, name)
            self.inputs[arg.name] = arg

        self.outputs = {}
        for name in self.template.outputs:
            arg = arguments.Argument(self, name)
            self.outputs[arg.name] = arg

    def get_id(self):
        return self.node_id

    def get_input_argument_by_name(self, name):
        return self.inputs[name]

    def get_output_argument_by_name(self, name):
        return self.outputs[name]

    def as_json(self):
        return {
            "node_id": self.node_id,
            "template": self.template.get_long_name(),
            "position": self.position,
        }

    @staticmethod
    def from_json(data):
        collection_name, template_name = data["template"].split("::")
        template = globals.TemplateInfo().manager.get_template(collection_name, template_name)
        return Node(
            template,
            data["position"],
            node_id=data["node_id"]
        )
