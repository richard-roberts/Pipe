from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.treeview import TreeView, TreeViewLabel

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
        globals.GraphWidget().set_instance(self)

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
        # update the current graph execution node if there is a graph
        if self.graph is not None:
            globals.TemplateInfo().manager.create_or_update_graph_template(self.graph)

        self.clear()

        self.graph = graph
        for node in self.graph.nodes.values():
            if node.is_graph_execution_node():
                new_node_widget = node_widgets.GraphNodeWidget()
            else:
                new_node_widget = node_widgets.NodeWidget()
            self.add_widget(new_node_widget)
            new_node_widget.setup(node)
            self.node_widgets[new_node_widget] = new_node_widget

        for edge in self.graph.edges.values():
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

            new_edge_widget = edge_widgets.EdgeWidget(edge, arg_widget_from, arg_widget_to)
            self.add_widget(new_edge_widget)
            self.edge_widgets[new_edge_widget] = new_edge_widget

    def rebuild(self):
        self.setup_from_graph(self.graph)

    def create_new_node(self, template, position):
        node = self.graph.create_node(template, position)
        if node.is_graph_execution_node():
            widget = node_widgets.GraphNodeWidget()
        else:
            widget = node_widgets.NodeWidget()
        self.add_widget(widget)
        widget.setup(node)
        self.selected_node_widget = widget
        self.node_widgets[widget] = widget
        globals.PipeInterface().instance.show_message("Created new node from %s template" % node.template.name)

    def new_template_and_node_prompt(self, position):
        def fn(pop):
            collection = pop.ids.collection.text
            name = pop.ids.name.text

            # If no collection was entered, it's probably a cancel?
            if collection == "":
                globals.PipeInterface().instance.show_warning("operation cancelled (no collection specified)")
                return

            # Avoid adding stuff to the graph execution collection
            if globals.TemplateInfo().manager.is_graph_execution_name(collection):
                globals.PipeInterface().instance.show_error("cannot add templates to the graph execution category")

            # If no named was entered, it's probably a cancel?
            if name == "":
                globals.PipeInterface().instance.show_warning("operation cancelled (no name specified)")
                return

            # Check its not a duplicate
            if globals.TemplateInfo().manager.already_exists(collection, name):
                globals.PipeInterface().instance.show_error("%s already has template named `%s`." % (name, collection))
                return

            # Process arguments and check at least one exists
            inputs_str = pop.ids.inputs.text.strip()
            outputs_str = pop.ids.outputs.text.strip()
            inputs = [] if inputs_str is "" else [arg.strip() for arg in inputs_str.split(",")]
            outputs = [] if outputs_str is "" else [arg.strip() for arg in outputs_str.split(",")]
            if len(inputs) == 0 and len(outputs) == 0:
                globals.PipeInterface().instance.show_error("a node must have at least one argument")
                return

            template = globals.TemplateInfo().manager.new_template(collection, name, inputs, outputs)
            self.create_new_node(template, position)
            globals.PipeInterface().instance.show_message("A new template named %s has been created" % name)

        popup = Factory.NewTemplatePopup()
        popup.bind(on_dismiss=fn)
        popup.open()

    def edit_template_via_node_widget(self, node_widget):

        if globals.TemplateInfo().manager.template_is_graph_execution(node_widget.node.template):
            globals.PipeInterface().instance.show_error("cannot edit graph execution templates")
            return

        old_template = node_widget.node.template

        def fn(pop):

            new_collection = pop.ids.collection.text
            new_name = pop.ids.name.text

            # If no new_collection was entered, it's probably a cancel?
            if new_collection == "":
                globals.PipeInterface().instance.show_warning("operation cancelled (no new_collection specified)")
                return

            # If no named was entered, it's probably a cancel?
            if new_name == "":
                globals.PipeInterface().instance.show_warning("operation cancelled (no new_name specified)")
                return

            # Process arguments and check at least one exists
            inputs_str = pop.ids.inputs.text.strip()
            outputs_str = pop.ids.outputs.text.strip()
            inputs = [] if inputs_str is "" else [arg.strip() for arg in inputs_str.split(",")]
            outputs = [] if outputs_str is "" else [arg.strip() for arg in outputs_str.split(",")]
            if len(inputs) == 0 and len(outputs) == 0:
                globals.PipeInterface().instance.show_error("a node must have at least one argument")
                return

            globals.TemplateInfo().manager.delete_template(old_template)
            new_template = globals.TemplateInfo().manager.new_template(new_collection, new_name, inputs, outputs)
            new_template.documentation = old_template.documentation
            globals.GraphInfo().manager.replace_template_a_with_b(old_template, new_template)
            self.rebuild()

        popup = Factory.EditTemplatePopup()
        popup.ids.collection.text = old_template.collection_name
        popup.ids.name.text = old_template.name
        popup.ids.inputs.text = old_template.input_string()
        popup.ids.outputs.text = old_template.output_string()
        popup.bind(on_dismiss=fn)
        popup.open()

    def create_new_edge(self, widget_from, widget_to):
        edge = self.graph.create_edge(widget_from.argument, widget_to.argument)
        widget = edge_widgets.EdgeWidget(edge, widget_from, widget_to)
        self.add_widget(widget)
        self.edge_widgets[widget] = widget

    def delete_node_only_by_widget(self, node_widget):
        # NOTE: THIS CALL TO DELETE_NODE WILL DELETE EDGES IN THE GRAPH
        self.graph.delete_node(node_widget.node)
        self.remove_widget(node_widget)
        del self.node_widgets[node_widget]
        globals.PipeInterface().instance.show_message("deleted %s" % node_widget.node.template.name)

    def delete_edge_by_widget(self, edge_widget):
        self.graph.delete_edge(edge_widget.edge)
        edge_widget.disconnect()
        self.remove_widget(edge_widget)
        del self.edge_widgets[edge_widget]

    def delete_node_and_connected_edges_by_widget(self, node_widget):
        edge_widgets_copy = [e for e in self.edge_widgets.values()]
        for edge_widget in edge_widgets_copy:
            if edge_widget.edge.is_connected_to_node(node_widget.node):
                # DON'T CALL DELETE_EDGE_BY_WIDGET, the graph handles deleting its own edges
                edge_widget.disconnect()
                self.remove_widget(edge_widget)
        self.delete_node_only_by_widget(node_widget)

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
            self.delete_node_and_connected_edges_by_widget(self.selected_node_widget)
        else:
            globals.PipeInterface().instance.show_warning("no node selected to delete")

    def start_new_node_prompt(self, position):
        popup = Factory.NewNodePopup()

        def divert_to_new_template():
            popup.used = True
            popup.dismiss()
            self.new_template_and_node_prompt(position)

        popup.new_template_callback = divert_to_new_template

        def cancelled(_):
            if not popup.used:
                globals.PipeInterface().instance.show_warning("cancelled new node operation")

        def make_change_to_fn(collection_name, template_name):
            def fn(instance, value):
                if value == "create":
                    popup.used = True
                    popup.dismiss()
                    template = globals.TemplateInfo().manager.get_template(collection_name, template_name)
                    self.create_new_node(template, position)
                elif value == "delete":
                    popup.used = True
                    popup.dismiss()
                    template = globals.TemplateInfo().manager.get_template(collection_name, template_name)
                    globals.GraphInfo().manager.delete_any_nodes_using_template(template)
                    globals.TemplateInfo().manager.delete_template_by_name(collection_name, template_name)
                    self.start_new_node_prompt(position)
                    self.setup_from_graph(self.graph)
                else:
                    raise ValueError("Got unexpected value ``" % value)
            return fn

        # See https://kivy.org/doc/stable/api-kivy.uix.treeview.html
        view = TreeView(
            hide_root=False,
            indent_level=4
        )
        dictionary = globals.TemplateInfo().manager.get_dictionary()
        for key in dictionary.keys():
            node = view.add_node(TreeViewLabel(text=key, is_open=False))
            for name in dictionary[key]:
                template = globals.TemplateInfo().manager.get_template(key, name)
                n_uses = globals.GraphInfo().manager.count_uses_of_template(template)
                if n_uses == 0:
                    label_str = '%s [ref=create][u]create[/u][/ref] [ref=delete][u]delete[/u][/ref]' % name
                else:
                    label_str = '%s [ref=create][u]create[/u][/ref]' % name

                view.add_node(
                    TreeViewLabel(
                        text=label_str,
                        markup=True,
                        on_ref_press=make_change_to_fn(key, name)
                    ),
                    node
                )
        popup.ids.options_menu.add_widget(view)
        popup.bind(on_dismiss=cancelled)
        popup.open()

    def handle_argument_touched(self, argument_widget, argument_widget_state):

        if type(argument_widget) == argument_widgets.InputArgumentWidget:

            if argument_widget_state == "down":
                self.activated_input_argument = argument_widget
                # globals.PipeInterface().instance.show_message("Set activate input argument to %s" % argument_widget.argument.name)
            elif argument_widget_state == "normal":
                self.activated_input_argument = None
                # globals.PipeInterface().instance.show_message("Deactivated argument")
            else:
                globals.PipeInterface().instance.show_error("The state %s is not valid" % argument_widget_state)

        elif type(argument_widget) == argument_widgets.OutputArgumentWidget:

            if argument_widget_state == "down":
                self.activated_output_argument = argument_widget
                # globals.PipeInterface().instance.show_message("Set activate output argument to %s" % argument_widget.argument.name)
            elif argument_widget_state == "normal":
                self.activated_output_argument = None
                # globals.PipeInterface().instance.show_message("Deactivated argument")
            else:
                globals.PipeInterface().instance.show_error("the state %s is not valid" % argument_widget_state)
                return

        else:
            raise ValueError("Error: %s is not a valid argument type (this shouldn't happen)?" % type(argument_widget))

        if self.activated_input_argument is not None and self.activated_output_argument is not None:

            if self.edge_already_exists(
                self.activated_output_argument,
                self.activated_input_argument
            ):
                self.delete_edge_widget_by_nodes_widgets(
                    self.activated_output_argument,
                    self.activated_input_argument
                )
                self.activated_output_argument.state = "normal"
                self.activated_input_argument.state = "normal"
                globals.PipeInterface().instance.show_message("Edge deleted")
                return

            if self.activated_input_argument.is_connected():
                globals.PipeInterface().instance.show_error("the input argument is already connected")
                self.activated_output_argument.state = "normal"
                self.activated_input_argument.state = "normal"
                return

            # Note:
            #   Need to have print first, since args
            #   get reset during edge creation
            globals.PipeInterface().instance.show_message(
                "New edge created from %s to %s" % (
                    self.activated_output_argument.argument.name,
                    self.activated_input_argument.argument.name
                )
            )

            self.create_new_edge(
                self.activated_output_argument,
                self.activated_input_argument
            )
            self.activated_output_argument.state = "normal"
            self.activated_input_argument.state = "normal"

    def handle_touch_down(self, touch):
        if touch.is_double_tap:
            # Handle double click if on node
            for widget in self.node_widgets.values():
                if widget.collide_point(*touch.pos):
                    if widget.node.is_graph_execution_node():
                        globals.PipeInterface().instance.setup_from_graph_by_name(widget.node.template.name)
                        return True
                    else:
                        # ignore touch
                        return True

            # double click not on background, so want to spawn new node
            self.start_new_node_prompt(touch.spos)
            return True

        # Handle single click, selects node
        for widget in self.node_widgets.values():
            if widget.collide_point(*touch.pos):
                self.selected_node_widget = widget
                return True

        self.selected_node_widget = None
        return False

    def handle_touch_move(self, touch):
        if self.selected_node_widget is None:
            for node_widget in self.node_widgets:
                node_widget.amend_position(
                    touch.sx - touch.psx,
                    touch.sy - touch.psy
                )
        else:
            self.selected_node_widget.amend_position(
                touch.sx - touch.psx,
                touch.sy - touch.psy
            )
