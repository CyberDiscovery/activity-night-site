import os
from flask import Flask, render_template, session, request
import firebase_admin
from app.auth import get_user


def create_app(config=None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='TempStringForDevPurposesOnly',
        DATABASE_URL='https://cd-eventtracker-test.firebaseio.com'
    )

    if config is None:
        app.config.from_pyfile('config.py',False)
    else:
        app.config.from_mapping(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    firebase_admin.initialize_app()

    @app.route('/')
    def test():
        return render_template('index.html')

    #Pre request handler
    @app.before_request
    def pre_request():
        # If a user is authenticated, we should load their user object.
        uid = session.get("userID")
        if uid:
            request.user = get_user(uid)
        else:
            request.user = None

    from . import auth
    app.register_blueprint(auth.bp)

    return app


