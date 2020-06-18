import os

from flask import Flask, app, current_app, session

from . import helpers

def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    @app.before_request
    def make_session_permanent():
        if session.get("id") == None:
            session["id"] = helpers.generateRandomString(20)
            session.permanent = True

    from . import db, model
    db.init_app(app)
    model.init_app(app)

    from . import predict
    app.register_blueprint(predict.bp)

    return app