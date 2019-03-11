class Argument:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.edge = None

    def get_node(self):
        return self.node

    def disconnect(self):
        self.edge = None

    def connect(self, edge):
        self.edge = edge

    def is_connected(self):
        return self.edge is not None

    def get_connected(self):
        return self.edge
