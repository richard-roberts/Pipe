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

        def assemble(node, argument):
            suffix = ("" if argument is None else ".%s" % argument.name)

            if node.template.is_root():
                return "%s()%s" % (node.template.function_name, suffix)
            else:

                # Build the argument sting (recursively compiling the execution of those arguments)
                argument_str = ""
                for input_arg in node.inputs.values():
                    edge = graph.get_edge_by_argument_to(node, input_arg)
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

        # Imports
        for name in globals.TemplateInfo().manager.get_collection_names():
            assembled_str += "from templates.%s import *\n" % name
        assembled_str += "\n"

        # Execution function
        assembled_str += "def execute():\n"
        leaves = [node for node in graph.nodes.values() if node.template.is_leaf()]
        for leaf in leaves:
            assembled_str += "    " + assemble(leaf, None) + "\n"
        assembled_str += "\n"

        # Execution call
        assembled_str += "if __name__ == \"__main__\":\n"
        assembled_str += "    execute()"

        return assembled_str
