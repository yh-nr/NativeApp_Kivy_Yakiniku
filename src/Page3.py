from kivy.uix.image import Image
from kivy.uix.widget import Widget 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from os.path import dirname, join

from .func import SavePic, show_toast
from camera4kivy import Preview





class CameraPreview(Preview):
    image_texture = ObjectProperty(None)
    image_capture = ObjectProperty(None)
    camera = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)
        pass
 
    def play(self):
        global Flg
        Flg = not Flg
        show_toast(f'{Flg}だよう')

        # if Flg == True:
        #     self.connect_camera(enable_analyze_pixels = True, enable_video = False)


        # else:self.disconnect_camera()


        


# 撮影ボタン
class ImageButton(ButtonBehavior, Image):
    pass


Flg = False
print(f'{Flg}だよう')