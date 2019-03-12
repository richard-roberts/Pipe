class Colors:

    class Node:
        generic_alpha = 0.2
        selected_alpha = 0.2

    class Edge:
        generic = [1.0, 1.0, 1.0]


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
