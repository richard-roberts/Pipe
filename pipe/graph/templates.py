from pipe.graph import arguments
from pipe.graph import outputs
from pipe.graph import routines


class BasicTemplate:

    def __init__(self, name, args, outs, routine):
        self.name = name
        self.args = args
        self.outs = outs
        self.routine = routine

    def __str__(self):
        return "%s(%s)->{%s}" % (
            self.name.replace(" ", ""),
            ", ".join([a.get_name() for a in self.args]),
            ",".join([o.get_name() for o in self.outs])
        )

    def get_name(self):
        return self.name

    def list_arguments(self):
        return [arg.get_name() for arg in self.args]

    def execute_to_get_log_and_results(self, argument_data=None):
        log, error = self.routine.execute_and_get_standard_output_and_error(
            self.args,
            self.outs,
            argument_data=argument_data
        )

        if error:
            error_message = "\n  %s's execution failed:\n" % str(self)
            for line in error.decode().split("\n"):
                error_message += "    %s\n" % line
            code = self.routine.generate_code(self.args, self.outs, argument_data=argument_data)
            for item in enumerate(code.split("\n")):
                ix, line = item
                error_message += "        %02d. %s\n" % (ix + 1, line)
            raise ValueError(error_message)

        return log.decode(), self.routine.read_results_file()


def from_json(data):
    return BasicTemplate(
        data["name"],
        [arguments.from_json(datum) for datum in data["args"]],
        [outputs.from_json(datum) for datum in data["outs"]],
        routines.from_json(data["code"])
    )
