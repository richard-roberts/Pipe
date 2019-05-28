class BasicArgument:

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_value(self):
        return None

    def as_json(self):
        return {
            "name": self.name
        }


def from_json(data):
    return BasicArgument(data["name"])
