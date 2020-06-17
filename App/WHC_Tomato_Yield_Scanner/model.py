from flask import app, current_app, g
from flask.cli import with_appcontext

import tensorflow as tf
from keras.models import load_model
from keras import backend as K

import click

def init_app(app):
    app.teardown_appcontext(clear_model)

def get_model():
    if "model" not in g:
        g.model = tf.keras.models.load_model(current_app.config["MODEL"])
    
    return g.model

def clear_model(e = None):
    model = g.pop("model", None)

    if model is not None:
        K.clear_session()