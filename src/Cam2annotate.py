"""CamPage.pyはカメラ機能のページの処理を記述しています。"""

from os.path import dirname, join
from kivy.uix.image import Image
from kivy.uix.button import Button
# from kivy.uix.widget import Widget 
# from kivy.uix.boxlayout import BoxLayout
# from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior


from .func import show_toast
from src import config_manager
from .predict import predict
from camera4kivy import Preview

from PIL import Image as PILImage

import datetime

# lastpic_path = 'あいうえお'

class ATButton(Button):
    custom_id = StringProperty('')

class CameraPreview(Preview):
    image_texture = ObjectProperty(None)
    image_capture = ObjectProperty(None)
    camera = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)
        pass

    def get_button_text(self, instance):
        settings = config_manager.settings
        return f"[{settings[instance.custom_id]['num']}]\n{settings[instance.custom_id]['name']}"
 
    def play(self):
        if self.camera_connected == False:
            # show_toast('カメラへの接続を試みます')
            self.connect_camera(enable_analyze_pixels = True, enable_video = False)
        else:
            # show_toast('カメラを切断します')
            self.disconnect_camera()

    def capture_button(self,instance):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)

        #windowsの場合に、subdir1が存在するかチェックするコードをここに入れる      
         
        settings = config_manager.settings
        subdir1 = settings['theme']
        subdir2 = str(settings[instance.custom_id]['num'])

        subdir = subdir1 + '/' + subdir2
        name = f'img{now:%y%m%d%H%M%S%f}'[:-3]
        self.capture_photo(subdir=subdir ,name=name)
        pass

    def save_button(self):
        settings = config_manager.settings
        config_manager.save_config_to_file('savetest.json', settings)

    def update_button(self):
        config_manager.update_setting('btn4', 12, 'おけまる')

    def load_button(self):
        config_manager.load_config_from_file('savetest.json')