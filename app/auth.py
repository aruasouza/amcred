from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime,timedelta
from models import db
from key import secret,admin_pass

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login_post():
    auth = request.authorization
    username = auth.username
    password = auth.password

    user = db.get_user(username)

    if not user:
        return jsonify({'message':'Usuário ou senha incorretos.'}),401
    elif not check_password_hash(user['password'], password):
        return jsonify({'message':'Usuário ou senha incorretos.'}),401
    
    token = jwt.encode({'user':username,'exp':datetime.utcnow() + timedelta(hours = 24)},secret,algorithm="HS256")
    return jsonify({'token':token}),200

@auth.route('/signup', methods=['POST'])
def signup_post():
    auth = request.authorization
    json = request.json

    if (auth.username != 'admin') or (auth.password != admin_pass):
        return jsonify({'message':'Permissão de administrador negada.'}),401

    username = json['username']
    password = json['password']
    profile = json['profile']
    orgname = json['organization']

    user = db.get_user(username)
    if user:
        return jsonify({'message':'Usuário já existe.'}),400
    org = db.get_org(orgname)
    if not org:
        return jsonify({'message':'Organização não cadastrada.'}),400
    
    new_user = username,generate_password_hash(password, method='scrypt'),profile,org['id']

    db.create_user(*new_user)

    return jsonify({'message':'Usuário criado com sucesso.'}),200