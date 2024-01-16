import os
import shutil
import random


def make_train_and_test_dirs(images_dir, test_split=0.2):
    # Create a test directory if it doesn't exist
    test_dir = os.path.join(images_dir, 'test')
    os.makedirs(test_dir, exist_ok=True)

    # Create a train directory if it doesn't exist
    train_dir = os.path.join(images_dir, 'train')
    os.makedirs(train_dir, exist_ok=True)

    # Get the list of class directories
    class_dirs = [d for d in os.listdir(images_dir) if os.path.isdir(os.path.join(images_dir, d)) and d not in ['test', 'train']]

    for class_dir in class_dirs:
        print(f'Creating test set for {class_dir}...')
        class_dir_path = os.path.join(images_dir, class_dir)

        # Get the list of image files for this class
        image_files = [f for f in os.listdir(class_dir_path) if os.path.isfile(os.path.join(class_dir_path, f))]

        # Shuffle the list of image files
        random.shuffle(image_files)

        # Calculate the number of test images
        num_test_images = int(len(image_files) * test_split)

        # Select the test images
        test_images = image_files[:num_test_images]

        # Select the train images
        train_images = image_files[num_test_images:]

        # Create a test directory for this class
        test_class_dir = os.path.join(test_dir, class_dir)
        os.makedirs(test_class_dir, exist_ok=True)

        # Create a train directory for this class
        train_class_dir = os.path.join(train_dir, class_dir)
        os.makedirs(train_class_dir, exist_ok=True)

        # Move the test images to the test directory
        for test_image in test_images:
            shutil.move(os.path.join(class_dir_path, test_image), os.path.join(test_class_dir, test_image))

        # Move the train images to the train directory
        for train_image in train_images:
            shutil.move(os.path.join(class_dir_path, train_image), os.path.join(train_class_dir, train_image))




