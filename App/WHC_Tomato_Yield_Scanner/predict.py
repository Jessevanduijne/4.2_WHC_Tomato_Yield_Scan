import os
import numpy as np

from flask import app, Blueprint, current_app, request, render_template, g, redirect
from flask_cors import CORS, cross_origin

from .model import get_model
from . import helpers

bp = Blueprint("predict", __name__, url_prefix="/")

@bp.route("/", methods=["GET", "POST"])
@cross_origin(origin="*", headers=["Content-Type","Authorization"])
def index():
    if request.method == "POST":
        if request.files:
            directory = helpers.createDirectory(request.files["image[]"].filename)
            files = helpers.transformImages(request.files.getlist("image[]"))
            input = helpers.prepareImagesForPrediction(directory)
            result = get_model().predict(input)[:,0]

            return render_template("predict/result.html", 
                result = np.column_stack([files, result]),
                summary = {
                    "total": result.size,
                    "unhealthy": sum(i <= 0.5 for i in result),
                    "healthy": sum(i > 0.5 for i in result)
                })
        else:
            return redirect("/")
    elif request.method == "GET":
        sliderPhotosDirectory = os.path.join(current_app.config["APP_ROOT"], "static\\img\\tomatoSlider")
        sliderPhotos = os.listdir(sliderPhotosDirectory)

        return render_template("predict/predict.html", sliderPhotos = sliderPhotos)