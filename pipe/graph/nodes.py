import config
import globals
from . import arguments


class Node(object):

    def __init__(self, template, position, node_id=None, setup_args=True):
        self.node_id = id(self) if node_id is None else node_id
        self.template = template
        self.position = position
        self.inputs = {}
        self.outputs = {}
        if setup_args:
            self.update_args_from_template()

    def __str__(self):
        return "%s[%s]" % (self.template.name, str(self.node_id))

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

    def is_graph_execution_node(self):
        return globals.TemplateInfo().manager.template_is_graph_execution(self.template)

    def replace_template(self, new_template):
        old_template = self.template
        for name in old_template.inputs:
            if name not in new_template.inputs:
                del self.inputs[name]
        for name in old_template.outputs:
            if name not in new_template.outputs:
                del self.outputs[name]

        for name in new_template.inputs:
            if name not in self.inputs.keys():
                arg = arguments.Argument(self, name)
                self.inputs[arg.name] = arg
        for name in new_template.outputs:
            if name not in self.outputs.keys():
                arg = arguments.Argument(self, name)
                self.outputs[arg.name] = arg

        self.template = new_template

    def get_input_argument_by_name(self, name):
        return self.inputs[name]

    def get_output_argument_by_name(self, name):
        print(self, name)
        return self.outputs[name]

    def list_inputs_needing_value(self):
        inputs = []
        for input_ in self.inputs.values():
            if input_.needs_input():
                inputs.append(input_)
        return inputs

    def list_disconnected_outputs(self):
        disconnected = []
        for output in self.outputs.values():
            if not output.is_connected():
                disconnected.append(output)
        return disconnected

    def has_outputs(self):
        return self.count_number_of_disconnected_outputs() > 0

    def count_number_of_inputs_needing_value(self):
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
            "inputs": [arg.as_json() for arg in self.inputs.values()],
            "outputs": [arg.as_json() for arg in self.outputs.values()]
        }

    @staticmethod
    def from_json(data):
        collection_name, template_name = data["template"].split("::")
        try:
            template = globals.TemplateInfo().manager.get_template(collection_name, template_name)
        except KeyError:
            return None

        node = Node(
            template,
            data["position"],
            node_id=data["node_id"],
            setup_args=False
        )
        for arg_data in data["inputs"]:
            arg = arguments.Argument.from_json(node, arg_data)
            node.inputs[arg.name] = arg
        for arg_data in data["outputs"]:
            arg = arguments.Argument.from_json(node, arg_data)
            node.outputs[arg.name] = arg
        return node


class GraphNode(Node):

    def __init__(self, template, position):
        super(GraphNode, self).__init__(template, position, node_id="GraphExecution%s" % template.name)
