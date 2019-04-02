import os
import tempfile
import subprocess
from threading import Timer

import globals


class ExternalTemplateCodeEditor:

    update_time_in_seconds = 0.01

    def __init__(self, template):
        self.template = template
        self.editor = os.environ.get('EDITOR', 'vim')
        self.original = template.code
        self.file = None

        self.timer = None
        self.is_running = False

        self.write_to_new()
        self.open()

    def write_to_new(self):
        self.file = tempfile.NamedTemporaryFile(
            prefix="%s-%s_____" % (self.template.collection_name, self.template.name),
            suffix=".py"
        )
        self.file.write(bytes(self.original, encoding='utf8'))
        self.file.flush()

    def open(self):
        subprocess.call([self.editor, self.file.name])

    def apply_to_node(self):
        self.file.seek(0)
        self.template.code = self.file.read().decode()
        globals.PipeInterface().instance.update_code_input()

    def run_auto(self):
        self.is_running = False
        self.start_auto()
        self.apply_to_node()

    def start_auto(self):
        if not self.is_running:
            self.timer = Timer(self.update_time_in_seconds, self.run_auto)
            self.timer.start()
            self.is_running = True

    def stop_auto(self):
        self.timer.cancel()
        self.is_running = False

    def finish(self):
        self.stop_auto()
        self.file.close()

