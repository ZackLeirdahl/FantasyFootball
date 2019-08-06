import os, firebase_admin
from flask import Flask, g

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER=os.path.join(app.root_path, '\\static\\upload')
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    from .blueprints import auth, blog, profile, league
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(league.bp)
    app.add_url_rule('/', endpoint='index')

    
    return app



