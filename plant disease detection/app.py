import base64
import numpy as np
import io
import json
from PIL import Image
import keras
import cv2
from keras import backend as k
from keras.models import Sequential
from keras.models import load_model,model_from_json
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import request
from flask import jsonify
from flask import Flask
import tensorflow as tf
classes = ['Pepper bell Bacterial_spot','Pepper bell healthy',
           'Potato Early blight','Potato healthy','Potato Late_blight',
           'Tomato Bacterial spot','Tomato Early blight','Tomato healthy','Tomato Late blight','Tomato Leaf Mold',
           'Tomato Septoria leaf spot','Tomato Spider mites Two spotted spider mite','Tomato Target Spot',
           'Tomato mosaic virus','Tomato YellowLeaf Curl Virus']
app = Flask(__name__)

def get_model():
    global model,graph
    with open('plant_disease.json','r') as f:
        model_json = json.load(f)
    model = model_from_json(model_json)
    model.load_weights('plant_disease.h5')
    print("Model loaded....!!")
    graph = tf.get_default_graph()

def preprocess_image(image,target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    image = cv2.resize(image, target_size,0,0, cv2.INTER_LINEAR)
    image = image.astype(np.float32)
    image = np.multiply(image, 1.0 / 255.0)
    image = np.expand_dims(image,axis=0)
    return image

print("Loading keras model.....")
get_model()

@app.route("/predict",methods=["GET","POST"])
def predict():
    if request.method == "POST": 
        message = request.get_json(force=True)
        encoded = message['image']
        decoded = base64.b64decode(encoded)
        with graph.as_default():
            image = Image.open(io.BytesIO(decoded))
            processed_image = preprocess_image(image,target_size=(256,256))
            prediction = model.predict(processed_image)
            pred_class = int(prediction.argmax(axis=-1))
            result = str(pred_class)
            result = classes[pred_class]
     return result
