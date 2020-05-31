import os
import requests

def init():
    print('You want to restart DB? Y/N')
    if (input() == 'Y'):
        try:
            os.remove('NotADevs.db')
        except:
            os.system('start ../db_create.py')

def check_pages(page = ''):
    try:
        g = requests.get('http://127.0.0.1:10040/' + page)
        if (g.status_code == 200):
            if (page == ''):
                print('Successfully connected to server.')
            print('Page ' + 'http://127.0.0.1:10040/' + page + ' avaliable(' + str(g.status_code) + ') длина страницы: ' + str(len(g.text)))
            #Для каждой страницы должно вывести 200. Это означает, что они стабильно работают или переадресовывают в
            #случае, если пользователь не зарегистрирован или не авторизован
        else:
            print('Error ' + str(g.status_code))
        return g.status_code
    except:
        print("Can't to connect to server")
        return -1

def check_user_create(login, password):
    session = requests.sessions.session()
    session.post('http://127.0.0.1:10040/', {'login': login, 'password': password})
    session.post('http://127.0.0.1:10040/login', {'login': login, 'password': password})
    if (len(session.get('http://127.0.0.1:10040/account').text) > len(requests.get('http://127.0.0.1:10040/account').text)):
        print('Account successfully created')
        session.get('http://127.0.0.1:10040/exit')
        if (len(session.get('http://127.0.0.1:10040/account').text) == len(requests.get('http://127.0.0.1:10040/account').text)):
            print('Exit successfully')
def __main__():
    f = check_pages()
    s = check_pages('login')
    check_pages('account')
    check_pages('files')
    check_pages('exit')
    if f == s == 200:
        log = input()
        passwd = input()
        check_user_create(log, passwd)
if __name__ == "__main__":
    __main__()