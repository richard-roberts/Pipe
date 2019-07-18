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
            "type": "basic",
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

    def list_outputs(self):
        return [out.get_name() for out in self.outs]

    def execute(self, arguments, node_id):
        arg_data = []
        for arg in self.args:
            value = arguments[arg.name]
            arg_data.append(value)
        
        n_arg_data = len(arg_data)
        n_args = len(self.args)
        if n_arg_data != n_args:
            raise ValueError("required %d arguments, but %d were given." % (n_arg_data, n_args))

        result = self.routine.execute(arg_data, node_id)

        values = [v.strip() for v in result.split("\n") if v.strip() != ""]
        outputs = {}
        for (out, value) in zip(self.outs, values):
            outputs[out.name] = value
        return outputs

class FileTemplate:

    def __init__(self, filepath):
        self.filepath = filepath
        self.args = []
        self.outs = [outputs.BasicOutput("filepath")]
        self.execute({})

    def __str__(self):
        return f"FileTemplate[{self.filepath}]"

    def as_json(self):
        return {
            "type": "file",
            "args": [a.as_json() for a in self.args],
            "outs": [o.as_json() for o in self.outs],
            "filepath": self.filepath
        }

    def list_arguments(self):
        return [arg.get_name() for arg in self.args]

    def list_outputs(self):
        return [out.get_name() for out in self.outs]

    def execute(self, arguments):
        outputs = {
            "filepath": self.filepath
        }
        return outputs

def from_json(data):
    if data["type"] == "basic":
        return BasicTemplate(
            [arguments.from_json(datum) for datum in data["args"]],
            [outputs.from_json(datum) for datum in data["outs"]],
            routines.from_json(data["routine"])
        )
    elif data["type"] == "file":
        return FileTemplate(data["filepath"])
    else:
        raise ValueError(f"{data['type']} is not a valid template type")

def from_data(args, outs, extension, code):
    return BasicTemplate(
        [arguments.from_json({"name": a}) for a in args],
        [outputs.from_json({"name": o}) for o in outs],
        routines.from_extension_and_code(extension, code)
    )
