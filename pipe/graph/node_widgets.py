from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

import config


class NodeWidget(BoxLayout):
    node = ObjectProperty(None, allownone=True)
    background_color = ObjectProperty()
    input_widgets = ObjectProperty()
    output_widgets = ObjectProperty()

    def __init__(self, **kwargs):
        self.background_color = config.Colors.Node
        super(NodeWidget, self).__init__(**kwargs)
        self.node = None

    def redraw(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(
                self.background_color.r,
                self.background_color.g,
                self.background_color.b,
                self.background_color.a
            )
            Rectangle(pos=self.pos, size=self.size)

    def setup_arguments(self):
        self.input_widgets.pos = self.node.position
        self.input_widgets.setup(self.node.inputs.values())
        self.output_widgets.pos = self.node.position
        self.output_widgets.setup(self.node.outputs.values())

    def setup(self, node):
        self.node = node
        self.setup_arguments()
        self.update_position()

    def update_position(self):
        self.pos = (
            self.node.position[0] * Window.width,
            self.node.position[1] * Window.height
        )
        self.input_widgets.update_connector_position(
            (
                self.pos[0],
                self.pos[1]
            )
        )
        self.output_widgets.update_connector_position(
            (
                self.pos[0] + self.width,
                self.pos[1]
            )
        )

    def amend_position(self, delta_x, delta_y):
        self.node.position = (
            self.node.position[0] + delta_x,
            self.node.position[1] + delta_y
        )
        self.update_position()

    def reset_state_of_input_argument_widgets(self):
        self.input_widgets.reset_state()

    def reset_state_of_output_argument_widgets(self):
        self.output_widgets.reset_state()

    def get_input_argument_widget_by_argument_name(self, name):
        return self.input_widgets.get_argument_by_name(name)

    def get_output_argument_widget_by_argument_name(self, name):
        return self.output_widgets.get_argument_by_name(name)


class GraphNodeWidget(NodeWidget):

    def __init__(self, **kwargs):
        super(GraphNodeWidget, self).__init__(**kwargs)
        self.background_color = config.Colors.GraphNode
