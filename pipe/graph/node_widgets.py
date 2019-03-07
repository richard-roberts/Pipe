from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class NodeWidget(BoxLayout):
    node = ObjectProperty(None, allownone=True)
    input_widgets = ObjectProperty()
    output_widgets = ObjectProperty()
    template = ObjectProperty()

    def __init__(self, **kwargs):
        super(NodeWidget, self).__init__(**kwargs)
        self.node = None

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
