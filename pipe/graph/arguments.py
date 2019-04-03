class BasicArgument:

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_value(self):
        return None


class DefaultArgument:

    def __init__(self, name, default_value):
        self.name = name
        self.default_value = default_value

    def get_name(self):
        return self.name

    def get_default_value(self):
        return self.default_value

    def get_value(self):
        return self.default_value


def from_json(data):
    return BasicArgument(data["name"])
