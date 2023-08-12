#kivy関連import
from kivy.app import App            
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager

from kivy.config import Config
# Config.set('graphics', 'width', '480')
# Config.set('graphics', 'height', '960')
Config.set('kivy', 'log_level', 'debug')

import japanize_kivy
from os.path import dirname, join

from src.HomePage import ImageWidget
from src.Cam2annotate import CameraPreview
from src.DogCatCam import CameraPreview2
from src.func import show_toast, internal_savefile_location, external_savefile_location


# カメラへのアクセス許可を要求する
try:
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.CAMERA,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE
        ])
except:
    print('ここは毎回実行されてる？？？(permissionのexcept)')
    pass


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        curdir = dirname(__file__)
        screen = Builder.load_file(join(curdir, f'src/HomePage.kv'))
        self.switch_to(screen, direction='left')

class AppFrame(BoxLayout):
    screen_manager = ObjectProperty(None)
    
    def switch2page(self, page_name):
        sm = self.screen_manager
        curdir = dirname(__file__)
        Builder.unload_file(join(curdir, f'src/{page_name}.kv'))
        screen = Builder.load_file(join(curdir, f'src/{page_name}.kv'))
        sm.switch_to(screen, direction='left')


class YakinikuApp(App):
    def __init__(self, **kwargs):
        super(YakinikuApp, self).__init__(**kwargs)
        self.title = '焼き肉アプリ'

    def build(self):
        show_toast('Appをビルドしました！')
        return AppFrame()


if __name__ == '__main__':                      #main.pyが直接実行されたら、、、という意味らしい
    YakinikuApp().run()                         #
    


