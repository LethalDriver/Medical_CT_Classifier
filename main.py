from matplotlib import pyplot as plt
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
import keras


def load_rescale_images(batch_size=32, image_size=(150, 150), validation_split=0.2,
                        images_dir='CT-KIDNEY-DATASET-Normal-Cyst-Tumor-Stone'):
    train_data = keras.utils.image_dataset_from_directory(images_dir, image_size=image_size,
                                                          batch_size=batch_size,
                                                          validation_split=validation_split,
                                                          label_mode='categorical',
                                                          subset='training', seed=123)

    validation_data = keras.utils.image_dataset_from_directory(images_dir, image_size=image_size,
                                                               batch_size=batch_size,
                                                               label_mode='categorical',
                                                               validation_split=validation_split,
                                                               subset='validation', seed=123)

    train_data = train_data.map(lambda x, y: (x / 255, y))
    validation_data = validation_data.map(lambda x, y: (x / 255, y))

    return train_data, validation_data


def assemble_model(input_shape=(150, 150, 3), num_classes=4, first_dense_neurons=512, dropout=0.5):
    vgg_model = Sequential()

    pretrained_model = keras.applications.VGG16(include_top=False,
                                                input_shape=input_shape,
                                                pooling='max', classes=num_classes,
                                                weights='imagenet')

    vgg_model.add(pretrained_model)
    vgg_model.add(Flatten())
    vgg_model.add(Dense(first_dense_neurons, activation='relu'))
    vgg_model.add(BatchNormalization())
    vgg_model.add(Dropout(dropout))

    vgg_model.add(Dense(num_classes, activation='softmax'))
    pretrained_model.trainable = False

    return vgg_model


def plot_history(history):
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')

    plt.tight_layout()
    plt.show()

    VGG_model.save('kidney_diagnose.h5')


train_data, validation_data = load_rescale_images()
VGG_model = assemble_model()

VGG_model.compile(optimizer=keras.optimizers.Adam(0.0001),
                  loss=keras.losses.CategoricalCrossentropy(), metrics=["accuracy"])

history = VGG_model.fit(train_data, epochs=10,
                        validation_data=validation_data)

plot_history(history)