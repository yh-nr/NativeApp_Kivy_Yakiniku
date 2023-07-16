# 必要なモジュールのインポート
from PIL import Image
import numpy as np
from .func import show_toast

# pylint: disable=g-import-not-at-top
try:
  from tflite_runtime.interpreter import Interpreter
  from tflite_runtime.interpreter import load_delegate
except ImportError:
  import tensorflow as tf
  Interpreter = tf.lite.Interpreter

# # 学習済みモデルに合わせた前処理を追加
# def preprocess(image_path):
#     # 画像をロード
#     image = Image.open(image_path)
    
#     # PIL形式からnumpy配列に変換
#     img_array = np.array(image)
    

#     # 最初に縮小します。縦または横の辺のうち短い方が224となるようにします。
#     min_dim = tf.minimum(tf.shape(img_array)[0], tf.shape(img_array)[1])
#     new_height = img_array.shape[0] * 224 // min_dim
#     new_width = img_array.shape[1] * 224 // min_dim
#     img_resized = tf.image.resize(img_array, [new_height, new_width])

#     # 次に中央をクロップします。クロップするサイズは224x224となります。
#     start_height = (new_height - 224) // 2
#     start_width = (new_width - 224) // 2
#     img_cropped = tf.image.crop_to_bounding_box(img_resized, start_height, start_width, 224, 224)


    
#     # データ型をfloat32に変換
#     img_cropped = tf.cast(img_cropped, tf.float32) / 255.0
    
#     # データの正規化
#     mean = np.array([0.485, 0.456, 0.406])
#     std = np.array([0.229, 0.224, 0.225])
#     img_normalized = (img_cropped - mean) / std
    
#     # 画像の次元を増やす
#     img_expanded = np.expand_dims(img_normalized, axis=0)
#     return img_expanded


def preprocess(image_path):
  show_toast('しおり0A')
  # Load the image
  image = Image.open(image_path)
  show_toast('しおり０B')

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

  return img_expanded


# 学習済みモデルをもとに推論する
def predict(image_path):
  # モデルのロード
  interpreter = Interpreter(model_path="./src/dog_cat.tflite")
  interpreter.allocate_tensors()
  
  #　データの前処理
  input_data = preprocess(image_path)
  show_toast('しおり１')
  
  # 推論の実行 
  interpreter.set_tensor(interpreter.get_input_details()[0]["index"], input_data)
  interpreter.invoke()
  show_toast('しおり２')
  
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
