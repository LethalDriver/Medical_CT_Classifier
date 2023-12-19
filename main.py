from matplotlib import pyplot as plt
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

batch_size = 32
target_size = (150, 150)
kidneys_dir = 'CT-KIDNEY-DATASET-Normal-Cyst-Tumor-Stone'

img_gen = ImageDataGenerator(validation_split=0.2)

train=keras.utils.image_dataset_from_directory(kidneys_dir,image_size=target_size,
                                                validation_split=0.1,
                                                label_mode='categorical',
                                                subset='training',seed=123)
val=keras.utils.image_dataset_from_directory(kidneys_dir,image_size=target_size,
                                             label_mode = 'categorical',
                                                validation_split=0.2,
                                                subset='validation',seed=123)

train=train.map(lambda x,y:(x/255,y))
val=val.map(lambda x,y:(x/255,y))

VGG_model = Sequential()

pretrained_model= keras.applications.VGG16(include_top=False,
                   input_shape=(150,150,3),
                   pooling='max',classes=4,
                   weights='imagenet')


VGG_model.add(pretrained_model)
VGG_model.add(Flatten())
VGG_model.add(Dense(512, activation='relu'))
VGG_model.add(BatchNormalization())  # Batch Normalization layer
VGG_model.add(Dropout(0.5))

VGG_model.add(Dense(4, activation='softmax'))
pretrained_model.trainable=False

VGG_model.summary()


VGG_model.compile(optimizer=keras.optimizers.Adam(0.0001),
              loss=keras.losses.CategoricalCrossentropy(),metrics=["accuracy"])

history = VGG_model.fit(train,epochs=10,
              validation_data=val)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

# Plot training & validation loss values
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
