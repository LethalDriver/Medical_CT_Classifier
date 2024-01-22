from keras.callbacks import EarlyStopping
from keras import Sequential
from keras.src.layers import Rescaling
from keras.src.optimizers import Adam
from tensorflow.keras.applications.vgg16 import VGG16
from utils import load_images
from model import assemble_classifier, augmentation_pipeline
from utils import plot_history

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

train_data, validation_data, test_data = load_images('ChestCT', image_size=(150, 150), batch_size=32)
input_shape = (150, 150, 3)

pretrained_model = VGG16(include_top=False,
                         input_shape=input_shape,
                         pooling='max', classes=4,
                         weights='imagenet')

pretrained_model.trainable = False

model = Sequential([
    Rescaling(1. / 255, input_shape=input_shape),
])

model.add(pretrained_model)
model = assemble_classifier(model, num_classes=4, first_dense_neurons=512)
model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()
history = model.fit(train_data, epochs=30, validation_data=validation_data)

plot_history(history)

test_loss, test_accuracy = model.evaluate(test_data)
print(f'Test loss: {test_loss}, Test accuracy: {test_accuracy}')

