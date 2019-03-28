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
                    if input_arg.is_connected():
                        from_arg = input_arg.get_first_connected().argument_from
                        compiled_child = assemble(from_arg.get_node(), from_arg)
                        argument_str += compiled_child + ", "
                    else:
                        if input_arg.has_default_value():
                            argument_str += "%s, " % str(input_arg.default_value)
                        else:
                            argument_str += "%s, " % input_arg.code_name()

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
            for input_arg in node.list_inputs_needing_value():
                argument_string += "%s, " % input_arg.code_name()
        assembled_str += function_header % argument_string[:-2] # [:-2] to trim last comma.

        # Write execution calls
        terminating_nodes = [node for node in all_nodes if node.terminates_execution()]
        terminating_nodes.sort(key=lambda x: x.execution_index, reverse=False)

        for node in terminating_nodes:
            if node.has_outputs():
                assembled_str += "    tmp = %s\n" % (assemble(node, None))
                for output in node.list_disconnected_outputs():
                    assembled_str += "    %s=tmp.%s\n" % (output.code_name(), output.name)
            else:
                assembled_str += "    %s # %s\n" % (assemble(node, None), node.template.name)

        assembled_str += ""
        assembled_str += "    return {\n"
        for node in terminating_nodes:
            if node.has_outputs():
                for output in node.list_disconnected_outputs():
                    assembled_str += "        \"%s\": %s,\n" % (output.code_name(), output.code_name())
        assembled_str += "    }\n"
        assembled_str += "\n"

        # Run execution function, using sys.args when run as main
        assembled_str += "if __name__ == \"__main__\":\n"
        n = 0
        for node in all_nodes:
            n_for_node = node.count_number_of_inputs_needing_value()
            n += n_for_node

        assembled_str += "    if len(sys.argv) != %d:\n" % (n + 1)

        inputs_str = ""
        for node in all_nodes:
            for input_arg in node.list_inputs_needing_value():
                inputs_str += "               %s,\\n\\\n" % input_arg.code_name()
        assembled_str += "        print(\"Error: not enough inputs given, needed:\\n\\\n%s\")\n" % inputs_str[:-2]
        assembled_str += "        raise ValueError(\"Failed to parse arguments\")\n"

        argument_string = ""
        ix = 1
        for node in all_nodes:
            for input_arg in node.list_inputs_needing_value():
                argument_string += ("sys.argv[%d], " % ix)
                ix += 1
        assembled_str += "    execute(%s)" % argument_string[:-2] # [:-2] to trim last comma.
        assembled_str += "\n"

        return assembled_str
