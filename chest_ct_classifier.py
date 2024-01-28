import numpy as np
from keras.callbacks import EarlyStopping
from keras import Sequential
from keras.src.callbacks import LearningRateScheduler
from keras.src.layers import Rescaling, RandomZoom
from keras.src.optimizers import Adam
from tensorflow.keras.applications.vgg16 import VGG16
from model import assemble_chest_classifier
from utils import plot_history, step_decay, load_images


early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

train_data, validation_data, test_data = load_images('ChestCT', image_size=(150, 150), batch_size=32)
input_shape = (150, 150, 3)

pretrained_model = VGG16(include_top=False,
                         input_shape=input_shape,
                         pooling='max', classes=4,
                         weights='imagenet')

pretrained_model.trainable = False

model = Sequential([
    Rescaling(1. / 255, input_shape=input_shape),
    RandomZoom(0.1)
])

learning_rate_scheduling = LearningRateScheduler(step_decay)

model.add(pretrained_model)
model = assemble_chest_classifier(model, num_classes=4, first_dense_neurons=512)
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()
history = model.fit(train_data, epochs=60, validation_data=validation_data, callbacks=[learning_rate_scheduling])

plot_history(history)

test_loss, test_accuracy = model.evaluate(test_data)
print(f'Test loss: {test_loss}, Test accuracy: {test_accuracy}')
