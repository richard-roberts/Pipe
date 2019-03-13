#!/usr/local/bin/python3

import os
import shutil
import subprocess
import pathlib

import kivy
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

import globals
from config import Colors
from graph import graph_manager
from graph import graph_widgets
from templates import template_collection_manager

kivy.require("1.10.1")
Factory.register("GraphWidget", graph_widgets.GraphWidget)


class DesktopManager:

    def __init__(self):
        self.graphs = graph_manager.GraphManager()
        self.templates = template_collection_manager.TemplateCollectionManager()

    def clear(self):
        self.graphs.clear()
        self.templates.clear()

    def open_project(self, project_directory):
        templates_directory = os.path.join(project_directory, "templates")
        graphs_directory = os.path.join(project_directory, "graphs")
        self.clear()
        self.templates.import_collections(templates_directory)
        self.graphs.import_graphs(graphs_directory)

    def save_project(self, project_directory):
        shutil.rmtree(project_directory)
        templates_directory = os.path.join(project_directory, "templates")
        graphs_directory = os.path.join(project_directory, "graphs")
        if not os.path.exists(templates_directory):
            os.makedirs(templates_directory)
        if not os.path.exists(graphs_directory):
            os.makedirs(graphs_directory)
        self.templates.export_collections(templates_directory)
        self.graphs.export_graphs(graphs_directory)

    def assemble_project(self, project_directory):
        templates_directory = os.path.join(project_directory, "templates")
        graphs_directory = project_directory
        if not os.path.exists(templates_directory):
            os.makedirs(templates_directory)
            pathlib.Path(os.path.join(templates_directory, "__init__.py")).touch()
        if not os.path.exists(graphs_directory):
            os.makedirs(graphs_directory)
        self.templates.assemble_collections(templates_directory)
        self.graphs.assemble_graphs(graphs_directory)

    def list_graphs(self):
        return self.graphs.graphs.values()


class Desktop(FloatLayout):

    def __init__(self, **kwargs):
        super(Desktop, self).__init__(**kwargs)
        self.manager = DesktopManager()
        self.graph_buttons = []
        globals.PipeInterface().set_instance(self)

    def _set_status(self, message, color):
        bar = self.ids.status_bar
        bar.canvas.before.clear()
        with bar.canvas.before:
            Color(color.r, color.g, color.b, color.a)
            Rectangle(pos=bar.pos, size=bar.size)
        bar.text = "    %s" % message

    def show_message(self, message):
        self._set_status("Status: " + message, Colors.Message)

    def show_warning(self, message):
        self._set_status("Warning: " + message, Colors.Warning)

    def show_error(self, message):
        self._set_status("Error: " + message, Colors.Error)

    def show_execution(self, message):
        self._set_status("Execution: " + message.replace("\r\n", " \\\\ ").replace("\n", " \\\\ "), Colors.Execution)

    def setup_from_graph(self, graph):
        self.ids.editor.setup_from_graph(graph)

    def setup_from_graph_by_name(self, name):
        self.setup_from_graph(globals.GraphInfo().manager.get_by_name(name))

    def add_button_for_graph(self, graph):
        def fn(*args):
            self.setup_from_graph(graph)

        button = Button(text=graph.name, on_release=fn)
        self.ids.graph_selection_menu.add_widget(button)
        self.graph_buttons.append(button)

    def remove_buttons_for_graph(self):
        for button in self.graph_buttons:
            self.ids.graph_selection_menu.remove_widget(button)
        self.graph_buttons = []

    def open_project(self):
        # def fn(pop):
        #     project_directory = pop.ids.filechooser.path
        #     if not project_directory:
        #         self.show_message("Import cancelled (no directory specified)")
        #     self.manager.open_project(project_directory)
        #     self.show_message("Project opened successfully")
        # popup = Factory.OpenProjectPopup()
        # popup.bind(on_dismiss=fn)
        # popup.open()

        self.remove_buttons_for_graph()
        self.manager.open_project("C:/Development/Pipe/examples/testing")
        self.show_message("Project opened successfully")
        for graph in self.manager.list_graphs():
            self.add_button_for_graph(graph)
        self.ids.editor.setup_from_graph(globals.GraphInfo().manager.get_by_name("Main"))
        self.show_message("Switched to %s" % "Bob")
        self.ids.editor.redraw()

    def save_project(self):
        # def fn(pop):
        #     project_directory = pop.ids.filechooser.path
        #     if not project_directory:
        #         self.show_message("Export cancelled (no directory specified)")
        #         return
        #     self.manager.save_project(project_directory)
        #     self.show_message("Project saved successfully")
        # popup = Factory.SaveProjectPopup()
        # popup.bind(on_dismiss=fn)
        # popup.open()
        self.manager.save_project("C:/Development/Pipe/examples/testing")
        self.show_message("Project saved successfully")

    def assemble_and_execute(self):
        temporary = "./tmp"
        globals.TemplateInfo().manager.create_or_update_graph_template(self.ids.editor.graph)
        self.manager.assemble_project(temporary)
        command = 'python ./tmp/%s.py %s' % (self.ids.editor.graph.name, self.ids.command_line_args.text)

        # TODO: figure out what exception this should be
        try:
            result = subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            self.show_error("%s" % str(e))
            shutil.rmtree(temporary)
            return

        shutil.rmtree(temporary)
        if result:
            self.show_execution(result.decode("utf-8"))
        else:
            self.show_execution("no result return")

    def assemble_and_save(self):
        # def fn(pop):
        #     project_directory = pop.ids.filechooser.path
        #     if not project_directory:
        #         self.show_message("Import cancelled (no directory specified)")
        #
        #     self.manager.assemble_project(project_directory)
        #     self.show_message("Project assembled successfully")
        #
        # popup = Factory.ExportAssembledProgram()
        # popup.bind(on_dismiss=fn)
        # popup.open()
        globals.TemplateInfo().manager.create_or_update_graph_template(self.ids.editor.graph)
        self.manager.assemble_project("D:\\tmp")

    def start_new_graph_prompt(self):
        def fn(pop):
            name = pop.ids.name.text

            # If no named was entered, it's probably a cancel?
            if name == "":
                self.show_warning("operation cancelled (no name specified)")
                return

            # Check its not a duplicate
            if globals.GraphInfo().manager.already_exists(name):
                self.show_error("there is already has graph named `%s`." % name)
                return

            graph = self.manager.graphs.new_graph(name)
            self.add_button_for_graph(graph)
            self.ids.editor.setup_from_graph(graph)
            self.show_message("A new graph named %s has been created" % name)

        popup = Factory.NewGraphPopup()
        popup.bind(on_dismiss=fn)
        popup.open()

    def on_touch_down(self, touch):
        if super(Desktop, self).on_touch_down(touch):
            return True
        touch.grab(self)
        if self.ids.editor.collide_point(*touch.pos):
            self.ids.editor.handle_touch_down(touch)
            return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            if self.ids.editor.collide_point(*touch.pos):
                self.ids.editor.handle_touch_move(touch)
            return True
        return super(Desktop, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super(Desktop, self).on_touch_up(touch)


class PipeApp(App):
    def build(self):
        return Desktop()


if __name__ == '__main__':
    PipeApp().run()
