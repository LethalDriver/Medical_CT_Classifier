from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array


def preprocess_prediction_image(image: Image) -> np.ndarray:
    image = image.resize((150, 150))
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def get_prediction(image: Image, model_name: str) -> np.ndarray:
    img_array = preprocess_prediction_image(image)
    model = load_model(f"{model_name}.h5")
    prediction = model.predict(img_array)
    return prediction


def parse_prediction(prediction: np.ndarray, model_name: str) -> tuple[str, float]:
    classes = {
        "kidney_diagnose": ['Cyst', 'Normal', 'Stone', 'Tumor'],
        "chest_diagnose": ['Adenocarcinoma', "Large cell carcinoma", "Normal", "Squamous cell carcinoma"]
    }
    return classes[model_name][np.argmax(prediction)], float(np.max(prediction))


def prediction_pipeline(image: Image, model_name: str) -> tuple[str, float]:
    prediction = get_prediction(image, model_name)
    diagnosis, confidence = parse_prediction(prediction, model_name)
    return diagnosis, confidence
