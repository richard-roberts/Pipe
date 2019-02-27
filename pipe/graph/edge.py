from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty

from . import config

Config = config.Config


class Edge(FloatLayout):

    from_x = NumericProperty()
    from_y = NumericProperty()
    to_x = NumericProperty()
    to_y = NumericProperty()

    def __init__(self, **kwargs):
        super(Edge, self).__init__(**kwargs)

    def setup(self, arg_from, arg_to):
        self.arg_from = arg_from
        self.arg_to = arg_to
        self.name = "%s-%s" % (self.arg_from.name, self.arg_to.name)

    def update(self):
        self.from_x = self.arg_from.x + self.arg_from.width
        self.from_y = self.arg_from.y + self.arg_from.height / 2
        self.to_x = self.arg_to.x
        self.to_y = self.arg_to.y + self.arg_to.height / 2

    def as_json(self):
        return {
            "from": self.arg_from.name,
            "to": self.arg_to.name
        }

    def from_json(self, data):
        from_name, from_index_str = data["from"].split("_")
        to_name, to_index_str = data["to"].split("_")
        from_index, to_index = int(from_index_str), int(to_index_str)
        arg_from = self.parent.parent.node_editor.get_node_by_name(from_name).get_output_arg(from_index)
        arg_to = self.parent.parent.node_editor.get_node_by_name(to_name).get_input_arg(to_index)
        self.setup(arg_from, arg_to)

    def get_output_argument(self):
        return self.arg_from
