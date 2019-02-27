class Config:

    class Colors:

        class Node:
            generic_alpha = 0.2
            selected_alpha = 0.2

        class Edge:
            generic = [1.0, 1.0, 1.0]

    class Defaults:

        class Node:

            @staticmethod
            def code(function_name, n_inputs, n_outputs):
                input_vars = ["input%d" % i for i in range(n_inputs)]
                output_vars = ["output%d" % i for i in range(n_outputs)]

                header = "class %s:\n" % (function_name)
                
                body = ""
                body += "    def __init__(self%s%s):\n" % (("" if len(input_vars) == 0 else ", "), ", ".join(input_vars))
                if len(output_vars) == 0:
                    body += "        pass\n"
                else:
                    for output_var in output_vars:
                        body += "        self.%s = None\n" % output_var
                    
                return header + body

            @staticmethod
            def documentation(name):
                template = "A description of the %s node's behavior." 
                return template % name

