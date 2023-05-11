from flask import Flask
from auth import auth as auth_blueprint
from routes import main as main_blueprint
from key import secret

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = secret
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app