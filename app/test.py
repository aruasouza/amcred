import requests
import random

url = 'http://127.0.0.1:5000'

new_user = {'username':str(random.random())[2:12],'password':'1234','profile':1,'organization':'banco do empreendedor'}

req1 = requests.post(url + '/signup',json = new_user,auth = ('admin','deepen'))
print(req1)
print(req1.json())

if req1.status_code == 200:
    req2 = requests.get(url + '/login',auth = (new_user['username'],new_user['password']))
    print(req2)
    print(req2.json())

if req2.status_code == 200:
    req3 = requests.get(url,json = {'token':req2.json()['token'],'dados':{'nropessoasnacasa':10}})
    print(req3)
    print(req3.json())