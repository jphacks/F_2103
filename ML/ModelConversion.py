import tensorflow as tf
import numpy as np

dataset = './point_history.csv'

TIME_STEPS = 16
DIMENSION = 2
NUM_CLASSES = 3

X_dataset = np.loadtxt(dataset, delimiter=',', dtype='float32', usecols=list(range(1, (TIME_STEPS * DIMENSION) + 1 + 2)))

model_save_path = './gesture_classifier.hdf5'

model = tf.keras.models.load_model(model_save_path)

tflite_save_path = './gesture_classifier.tflite'

# モデルを変換(量子化)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_quantized_model = converter.convert()

open(tflite_save_path, 'wb').write(tflite_quantized_model)

interpreter = tf.lite.Interpreter(model_path=tflite_save_path)
interpreter.allocate_tensors()

# 入出力テンソルを取得
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 推論実施
interpreter.set_tensor(input_details[0]['index'], np.array([X_dataset[0]]))
interpreter.invoke()
tflite_results = interpreter.get_tensor(output_details[0]['index'])

print(np.squeeze(tflite_results))
print(np.argmax(np.squeeze(tflite_results)))

