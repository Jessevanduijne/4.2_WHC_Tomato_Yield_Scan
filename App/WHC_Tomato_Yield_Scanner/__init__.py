import os
from flask import Flask

def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    from . import db
    db.init_app(app)

    from . import predict
    app.register_blueprint(predict.bp)

    return app