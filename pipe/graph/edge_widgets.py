from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ObjectProperty


class EdgeWidget(FloatLayout):

    widget_from = ObjectProperty()
    widget_to = ObjectProperty()
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
        self.canvas.ask_update()

    def disconnect(self):
        self.widget_from.disconnect()
        self.widget_to.disconnect()

    def setup(self, edge, widget_from, widget_to):
        self.edge = edge
        self.widget_from = widget_from
        self.widget_to = widget_to
        self.widget_from.connect(self)
        self.widget_to.connect(self)
        self.update_position()
