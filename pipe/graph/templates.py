from pipe.graph import arguments
from pipe.graph import outputs
from pipe.graph import routines


class BasicTemplate:

    def __init__(self, args, outs, routine):
        self.args = args
        self.outs = outs
        self.routine = routine

    def __str__(self):
        return "(%s)->{%s}" % (
            ", ".join([a.get_name() for a in self.args]),
            ",".join([o.get_name() for o in self.outs])
        )

    def as_json(self):
        return {
            "args": [a.as_json() for a in self.args],
            "outs": [o.as_json() for o in self.outs],
            "routine": self.routine.as_json()
        }

    def get_code(self):
        return self.routine.code

    def get_code_with_line_numbers(self):
        code = ""
        for ix, line in enumerate(self.get_code().split("\n")):
            code += "%02d. %s\n" % (ix, line)
        return code

    def list_arguments(self):
        return [arg.get_name() for arg in self.args]

    def execute(self, arguments):
        arg_data = []
        for arg in self.args:
            value = arguments[arg.name]
            arg_data.append(value)
        
        n_arg_data = len(arg_data)
        n_args = len(self.args)
        if n_arg_data != n_args:
            raise ValueError("required %d arguments, but %d were given." % (n_arg_data, n_args))

        result = self.routine.execute(arg_data)

        values = [v.strip() for v in result.split("\n") if v.strip() != ""]
        outputs = {}
        for (out, value) in zip(self.outs, values):
            outputs[out.name] = value
        return outputs

def from_json(data):
    return BasicTemplate(
        [arguments.from_json(datum) for datum in data["args"]],
        [outputs.from_json(datum) for datum in data["outs"]],
        routines.from_json(data["routine"])
    )

def from_data(args, outs, extension, code):
    return BasicTemplate(
        [arguments.from_json({"name": a}) for a in args],
        [outputs.from_json({"name": o}) for o in outs],
        routines.from_extension_and_code(extension, code)
    )
