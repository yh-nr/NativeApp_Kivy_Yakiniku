#kivy関連import
from kivy.app import App            
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivy.config import Config
# Config.set('graphics', 'width', '480')
# Config.set('graphics', 'height', '960')
Config.set('kivy', 'log_level', 'debug')

import japanize_kivy
from os.path import dirname, join

from src.Page1 import ImageWidget
from src.Page2 import CameraClick
from src.Page3 import CameraPreview, ImageButton
from src.func import show_toast


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


class AppFrame(BoxLayout):
    screen_manager = ObjectProperty(None)
    
    def switch2page(self, page_name):
        sm = self.screen_manager
        curdir = dirname(__file__)
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


