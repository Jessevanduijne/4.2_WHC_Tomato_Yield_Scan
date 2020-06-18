from flask import app, current_app, g
from flask.cli import with_appcontext

import click

def init_app(app):
    app.teardown_appcontext(clear_model)

def get_model():
    if "model" not in g:
        import tensorflow as tf
        from keras.models import load_model

        g.model = tf.keras.models.load_model(current_app.config["MODEL"])
    
    return g.model

def clear_model(e = None):
    model = g.pop("model", None)

    if model is not None:
        from keras import backend as K
        K.clear_session()