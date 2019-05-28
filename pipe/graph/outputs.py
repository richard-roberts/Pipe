class BasicOutput:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "%s" % (self.name)

    def get_name(self):
        return self.name

    def as_json(self):
        return {
            "name": self.name
        }


def from_json(data):
    return BasicOutput(data["name"])
