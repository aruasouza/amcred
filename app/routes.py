from flask import Blueprint, request, jsonify
from functools import wraps
import json
from jwt import decode,InvalidSignatureError,ExpiredSignatureError
import numbers
from models import db
from key import secret
from api_model import atributos,calculate

main = Blueprint('main', __name__)

permited = json.load(open('permited_values.json','r',encoding = 'utf-8'))
numeric = json.load(open('numeric.json','r'))
numeric = set(numeric)

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = request.json['token']
        if not token:
            return jsonify({'message':'Token ausente.'}),401
        try:
            data = decode(token,secret,algorithms=["HS256"])
        except InvalidSignatureError:
            return jsonify({'message':'Token inválido.'}),401
        except ExpiredSignatureError:
            return jsonify({'message':'Token expirado.'}),401
        return f(*args,**kwargs)
    return decorated

@main.route('/')
@token_required
def index():
    dados = request.json['dados']
    if not dados:
        jsonify({'message':'Nenhuma informação recebida.'}),400
    data_dict = {}
    valores_negados = {}
    for atributo in atributos:
        if atributo in dados:
            if (atributo in numeric) and isinstance(dados[atributo],numbers.Number):
                data_dict[atributo] = dados.pop(atributo)
            elif dados[atributo] in permited[atributo]:
                data_dict[atributo] = dados.pop(atributo)
            else:
                valores_negados[atributo] = dados.pop(atributo)
    if valores_negados or dados:
        return jsonify({'message':'Alguns atributos e/ou valores não foram reconhecidos.',
                        'errors':{'atributos negados':dados,'valores negados':valores_negados}}),400
    return jsonify({'probabilidade':calculate(data_dict)}),200