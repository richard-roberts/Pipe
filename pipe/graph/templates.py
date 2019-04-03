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

    def execute(self, argument_data=None):
        self.routine.execute_and_get_standard_output_and_error(
            self.args,
            self.outs,
            argument_data=argument_data
        )
        return self.routine.read_results_file()


def from_json(data):
    return BasicTemplate(
        data["name"],
        [arguments.from_json(datum) for datum in data["args"]],
        [outputs.from_json(datum) for datum in data["outs"]],
        routines.from_json(data["code"])
    )
