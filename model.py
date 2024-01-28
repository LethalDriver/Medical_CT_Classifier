from tensorflow.keras.layers import BatchNormalization, Dense, Dropout, Flatten
from tensorflow.keras.models import Sequential


def assemble_kidney_classifier(model, num_classes, first_dense_neurons, dropout=0.5,
                               activation='softmax') -> Sequential:
    """Function that assembles a kidney classifier model.

    Parameters
    ----------
    model: keras.models.Sequential
        Model to add the classifier part to.

    num_classes: int
        The number of possible classes.
    first_dense_neurons: int
        Number of neurons in the first dense layer.
    dropout: float
        Dropout rate.
    activation: str
        Activation function for the last layer, refer to Keras documentation for more information.

    Returns
    -------
    model: keras.models.Sequential
        Model with the classifier part added.
    """

    model.add(Flatten())
    model.add(Dense(first_dense_neurons, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(dropout))

    model.add(Dense(num_classes, activation=activation))

    return model


def assemble_chest_classifier(model, num_classes, first_dense_neurons, dropout=0.5, activation='softmax') -> Sequential:
    """Function that assembles a chest classifier model.

    Parameters
    ----------
    model: keras.models.Sequential
        Model to add the classifier part to.

    num_classes: int
        The number of possible classes.
    first_dense_neurons: int
        Number of neurons in the first dense layer.
    dropout: float
        Dropout rate.
    activation: str
        Activation function for the last layer, refer to Keras documentation for more information.

    Returns
    -------
    model: keras.models.Sequential
        Model with the classifier part added.
    """
    model.add(Flatten())
    model.add(Dense(first_dense_neurons, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(dropout))
    model.add(Dense(first_dense_neurons // 2, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(dropout))

    model.add(Dense(num_classes, activation=activation))

    return model
