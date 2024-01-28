from tensorflow.keras.layers import BatchNormalization, Dense, Dropout, Flatten
from tensorflow.keras.models import Sequential


def assemble_kidney_classifier(model, num_classes, first_dense_neurons, dropout=0.5,
                               activation='softmax') -> Sequential:
    model.add(Flatten())
    model.add(Dense(first_dense_neurons, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(dropout))

    model.add(Dense(num_classes, activation=activation))

    return model


def assemble_chest_classifier(model, num_classes, first_dense_neurons, dropout=0.5, activation='softmax') -> Sequential:
    model.add(Flatten())
    model.add(Dense(first_dense_neurons, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(dropout))
    model.add(Dense(first_dense_neurons // 2, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(dropout))

    model.add(Dense(num_classes, activation=activation))

    return model
