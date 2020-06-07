import os
import requests
import app.views
from app import app
from app.views import SecureStr
from app.views import SecureFile
from app.views import get_size
from app.views import exit
from app.views import indexPost
from flask import redirect
import random
def test_SecureStr():
    assert SecureStr('#') == False
    assert SecureStr(' ') == True


def test_SecureFile():
    assert SecureFile('../') == False
    assert SecureFile('file.txt') == True


def test_get_size():
    assert get_size('../ForTests/Nothing/') == 0
    assert get_size('../ForTests/') == 1


def test_exit():
    a = redirect("/")
    a.set_cookie('key', str(""), max_age=0)
    assert type(exit()) == type(a)


# def test_indexPost():
#     assert len(requests.get('http://127.0.0.1:10040/').content) == 744
#     assert len(requests.post('http://127.0.0.1:10040/', {'login' : 'abcdew', 'password' : 'qwertt'}).content) == 778
#     rnd = 'qwrtzxcvbnmdfghjklrtyuiopeyhwds'
#     rnd = [i for i in rnd]
#     random.shuffle(rnd)
#     rnd = ''.join(rnd)
#     assert len(requests.post('http://127.0.0.1:10040/', {'login' : rnd, 'password' : 'qwertt'}).content) == 680

def check_user_create(login, password):
    session = requests.sessions.session()
    session.post('http://127.0.0.1:10040/', {'login': login, 'password': password})
    session.post('http://127.0.0.1:10040/login', {'login': login, 'password': password})
    if (len(session.get('http://127.0.0.1:10040/account').text) > len(requests.get('http://127.0.0.1:10040/account').text)):
        print('Account successfully created')
        session.get('http://127.0.0.1:10040/exit')
        if (len(session.get('http://127.0.0.1:10040/account').text) == len(requests.get('http://127.0.0.1:10040/account').text)):
            print('Exit successfully')

def test_indexPost():
    napp = app.test_client()
    napp.testing = True
    assert len(napp.get('/').data) == 744
    assert len(napp.post('/', data={'login' : 'abcdew', 'password' : 'qwertt'}).data) == 778
    rnd = 'qwrtzxcvbnmdfghjklrtyuiopeyhwds'
    rnd = [i for i in rnd]
    random.shuffle(rnd)
    rnd = ''.join(rnd)
    assert len(napp.post('/', data={'login' : rnd, 'password' : 'qwertt'}).data) == 680
    return rnd
def test_login_and_index():
    name = test_indexPost()
    napp = app.test_client()
    napp.testing = True
    napp.post('/login', data={'login' : name, 'password' : 'qwertt'})
    assert napp.get('/').status_code == 302
    assert napp.get('/login').status_code == 302
    napp.set_cookie(server_name='localhost.local', key='key', value='fedgfdgfhmgjhgfdghjtgrfergthjyukjyhtrgrhtjyujyhtrgegrhtjy')
    open('r.html', 'w+').write(napp.get('/login').data.decode())
    assert napp.get('login').status_code == 200
def test_redirect():
    napp = app.test_client()
    napp.testing = True
    assert napp.get('/account').status_code == 302
    assert napp.get('/files').status_code == 302
    assert napp.get('/exit').status_code == 302
    napp.set_cookie(server_name='localhost.local', key='key', value='fedgfdgfhmgjhgfdghjtgrfergthjyukjyhtrgrhtjyujyhtrgegrhtjy')
    assert napp.get('/account').status_code == 302
    assert napp.get('/files').status_code == 302
    assert napp.get('/exit').status_code == 302
def test_account():
    napp = app.test_client()
    napp.testing = True
    napp.post('/login', data={'login' : 'abcdew', 'password' : 'qwertt'})
    assert napp.get('/account').status_code == 200
test_SecureStr()
test_SecureFile()
test_exit()
test_indexPost()
test_login_and_index()
test_redirect()
test_account()