import tensorflow as tf
from tensorflow import keras
import cv2
import numpy as np
import os

# 1. Categories (Flush Left)
CATEGORIES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 
    'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

# 2. Image Processing Function
def prepare_image(path):
    img = cv2.imread(path)
    if img is None:
        return None
    new_arr = cv2.resize(img, (100, 100))
    new_arr = np.array(new_arr/255.0)
    new_arr = new_arr.reshape(-1, 100, 100, 3)
    return new_arr

# 3. Load the Model
model_path = 'my_model.h5' 

if os.path.exists(model_path):
    model = keras.models.load_model(model_path)
    print(f"Model {model_path} loaded successfully!")
else:
    print(f"Error: {model_path} not found. Ensure it is in the same folder.")
    exit()

# 4. Run Prediction
test_image = 'Dataset/valid/Potato___healthy/00fc2ee5-729f-4757-8aeb-65c3355874f2___RS_HL 1864_180deg.JPG'
processed_img = prepare_image(test_image)

if processed_img is not None:
    prediction = model.predict(processed_img)
    result = CATEGORIES[np.argmax(prediction)]
    confidence = np.max(prediction) * 100
    print(f"\n[RESULT] Predicted Class: {result}")
    print(f"[INFO] Confidence: {confidence:.2f}%")