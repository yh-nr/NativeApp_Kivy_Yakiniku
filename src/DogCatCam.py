"""CamPage.pyはカメラ機能のページの処理を記述しています。"""

from os.path import dirname, join
import re
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from .func import show_toast, internal_savefile_location, get_data_dir
from .predict import predict
from camera4kivy import Preview

from PIL import Image as PILImage
from kivy.clock import Clock

import datetime

# lastpic_path = 'あいうえお'

class CameraPreview2(Preview):
    image_texture = ObjectProperty(None)
    image_capture = ObjectProperty(None)
    camera = ObjectProperty(None)
    res_predict = ObjectProperty(None)
    res_predict_img = StringProperty('.\\temp\\temp230729164946678.jpg')
    res_predict_str = StringProperty('SPテスト')


    def __init__(self, **kwargs):
        super(CameraPreview2, self).__init__(**kwargs)
        pass
 
    def play(self):
        if self.camera_connected == False:
            show_toast('カメラへの接続を試みます')
            self.connect_camera(enable_analyze_pixels = True, enable_video = False, filepath_callback = self.show_toast2)
        else:
            show_toast('カメラを切断します')
            self.disconnect_camera()

    # capture_photoのコールバック関数
    def show_toast2(self, message):
        # if message.endswith("temp*.jpg"):
        if re.match(r'.*temp\d{15}\.jpg$', message):
            # show_toast('保存した写真で推論を実行するよ！')
            pred, animalNameProba_ = predict(message)
            # show_toast('しおり３')
            animalName_ = self.getName(pred)
            self.imagedisplay(message)
            show_toast(str(animalName_) + str(animalNameProba_))
            self.res_predict_str = str(animalName_) + str(animalNameProba_)
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
    

    def predict_button(self):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)

        self.capture_photo(location='private', subdir='temp', name=f'temp{now:%y%m%d%H%M%S%f}'[:-3])

    #　推論したラベルから犬か猫かを返す関数
    def getName(self, label):
        if label==0: return '猫'
        elif label==1: return '犬'

        
    def imagedisplay(self, source='.\\temp\\temp230729111042246.jpg'):
        pre_res = self.res_predict
        self.res_predict_img = source
        pre_res.disabled = False
        pre_res.opacity = 1
        # Clock.schedule_once(self.update_gui)
 

class PredictResultImage(Image):
    # def imagedisplay(self, source='.\\temp\\temp230729111042245.jpg'):
    #     self.disabled = False
    #     self.source = source
    #     self.opacity = 1
    pass