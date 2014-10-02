import kivy
kivy.require('1.7.0')

from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.event import EventDispatcher



class DataModel(EventDispatcher):
    a = StringProperty('')
    b = StringProperty('')
    c = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(DataModel, self).__init__(*args, **kwargs)
        self.a = 'This is a'
        self.b ='This is b'
        self.bind(a=self.set_c)
        self.bind(b=self.set_c)

    def set_c(self, instance, value):
        self.c = self.a + ' and ' + self.b    

class RootWidget(StackLayout):
    data_model = ObjectProperty(DataModel())

    def button_press(self, *args):
        self.data_model.a = 'This is a and it is really long now'
        print self.data_model.c

    def button_press2(self, *args):
        self.data_model.b = 'B'
        print self.data_model.c

class TestApp(App):
    def build(self):
        return RootWidget()

app = TestApp()
app.run()