from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

import config


class EdgeWidget(FloatLayout):
    node = ObjectProperty(None, allownone=True)
    edge_color = ObjectProperty()
    widget_from = ObjectProperty()
    widget_to = ObjectProperty()

    def __init__(self, edge, widget_from, widget_to, **kwargs):
        self.edge_color = config.Colors.Edge
        self.edge = edge
        self.widget_from = widget_from
        self.widget_to = widget_to
        self.widget_from.connect(self)
        self.widget_to.connect(self)
        super(EdgeWidget, self).__init__(**kwargs)

    def pretty(self):
        return "Edge<%s-%s>" % (self.widget_from.pretty(), self.widget_to.pretty())

    def redraw(self):
        pass

    def disconnect(self):
        self.widget_from.disconnect()
        self.widget_to.disconnect()

