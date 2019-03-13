class Colors:

    class Message:
        r = 54.0 / 255
        g = 54.0 / 255
        b = 54.0 / 255
        a = 1.0

    class Warning:
        r = 232.0 / 255
        g = 179.0 / 255
        b = 69.0 / 255
        a = 1.0

    class Error:
        r = 255.0 / 255
        g = 98.0 / 255
        b = 88.0 / 255
        a = 1.0

    class Execution:
        r = 141.0 / 255
        g = 69.0 / 255
        b = 232.0 / 255
        a = 1.0

    class Edge:
        r = 240.0 / 255
        g = 240.0 / 255
        b = 240.0 / 255
        a = 1.0

    class Node:
        r = 212.0 / 255
        g = 117.0 / 255
        b = 209.0 / 255
        a = 1.0

    class GraphNode:
        r = 255.0 / 255
        g = 175.0 / 255
        b = 95.0 / 255
        a = 1.0


class Defaults:

    class Template:

        @staticmethod
        def new_template_code(function_name, input_arguments, output_arguments):
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
        def new_template_documentation(name):
            template = "A description of the %s node's behavior."
            return template % name

        @staticmethod
        def graph_execution_template_code(graph_name, input_arguments, output_arguments):
            header = "class %s:\n" % graph_name

            body = ""
            body += "    def __init__(self%s%s):\n" % (
                ("" if len(input_arguments) == 0 else ", "),
                ", ".join(input_arguments)
            )
            if len(output_arguments) == 0:
                body += "        import %s as graph\n" % graph_name
                body += "        execute(%s)\n" % ", ".join(input_arguments)
            else:
                body += "        import %s as graph\n" % graph_name
                body += "        result = graph.execute(%s)\n" % ", ".join(input_arguments)
                for output_var in output_arguments:
                    body += "        self.%s = result[\"%s\"]\n" % (output_var, output_var)

            return header + body

        @staticmethod
        def graph_execution_template_documentation(name):
            template = "Executes the %s graph's behavior. Note, this is NOT editable."
            return template % name
