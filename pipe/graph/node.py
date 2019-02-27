from kivy.factory import Factory
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, ObjectProperty

from . import config

Config = config.Config


class InputArgument(ToggleButton):
    
    def __init__(self, **kwargs):
        super(InputArgument, self).__init__(**kwargs)
        
    def setup(self, node, index):
        self.name = node.name + "_" + str(index)
        self.text = str(index)
        self.bind(state=self.parent.parent.parent.parent.handle_argument_touched)

    def get_node_name(self):
        return self.name.split("_")[0]

    def get_argument_index(self):
        return int(self.name.split("_")[1])


class OutputArgument(ToggleButton):
    
    def __init__(self, **kwargs):
        super(OutputArgument, self).__init__(**kwargs)
        
    def setup(self, node, index):
        self.name = node.name + "_" + str(index)
        self.text = str(index)
        self.bind(state=self.parent.parent.parent.parent.handle_argument_touched)

    def get_node_name(self):
        return self.name.split("_")[0]

    def get_argument_index(self):
        return int(self.name.split("_")[1])
    

class InputArgumentSet(BoxLayout):
    n = NumericProperty()

    def __init__(self, **kwargs):
        super(InputArgumentSet, self).__init__(**kwargs)
        self.args = []

    def setup(self, node):
        for i in range(self.n):
            arg = InputArgument()
            self.add_widget(arg)
            arg.setup(node, i)
            self.args.append(arg)

    def get_arg(self, index):
        return self.args[index]

    def reset_state(self):
        for arg in self.args:
            arg.state = "normal"


class OutputArgumentSet(BoxLayout):
    n = NumericProperty()

    def __init__(self, **kwargs):
        super(OutputArgumentSet, self).__init__(**kwargs)
        self.args = []

    def setup(self, node):
        for i in range(self.n):
            arg = OutputArgument()
            self.add_widget(arg)
            arg.setup(node, i)
            self.args.append(arg)

    def get_arg(self, index):
        return self.args[index]

    def reset_state(self):
        for arg in self.args:
            arg.state = "normal"

class Node(BoxLayout):
    input_set = ObjectProperty()
    output_set = ObjectProperty()
    name = StringProperty()
    documentation = StringProperty()
    code = StringProperty()

    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)

    def setup(self, name, n_inputs, n_outputs, position):
        self.name = name
        self.function_name = name.replace(" ", "_")
        self.code = Config.Defaults.Node.code(self.function_name, n_inputs, n_outputs)
        self.documentation = Config.Defaults.Node.documentation(name)
        self.position = position

        self.input_set.n = n_inputs
        self.input_set.pos = position
        self.input_set.setup(self)

        self.output_set.n = n_outputs
        self.output_set.pos = position
        self.output_set.setup(self)

        self.update_position()

    def update_position(self):
        self.pos = self.position[0] * self.parent.width, self.position[1] * self.parent.height

    def amend_position(self, delta_x, delta_y):
        self.position = (
            self.position[0] + delta_x,
            self.position[1] + delta_y
        )
        self.update_position()

    def as_json(self):
        return {
            "name": self.name,
            "position": self.position,
            "n_inputs": self.input_set.n,
            "n_outputs": self.output_set.n,
            "code" : self.code,
            "documentation": self.documentation
        }

    def from_json(self, data):
        self.setup(data["name"], data["n_inputs"], data["n_outputs"], data["position"])
        self.code = data["code"]
        self.documentation = data["documentation"]

    def get_input_arg(self, index):
        return self.input_set.get_arg(index)

    def get_number_of_inputs(self):
        return self.input_set.n

    def get_output_arg(self, index):
        return self.output_set.get_arg(index)

    def reset_state_of_input_arguments(self):
        self.input_set.reset_state()

    def reset_state_of_output_arguments(self):
        self.output_set.reset_state()

    def is_root(self):
        return self.input_set.n == 0
        
    def is_leaf(self):
        return self.output_set.n == 0

