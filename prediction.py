from typing import Tuple, Any

from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array


def preprocess_prediction_image(image: Image) -> np.ndarray:
    image = image.convert('RGB')
    image = image.resize((150, 150))
    img_array = img_to_array(image)
    img_array /= 255
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def get_prediction(image: Image) -> np.ndarray:
    img_array = preprocess_prediction_image(image)
    model = load_model('kidney_diagnose.h5')
    prediction = model.predict(img_array)
    return prediction


def parse_prediction(prediction: np.ndarray) -> tuple[str, float]:
    classes = ['Cyst', 'Normal', 'Stone', 'Tumor']
    return classes[np.argmax(prediction)], float(np.max(prediction))