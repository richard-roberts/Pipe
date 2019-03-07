class TemplateInfo:
    __shared_state = {
        "manager": None
    }

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.manager = self.__shared_state["manager"]

    def set_manager(self, manager):
        self.__shared_state["manager"] = manager


class GraphInfo:
    __shared_state = {
        "manager": None
    }

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.manager = self.__shared_state["manager"]

    def set_manager(self, manager):
        self.__shared_state["manager"] = manager
