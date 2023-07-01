from kivy.uix.image import Image
from kivy.uix.widget import Widget 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from os.path import dirname, join
import cv2

from .func import SavePic, show_toast

class CameraPreview(Widget):
    image_texture = ObjectProperty(None)
    image_capture = ObjectProperty(None)
    camera = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)
        # self.image_capture = cv2.VideoCapture(0)
        print("どうよどうよ！！！")
        # Clock.schedule_interval(self.update, 1.0 / 1)
        pass
 
    def play(self, camnum):
        global Flg
        Flg = not Flg
        print(Flg)
        if Flg == True:
            self.image_capture = cv2.VideoCapture(camnum)
            print(self.image_capture)
            Clock.schedule_interval(self.update, 1.0 / 30)
            show_toast(f'videocaptureがopenかどうか：{self.image_capture.isOpened()}')
        else:
            Clock.unschedule(self.update)
            self.image_capture.release()

    # インターバルで実行する描画メソッド
    def update(self, dt):
        # フレームを読み込み
        
        print('update関数は動いている')
        print(f'videocaptureがopenかどうか：{self.image_capture.isOpened()}')

        ret, frame = self.image_capture.read()
        if ret:
            buf = cv2.flip(frame, 0)
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
            image_texture.blit_buffer(buf.tostring(), colorfmt='bgr', bufferfmt='ubyte')
            # camera = self.ids.camera
            self.camera.texture = image_texture
            print('update動作確認2！！！')


    def camera_release(self):
        Clock.unschedule(self.update)
        try:self.image_capture.release()
        except:pass
        global Flg
        Flg = False
        


# 撮影ボタン
class ImageButton(ButtonBehavior, Image):
    pass
    # preview = ObjectProperty(None)

    # ボタンを押したときに実行
    # def on_press(self):
    #     # cv2.namedWindow("CV2 Image")
    #     # cv2.imshow("CV2 Image", self.preview.frame)
    #     # cv2.waitKey(0)
    #     # cv2.destroyAllWindows()
    #     CameraPreview.play()


Flg = False
print(f'{Flg}だよう')