from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array


def preprocess_prediction_image(image: Image) -> np.ndarray:
    """Function that preprocesses an image for prediction.

    Parameters
    ----------
    image: PIL.Image
        Image to preprocess.

    Returns
    -------
    img_array: np.ndarray
        Preprocessed image, in the format expected by the model (1, 150, 150, 3).
    """
    image = image.convert('RGB')
    image = image.resize((150, 150))
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def get_prediction(image: Image, model_name: str) -> np.ndarray:
    """Function that loads a specified model and returns prediction vector for a given image.

    Parameters
    ----------
    image: PIL.Image
        Image to make a prediction on.

    model_name: str
        Name of the model to load, currently supported models are: 'kidney_diagnose', 'chest_diagnose'.

    Returns
    -------
    prediction: np.ndarray
        Prediction vector.
    """
    img_array = preprocess_prediction_image(image)
    model = load_model(f"{model_name}.h5")
    prediction = model.predict(img_array)
    return prediction


def parse_prediction(prediction: np.ndarray, model_name: str) -> tuple[str, float]:
    """Function that parses prediction vector and returns prediction in form of a diagnosis and its confidence.

    Parameters
    ----------
    prediction: np.ndarray
        Prediction vector.
    model_name: str
        Name of the model used to make a prediction, currently supported models are: 'kidney_diagnose', 'chest_diagnose'.

    Returns
    -------
    diagnosis: str
        Diagnosis, based on model's prediction. Possible values for 'kidney_diagnose'
        model are: 'Cyst', 'Normal', 'Stone', 'Tumor'.
        Possible values for 'chest_diagnose' model are: 'Adenocarcinoma',
        "Large cell carcinoma", "Normal", "Squamous cell carcinoma".
    confidence: float
        Confidence of the diagnosis.
    """
    classes = {
        "kidney_diagnose": ['Cyst', 'Normal', 'Stone', 'Tumor'],
        "chest_diagnose": ['Adenocarcinoma', "Large cell carcinoma", "Normal", "Squamous cell carcinoma"]
    }
    return classes[model_name][np.argmax(prediction)], float(np.max(prediction))


def prediction_pipeline(image: Image, model_name: str) -> tuple[str, float]:
    """Function that applies entire prediction pipeline to a given image.

    Parameters
    ----------
    image: PIL.Image
        Image to make a prediction on.
    model_name: str
        Name of the model used to make a prediction, currently supported models are: 'kidney_diagnose', 'chest_diagnose'.

    Returns
    -------
    diagnosis: str
        Diagnosis, based on model's prediction. Possible values for 'kidney_diagnose'
        model are: 'Cyst', 'Normal', 'Stone', 'Tumor'.
        Possible values for 'chest_diagnose' model are: 'Adenocarcinoma',
        "Large cell carcinoma", "Normal", "Squamous cell carcinoma".
    confidence: float
        Confidence of the diagnosis.
    """
    prediction = get_prediction(image, model_name)
    diagnosis, confidence = parse_prediction(prediction, model_name)
    return diagnosis, confidence
