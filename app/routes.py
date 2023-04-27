from flask import Blueprint, request, jsonify
from functools import wraps
import json
from jwt import decode,InvalidSignatureError
from models import db
from key import secret
from api_model import atributos,calculate

main = Blueprint('main', __name__)

permited = json.load(open('permited_values.json','r',encoding = 'utf-8'))

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = request.json['token']
        if not token:
            return jsonify({'message':'Token ausente.'}),401
        try:
            data = decode(token,secret,algorithms=["HS256"])
        except InvalidSignatureError as e:
            return jsonify({'message':'Token inválido.'}),401
        return f(*args,**kwargs)
    return decorated

@main.route('/')
@token_required
def index():
    dados = request.json['dados']
    data_dict = {}
    valores_negados = {}
    for atributo in atributos:
        if atributo in dados:
            if dados[atributo] in permited[atributo]:
                data_dict[atributo] = dados.pop(atributo)
            else:
                valores_negados[atributo] = dados.pop(atributo)
    if valores_negados or dados:
        return jsonify({'message':'Alguns atributos e/ou valores não foram reconhecidos.',
                        'errors':{'atributos negados':dados,'valores negados':valores_negados}}),400
    return jsonify({'probabilidade':calculate(data_dict)}),200