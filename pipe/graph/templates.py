class BasicTemplate:

    def __init__(self, name, arguments, outputs, routine):
        self.name = name
        self.arguments = arguments
        self.outputs = outputs
        self.routine = routine

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def list_arguments(self):
        return [arg.get_name() for arg in self.arguments]

    def execute(self, argument_data=None):
        self.routine.execute_and_get_standard_output_and_error(
            self.arguments,
            self.outputs,
            argument_data=argument_data
        )
        return self.routine.read_results_file()
