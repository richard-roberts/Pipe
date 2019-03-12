import globals
from . import arguments


class Node:

    def __init__(self, template, position, node_id=None):
        self.node_id = id(self) if node_id is None else node_id
        self.template = template
        self.position = position
        self.inputs = {}
        self.outputs = {}
        self.update_args_from_template()

    def update_args_from_template(self):
        self.inputs = {}
        self.outputs = {}
        for name in self.template.inputs:
            arg = arguments.Argument(self, name)
            self.inputs[arg.name] = arg
        for name in self.template.outputs:
            arg = arguments.Argument(self, name)
            self.outputs[arg.name] = arg

    def get_id(self):
        return self.node_id

    def replace_template(self, new_template):
        self.template = new_template
        self.update_args_from_template()

    def get_input_argument_by_name(self, name):
        return self.inputs[name]

    def get_output_argument_by_name(self, name):
        return self.outputs[name]

    def list_disconnected_inputs(self):
        disconnected = []
        for input_ in self.inputs.values():
            if not input_.is_connected():
                disconnected.append(input_)
        return disconnected

    def list_disconnected_outputs(self):
        disconnected = []
        for output in self.outputs.values():
            if not output.is_connected():
                disconnected.append(output)
        return disconnected

    def has_outputs(self):
        return self.count_number_of_disconnected_outputs() > 0

    def count_number_of_disconnected_inputs(self):
        n = 0
        for input_ in self.inputs.values():
            if not input_.is_connected():
                n += 1
        return n

    def count_number_of_disconnected_outputs(self):
        n = 0
        for output in self.outputs.values():
            if not output.is_connected():
                n += 1
        return n

    def count_number_of_connected_outputs(self):
        n = 0
        for output in self.outputs.values():
            if output.is_connected():
                n += 1
        return n

    def terminates_execution(self):
        return self.count_number_of_connected_outputs() == 0

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
