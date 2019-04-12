import os
import subprocess
import tempfile
import json


class BasicRoutine:

    def __init__(self, *expressions):
        self.expressions = expressions
        self.results_file = tempfile.NamedTemporaryFile()

    def generate_code(self, arguments, results, argument_data=None):
        def set_header():
            content = "# Header\n"
            content += "import json\n"
            content += "\n"
            return content

        def set_arguments():
            content = "# Arguments\n"
            for argument in arguments:
                if argument_data is not None and argument.get_name() in argument_data.keys():
                    value = argument_data[argument.get_name()]
                else:
                    value = argument.get_value()
                content += "%s=%s\n" % (argument.get_name(), value)
            content += "\n"
            return content

        def routine_part():
            content = "# Routine\n"
            for expression in self.expressions:
                content += "%s\n" % expression
            content += "\n"
            return content

        def results_part():
            content = "# Results\n"
            content += "result = {\n"
            for result in results:
                key = result.get_name()
                content += "    \"%s\": %s,\n" % (key, key)
            content += "}\n"
            content += "\n"
            content += "f = open('%s', 'w')\n" % self.results_file.name
            content += "f.write(json.dumps(result, indent=4, separators=(',', ': ')))\n"
            content += "f.close()\n"
            content += "\n"
            return content

        return set_header() + set_arguments() + routine_part() + results_part()

    def execute_and_get_standard_output_and_error(self, arguments, results, argument_data=None):
        execution_file = None

        def write_execution_file():
            content = self.generate_code(arguments, results, argument_data=argument_data)
            file = tempfile.NamedTemporaryFile()
            file.write(bytes(content, encoding="utf-8"))
            file.seek(0)
            return file

        def execute_and_read_standard():
            process_result = subprocess.Popen(
                ['python3', execution_file.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=os.environ.copy()
            )
            output, error = process_result.communicate()
            return output, error

        execution_file = write_execution_file()
        return execute_and_read_standard()

    def read_results_file(self):
        self.results_file.seek(0)
        content = self.results_file.read().decode(encoding="utf-8")
        return json.loads(content)


def from_json(data):
    return BasicRoutine(*data)
