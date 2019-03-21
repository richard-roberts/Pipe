from kivy.factory import Factory
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

import config
import globals


class NodeWidget(BoxLayout):
    node = ObjectProperty(None, allownone=True)
    background_color = ObjectProperty()
    input_widgets = ObjectProperty()
    output_widgets = ObjectProperty()

    def __init__(self, background_color=None, **kwargs):
        self.background_color = config.Colors.Node if background_color is None else background_color
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
        self.ids.execution_index_button.text = "i=%s" % self.node.execution_index

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

    def start_set_execution_index_prompt(self, *args):
        popup = Factory.SetExecutionIndexPopup(title="Set execution index for %s" % self.node.template.name)

        def fn(_):
            if not popup.used:
                globals.PipeInterface().instance.show_warning("cancelled operation")
                return

            try:
                new_index = int(popup.ids.new_index.text)
            except ValueError:
                globals.PipeInterface().instance.show_error("%s is not a valid index" % str(popup.ids.new_index.text))
                return

            self.node.set_execution_index(new_index)
            self.ids.execution_index_button.text = "i=%d" % new_index
            globals.PipeInterface().instance.show_message("%s's index set to %d" % (self.node.template.name, new_index))

        popup.bind(on_dismiss=fn)
        popup.open()


class GraphNodeWidget(NodeWidget):

    def __init__(self, **kwargs):
        super(GraphNodeWidget, self).__init__(background_color=config.Colors.GraphNode, **kwargs)
