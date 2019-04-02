import json

import config


class TemplateArg(object):

    def __init__(self, name):
        self.name = name


class InputTemplateArg(TemplateArg):

    def __init__(self, name, default=None):
        super(InputTemplateArg, self).__init__(name)
        self._default = default

    def set_default(self, default):
        self._default = default

    def get_default(self):
        return self._default

    def as_json(self):
        return {
            "name": self.name,
            "default": self._default
        }

    @staticmethod
    def from_json(datum):
        return InputTemplateArg(
            datum["name"],
            default=datum["default"]
        )

    def has_default(self):
        return not (self._default is None)


class OutputTemplateArg(TemplateArg):

    def as_json(self):
        return {
            "name": self.name
        }

    @staticmethod
    def from_json(datum):
        return OutputTemplateArg(
            datum["name"]
        )

    def has_default(self):
        return False


class Template(object):

    def __init__(self):
        self.collection_name = ""
        self.name = ""
        self.function_name = ""
        self.inputs = {}
        self.outputs = {}
        self.documentation = ""
        self.code = ""

    def setup(self, collection_name, name, inputs, outputs):
        self.collection_name = collection_name
        self.name = name
        self.function_name = name.replace(" ", "_")
        self.inputs = {}
        for i in inputs:
            a = InputTemplateArg(i)
            self.inputs[a.name] = a
        self.outputs = {}
        for o in outputs:
            a = OutputTemplateArg(o)
            self.outputs[a.name] = a
        self.documentation = config.Defaults.Template.new_template_documentation(name)
        self.code = config.Defaults.Template.new_template_code(self.function_name, inputs, outputs)

    def __str__(self):
        return "Template[%s::%s]" % (self.collection_name, self.name)

    def as_json(self):
        return {
            "collection_name": self.collection_name,
            "name": self.name,
            "inputs": [i.as_json() for i in self.inputs.values()],
            "outputs": [o.as_json() for o in self.outputs.values()],
            "code": self.code,
            "documentation": self.documentation
        }

    def from_json(self, data):
        self.collection_name = data["collection_name"]
        self.name = data["name"]
        self.function_name = self.name.replace(" ", "_")
        for d in data["inputs"]:
            a = InputTemplateArg.from_json(d)
            self.inputs[a.name] = a
        for d in data["outputs"]:
            a = OutputTemplateArg.from_json(d)
            self.outputs[a.name] = a
        self.documentation = data["documentation"]
        self.code = data["code"]

    def is_root(self):
        return len(self.inputs) == 0

    def is_leaf(self):
        return len(self.outputs) == 0

    def input_string(self):
        input_str = "("
        for i in self.inputs.values():
            input_str += "%s=%s," % (i.name, i.name)
        input_str = input_str[:-1] + "}\n"
        return input_str

    def output_string(self):
        output_str = "{"
        for o in self.outputs.values():
            output_str += "\"%s\" = %s," % (o.name, o.name)
        output_str = output_str[:-1] + "}\n"
        return output_str

    def get_long_name(self):
        return "%s::%s" % (self.collection_name, self.name)

    def get_arg_by_name(self, name):
        if name in self.inputs.keys():
            return self.inputs[name]
        elif name in self.outputs.keys():
            return self.outputs[name]
        else:
            raise IndexError("%s is not an argument of %s" % (name, self))


class GraphTemplate(Template):

    def setup(self, collection_name, name, inputs, outputs):
        inputs_names = [i.code_name() for i in inputs]
        outputs_names = [o.code_name() for o in outputs]
        super(GraphTemplate, self).setup(collection_name, name, inputs_names, outputs_names)
        self.code = config.Defaults.Template.graph_execution_template_code(self.function_name, inputs, outputs)
