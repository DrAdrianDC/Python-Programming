
import tensorflow as tf
from tensorflow.keras.utils import to_categorical




(x_train, y_train), _ = tf.keras.datasets.mnist.load_data()


x_train = x_train.reshape(60000, 784).astype('float32')/255
y_train = to_categorical(y_train, num_classes=10)


model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(10, activation='tanh', 
            input_shape=(784,)))
model.add(tf.keras.layers.Dense(10, activation='softmax'))


model.compile(loss="categorical_crossentropy", optimizer="sgd", 
                 metrics = ['accuracy'])

model.fit(x_train, y_train, epochs=10, verbose=0)

