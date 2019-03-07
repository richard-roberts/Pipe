from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ListProperty


class ArgumentWidget(ToggleButton):

    def __init__(self, **kwargs):
        super(ArgumentWidget, self).__init__(**kwargs)
        self.argument = None

    def setup(self, argument):
        self.argument = argument
        self.text = argument.name
        self.bind(state=self.parent.parent.parent.handle_argument_touched)


class InputArgumentWidget(ArgumentWidget):
    pass


class OutputArgumentWidget(ArgumentWidget):
    pass


class ArgumentSetWidget(BoxLayout):
    names = ListProperty()
    argument_class = None

    def __init__(self, **kwargs):
        super(ArgumentSetWidget, self).__init__(**kwargs)
        self.args = {}

    def setup(self, arguments):
        for argument in arguments:
            arg = self.argument_class()
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


class InputArgumentSetWidget(ArgumentSetWidget):
    argument_class = InputArgumentWidget


class OutputArgumentSetWidget(ArgumentSetWidget):
    argument_class = OutputArgumentWidget
