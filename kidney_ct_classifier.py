from keras.optimizers import Adam
from keras.losses import SparseCategoricalCrossentropy
from utils import load_images, plot_history
from model import assemble_model

train_data, validation_data, test_data = load_images('CT-KIDNEY-DATASET-Normal-Cyst-Tumor-Stone')
VGG_model = assemble_model(num_classes=4, first_dense_neurons=512)

VGG_model.compile(optimizer=Adam(0.0001),
                  loss=SparseCategoricalCrossentropy(), metrics=["accuracy"])

history = VGG_model.fit(train_data, epochs=10,
                        validation_data=validation_data)

test_loss, test_accuracy = VGG_model.evaluate(test_data)

plot_history(history)
print(f'Test loss: {test_loss}, Test accuracy: {test_accuracy}')

VGG_model.save('kidney_diagnose.h5')
