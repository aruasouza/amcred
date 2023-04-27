from xgboost import XGBClassifier
import numpy as np
import json

catdict = json.load(open('categories.json','r',encoding = 'utf-8'))
normalize_dict = json.load(open('normalization.json','r',encoding = 'utf-8'))
popt = json.load(open('coef.json','r'))
atributos = json.load(open('ordem_atributos.json','r',encoding = 'utf-8'))
nafill = json.load(open('nafill.json','r',encoding = 'utf-8'))
model = XGBClassifier()
model.load_model('model_load.json')

def square(x,a,b,c):
    return ((x ** 2) * a) + (x * b) + c

corrector = lambda x: square(x,*popt)

def calculate(data_dict):
    vector = []
    for atributo in atributos:
        if atributo not in data_dict:
            value = nafill[atributo]
        else:
            value = data_dict[atributo]
        if atributo in catdict:
            value = catdict[atributo][value]
        value = (value - normalize_dict[atributo]['mean']) / normalize_dict[atributo]['std']
        vector.append(value)
    vector = np.array([vector])
    pred = model.predict_proba(vector)[0,1]
    return corrector(pred)