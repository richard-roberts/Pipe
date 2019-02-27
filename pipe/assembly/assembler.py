class Assembler:

    @staticmethod
    def assemble(node_editor, edge_editor):

            def header():
                header_str = ""
                header_str += "\n"
                return header_str
            
            def functions():
                function_str = ""
                for node in node_editor.nodes.values():
                    function_str += node.code + "\n"
                return function_str

            def execution():
                def compile_execution(node, index):
                    n = node.get_number_of_inputs()
                    if n == 0:
                        return "%s()%s" % (node.function_name, ("" if index == -1 else ".output%d" % index))
                    else:
                        argument_str = ""
                        for ix in range(n):
                            edge = edge_editor.get_input_edge_by_argument(node.get_input_arg(ix))
                            connected_argument = edge.get_output_argument()
                            child_node_name = connected_argument.get_node_name()
                            child_node_index = connected_argument.get_argument_index()
                            child_node = node_editor.nodes[child_node_name]
                            compiled_child = compile_execution(child_node, child_node_index)
                            argument_str += compiled_child + ", "
                        argument_str = argument_str[:-2]
                        return "%s(%s)%s" % (node.function_name, argument_str, ("" if index == -1 else ".output%d" % index))

                execution_str = "if __name__ == \"__main__\":\n"
                leaves = [node for node in node_editor.nodes.values() if node.is_leaf()]
                for leaf in leaves:
                    execution_str += "    " + compile_execution(leaf, -1) + "\n"
                return execution_str

            if len(node_editor.nodes) == 0:
                return header()
            elif len(node_editor.nodes) < 2:
                return header() + functions()
            else:
                return header() + functions() + execution()
