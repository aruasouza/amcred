import streamlit as st
import requests
import json

req_port = 'http://127.0.0.1:5000/'

def login():
    user = st.session_state['username']
    password = st.session_state['password']
    if user and password:
        req = requests.get(req_port + 'login',auth = (user,password))
        if req.status_code == 200:
            token = req.json()['token']
            st.session_state.page = 1
            st.session_state.token = token
        else:
            try:
                st.error(req.json()['message'])
            except:
                st.error('Erro interno do Servidor')

def call_api():
    cats = st.session_state.categorical
    num = st.session_state.numeric
    call = {}
    for key in cats:
        if st.session_state[key]:
            call[key] = st.session_state[key]
    for key in num:
        if st.session_state[key]:
            try:
                call[key] = float(st.session_state[key].replace(',','.'))
            except ValueError:
                st.error('Há campos numéricos com valores inválidos.')
    token = st.session_state.token
    full_call = {'token':token,'dados':call}
    req = requests.get(req_port,json = full_call)
    if req.status_code == 200:
        answer = req.json()['probabilidade']
        st.session_state.page = 2
        st.session_state.answer = answer
    else:
        st.error(req.json()['message'])

def page_1():
    st.session_state.page = 1

def page_3():
    st.session_state.page = 3

def page_0():
    st.session_state.page = 0

def check_pass():
    if st.session_state.new_user:
        if st.session_state.new_pass:
            if st.session_state.new_pass == st.session_state.conf_pass:
                st.session_state.form_pass = st.session_state.new_pass
                st.session_state.form_user = st.session_state.new_user
                st.session_state.page = 4
            else:
                st.error('Digite um nome de usuário.')
        else:
            st.error('Digite uma senha.')
    else:
        st.error('As senhas não correspondem.')

def cadastrar():
    form = {'username':st.session_state.form_user,'password':st.session_state.form_pass}
    admin_pass = st.session_state.admin_pass
    req = requests.post(req_port + 'signup',json = form,auth = ('admin',admin_pass))
    if req.status_code == 200:
        st.session_state.page = 5
    else:
        try:
            st.error(req.json()['message'])
        except:
            st.error('Erro interno do Servidor')
        st.session_state.page = 3

st.set_page_config(page_title = 'api deepen/amcred',layout = 'wide',page_icon = '💰')
style = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.block-container {padding-top:1rem;}
.e1fqkh3o4 {padding-top:1rem;}
</style>
'''
st.markdown(style,unsafe_allow_html=True)

placeholder = st.empty()

if "page" not in st.session_state:
    st.session_state.page = 0
    st.session_state.categorical = json.load(open('categorical.json','r',encoding = 'utf-8'))
    st.session_state.numeric = json.load(open('numeric.json','r',encoding = 'utf-8'))
    st.session_state.permited = json.load(open('permited_values.json','r',encoding = 'utf-8'))

if st.session_state.page == 0:
    col1,col2,col3 = placeholder.columns(3)
    col2.title('API Deepen-AMCRED')
    col2.header('Login')
    col2.text_input('Usuário:', value="", max_chars=20,key = 'username')
    col2.text_input('Senha:', value="", max_chars=20,type = 'password',key = 'password')
    col2.button('Entrar',on_click = login)
    col2.button('Novo usuário',on_click = page_3)
elif st.session_state.page == 1:
    col1,col2,col3 = placeholder.columns(3)
    col2.title('API Deepen-AMCRED')
    col2.header('Informações do Cliente')
    cats = st.session_state.categorical
    for key in cats:
        col2.selectbox(cats[key],options = [''] + st.session_state.permited[key],key = key)
    num = st.session_state.numeric
    for key in num:
        col2.text_input(num[key],key = key)
    col2.button('Enviar',on_click = call_api)
elif st.session_state.page == 2:
    col1,col2,col3 = placeholder.columns(3)
    col2.title('API Deepen-AMCRED')
    col2.metric('Probabilidade de inadimplencia:',str(round(st.session_state.answer * 100,1)) + '%')
    col2.button('Novo cliente',on_click = page_1)
elif st.session_state.page == 3:
    col1,col2,col3 = placeholder.columns(3)
    col2.title('API Deepen-AMCRED')
    col2.header('Novo Usuário')
    col2.text_input('Usuário:', value="", max_chars=20,key = 'new_user')
    col2.text_input('Senha:', value="", max_chars=20,type = 'password',key = 'new_pass')
    col2.text_input('Confirmar senha:', value="", max_chars=20,type = 'password',key = 'conf_pass')
    col2.button('Cadastrar',on_click = check_pass)
elif st.session_state.page == 4:
    col1,col2,col3 = placeholder.columns(3)
    col2.title('API Deepen-AMCRED')
    col2.header('Essa ação requer permissão de administrador.')
    col2.text_input('Senha:', value="", max_chars=20,type = 'password',key = 'admin_pass')
    col2.button('Confirmar',on_click = cadastrar)
elif st.session_state.page == 5:
    col1,col2,col3 = placeholder.columns(3)
    col2.title('API Deepen-AMCRED')
    col2.header('Usuário criado com sucesso.')
    col2.button('Voltar',on_click = page_0)