import csv
import copy

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

dataset = './point_history.csv'
model_save_path = './gesture_classifier.hdf5'

TIME_STEPS = 16
DIMENSION = 2
NUM_CLASSES = 3

X_dataset = np.loadtxt(dataset, delimiter=',', dtype='float32', usecols=list(range(1, (TIME_STEPS * DIMENSION) + 1 + 2)))

y_dataset = np.loadtxt(dataset, delimiter=',', dtype='int32', usecols=(0))

for dataset_index, X_data in enumerate(X_dataset):    
    for data_index in range(0, len(X_data), 2):
        if data_index == 0:
            image_width = X_data[data_index]
            image_height = X_data[data_index + 1]
            continue

        if data_index == 2:
            base_x = X_data[data_index]
            base_y = X_data[data_index + 1]

        X_data[data_index] = (X_data[data_index] - base_x) / image_width
        X_data[data_index + 1] = (X_data[data_index + 1] - base_y) / image_height


X_dataset = np.delete(X_dataset, [0, 1, 2, 3], 1)

X_train, X_test, y_train, y_test = train_test_split(X_dataset, y_dataset, train_size=0.75, random_state=42)

input_size = (TIME_STEPS * DIMENSION) - 2

model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(input_size, )),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

# print(model.summary())

# モデルコンパイル
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# モデルチェックポイントのコールバック
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    model_save_path, verbose=1, save_weights_only=False)
# 早期打ち切り用コールバック
es_callback = tf.keras.callbacks.EarlyStopping(patience=20, verbose=1)

model.fit(
    X_train,
    y_train,
    epochs=1000,
    batch_size=128,
    validation_data=(X_test, y_test),
    callbacks=[cp_callback, es_callback]
)

# 推論テスト
predict_result = model.predict(np.array([X_test[0]]))
print(np.squeeze(predict_result))
print(np.argmax(np.squeeze(predict_result)))

# 推論専用のモデルとして保存
model.save(model_save_path, include_optimizer=False)