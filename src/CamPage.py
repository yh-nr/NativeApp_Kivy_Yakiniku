"""CamPage.pyはカメラ機能のページの処理を記述しています。"""

from os.path import dirname, join
from kivy.uix.image import Image
from kivy.uix.widget import Widget 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior

from .func import show_toast, internal_savefile_location
from .predict import predict
from camera4kivy import Preview

from PIL import Image as PILImage

import datetime

# lastpic_path = 'あいうえお'

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
            self.connect_camera(enable_analyze_pixels = True, enable_video = False, filepath_callback = self.show_toast2)
        else:
            show_toast('カメラを切断します')
            self.disconnect_camera()

    def show_toast2(self, message):
        if message.endswith("temp.jpg"):
            show_toast('保存した写真で推論を実行するよ！')
            pred, animalNameProba_ = predict(message)
            show_toast('しおり３')
            animalName_ = self.getName(pred)
            show_toast(str(animalName_) + str(animalNameProba_))
        else:
            show_toast('写真を保存しただけだよ！')
        return message

    def capture_button(self,subdir1,subdir2):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)

        #windowsの場合に、subdir1が存在するかチェックするコードをここに入れる       

        subdir = subdir1 + '/' + subdir2
        name = f'img{now:%y%m%d%H%M%S%f}'[:-3]
        self.capture_photo(subdir=subdir ,name=name)
        pass
    

    def predict_button(self,subdir1,subdir2):
        subdir = subdir1 + '/' + subdir2
        name = 'temp'
        self.capture_photo(subdir=subdir ,name=name)
        pred, animalNameProba_ = predict('temp.jpg')
        animalName_ = self.getName(pred)
        show_toast(str(animalName_) + str(animalNameProba_))

    #　推論したラベルから犬か猫かを返す関数
    def getName(self, label):
        if label==0: return '猫'
        elif label==1: return '犬'

    #　推論したラベルから犬か猫かを返す関数
    def test_button(self):
        show_toast(internal_savefile_location())
        self.capture_photo(location='private', subdir='temp', name='temp')

# 撮影ボタン
class ImageButton(ButtonBehavior, Image):
    pass
