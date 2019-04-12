class BasicOutput:

    def __init__(self, name):
        self.name = name
        self.value = None

    def __str__(self):
        return "%s=%s" % (self.name, self.value)

    def get_name(self):
        return self.name


def from_json(data):
    return BasicOutput(data["name"])
