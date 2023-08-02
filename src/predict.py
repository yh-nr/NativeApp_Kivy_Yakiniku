# 必要なモジュールのインポート
from io import BytesIO, SEEK_END
from PIL import Image
import numpy as np
from .func import show_toast

try:
  from tflite_runtime.interpreter import Interpreter
  from tflite_runtime.interpreter import load_delegate
except ImportError:
  import tensorflow as tf
  Interpreter = tf.lite.Interpreter

from kivy.graphics.texture import Texture
from kivy.utils import platform
try: from jnius import autoclass
except:pass
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def preprocess(image_path):
  image = Image.open(image_path)
  
  # if platform == 'android':
  #   FileInputStream = autoclass('java.io.FileInputStream')
  #   bytes_io = BytesIO()

  #   with FileInputStream(image_path) as f:
  #     while True:
  #       buf = f.read().to_bytes(2,"big")
  #       if not buf:  # バイト列が空ならループを終了
  #         break
  #       bytes_io.write(buf)

  #   bytes_io.seek(0)
  #   image = Image.open(bytes_io)

  # elif platform == 'win': 
  #   image = Image.open(image_path)

  # Resize the image so that the shortest side is 224 pixels
  if image.size[0] < image.size[1]:
      new_width = 224
      new_height = 224 * image.size[1] // image.size[0]
  else:
      new_height = 224
      new_width = 224 * image.size[0] // image.size[1]

  image = image.resize((new_width, new_height))

  # Crop the center 224x224 pixels
  left = (new_width - 224) / 2
  top = (new_height - 224) / 2
  right = (new_width + 224) / 2
  bottom = (new_height + 224) / 2
  image = image.crop((left, top, right, bottom))

  # Convert image to numpy array
  img_array = np.array(image)

  # Normalize image data to [0, 1] range
  img_normalized = img_array / 255.0

  # Normalize to ImageNet mean and standard deviation
  mean = np.array([0.485, 0.456, 0.406])
  std = np.array([0.229, 0.224, 0.225])
  img_normalized = (img_normalized - mean) / std

  # Add a new dimension for the batch
  img_expanded = np.expand_dims(img_normalized, axis=0)
  img_expanded = img_expanded.transpose((0, 3, 1, 2))
  
  
  texture = Texture.create(size=(224,224), colorfmt='rgb', bufferfmt='ubyte')
  texture.blit_buffer(image.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
  texture.flip_vertical()

  return img_expanded.astype(np.float32), texture


# 学習済みモデルをもとに推論する
def predict(image_path):
  # モデルのロード
  interpreter = Interpreter(model_path="./src/dog_cat.tflite")
  interpreter.allocate_tensors()
  
  #　データの前処理
  input_data, texture = preprocess(image_path)
  
  # 推論の実行 
  interpreter.set_tensor(interpreter.get_input_details()[0]["index"], input_data)
  interpreter.invoke()
  # show_toast('しおり２')
  
  # 結果の取得
  output_data = interpreter.get_tensor(interpreter.get_output_details()[0]["index"])
  
  # 結果の解釈（１）
  predicted_label = np.argmax(output_data)

  # Manual softmax implementation
  exps = np.exp(output_data - np.max(output_data))
  y_pred_proba = exps / np.sum(exps)

  # Convert to percentage
  y_pred_proba_max = round((np.max(y_pred_proba) * 100), 2)
  
  return getName(predicted_label), y_pred_proba_max, texture


#　推論したラベルから犬か猫かを返す関数
def getName(label):
    if label==0: return '猫'
    elif label==1: return '犬'




def old_preprocess(image_path):
  # show_toast('しおり0A')
  # Load the image
  image = Image.open(image_path)
  # show_toast('しおり０B')

  # Resize the image so that the shortest side is 224 pixels
  if image.size[0] < image.size[1]:
      new_width = 224
      new_height = 224 * image.size[1] // image.size[0]
  else:
      new_height = 224
      new_width = 224 * image.size[0] // image.size[1]

  image = image.resize((new_width, new_height))

  # Crop the center 224x224 pixels
  left = (new_width - 224) / 2
  top = (new_height - 224) / 2
  right = (new_width + 224) / 2
  bottom = (new_height + 224) / 2
  image = image.crop((left, top, right, bottom))

  # Convert image to numpy array
  img_array = np.array(image)

  # Normalize image data to [0, 1] range
  img_normalized = img_array / 255.0

  # Normalize to ImageNet mean and standard deviation
  mean = np.array([0.485, 0.456, 0.406])
  std = np.array([0.229, 0.224, 0.225])
  img_normalized = (img_normalized - mean) / std

  # Add a new dimension for the batch
  img_expanded = np.expand_dims(img_normalized, axis=0)
  img_expanded = img_expanded.transpose((0, 3, 1, 2))

  return img_expanded.astype(np.float32)


# 学習済みモデルをもとに推論する
def old_predict(image_path):
  # モデルのロード
  interpreter = Interpreter(model_path="./src/dog_cat.tflite")
  interpreter.allocate_tensors()
  
  #　データの前処理
  input_data = preprocess(image_path)
  # show_toast('しおり１')
  
  # 推論の実行 
  interpreter.set_tensor(interpreter.get_input_details()[0]["index"], input_data)
  interpreter.invoke()
  # show_toast('しおり２')
  
  # 結果の取得
  output_data = interpreter.get_tensor(interpreter.get_output_details()[0]["index"])
  
  # 結果の解釈（１）
  predicted_label = np.argmax(output_data)

  # Manual softmax implementation
  exps = np.exp(output_data - np.max(output_data))
  y_pred_proba = exps / np.sum(exps)

  # Convert to percentage
  y_pred_proba_max = round((np.max(y_pred_proba) * 100), 2)
  
  return predicted_label, y_pred_proba_max
