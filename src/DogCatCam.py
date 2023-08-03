"""CamPage.pyはカメラ機能のページの処理を記述しています。"""

import re, datetime

from kivy.properties import ObjectProperty, StringProperty
from kivy.utils import platform
from kivy.clock import Clock
from camera4kivy import Preview
try: from jnius import autoclass
except:pass

from .func import show_toast
from .predict import predict

class CameraPreview2(Preview):
    image_texture = ObjectProperty(None)
    image_capture = ObjectProperty(None)
    camera = ObjectProperty(None)
    res_predict = ObjectProperty(None)
    res_predict_img = ObjectProperty(None)
    res_predict_str = StringProperty('SPテスト')


    def __init__(self, **kwargs):
        super(CameraPreview2, self).__init__(**kwargs)
        pass
 
    def play(self):
        if self.camera_connected == False:
            # show_toast('カメラへの接続を試みます')
            self.connect_camera(enable_analyze_pixels = True, enable_video = False, filepath_callback = self.show_toast2)
        else:
            # show_toast('カメラを切断します')
            self.disconnect_camera()

    # capture_photoのコールバック関数
    # このページの機能は推論だけになったので、if分岐は要らないかも
    def show_toast2(self, message):
        if re.match(r'.*temp\d{15}\.jpg$', message):
            pred, animalNameProba_, texture = predict(message)
            self.imagedisplay(texture)
            show_toast(str(pred) + str(animalNameProba_))
            self.res_predict_str = str(pred) + str(animalNameProba_)
        else:
            show_toast('写真を保存しただけだよ！')
        return message
    

    def predict_button(self):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)

        self.capture_photo(location='private', subdir='temp', name=f'temp{now:%y%m%d%H%M%S%f}'[:-3])


        
    def imagedisplay(self, texture):
        pre_res = self.res_predict
        pre_res_img = self.res_predict_img
        pre_res_img.texture = texture
        # pre_res.opacity = 1