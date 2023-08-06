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


from .func import show_toast, load_setting
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
        settings = load_setting()
        return f"[{settings[instance.custom_id]['num']}]\n{settings[instance.custom_id]['name']}"
 
    def play(self):
        if self.camera_connected == False:
            show_toast('カメラへの接続を試みます')
            self.connect_camera(enable_analyze_pixels = True, enable_video = False, filepath_callback = self.show_toast2)
        else:
            show_toast('カメラを切断します')
            self.disconnect_camera()

    def show_toast2(self, message):
        if message.endswith("temp.jpg"):
            # show_toast('保存した写真で推論を実行するよ！')
            pred, animalNameProba_ = predict(message)
            # show_toast('しおり３')
            animalName_ = self.getName(pred)
            show_toast(str(animalName_) + str(animalNameProba_))
            self.res_predict.text = str(animalName_) + str(animalNameProba_)
        else:
            show_toast('写真を保存しただけだよ！')
        return message

    def capture_button(self,instance):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)

        #windowsの場合に、subdir1が存在するかチェックするコードをここに入れる      
         
        settings = load_setting()
        subdir1 = settings['theme']
        subdir2 = str(settings[instance.custom_id]['num'])

        subdir = subdir1 + '/' + subdir2
        name = f'img{now:%y%m%d%H%M%S%f}'[:-3]
        self.capture_photo(subdir=subdir ,name=name)
        pass