import tensorflow as tf
import utils.utils as nnUtils
from tensorflow.keras import layers
from keras.optimizers import Adam

def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    nnUtils.restrict_to_physcial_gpu()
    nnUtils.set_memory_growth()

    model = tf.keras.Sequential([
        layers.Conv2D(16, activation = "relu", input_shape = (input_rows,input_columns,channels), kernel_size=3,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Conv2D(32, activation='relu', kernel_size=4,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Conv2D(64, activation='relu', kernel_size=4,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Conv2D(128, activation='relu', kernel_size=4,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(movements_number, activation = "softmax")
    ])

    # model.summary()

    model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam" , metrics = ["accuracy"])

    return model

# Winner CNN model for Sergio.