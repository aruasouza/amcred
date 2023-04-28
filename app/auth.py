from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime,timedelta
from models import db,User
from key import secret,admin_pass

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login_post():
    auth = request.authorization
    username = auth.username
    password = auth.password

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message':'Usuário ou senha incorretos.'}),401
    
    token = jwt.encode({'user':username,'exp':datetime.utcnow() + timedelta(hours = 24)},secret,algorithm="HS256")
    return jsonify({'token':token})

@auth.route('/signup', methods=['POST'])
def signup_post():
    auth = request.authorization
    json = request.json

    if (auth.username != 'admin') or (auth.password != admin_pass):
        return jsonify({'message':'Permissão de administrador negada.'}),401

    username = json['username']
    password = json['password']
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message':'Usuário já existe.'}),400
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'Usuário criado com sucesso.'}),200