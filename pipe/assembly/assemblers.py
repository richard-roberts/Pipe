import globals


class Assembler:

    @staticmethod
    def assemble_collection(collection):
        def assemble(template):
            return template.code

        assembled_str = ""
        for item in collection.templates.values():
            assembled_str += assemble(item) + "\n"
        return assembled_str

    @staticmethod
    def assemble_graph(graph):

        all_nodes = graph.nodes.values()

        def assemble(node, argument):
            suffix = ("" if argument is None else ".%s" % argument.name)

            if node.template.is_root():
                return "%s()%s" % (node.template.function_name, suffix)
            else:

                # Build the argument sting (recursively compiling the execution of those arguments)
                argument_str = ""
                for input_arg in node.inputs.values():
                    edge = graph.get_edge_by_argument_to(node, input_arg)
                    if edge is None:
                        argument_str += "%s_%s, " % (node.template.name, input_arg.name)
                    else:
                        child_node = graph.nodes[edge.argument_from.get_node().get_id()]
                        compiled_child = assemble(child_node, edge.argument_from)
                        argument_str += compiled_child + ", "
                argument_str = argument_str[:-2]

                # Compile the invocation
                return "%s(%s)%s" % (
                    node.template.function_name,
                    argument_str,
                    suffix
                )

        assembled_str = ""

        # Standard imports
        assembled_str += "import sys" # used to get command line args
        assembled_str += "\n"

        # Graph imports
        for name in globals.TemplateInfo().manager.get_collection_names():
            assembled_str += "from templates.%s import *\n" % name
        assembled_str += "\n"

        # Write function header with inputs
        function_header = "def execute(%s):\n"
        argument_string = ""
        for node in all_nodes:
            for input_arg in node.list_disconnected_inputs():
                argument_string += ("%s_%s, " % (node.template.name, input_arg.name))
        assembled_str += function_header % argument_string[:-2] # [:-2] to trim last comma.

        # Write function body
        terminating_nodes = [node for node in all_nodes if node.terminates_execution()]

        # Write execution calls
        for node in terminating_nodes:
            if node.has_outputs():
                var_str = ""
                for output in node.list_disconnected_outputs():
                    var_str += "%s_%s, " % (node.template.name, output.name)
                assembled_str += "    %s = %s\n" % (var_str[:-2], assemble(node, output))  # [:-2] to trim last comma.
            else:
                assembled_str += "    %s # %s\n" % (assemble(node, None), node.template.name)

        assembled_str += ""
        assembled_str += "    return {\n"
        for node in terminating_nodes:
            if node.has_outputs():
                for output in node.list_disconnected_outputs():
                    var_name = "%s_%s" % (node.template.name, output.name)
                    assembled_str += "        \"%s\": %s,\n" % (var_name, var_name)
        assembled_str += "    }\n"
        assembled_str += "\n"

        # Run execution function, using sys.args when run as main
        assembled_str += "if __name__ == \"__main__\":\n"
        n = sum([node.count_number_of_disconnected_inputs() for node in all_nodes])
        assembled_str += "    if len(sys.argv) != %d:\n" % (n + 1)

        for node in all_nodes:
            inputs_str = ""
            for input_arg in node.list_disconnected_inputs():
                inputs_str += "%s_%s, " % (node.template.name, input_arg.name)
        assembled_str += "        print(\"Error: not enough inputs given, needed: %s\")\n" % inputs_str[:-2]
        assembled_str += "        raise ValueError(\"Failed to parse arguments\")\n"

        argument_string = ""
        ix = 1
        for node in all_nodes:
            for input_arg in node.list_disconnected_inputs():
                argument_string += ("%s_%s=sys.argv[%d], " % (node.template.name, input_arg.name, ix))
                ix += 1
        assembled_str += "    execute(%s)" % argument_string[:-2] # [:-2] to trim last comma.
        assembled_str += "\n"

        return assembled_str
