from tensorflow.keras.layers import BatchNormalization, Dense, Dropout, Flatten, Rescaling
from tensorflow.keras.models import Sequential
from keras.applications.vgg16 import VGG16


def assemble_model(num_classes, first_dense_neurons, input_shape=(150, 150, 3), dropout=0.5, activation='softmax'):
    vgg_model = Sequential()

    pretrained_model = VGG16(include_top=False,
                             input_shape=input_shape,
                             pooling='max', classes=num_classes,
                             weights='imagenet')

    vgg_model.add(Rescaling(1. / 255, input_shape=input_shape))
    vgg_model.add(pretrained_model)
    vgg_model.add(Flatten())
    vgg_model.add(Dense(first_dense_neurons, activation='relu'))
    vgg_model.add(BatchNormalization())
    vgg_model.add(Dropout(dropout))

    vgg_model.add(Dense(num_classes, activation=activation))
    pretrained_model.trainable = False

    return vgg_model
