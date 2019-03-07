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
                def compile_execution(node, argument):
                    suffix = ("" if argument is None else ".%s" % argument.get_argument_name())

                    if node.is_root():
                        return "%s()%s" % (node.function_name, suffix)
                    else:

                        # Build the argument sting (recursively compiling the execution of those arguments)
                        argument_str = ""
                        for input_arg in node.input_set.args:
                            edge = edge_editor.get_input_edge_by_argument(input_arg)
                            connected_output_arg = edge.get_output_argument()
                            child_node = node_editor.nodes[connected_output_arg.get_node_name()]
                            compiled_child = compile_execution(child_node, connected_output_arg)
                            argument_str += compiled_child + ", "
                        argument_str = argument_str[:-2]

                        # Compile the invocation
                        return "%s(%s)%s" % (
                            node.function_name,
                            argument_str,
                            suffix
                        )

                execution_str = "if __name__ == \"__main__\":\n"
                leaves = [node for node in node_editor.nodes.values() if node.is_leaf()]
                for leaf in leaves:
                    execution_str += "    " + compile_execution(leaf, None) + "\n"
                return execution_str

            if len(node_editor.nodes) == 0:
                return header()
            elif len(node_editor.nodes) < 2:
                return header() + functions()
            else:
                return header() + functions() + execution()
