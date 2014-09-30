import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.widget import Widget


class IRC_Widget(Widget): pass

class Chat_Window(TabbedPanel): pass

class Channel(TabbedPanelItem): pass

class User_List(Label): pass

class Text_Entry(BoxLayout): pass

class Menu_Bar(BoxLayout): pass

class IRC_ClientApp(App): 
    
    def build(self):
        return IRC_Widget()
                
if __name__ == "__main__":
    IRC_ClientApp().run()