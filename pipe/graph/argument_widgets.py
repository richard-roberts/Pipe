from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ListProperty

import config


class ArgumentWidget(ToggleButton):

    argument = ObjectProperty()
    _instances = []

    @classmethod
    def all_update_color(cls):
        for i in cls._instances:
            i.update_color()

    def __init__(self, **kwargs):
        self.background_color = config.Colors.Argument.as_list()
        super(ArgumentWidget, self).__init__(**kwargs)
        self.argument = None
        self._instances.append(self)

    def get_name(self):
        return self.argument.get_name()

    def update_color(self):
        if self.argument.is_connected():
            self.background_color = config.Colors.ArgumentWithEdgeConnected.as_list()
        else:
            if self.argument.has_default_value():
                self.background_color = config.Colors.ArgumentWithDefaultValue.as_list()
            else:
                self.background_color = config.Colors.Argument.as_list()
        self.canvas.ask_update()

    def get_alias(self):
        return self.argument.get_alias()

    def update_alias(self, alias):
        self.text = alias
        self.argument.set_alias(alias)

    def reset_default_value(self):
        self.argument.reset_default_value()
        self.all_update_color()

    def update_default_value(self, value):
        self.argument.set_default_value(value)
        self.all_update_color()

    def update_evaluated_value(self, value):
        self.argument.set_evaluated_value(value)

    def get_evaluated_value(self):
        return self.argument.get_evaluated_value()

    def setup(self, argument):
        self.argument = argument
        self.text = argument.get_alias()
        self.update_color()

    def on_state(self, widget, value):
        self.parent.parent.parent.parent.handle_argument_touched(self)

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
            if arg.get_name() == name:
                return arg
        raise IndexError(
            "%s was not found in %s" % (
                name,
                str([arg.get_name() for arg in self.args.values()])
            )
        )

    def list_args_widgets(self):
        return self.args.values()


class InputArgumentSetWidget(ArgumentSetWidget):
    argument_class = InputArgumentWidget

    def get_evaluated_as_name_value_pairs(self):
        return [(widget.get_name(), widget.get_evaluated_value()) for widget in self.args.values()]


class OutputArgumentSetWidget(ArgumentSetWidget):
    argument_class = OutputArgumentWidget

