import os
import secrets
import string

from flask import Flask, app, current_app, session

def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    @app.before_request
    def make_session_permanent():
        if session.get("id") == None:
            session["id"] = "".join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(20))
            session.permanent = True

    from . import db, model
    db.init_app(app)
    model.init_app(app)

    from . import predict
    app.register_blueprint(predict.bp)

    return app