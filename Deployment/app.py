from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np
import cv2
from datetime import datetime

# Keras & TensorFlow
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask & SQLAlchemy
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Models ---

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expert_name = db.Column(db.String(100), default="General Pathologist")
    scheduled_time = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="Confirmed")
    date_booked = db.Column(db.DateTime, default=datetime.now)

# Initialize Database on Mac Mini
with app.app_context():
    db.create_all()

# --- Model Loading ---
MODEL_PATH = 'my_model.h5'
model = load_model(MODEL_PATH)

def model_predict(img_path, model):
    img = cv2.imread(img_path)
    new_arr = cv2.resize(img,(100,100)) # Change 256 to 100
    new_arr = np.array(new_arr/255)
    new_arr = new_arr.reshape(-1, 100, 100, 3) # Change 256 to 100
    preds = model.predict(new_arr)
    return preds

# --- Routes ---

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', result=None)

@app.route('/history')
def history():
    past_predictions = Prediction.query.order_by(Prediction.date_created.desc()).all()
    return render_template('history.html', predictions=past_predictions)

@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        filename = f.filename
        file_path = os.path.join(basepath, 'static/uploads', filename)
        f.save(file_path)

        preds = model_predict(file_path, model)
        pred_class = preds.argmax()

        # --- FULL 38 CATEGORIES LIST ---
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
        
        result_text = CATEGORIES[pred_class]
        img_display_path = url_for('static', filename='uploads/' + filename)

        try:
            new_entry = Prediction(
                disease_name=result_text,
                image_path=img_display_path,
                date_created=datetime.now()
            )
            db.session.add(new_entry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to database: {e}")

        return render_template('index.html', result=result_text, image_path=img_display_path)
    return redirect(url_for('index'))

@app.route('/delete_log/<int:id>', methods=['POST'])
def delete_log(id):
    record = Prediction.query.get_or_404(id)
    try:
        db.session.delete(record)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('history'))

@app.route('/consultations')
def consultations():
    all_bookings = Consultation.query.order_by(Consultation.date_booked.desc()).all()
    return render_template('consultations.html', bookings=all_bookings)

@app.route('/book_expert', methods=['POST'])
def book_expert():
    selected_time = request.form.get('expert-time')
    if selected_time:
        try:
            new_booking = Consultation(scheduled_time=selected_time)
            db.session.add(new_booking)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    return redirect(url_for('consultations'))

@app.route('/delete_consultation/<int:id>', methods=['POST'])
def delete_consultation(id):
    booking = Consultation.query.get_or_404(id)
    try:
        db.session.delete(booking)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
    return redirect(url_for('consultations'))

@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')

if __name__ == '__main__':
    app.run(debug=True)