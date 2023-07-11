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
        if self.camera_connected == False:
            show_toast('カメラへの接続を試みます')
            self.connect_camera(enable_analyze_pixels = True, enable_video = False, filepath_callback = show_toast)
        else:
            show_toast('カメラを切断します')
            self.disconnect_camera()

    def capture_button(self,subdir1,subdir2):
        subdir = subdir1 + '/' + subdir2
        name = 'img'
        self.capture_photo(subdir=subdir ,name=name)
        pass
    
    def show_toast2(self, message):
        show_toast(message)



# 撮影ボタン
class ImageButton(ButtonBehavior, Image):
    pass
