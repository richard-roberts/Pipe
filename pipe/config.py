class Colors:

    class Node:
        generic_alpha = 0.2
        selected_alpha = 0.2

    class Edge:
        generic = [1.0, 1.0, 1.0]


class Defaults:

    class Template:

        @staticmethod
        def code(function_name, input_arguments, output_arguments):
            header = "class %s:\n" % function_name

            body = ""
            body += "    def __init__(self%s%s):\n" % (
                ("" if len(input_arguments) == 0 else ", "),
                ", ".join(input_arguments)
            )
            if len(output_arguments) == 0:
                body += "        pass\n"
            else:
                for output_var in output_arguments:
                    body += "        self.%s = None\n" % output_var

            return header + body

        @staticmethod
        def documentation(name):
            template = "A description of the %s node's behavior."
            return template % name
