#!/usr/local/bin/python3

import os
import json
import subprocess

import kivy
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
kivy.require("1.10.1")

import editor
from assembly import assembler
Assembler = assembler.Assembler


class Desktop(FloatLayout):
    
    def __init__(self, **kwargs):
        super(Desktop, self).__init__(**kwargs)

    def as_json(self):
        return self.ids.editor.as_json()

    def from_json(self, data):
        self.ids.editor.from_json(data)
        self.set_status("Imported program")

    def set_status(self, message):
        message = message.replace('\n','')
        message = message.replace('\t','')
        message = message.replace('\r\t','')
        self.ids.status_bar.text = "    %s"  % message

    def import_graph(self):
        def fn(popup):
            has_selection = len(popup.ids.filechooser.selection) > 0
            if not has_selection:
                self.set_status("Import cancelled (no file specified)")
                return

            path = popup.ids.filechooser.path
            filename = popup.ids.filechooser.selection[0]

            with open(os.path.join(path, filename)) as stream:
                string = stream.read()
                data = json.loads(string)
                self.from_json(data)

            self.set_status("Import successful")
                

        popup = Factory.ImportGraphPopup()
        popup.bind(on_dismiss=fn)
        popup.open()

    def export_graph(self):
        def fn(popup):
            path = popup.ids.filechooser.path
            filename = popup.ids.text_input.text
            if not filename:
                self.set_status("Export cancelled (no file specified)")
                return

            with open(os.path.join(path, filename), 'w') as stream:
                string = json.dumps(
                    self.as_json(),
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')
                )
                stream.write(string)

            self.set_status("Export successful")

        popup = Factory.ExportGraphPopup()
        popup.bind(on_dismiss=fn)
        popup.open()

    def assemble_and_execute(self):
        filepath = "./tmp.py"
        with open(filepath, 'w') as stream:
            stream.write(
                Assembler.assemble(
                    self.ids.editor.node_editor, self.ids.editor.edge_editor
                )
            )
        command = 'python %s' % filepath
        try:
            result = subprocess.check_output(command, shell=True)
        except:
            self.set_status("Execution failed")
            os.remove(filepath)
            return

        os.remove(filepath)
        if result:
            self.set_status("Execution successful: %s" % result.decode("utf-8"))
        else:
            self.set_status("Execution successful")

    def assemble_and_save(self):
        def fn(popup):
            filepath = popup.ids.text_input.text

            path = popup.ids.filechooser.path
            filename = popup.ids.text_input.text
            if not filename:
                self.set_status("Export assembled cancelled (no file specified)")
                return

            with open(filepath, 'w') as stream:
                stream.write(
                    Assembler.assemble(
                        self.ids.editor.node_editor, self.ids.editor.edge_editor
                    )
                )
        popup = Factory.ExportAssembledProgram()
        popup.bind(on_dismiss=fn)
        popup.open()

    def on_touch_down(self, touch):
        print(touch)
        if super(Desktop, self).on_touch_down(touch): return True
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