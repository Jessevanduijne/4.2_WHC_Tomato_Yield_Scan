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
from keras.preprocessing.image import load_img
from flask import request, redirect, url_for
from flask import jsonify
from flask import Flask, render_template
from flask_cors import CORS,cross_origin
import sys
import os
import cv2

app = Flask(__name__)
app.config["IMAGE-UPLOADS"] = "C:/Users\Rohan/Downloads/WHC_Tomato_Yield_Scan/App/static/uploads"

def get_model():
    global model
    model = tf.keras.models.load_model("../Code/model1.h5")
    print("Model is loaded!")
    return model

# Convert from filestorage list to filename array
def gen_list(list):
    images = []
    for item in list:
        filename = item.filename
        images.append(filename)
    return images

# resized image keeping their aspect ratio, SO Jesse
def resize_image(image, target_width, target_height):
    image = Image.open(image)
    target_ratio = target_height / target_width
    img_ratio = image.height / image.width
    
    if target_ratio > img_ratio:
        # It must be fixed by width
        resize_width = target_width
        resize_height = round(resize_width * img_ratio)
    else:
        # Fixed by height
        resize_height = target_height
        resize_width = round(resize_height / img_ratio)
        
    image_resize = image.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (target_width, target_height), 0)
    offset = (round((target_width - resize_width) / 2), round((target_height - resize_height) / 2))
    background.paste(image_resize, offset)
    return background.convert('RGB')

# predict images
def predict_image(list, folder, model):
    results = {}
    for image in list:
        image_name = image
        image_path = os.getcwd() + "\\static\\uploads\\" + image
        image = load_img(image_path, target_size=(300, 300))
        image = img_to_array(image)
        image = image.reshape(1, 300, 300, 3)
        image = image.astype('float32')
        prediction = model.predict(image)
        predict_obj = {image_name: prediction[0][0]}
        results.update(predict_obj)
    return results

@app.route("/", methods=["GET", "POST"])
@cross_origin(origin="*",headers=["Content-Type","Authorization"])
def render():
    model = get_model()
    if request.method == "POST":
        if request.files:
            # create folder in uploads
            folder_str = request.files["image[]"].filename
            folder_splt = folder_str.split("/")
            folder = folder_splt[0]
            folder_created_path = os.path.join(app.root_path, "static\\uploads", folder)
            os.mkdir(folder_created_path)

            images = request.files.getlist("image[]")
            for image in images:
                resized_image = resize_image(image, target_width=300, target_height=300)
                resized_image.save(os.path.join(app.root_path, "static\\uploads",image.filename))

            image_list = gen_list(images)
            predict_result = predict_image(image_list, folder, model)
            return render_template("image-grid.html", result=predict_result)

    return render_template("predict.html")

# old, but stil needed for reference
@app.route("/predict", methods=["POST"])
@cross_origin(origin="*",headers=["Content-Type","Authorization"])
def predict():
    message = request.get_json(force=True)
    encoded = message["image"]
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(300, 300))

    prediction = model.predict(processed_image).tolist()
    print(prediction, file=sys.stderr)
    response = {
        "prediction": {
            "value": prediction[0][0]
        }
    }
    return jsonify(response)