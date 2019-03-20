from kivy.factory import Factory

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ListProperty, ObjectProperty

import config
import globals


class ArgumentWidget(ToggleButton):

    # bg = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.background_color = config.Colors.Argument.as_list()
        super(ArgumentWidget, self).__init__(**kwargs)
        self.argument = None

    def update_color(self):
        if self.argument.is_connected():
            self.background_color = config.Colors.ArgumentWithEdgeConnected.as_list()
            print("%s.color should be " % self.pretty(), self.background_color)
        else:
            if self.argument.has_default_value():
                self.background_color = config.Colors.ArgumentWithDefaultValue.as_list()
                print("%s.color should be " % self.pretty(), self.background_color)
            else:
                self.background_color = config.Colors.Argument.as_list()
                print("%s.color should be " % self.pretty(), self.background_color)
        self.canvas.ask_update()

    def setup(self, argument):
        self.argument = argument
        self.text = "_".join(argument.name.split("_")[:-1]) if "_" in argument.name else argument.name

    def start_set_default_value_prompt(self):
        popup = Factory.SetDefaultValuePopup(title="Set default value for %s" % self.pretty())

        def fn(_):
            if popup.reset_to_none:
                self.argument.reset_default_value()
                self.update_color()
                globals.PipeInterface().instance.show_message("default value reset")
                return

            has_bool = popup.ids.bool_value.text != ""
            has_num = popup.ids.num_value.text != ""
            has_str = popup.ids.str_value.text != ""

            count = 0
            if has_bool: count += 1
            if has_num: count += 1
            if has_str: count += 1
            if count != 1:
                globals.PipeInterface().instance.show_error("more than one value was entered")
                return
            elif count == 0:
                globals.PipeInterface().instance.show_error("no default value was entered")
                return

            if has_bool:
                value = bool(popup.ids.str_value.text)
            elif has_num:
                value = float(popup.ids.num_value.text)
            elif has_str:
                value = str(popup.ids.bool_value.text)
            else:
                raise ValueError("This should never happen?")

            self.argument.set_default_value(value)
            self.update_color()

        popup.bind(on_dismiss=fn)
        popup.open()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.start_set_default_value_prompt()
            else:
                self.state = "normal" if self.state != "normal" else "down"
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
