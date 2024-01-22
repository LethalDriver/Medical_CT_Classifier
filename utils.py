import base64
import os
import shutil
import random

from tensorflow.keras.preprocessing import image_dataset_from_directory
import matplotlib.pyplot as plt


def load_images(images_dir,
                batch_size=32,
                image_size=(150, 150),
                validation_split=0.2,
                labels='inferred',
                label_mode='categorical'):
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


def encode_image(image_path):
    image = open(image_path, 'rb')
    image_bytes = image.read()
    image_b64 = base64.b64encode(image_bytes)
    image_str = image_b64.decode('utf-8')
    return image_str


def delete_dcm_files(images_dir):
    class_dirs = [d for d in os.listdir(images_dir) if
                  os.path.isdir(os.path.join(images_dir, d)) and d not in ['test', 'train']]

    for class_dir in class_dirs:
        class_dir_path = os.path.join(images_dir, class_dir)
        image_files = [f for f in os.listdir(class_dir_path)
                       if os.path.isfile(os.path.join(class_dir_path, f))]

        for image_file in image_files:
            if image_file.endswith('.dcm'):
                os.remove(os.path.join(class_dir_path, image_file))

    print('Successfully deleted dcm files.')


