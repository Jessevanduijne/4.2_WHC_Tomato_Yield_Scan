import os

from flask import app, Blueprint, current_app, request, render_template, g
from flask_cors import CORS, cross_origin

from PIL import Image
from keras.preprocessing.image import load_img, img_to_array

from .model import get_model

bp = Blueprint("predict", __name__, url_prefix="/")

# Global summary result array
# [total images][total healthy][total unhealthy]
prediction_summary = {'total': 0, 'healthy': 0, 'unhealthy': 0}

# Increment type of prediction summary
def edit_total_PS(type):
    global prediction_summary
    if type == 'total':
        prediction_summary['total'] += 1
    elif type == 'healthy':
        prediction_summary['healthy'] += 1
    else:
        prediction_summary['unhealthy'] += 1

# reset prediction summary array
def reset_PS():
    global prediction_summary
    prediction_summary = {'total': 0, 'healthy': 0, 'unhealthy': 0}

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
def predict_image(list, folder):
    reset_PS()
    results = {}
    for image in list:
        image_name = image
        image_path = current_app.config["IMAGE_UPLOADS"] + image
        image = load_img(image_path, target_size=(224, 224))
        image = img_to_array(image)
        image = image.reshape(1, 224, 224, 3)
        image = image.astype('float32')
        prediction = get_model().predict(image)
        predict_obj = {image_name: prediction[0][0]}

        # Edit prediction summary
        edit_total_PS('total')
        if prediction[0][0] == 0.0:
            edit_total_PS('unhealthy')
        else:
            edit_total_PS('healthy')
        results.update(predict_obj)
    return results


# Get all tomatoes folder in static
def get_tomatoesPhotos():
    path = current_app.root_path + "\\static\\img\\tomatoSlider"
    list_tomatoes = os.listdir(path)
    return list_tomatoes

@bp.route("/", methods=["GET", "POST"])
@cross_origin(origin="*", headers=["Content-Type","Authorization"])
def index():
    if request.method == "POST":
        if request.files:
            # create folder in uploads
            folder_str = request.files["image[]"].filename
            folder_splt = folder_str.split("/")
            folder = folder_splt[0]
            folder_created_path = os.path.join(current_app.config["IMAGE_UPLOADS"], folder)
            if not os.path.isdir(folder_created_path):
                os.mkdir(folder_created_path)

            images = request.files.getlist("image[]")
            for image in images:
                resized_image = resize_image(image, target_width=224, target_height=224)
                resized_image.save(os.path.join(current_app.config["IMAGE_UPLOADS"], image.filename))

            image_list = gen_list(images)
            predict_result = predict_image(image_list, folder)
            return render_template("predict/result.html", result=predict_result, summary=prediction_summary)

    tomatoesPhotos = get_tomatoesPhotos()
    return render_template("predict/predict.html", tomatoes=tomatoesPhotos)