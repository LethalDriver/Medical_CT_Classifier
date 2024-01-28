from fastapi import FastAPI
from pydantic import BaseModel
from prediction import prediction_pipeline
from utils import decode_image


class ImageData(BaseModel):
    image: str


class Prediction(BaseModel):
    diagnosis: str
    confidence: float


app = FastAPI()


@app.post("/kidney")
async def get_kidney_diagnosis(data: ImageData):
    """Fast API endpoint for kidney diagnosis.

    Parameters
    ----------
    data: ImageData
        Image data, encoded in base64.

    Returns
    -------
    response: Prediction
        Prediction response containing diagnosis and confidence.
    """
    image = decode_image(data.image)
    diagnosis, confidence = prediction_pipeline(image, "kidney_diagnose")
    response = Prediction(diagnosis=diagnosis, confidence=confidence)
    return response


@app.post("/chest")
async def get_chest_diagnosis(data: ImageData):
    """Fast API endpoint for chest diagnosis.

        Parameters
        ----------
        data: ImageData
            Image data, encoded in base64.

        Returns
        -------
        response: Prediction
            Prediction response containing diagnosis and confidence.
        """
    image = decode_image(data.image)
    diagnosis, confidence = prediction_pipeline(image, "chest_diagnose")
    response = Prediction(diagnosis=diagnosis, confidence=confidence)
    return response


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
