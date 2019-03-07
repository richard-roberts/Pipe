from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty

from . import edges


class EdgeWidget(FloatLayout):

    from_x = NumericProperty()
    from_y = NumericProperty()
    to_x = NumericProperty()
    to_y = NumericProperty()

    def __init__(self, **kwargs):
        super(EdgeWidget, self).__init__(**kwargs)
        self.edge = None
        self.widget_from = None
        self.widget_to = None

    def update_position(self):
        self.from_x = self.widget_from.x + self.widget_from.width
        self.from_y = self.widget_from.y + self.widget_from.height / 2
        self.to_x = self.widget_to.x
        self.to_y = self.widget_to.y + self.widget_to.height / 2

    def setup(self, edge, widget_from, widget_to):
        self.edge = edge
        self.widget_from = widget_from
        self.widget_to = widget_to
        self.update_position()
