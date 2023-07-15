# 必要なモジュールのインポート
from PIL import Image
import numpy as np

# pylint: disable=g-import-not-at-top
try:
  # Import TFLite interpreter from tflite_runtime package if it's available.
  from tflite_runtime import tf
except:
  # If not, fallback to use the TFLite interpreter from the full TF package.
  import tensorflow as tf

# 学習済みモデルに合わせた前処理を追加
def preprocess(image_path):
    # 画像をロード
    image = Image.open(image_path)
    
    # PIL形式からnumpy配列に変換
    img_array = np.array(image)
    
    # 画像をリサイズし、中央で224x224のクロップを行う
    # img_resized = tf.image.resize_with_crop_or_pad(img_array, 224, 224)


    # 最初に縮小します。縦または横の辺のうち短い方が224となるようにします。
    min_dim = tf.minimum(tf.shape(img_array)[0], tf.shape(img_array)[1])
    new_height = img_array.shape[0] * 224 // min_dim
    new_width = img_array.shape[1] * 224 // min_dim
    img_resized = tf.image.resize(img_array, [new_height, new_width])

    # 次に中央をクロップします。クロップするサイズは224x224となります。
    start_height = (new_height - 224) // 2
    start_width = (new_width - 224) // 2
    img_cropped = tf.image.crop_to_bounding_box(img_resized, start_height, start_width, 224, 224)


    
    # データ型をfloat32に変換
    img_cropped = tf.cast(img_cropped, tf.float32) / 255.0
    
    # データの正規化
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    img_normalized = (img_cropped - mean) / std
    
    # 画像の次元を増やす
    img_expanded = np.expand_dims(img_normalized, axis=0)
    return img_expanded

# 学習済みモデルをもとに推論する
def predict(image_path):
    # モデルのロード
    interpreter = tf.lite.Interpreter(model_path="./src/dog_cat.tflite")
    interpreter.allocate_tensors()
    
    #　データの前処理
    input_data = preprocess(image_path)
    input_data = tf.transpose(input_data, perm=[0, 3, 1, 2])
    
    # 推論の実行 interpreter.set_tensor(interpreter.get_input_details()[0]["index"], input_data)
    interpreter.invoke()
    
    # 結果の取得
    output_data = interpreter.get_tensor(interpreter.get_output_details()[0]["index"])
    
    # 結果の解釈
    predicted_label = np.argmax(output_data)
    y_pred_proba = round((np.max(tf.nn.softmax(output_data, axis=-1)) * 100), 2)
    
    return predicted_label, y_pred_proba
