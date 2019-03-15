from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ListProperty


class ArgumentWidget(ToggleButton):

    def __init__(self, **kwargs):
        super(ArgumentWidget, self).__init__(**kwargs)
        self.argument = None
        self.edge_widget = None

    def setup(self, argument):
        self.argument = argument
        self.text = "_".join(argument.name.split("_")[:-1]) if "_" in argument.name else argument.name
        self.bind(state=self.parent.parent.parent.parent.handle_argument_touched)

    # def disconnect(self):
    #     self.edge_widget = None

    # def connect(self, edge_widget):
    #     self.edge_widget = edge_widget

    # def is_connected(self):
    #     return self.edge_widget is not None

    # def get_edge_widget(self):
    #     return self.edge_widget

    def pretty(self):
        return self.argument.pretty()


class InputArgumentWidget(ArgumentWidget):
    pass


class OutputArgumentWidget(ArgumentWidget):
    pass


class ArgumentSetWidget(BoxLayout):
    names = ListProperty()
    argument_class = None
    widgets = ListProperty()

    def __init__(self, **kwargs):
        super(ArgumentSetWidget, self).__init__(**kwargs)
        self.args = {}

    def setup(self, arguments):
        for argument in arguments:
            arg = self.argument_class()
            self.widgets.append(arg)
            self.add_widget(arg)
            arg.setup(argument)
            self.args[arg] = arg

    def reset_state(self):
        for arg in self.args:
            arg.state = "normal"

    def get_argument_by_name(self, name):
        for arg in self.args.values():
            if arg.argument.name == name:
                return arg
        raise IndexError(
            "%s was not found in %s" % (
                name,
                str([arg.argument.name for arg in self.args.values()])
            )
        )


class InputArgumentSetWidget(ArgumentSetWidget):
    argument_class = InputArgumentWidget


class OutputArgumentSetWidget(ArgumentSetWidget):
    argument_class = OutputArgumentWidget
