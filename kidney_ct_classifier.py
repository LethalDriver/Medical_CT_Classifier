from keras import Sequential
from keras.optimizers import Adam
from keras.losses import CategoricalCrossentropy
from keras.src.layers import Rescaling

from utils import load_images, plot_history
from model import assemble_model
from keras.applications.vgg16 import VGG16

train_data, validation_data, test_data = load_images('CT-KIDNEY-DATASET-Normal-Cyst-Tumor-Stone')

input_shape = (150, 150, 3)

pretrained_model = VGG16(include_top=False,
                             input_shape=input_shape,
                             pooling='max', classes=4,
                             weights='imagenet')

pretrained_model.trainable = False

VGG_model = Sequential([
    Rescaling(1. / 255, input_shape=(150, 150, 3)),
    pretrained_model,
    assemble_model(num_classes=4,
                   first_dense_neurons=512,
                   )
])



VGG_model.compile(optimizer=Adam(0.0001),
                  loss=CategoricalCrossentropy(), metrics=["accuracy"])

history = VGG_model.fit(train_data, epochs=10,
                        validation_data=validation_data)

test_loss, test_accuracy = VGG_model.evaluate(test_data)

plot_history(history)
print(f'Test loss: {test_loss}, Test accuracy: {test_accuracy}')

VGG_model.save('kidney_diagnose.h5')
