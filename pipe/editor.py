import os
import subprocess

from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

from graph import node
from graph import edge
from assembly import assembler


InputArgument = node.InputArgument
OutputArgument = node.OutputArgument
Node = node.Node
Edge = edge.Edge
Assembler = assembler.Assembler


class NodeEditor(FloatLayout):
    selected = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(NodeEditor, self).__init__(**kwargs)
        self.nodes = {}

    def as_json(self):
        data = []
        for node in self.nodes.values():
            data.append(node.as_json())
        return data

    def from_json(self, data):
        nodes_copy = [e for e in self.nodes.values()]
        for node in nodes_copy:
            self.delete_node(node)

        for datum in data:
            node = Node()
            self.add_widget(node)
            node.from_json(datum)
            self.nodes[node.name] = node

    def set_status(self, message):
        self.parent.set_status(message)

    def delete_node(self, node):
        self.remove_widget(node)
        del self.nodes[node.name]

    def does_named_node_exist(self, name):
        return name in self.nodes.keys()

    def get_node_by_name(self, name):
        for key in self.nodes.keys():
            if key == name:
                return self.nodes[key]
        raise IndexError("No node named `%s` was found" % name)

    def create_new_node(self, name, n_inputs, n_outputs, position):
        # Check name is value            
        if not name or name == "":
            raise ValueError("`%s` is not a valid node name." % name)

        # Check its not a duplicate
        if self.does_named_node_exist(name):
            raise ValueError("`%s` already exists as a node." % name)

        # Create and initialize the node
        node = Node()
        self.add_widget(node)
        node.setup(name, n_inputs, n_outputs, position)

        # Update records
        self.selected = node
        self.nodes[node.name] = node
        
        self.set_status("Created new node named %s" % node.name)

    def start_new_node_prompt(self, position):
        def fn(popup):
            name = popup.ids.name.text

            # If no named was entered, it's probably a cancel?
            if name == "":
                self.set_status("Warning: new node operation cancelled")
                return

            n_inputs = int(popup.ids.n_inputs.text)
            if n_inputs < 0:
                self.set_status("Error: a node must have zero or more inputs")
                return

            n_outputs = int(popup.ids.n_outputs.text)
            if n_inputs < 0:
                self.set_status("Error: a node must have zero or more outputs")
                return

            if n_inputs == 0 and n_outputs == 0:
                self.set_status("Error: a node must have at least one argument")
                return

            self.create_new_node(name, n_inputs, n_outputs, position)

        popup = Factory.NewNodePopup()
        popup.bind(on_dismiss=fn)
        popup.open()
        
    def handle_touch_down(self, touch):
        for node in self.nodes.values():
            if node.collide_point(*touch.pos):
                self.selected = node
                return True
        return False

    def handle_touch_move(self, touch):
        for node in self.nodes.values():
            if node.collide_point(*touch.pos):
                node.amend_position(
                    touch.sx - touch.psx,
                    touch.sy - touch.psy
                )


class EdgeEditor(FloatLayout):

    def __init__(self, **kwargs):
        super(EdgeEditor, self).__init__(**kwargs)
        self.edges = {}

    def as_json(self):
        data = []
        for edge in self.edges.values():
            data.append(edge.as_json())
        return data

    def from_json(self, data):
        edges_copy = [e for e in self.edges.values()]
        for edge in edges_copy:
            self.delete_edge(edge)

        for datum in data:
            edge = Edge()
            self.add_widget(edge)
            edge.from_json(datum)
            self.edges[edge] = edge
        self.update()

    def delete_edge(self, edge):
        if edge not in self.edges:
            raise IndexError("The edge %s does not exist among edges." % edge.name)
        self.remove_widget(edge)
        del self.edges[edge]
    
    def delete_edge_between(self, arg_from, arg_to):
        for edge in self.edges.values():
            if edge.arg_from == arg_from and edge.arg_to == arg_to:
                self.delete_edge(edge)
                return
        raise ValueError("No edge found between %s and %s" % (arg_from.name, arg_to.name))

    def delete_edges_connected_to_node(self, node):
        # use copy to avoid modify dict during iteration
        edges_copy = [e for e in self.edges.values()]
        for edge in edges_copy:
            if edge.arg_from.get_node_name() == node.name or edge.arg_to.get_node_name() == node.name:
                self.delete_edge(edge)

    def edge_already_exists(self, arg_from, arg_to):
        for edge in self.edges.values():
            if edge.arg_from == arg_from and edge.arg_to == arg_to:
                return True
        return False

    def add_new_edge(self, arg_from, arg_to):
        edge = Edge()
        self.add_widget(edge)
        edge.setup(arg_from, arg_to)
        self.edges[edge] = edge
        self.update()

    def get_input_edge_by_argument(self, argument):
        for edge in self.edges.values():
            if edge.name.split("-")[1] == argument.name:
                return edge
        raise ValueError("No edge features an input argument named `%s`" % argument.name)
            

    def update(self):
        for edge in self.edges.values():
            edge.update()

    def handle_touch_move(self, touch):
        self.update()


class Editor(FloatLayout):
    
    def __init__(self, node_editor=None, edge_editor=None, **kwargs):
        super(Editor, self).__init__(**kwargs)
        self.node_editor = NodeEditor() if node_editor is None else node_editor
        self.edge_editor = EdgeEditor() if edge_editor is None else edge_editor
        self.add_widget(self.node_editor, index=2)
        self.add_widget(self.edge_editor, index=1)

        self.activated_input_argument = None
        self.activated_output_argument = None

    def as_json(self):
        return {
            "nodes": self.node_editor.as_json(),
            "edges" : self.edge_editor.as_json()
        }

    def from_json(self, data):
        self.node_editor.from_json(data["nodes"])
        self.edge_editor.from_json(data["edges"])
        
    def set_status(self, message):
        self.parent.parent.parent.parent.set_status(message)

    def delete_selected(self):
        if self.node_editor.selected is not None:
            self.node_editor.delete_node(self.node_editor.selected)
            self.edge_editor.delete_edges_connected_to_node(self.node_editor.selected)
        else:
            self.set_status("Warning: no node selected to delete")

    def handle_argument_touched(self, *args):
        argument = args[0]
        
        if type(argument) == InputArgument:
            
            if argument.state == "down":
                self.activated_input_argument = argument
                self.set_status("Set activate input argument to %s" % argument.name)
            
            elif argument.state == "normal":
                self.activated_input_argument = None
            
            else:
                self.set_status("Error: The state %s is not valid" % argument.state)
        
        elif type(argument) == OutputArgument:
            
            if argument.state == "down":
                self.activated_output_argument = argument
                self.set_status("Set activate input argument to %s" % argument.name)
            
            elif argument.state == "normal":
                self.activated_output_argument = None
            
            else:
                self.set_status("Error: the state %s is not valid" % argument.state)
                return
        
        else:
            self.set_status("Error: %s is not a valid argument" % type(argument))
            return

        if self.activated_input_argument is not None and self.activated_output_argument is not None:
            self.set_status(
                "New edge created from %s to %s" % (
                    self.activated_output_argument.name,
                    self.activated_input_argument.name
                )
            )

            if self.edge_editor.edge_already_exists(
                self.activated_output_argument,
                self.activated_input_argument
            ):
                self.edge_editor.delete_edge_between(
                    self.activated_output_argument,
                    self.activated_input_argument
                )
            else:
                self.edge_editor.add_new_edge(
                    self.activated_output_argument,
                    self.activated_input_argument
                )
            self.activated_output_argument.state = "normal"
            self.activated_input_argument.state = "normal"

    def update(self):
        self.node_editor.update()
        self.edge_editor.update()

    def handle_touch_down(self, touch):
        if not self.node_editor.handle_touch_down(touch):
            self.node_editor.start_new_node_prompt(touch.spos)

    def handle_touch_move(self, touch):
        self.node_editor.handle_touch_move(touch)
        self.edge_editor.handle_touch_move(touch)

    def compile_and_execute(self):
        filepath = "./tmp.py"
        with open(filepath, 'w') as stream:
            stream.write(self.compile())
        command = 'python tmp.py'
        result = subprocess.check_output(command, shell=True)
        self.set_status(result.decode("utf-8"))
        os.remove(filepath)

    def compile_and_save(self):
        def fn(popup):
            filepath = "./%s.py" % popup.text_input.text
            with open(filepath, 'w') as stream:
                stream.write(self.compile())
        popup = Factory.SaveCompiledGraph()
        popup.bind(on_dismiss=fn)
        popup.open()

Factory.register('Editor', cls=Editor)