import base64
import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import request
from flask import jsonify
from flask import Flask, render_template
from flask_cors import CORS,cross_origin
import sys

app = Flask(__name__)

def get_model():
    global model
    model = tf.keras.models.load_model('../Code/model1.h5')
    print('Model is loaded!')

def preprocess_image(image, target_size):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image

print('* Loading keras model...')
get_model()

@app.route('/predict', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(300, 300))

    prediction = model.predict(processed_image).tolist()
    print(prediction, file=sys.stderr)
    response = {
        'prediction': {
            'value': prediction[0][0]
        }
    }
    return jsonify(response)

@app.route('/', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def render():
    return render_template('predict.html')
    