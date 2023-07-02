from kivy.utils import platform
from os.path import dirname, join
from plyer import notification


def SavePic(camera, timestr):
    if platform == 'android':
        from jnius import autoclass     
        # AndroidのJavaクラスにアクセス
        Environment = autoclass('android.os.Environment')
        # Build_VERSION = autoclass('android.os.Build$VERSION')
        # Context = autoclass('android.content.Context')
        # MediaStore = autoclass('android.provider.MediaStore')
        # ContentValues = autoclass('android.content.ContentValues')
        # PythonActivity = autoclass('org.kivy.android.PythonActivity')

        # print('###### SDK VERSION ######'), print(int(Build_VERSION.SDK_INT))
        app_storage_path = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM).getAbsolutePath()


        # # Scoped Storageが使用可能なAndroidバージョンかをチェック
        # if int(Build_VERSION.SDK_INT) >= 29:
        #     # アプリの外部ファイルディレクトリへのパスを取得
        #     # app_storage_path = PythonActivity.mActivity.getExternalFilesDir(None).getAbsolutePath()
        #     content_resolver = PythonActivity.mActivity.getContentResolver()
        #     values = ContentValues()
        #     image_uri = content_resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values)
        #     app_storage_path = image_uri.getPath()

        # else:
        #     # Android 9以前の場合、従来のストレージアクセスを利用
        #     app_storage_path = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM).getAbsolutePath()

    elif platform == 'win': 
        CSIDL_MYPICTURES = 39           # CSIDL_MYPICTURES の値は 39
        MAX_PATH = 260                  # 最大パス長

        # SHGetFolderPath 関数を呼び出すためのセットアップ        
        import ctypes
        shell32 = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(MAX_PATH)
        shell32.SHGetFolderPathW(0, CSIDL_MYPICTURES, 0, 0, buf)

        app_storage_path = buf.value    # パスを取得

    filename = f"IMG_{timestr}.png"
    filepath = join(app_storage_path, filename)
    camera.export_to_png(filepath)
    try:camera.export_to_png(filename)
    except:pass

    return filepath


def show_toast(message):
        notification.notify(
            message=message,
            timeout=15,
            toast=True
        )





# // Defines a new Uri object that receives the result of the insertion
# Uri newUri;
 
# ...
 
# // Defines an object to contain the new values to insert
# ContentValues newValues = new ContentValues();
 
# // Sets the values of each column and inserts the word. 
# // The arguments to the "put" method are "column name" and "value"
# newValues.put(UserDictionary.Words.APP_ID, "example.user");
# newValues.put(UserDictionary.Words.LOCALE, "en_US");
# newValues.put(UserDictionary.Words.WORD, "insert");
# newValues.put(UserDictionary.Words.FREQUENCY, "100");
 
# newUri = getContentResolver().insert(
#     UserDictionary.Words.CONTENT_URI,   // the user dictionary content URI
#     newValues                          // the values to insert
# );




# # 必要なモジュールのインポート
# from torchvision import transforms
# import pytorch_lightning as pl
# import torch.nn as nn
# #学習時に使ったのと同じ学習済みモデルをインポート
# from torchvision.models import resnet18 

# # 学習済みモデルに合わせた前処理を追加
# transform = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
# ])

# #　ネットワークの定義
# class Net(pl.LightningModule):

#     def __init__(self):
#         super().__init__()

#         #学習時に使ったのと同じ学習済みモデルを定義
#         self.feature = resnet18(pretrained=True) 
#         self.fc = nn.Linear(1000, 2)

#     def forward(self, x):
#         #学習時に使ったのと同じ順伝播
#         h = self.feature(x)
#         h = self.fc(h)
#         return h
