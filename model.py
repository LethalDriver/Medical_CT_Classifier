from tensorflow.keras.layers import BatchNormalization, Dense, Dropout, Flatten, Rescaling
from tensorflow.keras.models import Sequential
from keras.layers import RandomFlip, RandomRotation, RandomZoom, RandomContrast


def assemble_model(num_classes, first_dense_neurons, dropout=0.5, activation='softmax') -> Sequential:

    model = Sequential([
        Flatten(),
        Dense(first_dense_neurons, activation='relu'),
        BatchNormalization(),
        Dropout(dropout),
        Dense(num_classes, activation=activation)
    ])

    return model


def augmentation_pipeline() -> Sequential:
    return Sequential([
        RandomFlip(input_shape=(150, 150, 3)),
        RandomRotation(0.1),
        RandomZoom(0.1),
        RandomContrast(0.05)
    ])
