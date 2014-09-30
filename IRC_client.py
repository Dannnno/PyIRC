import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.widget import Widget



class IRC_Widget(Widget): pass


class IRC_Client(App): 
    
    def build(self):
        big_layout = BoxLayout(orientation="vertical")
        filebar = BoxLayout(orientation="horizontal")
        filebar.size_hint = (1, 0.1)
        filebutton = Button(text="File")
        setbutton = Button(text="Settings")
        helpbutton = Button(text="Help")
        filebar.add_widget(filebutton)
        filebar.add_widget(setbutton)
        filebar.add_widget(helpbutton)
        sidebar = Label(text="This will be where you can pick from your servers and channels")
        sidebar.size_hint = (.3, 1)
        body = BoxLayout(orientation="horizontal")
        chat_area = BoxLayout(orientation="vertical")
        users = Label(text="This will be where you see the users!")
        users.size_hint = (.3, 1)
        chat = Label(text="This is where you see messages")
        chat.size_hint = (1, .9)
        entry = Label(text="This is where you type")
        entry.size_hint = (1, .1)
        chat_area.add_widget(chat)
        chat_area.add_widget(entry)
        body.add_widget(sidebar)
        body.add_widget(chat_area)
        body.add_widget(users)
        big_layout.add_widget(filebar)
        big_layout.add_widget(body)
        return big_layout
        
if __name__ == "__main__":
    IRC_Client().run()