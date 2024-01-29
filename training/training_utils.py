import base64
import io
import os
import shutil
import random
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image_dataset_from_directory
import matplotlib.pyplot as plt


def load_images(images_dir,
                batch_size=32,
                image_size=(150, 150),
                validation_split=0.2,
                labels='inferred',
                label_mode='categorical'):
    """Function that loads images from a directory and returns train, validation and test tf datasets,
    if test directory exists, otherwise returns only train and validation tf datasets.

    Parameters
    ----------
    images_dir: str
        Path to directory containing images.
    batch_size: int
        Returned datasets' batch sizes.
    image_size: tuple of int
        Returned datasets' image sizes.
    validation_split:
        Fraction of images reserved for validation.
    labels: str
        Labels mode: 'inferred', None or list of labels corresponding to the directories found in the images_dir,
        refer to Keras documentation for more details.
    label_mode: str
        Labels mode: 'categorical', 'binary', 'sparse', 'int', refer to Keras documentation for more details.

    Returns
    -------
    train_data: tf.data.Dataset
        Train dataset.
    validation_data: tf.data.Dataset
        Validation dataset.
    test_data: tf.data.Dataset or None
        Test dataset, if test directory exists, otherwise None.
    """

    is_test_dir = os.path.isdir(f'{images_dir}/test')
    is_val_dir = os.path.isdir(f'{images_dir}/valid')

    test_data = None

    if is_test_dir:
        test_data = image_dataset_from_directory(f'{images_dir}/test',
                                                 image_size=image_size,
                                                 batch_size=batch_size,
                                                 labels=labels,
                                                 label_mode=label_mode)
        train_dir = f'{images_dir}/train'
    else:
        train_dir = images_dir

    if is_val_dir:
        validation_data = image_dataset_from_directory(f'{images_dir}/valid',
                                                       image_size=image_size,
                                                       batch_size=batch_size,
                                                       labels=labels,
                                                       label_mode=label_mode, seed=123)

        train_data = image_dataset_from_directory(train_dir, image_size=image_size,
                                                  batch_size=batch_size,
                                                  labels=labels,
                                                  label_mode=label_mode,
                                                  seed=123)
    else:
        train_data = image_dataset_from_directory(train_dir, image_size=image_size,
                                                  batch_size=batch_size,
                                                  validation_split=validation_split,
                                                  labels=labels,
                                                  label_mode=label_mode,
                                                  subset='training', seed=123)
        validation_data = image_dataset_from_directory(train_dir, image_size=image_size,
                                                       batch_size=batch_size,
                                                       labels=labels,
                                                       label_mode=label_mode,
                                                       validation_split=validation_split,
                                                       subset='validation', seed=123)

    return (train_data, validation_data, test_data) if is_test_dir else (train_data, validation_data)


def plot_history(history):
    """Function that plots model's training and validation accuracy and loss.

    Parameters
    ----------
    history: keras.callbacks.History
        Model's history.

    Returns
    -------
    None
    """

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


def make_train_and_test_dirs(images_dir, test_split=0.2):
    """Utility function for creating train and test directories from a directory containing images.

    Parameters
    ----------
    images_dir: str
        Path to directory containing images.
    test_split: float
        Fraction of images reserved for test set.

    Returns
    -------
    None
    """

    test_dir = os.path.join(images_dir, 'test')
    os.makedirs(test_dir, exist_ok=True)

    train_dir = os.path.join(images_dir, 'train')
    os.makedirs(train_dir, exist_ok=True)

    class_dirs = [d for d in os.listdir(images_dir) if
                  os.path.isdir(os.path.join(images_dir, d)) and d not in ['test', 'train']]

    for class_dir in class_dirs:
        print(f'Creating test set for {class_dir}...')
        class_dir_path = os.path.join(images_dir, class_dir)

        image_files = [f for f in os.listdir(class_dir_path)
                       if os.path.isfile(os.path.join(class_dir_path, f))]

        random.shuffle(image_files)

        num_test_images = int(len(image_files) * test_split)

        test_images = image_files[:num_test_images]

        train_images = image_files[num_test_images:]

        test_class_dir = os.path.join(test_dir, class_dir)
        os.makedirs(test_class_dir, exist_ok=True)

        train_class_dir = os.path.join(train_dir, class_dir)
        os.makedirs(train_class_dir, exist_ok=True)

        for test_image in test_images:
            shutil.move(os.path.join(class_dir_path, test_image), os.path.join(test_class_dir, test_image))

        for train_image in train_images:
            shutil.move(os.path.join(class_dir_path, train_image), os.path.join(train_class_dir, train_image))

        os.rmdir(class_dir_path)

    print('Successfully created test set.')





def step_decay(epoch):
    """Step decay function for learning rate scheduling in chest_ct_classifier.py.

    Parameters
    ----------
    epoch:
        Number of the current epoch.

    Returns
    -------
    lrate: float
        Learning rate to be applied to the model.
    """
    initial_lrate = 0.001
    drop = 0.5
    epochs_drop = 15
    lrate = initial_lrate * np.power(drop, np.floor((1 + epoch) / epochs_drop))
    return lrate
