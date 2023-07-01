from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import time

from .func import SavePic, show_toast



# 必要なモジュールのインポート
import torch
from .animal import transform, Net # animal.py から前処理とネットワークの定義を読み込み
import io
from PIL import Image
# import base64
from kivy.core.image import Image as CoreImage
import io
import cv2 


class CameraClick(BoxLayout):
    camera_ref = ObjectProperty(None)

    # def capture(self):
    #     timestr = time.strftime("%Y%m%d_%H%M%S")
    #     filepath = SavePic(self.camera_ref, timestr)
    #     message = f"Captured ({filepath})"
    #     show_toast(message=message)

    def capture(self):
        self.camera_ref.export_as_image().texture.save('temp.png')
        image = Image.open('temp.png').convert('RGB')
        print(type(image))
        pred, animalNameProba_ = predict(image)
        animalName_ = getName(pred)
        show_toast(str(animalName_) + str(animalNameProba_))



# 学習済みモデルをもとに推論する
def predict(img):
    # ネットワークの準備
    net = Net().cpu().eval()
    # # 学習済みモデルの重み（dog_cat.pt）を読み込み
    # net.load_state_dict(torch.load('./src/dog_cat.pt', map_location=torch.device('cpu')))
    net.load_state_dict(torch.load('./src/dog_cat.pt', map_location=torch.device('cpu')))
    #　データの前処理
    img = transform(img)
    img =img.unsqueeze(0) # 1次元増やす
    #　推論
    y = torch.argmax(net(img), dim=1).cpu().detach().numpy()
    y_pred_proba = round((max(torch.softmax(net(img), dim=1)[0]) * 100).item(),2)
    return y, y_pred_proba


#　推論したラベルから犬か猫かを返す関数
def getName(label):
    if label==0:
        return '猫'
    elif label==1:
        return '犬'


# def predicts():
#     # ファイルがなかった場合の処理
#     if 'filename' not in request.files:
#         return redirect(request.url)

#     # データの取り出し
#     file = request.files['filename']
#     # ファイルのチェック
#     if file and allwed_file(file.filename):

#         #　画像ファイルに対する処理
#         #　画像書き込み用バッファを確保
#         buf = io.BytesIO()
#         image = Image.open(file).convert('RGB')

#         # 画像の大きさを調整する
#         # 講義資料にはなく、追加しています！
#         new_width = 500
#         new_height = 500
#         image = image.resize((new_width, new_height))

#         #　画像データをバッファに書き込む
#         image.save(buf, 'png')
#         #　バイナリデータを base64 でエンコードして utf-8 でデコード
#         base64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
#         #　HTML 側の src  の記述に合わせるために付帯情報付与する
#         base64_data = 'data:image/png;base64,{}'.format(base64_str)

#         # 入力された画像に対して推論
#         pred, animalNameProba_ = predict(image)
#         animalName_ = getName(pred)
        
#         show_toast(animalName_ + animalNameProba_)