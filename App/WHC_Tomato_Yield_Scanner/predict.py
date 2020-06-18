import os
import numpy as np

from flask import app, Blueprint, current_app, request, render_template, g, redirect, session
from flask_cors import CORS, cross_origin

from . import helpers
from .model import get_model
from .db import get_db

bp = Blueprint("predict", __name__, url_prefix="/")

@bp.route("/", method=["GET"])
def index():
    sliderPhotosDirectory = os.path.join(current_app.config["APP_ROOT"], "static\\img\\tomatoSlider")
    sliderPhotos = os.listdir(sliderPhotosDirectory)

    return render_template("predict/predict.html", sliderPhotos = sliderPhotos)

@bp.route("/predict", method="POST")
@cross_origin(origin="*", headers=["Content-Type","Authorization"])
def predict():
    if request.files:
        directory = helpers.createDirectory(request.files["image[]"].filename)
        files = helpers.transformImages(request.files.getlist("image[]"))
        input = helpers.prepareImagesForPrediction(directory)
        result = get_model().predict(input)[:,0]

        db = get_db()
        db.execute(
            "INSERT INTO results (unique_id, session_id, files, val) VALUES (?, ?, ?, ?)",
            (helpers.generateRandomString(20), session.get("id"), files.tostring(), result.tostring())
        )
        db.commit()

        return render_template("predict/result.html", 
            result = np.column_stack([files, result]),
            summary = {
                "total": result.size,
                "unhealthy": sum(i <= 0.5 for i in result),
                "healthy": sum(i > 0.5 for i in result)
            })
    else:
        return redirect("/")