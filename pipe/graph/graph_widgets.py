from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

import globals
from . import argument_widgets
from . import node_widgets
from . import edge_widgets


class GraphWidget(FloatLayout):
    selected_node_widget = ObjectProperty(None, allownone=True)
    graph = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        self.graph = None
        self.activated_input_argument = None
        self.activated_output_argument = None
        self.node_widgets = {}
        self.edge_widgets = {}

    def clear(self):
        self.activated_input_argument = None
        self.activated_output_argument = None
        self.clear_node_widgets()
        self.clear_edge_widgets()

    def clear_node_widgets(self):
        widgets_copy = [w for w in self.node_widgets.values()]
        for widget in widgets_copy:
            self.remove_widget(widget)
            del self.node_widgets[widget]

    def clear_edge_widgets(self):
        widgets_copy = [w for w in self.edge_widgets.values()]
        for widget in widgets_copy:
            self.remove_widget(widget)
            del self.edge_widgets[widget]

    def setup_from_graph(self, graph):
        self.clear()
        self.graph = graph
        for node in self.graph.nodes.values():
            new_node_widget = node_widgets.NodeWidget()
            self.add_widget(new_node_widget)
            new_node_widget.setup(node)
            self.node_widgets[new_node_widget] = new_node_widget

        for edge in self.graph.edges.values():
            new_edge_widget = edge_widgets.EdgeWidget()
            self.add_widget(new_edge_widget)

            node_widget_from = None
            for widget in self.node_widgets.values():
                if widget.node == edge.argument_from.get_node():
                    node_widget_from = widget
                    break
            if node_widget_from is None:
                raise ValueError("Could not find from-node widget (edge `%s`)" % edge)

            arg_widget_from = node_widget_from.get_output_argument_widget_by_argument_name(edge.argument_from.name)
            if arg_widget_from is None:
                raise ValueError("Could not find from-argument widget (edge `%s`)" % edge)

            node_widget_to = None
            for widget in self.node_widgets.values():
                if widget.node == edge.argument_to.get_node():
                    node_widget_to = widget
                    break
            if node_widget_to is None:
                raise ValueError("Could not find to-node widget (edge `%s`)" % edge)

            arg_widget_to = node_widget_to.get_input_argument_widget_by_argument_name(edge.argument_to.name)
            if arg_widget_to is None:
                raise ValueError("Could not find to-argument widget (edge `%s`)" % edge)

            new_edge_widget.setup(edge, arg_widget_from, arg_widget_to)
            self.edge_widgets[new_edge_widget] = new_edge_widget

    def set_status(self, message):
        self.parent.parent.parent.parent.set_status(message)

    def create_new_node(self, template, position):
        node = self.graph.create_node(template, position)
        widget = node_widgets.NodeWidget()
        self.add_widget(widget)
        widget.setup(node)
        self.selected_node_widget = widget
        self.node_widgets[widget] = widget
        self.set_status("Created new node from %s template" % node.template.name)

    def create_new_edge(self, widget_from, widget_to):
        edge = self.graph.create_edge(widget_from.argument, widget_to.argument)
        widget = edge_widgets.EdgeWidget()
        self.add_widget(widget)
        widget.setup(edge, widget_from, widget_to)
        self.edge_widgets[widget] = widget

    def delete_node_by_widget(self, node_widget):
        self.graph.delete_node(node_widget.node)
        self.remove_widget(node_widget)
        del self.node_widgets[node_widget]

    def delete_edge_by_widget(self, edge_widget):
        self.graph.delete_edge(edge_widget.edge)
        self.remove_widget(edge_widget)
        del self.edge_widgets[edge_widget]

    def delete_connected_edges_and_node_by_widget(self, node_widget):
        edge_widgets_copy = [e for e in self.edge_widgets.values()]
        for edge_widget in edge_widgets_copy:
            if edge_widget.edge.is_connected_to_node(node_widget.node):
                self.delete_edge_by_widget(edge_widget)
        self.delete_node_by_widget(node_widget)

    def delete_edge_widget_by_nodes_widgets(self, widget_from, widget_to):
        for edge_widget in self.edge_widgets.values():
            if edge_widget.widget_from == widget_from and edge_widget.widget_to == widget_to:
                self.delete_edge_by_widget(edge_widget)
                return

    def edge_already_exists(self, widget_from, widget_to):
        for edge_widget in self.edge_widgets.values():
            if edge_widget.widget_from == widget_from and edge_widget.widget_to == widget_to:
                return True
        return False

    def delete_selected(self):
        if self.selected_node_widget is not None:
            self.delete_connected_edges_and_node_by_widget(self.selected_node_widget)
        else:
            self.set_status("Warning: no node selected to delete")

    def start_new_node_prompt(self, position):
        if len(globals.TemplateInfo().manager.get_names()) == 0:
            self.set_status("Error: no templates have been registered")
            return

        def fn(pop):
            name = pop.ids.options.text
            if name == "Select template":
                self.set_status("Warning: new node cancelled (no template selected)")
                return

            collection_name, template_name = name.split("::")
            template = globals.TemplateInfo().manager.get_template(collection_name, template_name)
            self.create_new_node(template, position)

        popup = Factory.NewNodePopup()
        popup.names = globals.TemplateInfo().manager.get_names()
        popup.bind(on_dismiss=fn)
        popup.open()

    def handle_argument_touched(self, argument_widget, argument_widget_state):

        if type(argument_widget) == argument_widgets.InputArgumentWidget:

            if argument_widget_state == "down":
                self.activated_input_argument = argument_widget
                self.set_status("Set activate input argument to %s" % argument_widget.argument.name)

            elif argument_widget_state == "normal":
                self.activated_input_argument = None

            else:
                self.set_status("Error: The state %s is not valid" % argument_widget_state)

        elif type(argument_widget) == argument_widgets.OutputArgumentWidget:

            if argument_widget_state == "down":
                self.activated_output_argument = argument_widget
                self.set_status("Set activate input argument to %s" % argument_widget.argument.name)

            elif argument_widget_state == "normal":
                self.activated_output_argument = None

            else:
                self.set_status("Error: the state %s is not valid" % argument_widget_state)
                return

        else:
            raise ValueError("Error: %s is not a valid argument type (this shouldn't happen)?" % type(argument_widget))

        if self.activated_input_argument is not None and self.activated_output_argument is not None:
            self.set_status(
                "New edge created from %s to %s" % (
                    self.activated_output_argument.argument.name,
                    self.activated_input_argument.argument.name
                )
            )

            if self.edge_already_exists(
                self.activated_output_argument,
                self.activated_input_argument
            ):
                self.delete_edge_widget_by_nodes_widgets(
                    self.activated_output_argument,
                    self.activated_input_argument
                )
            else:
                self.create_new_edge(
                    self.activated_output_argument,
                    self.activated_input_argument
                )
            self.activated_output_argument.state = "normal"
            self.activated_input_argument.state = "normal"

    def handle_touch_down(self, touch):
        for widget in self.node_widgets.values():
            if widget.collide_point(*touch.pos):
                self.selected_node_widget = widget
                return True

        self.start_new_node_prompt(touch.spos)

    def handle_touch_move(self, touch):
        if self.selected_node_widget is None:
            return

        self.selected_node_widget.amend_position(
            touch.sx - touch.psx,
            touch.sy - touch.psy
        )

        # Update all edges
        # TODO: should optimise this so that only connected edges are updated
        for edge_widget in self.edge_widgets:
            edge_widget.update_position()
