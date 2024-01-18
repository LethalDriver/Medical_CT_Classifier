from fastapi import FastAPI
from pydantic import BaseModel
import base64
from io import BytesIO
from PIL import Image
from prediction import get_prediction, parse_prediction


class ImageData(BaseModel):
    image: str


class Prediction(BaseModel):
    diagnosis: str
    confidence: float


app = FastAPI()


@app.post("/upload_image")
async def upload_image(data: ImageData):
    base64_img_bytes = base64.b64decode(data.image)
    image = Image.open(BytesIO(base64_img_bytes))
    prediction = get_prediction(image)
    diagnosis, confidence = parse_prediction(prediction)
    response = Prediction(diagnosis=diagnosis, confidence=confidence)
    return {"prediction": response}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
