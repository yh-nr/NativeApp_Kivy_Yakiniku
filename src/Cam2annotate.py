"""CamPage.pyはカメラ機能のページの処理を記述しています。"""

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.clock import Clock

from .func import show_toast
from src import config_manager
from camera4kivy import Preview


import datetime

# lastpic_path = 'あいうえお'

class ATButton(Button):
    custom_id = StringProperty('')

class CameraPreview(Preview):
    image_texture = ObjectProperty(None)
    image_capture = ObjectProperty(None)
    camera = ObjectProperty(None)
    btn_name = ListProperty(['btn0','btn1','btn2','btn3','btn4','btn5','btn6','btn7','btn8','btn9','btn10','btn11'])
    

    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)
        for n in range(len(self.btn_name)):
            self.btn_name[n] = '['+str(config_manager.settings[f'btn{n}']['num'])+']\n'+config_manager.settings[f'btn{n}']['name']
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


    def update_setting(self, btn, num, name):
        config_manager.update_setting(btn, num, name)
        self.update_button_name()

    def load_button(self):
        setting = config_manager.load_config_from_file(r'./assets/config.json')
        config_manager.save_config_to_file('config.json', setting)
        self.update_button_name()
    
    def update_button_name(self):
            for n in range(len(self.btn_name)):
                self.btn_name[n] = '['+str(config_manager.settings[f'btn{n}']['num'])+']\n'+config_manager.settings[f'btn{n}']['name']

    def change_button_text(self, value):
        print('test')
        pass

    def popup_open(self):
        content = PopupMenu(popup_close=self.popup_close)
        self.popup = Popup(title='Popup Test', content=content, size_hint=(0.5, 0.5), auto_dismiss=False)
        self.popup.open()

    def popup_close(self):
        self.popup.dismiss()

class PopupMenu(BoxLayout):
    popup_close = ObjectProperty(None)
