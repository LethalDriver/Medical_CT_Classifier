from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the model
model = load_model('kidney_diagnose.h5')

# Load the image you want to make a prediction on
img = image.load_img('CT-KIDNEY-DATASET-Normal-Cyst-Tumor-Stone/train/Tumor/Tumor- (32).jpg', target_size=(150, 150))

# Convert the image to a numpy array
img_array = image.img_to_array(img)

# Scale the image pixels by 255
img_array /= 255

# Expand dimensions to fit the model's expected input shape
img_array = np.expand_dims(img_array, axis=0)

# Make the prediction
prediction = model.predict(img_array)

# Print the prediction
print(prediction)