import os

from flask import Flask, render_template

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskExample.sqlite'),
    )

    if test_config is None:
        # Load config file if it exists, while NOT testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load test configs if they are passed
        app.config.from_mapping(test_config)
    
    # Ensuring the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    # Simple page that says 'Hello!'. Needed for tests
    @app.route('/hello')
    def hello():
        return 'Hello, world!'
    
    # Simple page that shows site is working for normal users
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app