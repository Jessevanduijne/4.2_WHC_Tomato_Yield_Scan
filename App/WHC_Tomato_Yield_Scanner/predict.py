import os
import numpy as np
from markupsafe import escape
import json

from flask import app, Blueprint, current_app, request, render_template, g, redirect, session, url_for
from flask_cors import CORS, cross_origin

from . import helpers
from .model import get_model
from .db import get_db, getResult, getResults, insertResult

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

    return redirect(url_for("predict.result", unique_id = unique_id))

@bp.route("/results/<unique_id>", methods=["GET"])
def result(unique_id):
    session_id = session.get("id")

    result = getResult(escape(unique_id))
    history = getResults(session_id)

    files = np.fromstring(result["files"], np.dtype(result["files_dtype"]))
    values = np.fromstring(result["val"], np.dtype("float32"))

    return render_template("predict/result.html",
        result = {
            "unique_id": unique_id,
            "session_id": session_id,
            "predictions": dict(zip(files, values)),
            "percent_healthy": int(result["percent_healthy"]*100),
            "result_date": result["result_date"]
        },
        jsData = {
            "unique_id": unique_id,

            "total": values.size,
            "healthy": sum(i > current_app.config["TOMATO_HEALTHY_PERCENTAGE"] for i in values),
            "unhealthy": sum(i <= current_app.config["TOMATO_HEALTHY_PERCENTAGE"] for i in values),

            "unique_ids": json.dumps([h["unique_id"] for h in history]),
            "healthy_percentages": json.dumps([int(h["percent_healthy"]*100) for h in history]),
            "result_dates": json.dumps([h["result_date"] for h in history], default=str)
        }
    )