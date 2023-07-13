#kivy関連import
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from random import randint


class ImageWidget(Widget):
    source = StringProperty('./image/000001.jpg')
    
    def buttonStarted(self):
        self.source= './image/000001.jpg'

    def buttonRandom(self):
        self.source = f'./image/00000{randint(1, 9)}.jpg'

