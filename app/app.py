from flask import Flask
from models import db,User
from auth import auth as auth_blueprint
from routes import main as main_blueprint
from key import secret

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = secret
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app