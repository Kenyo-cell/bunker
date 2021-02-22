import kivy
from kivy.app import App

from kivy.config import Config
Config.set('graphics','resizable',0)
from kivy.core.window import Window
from kivy.lang import Builder

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from random import randint
import os



global INFO
global WORLD
global w
global color
INFO = dict()
WORLD = dict()
color = [.9, .83, .67, 1]
w = Window



sex = ["мужчина", "женщина"]

INFO["пол и возраст"] = sex[randint(0, 1)] + ", " + str(randint(0, 100)) + " лет\n"

directory = os.getcwd()

files = ["профессия", "состояние здоровья", "человеческая черта", "хобби", "доп информация",
         "багаж", "фобия", "карта 1", "карта 2"]

scenes = ["катастрофа", "событие"]


def start():
    for state in files:
        f = open(directory + "\\info\\" + state + ".txt", "r")
        states = []
        for line in f:
            states.append(line)
        INFO[state] = states

    for state in scenes:
        f = open(directory + "\\info\\" + state + ".txt", "r", encoding="utf-8", errors="ignore")
        states = []
        for line in f:
            states.append(line)
        WORLD[state] = states

WINDOW_WIDTH = 300
BLOCK_SIZE = 40

class TestApp(App):
        title="Bunker"
        players = []

        def build(self):
                self.main_bl = BoxLayout(orientation="vertical")

                self.head_bar()

                self.box = BoxLayout(orientation="vertical")
                self.main_bl.add_widget(self.box)

                self.add_player(1)

                return self.main_bl

        def head_bar(self):
                self.head_grid = GridLayout(cols=3, rows=2)

                self.add_btn = Button(text="add", on_press=self.add,
                background_color=[0, 1, 0, 1], size_hint=(0.5, 1))
                self.generate_bio = Button(text="generate bio", on_press=self.bio,
                background_color=color)
                self.generate_event = Button(text="create event", on_press=self.event,
                background_color=color)
        
                self.head_grid.add_widget(self.generate_bio)
                self.head_grid.add_widget(self.generate_event)
                self.head_grid.add_widget(self.add_btn)
                self.head_grid.add_widget(Widget(size_hint=(1, .2)))

                self.main_bl.add_widget(self.head_grid)

        def add(self, inst):
                self.add_player(len(self.players) + 1)

        def add_player(self, num):
                p = PlayerString(self, num)
                w.size = (WINDOW_WIDTH, BLOCK_SIZE * (num + 1))
                self.head_grid.size_hint = (1, 1/num)
                self.players.append(p)
                self.box.add_widget(p.add_string())

        def bio(self, inst):
                for player in self.players:
                        f = open(directory + "\\player scripts\\" + player.get_name() + ".txt", "w")
                        for state in INFO:
                                if state != "пол и возраст":
                                        f.write(state + ": " + INFO[state][randint(0, len(INFO[state]) - 1)])
                                else:
                                        f.write(state + ": " + sex[randint(0, 1)] + ", " + str(randint(8, 70)) + " лет\n")
                state = "катастрофа"
                f = open(directory + "\\player scripts\\" + state + ".txt", "w", errors="ignore")
                f.write(WORLD[state][randint(0, len(WORLD[state]) - 1)])

        def event(self, inst):
                state = "событие"
                f = open(directory + "\\event scripts\\" + state + ".txt", "w")
                f.write(WORLD[state][randint(0, len(WORLD[state]) - 1)])
        
class PlayerString(GridLayout):
        string_hint = (1.5, 1)
        def __init__(self, root,  num):
                self.root = root
                
                self.player_name = "Player" + str(num)

                self.box = BoxLayout()

                
                self.lbl = PlayerLabel(self.player_name, size_hint=self.string_hint)
                self.box.add_widget(self.lbl)

                self.change_btn = Button(text="change name", on_press=self.change_name,
                background_color=color)
                self.delete_btn = Button(text="delete", on_press=self.remove_player, 
                background_color=[1, 0, 0, 1], size_hint=(0.62, 1))

                self.box.add_widget(self.change_btn)
                self.box.add_widget(self.delete_btn)

        def get_name(self):
                return self.lbl.get_player_name()
        
        def add_string(self):
                return self.box

        def remove_player(self, inst):
                self.root.box.remove_widget(self.box)
                self.root.players.remove(self)
                num = len(self.root.players)
                
                if num != 0:
                        w.size = (WINDOW_WIDTH, BLOCK_SIZE * (num+1))
                        self.root.head_grid.size_hint = (1, 1/num)

        def change_name(self, inst):
                self.lbl.change()

class PlayerLabel(BoxLayout):
        player_name = None

        def __init__(self, player_name, *args, **kwargs):
                super(PlayerLabel, self).__init__(*args, **kwargs)
                self.player_name = player_name
                self.lbl = Label(text=self.player_name)
                self.add_widget(self.lbl)

        def on_touch_down(self, touch):
                if touch.is_double_tap and self.collide_point(touch.x, touch.y):

                        self.remove_widget(self.lbl)
                        self.lbl = TextInput(text=self.player_name, multiline=False,
                                             halign='center', padding_y=BLOCK_SIZE/4,
                                             background_color=[0, 0, 0, 1],
                                             foreground_color=[.7, .7, 1, 1])


                        self.add_widget(self.lbl)
                        
                return super(PlayerLabel, self).on_touch_down(touch)
        
        def change(self):
                self.player_name = self.lbl.text

                self.remove_widget(self.lbl)
                self.lbl = Label(text=self.player_name)

                self.add_widget(self.lbl)

        def get_player_name(self):
                return self.player_name

if __name__ == '__main__':
        start()
        TestApp().run()
