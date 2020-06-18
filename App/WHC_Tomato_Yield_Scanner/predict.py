import os
import numpy as np

from flask import app, Blueprint, current_app, request, render_template, g, redirect, session
from flask_cors import CORS, cross_origin

from . import helpers
from .model import get_model
from .db import get_db, insertResult

bp = Blueprint("predict", __name__, url_prefix="/")

@bp.route("/", methods=["GET"])
def index():
    sliderPhotosDirectory = os.path.join(current_app.config["APP_ROOT"], "static\\img\\tomatoSlider")
    sliderPhotos = os.listdir(sliderPhotosDirectory)

    return render_template("predict/predict.html", sliderPhotos = sliderPhotos)

@bp.route("/predict", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type","Authorization"])
def predict():
    directory = helpers.createDirectory(request.files["image[]"].filename)
    files = helpers.transformImages(request.files.getlist("image[]"))
    input = helpers.prepareImagesForPrediction(directory)
    result = get_model().predict(input)[:,0]
    
    ## Insert result into DB
    unique_id = insertResult(files, result)

    return render_template("predict/result.html", 
        result = np.column_stack([files, result]),
        summary = {
            "total": result.size,
            "unhealthy": sum(i <= current_app.config["TOMATO_HEALTHY_PERCENTAGE"] for i in result),
            "healthy": sum(i > current_app.config["TOMATO_HEALTHY_PERCENTAGE"] for i in result)
        })

@bp.route("/results/<unique_id>", methods=["GET"])
def result():
    return redirect("/")