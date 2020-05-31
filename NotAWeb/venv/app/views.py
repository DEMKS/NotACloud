import flask
from flask import render_template, flash, redirect, request, make_response
import mysql.connector
from app import app
from app.forms import LoginForm
import sqlite3
import hashlib
import os
import time
import base64
import pbkdf2
UPLOAD_FOLDER = 'app/static/../../../../uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Lname = 'login.html'
def SecureStr(str):
    if -1 == str.find(";") == str.find("'") == str.find('"') == str.find("#") == str.find("="):
        return True
    return False
def SecureFile(str):
    if -1 == str.find("../") == str.find("%"):
        return True
    return False
def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            # skip if it is symbolic link
            if not os.path.islink(filepath):
                total_size += os.path.getsize(filepath)
    return total_size
def filesPost():
    if request.cookies.get('key'):
        DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
        cursor = DB.cursor()
        cursor.execute("USE userinfo")
        print(cursor.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key") + "'"))
        s = []
        files = cursor.fetchall()
        if (files.__sizeof__() > 20):
            for i in range(0, 4):
                s += [item[i] for item in files]
            cursor.execute("SELECT * FROM users WHERE id='" + str(s[3]) + "';")
            s = []
            files = cursor.fetchall()
            if (files.__sizeof__() > 20):
                for i in range(0, 4):
                    s += [item[i] for item in files]
                q = os.listdir("app/static/../../../../uploads/" + s[1].replace('/', 'a'))
                q = [base64.b64decode(i.split('!')[0].split('.')[0]).decode() for i in q]
                return render_template('files.html', s=q)
            else:
                return make_response(redirect("login"))
        else:
            return make_response(redirect("/"))
    else:
        return make_response(redirect("/"))
def fileDownload(pathh, file):
    if (SecureFile(file)):
        return make_response(flask.send_from_directory(pathh, file + '.' + base64.b64decode(file).decode().split('.')[-1] , as_attachment=True))
    else:
        return render_template("account.html", message="You filename contain incorrect letters")
def indexPost():
    if request.method == 'POST' and SecureStr(request.form["login"]):
        login = pbkdf2.crypt(request.form["login"], iterations=150, salt="NotASalt")
        password = pbkdf2.crypt(request.form["password"], iterations=150, salt="NotASalt")
        DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
        cursor = DB.cursor()
        cursor.execute("USE userinfo")
        cursor.execute("SELECT * FROM users WHERE login_unhashed='" + login + "'")
        s = []
        files = cursor.fetchall()
        print(1)
        if len(str(files)) < 20:
            for i in range(0, 3):
                s += [item[i] for item in files]
            cursor = DB.cursor()
            cursor.execute("USE userinfo")
            cursor.execute('select * from users')
            a = cursor.fetchall()
            cursor.execute(
                "INSERT INTO users(id, login_unhashed, login, password) VALUES('" + str(len(a) + 1) + "','" +
                request.form["login"] + "','" + login + "','" + password + "');")
            import os
            os.mkdir(app.config['UPLOAD_FOLDER'] + pbkdf2.crypt(login, iterations=150, salt="NotASalt").replace('/', 'a'))
            print(app.config['UPLOAD_FOLDER'] + pbkdf2.crypt(login, iterations=150, salt="NotASalt").replace('/', 'a'))
            r = make_response(render_template("login.html", form=LoginForm()))
            cursor.close()
            DB.commit()
            return r
        else:
            return render_template('registration.html',
                                   title='Sign in',
                                   form=LoginForm(), message="User with this login already exist")
    else:
        return render_template('registration.html', title='Sign in', form=LoginForm())
def loginPost():
    if request.method == 'POST' and SecureStr(request.form["login"]):
        login = pbkdf2.crypt(request.form["login"], iterations=150, salt="NotASalt")
        password = pbkdf2.crypt(request.form["password"], iterations=150, salt="NotASalt")
        DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
        cursor = DB.cursor()
        cursor.execute("USE userinfo")
        cursor.execute("SELECT * FROM users WHERE login='" + login + "'")

        s = []
        files = cursor.fetchall()

        if (str(files).__len__() > 3):
            for i in range(0, 3):
                s += [item[i] for item in files]
            timee = time.time()
            key = pbkdf2.crypt(str(login + password + str(timee)), iterations=150, salt="NotASalt")
            r = make_response(redirect("/account"))
            r.set_cookie('key', str(key), max_age=1800)
            cursor.execute('select * from tokens')
            a = cursor.fetchall()
            cursor.execute("INSERT INTO tokens(id, token,ttime,user_id) VALUES('" + str(len(a) + 1) + "','" + str(key) + "','" + str(
                int(timee) + 1800) + "','" + str(s[0]) + "');")

            DB.commit()

            return r
        else:
            return render_template(Lname, title='Sign in', form=LoginForm(), message="Login or password is incorrect")
        cursor.close()
        conn.close()
    else:
        return render_template(Lname,
                               title='Sign in',
                               form=LoginForm())
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def file_upload(path1, idd, free_space):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    s = file.readlines()
    file.seek(0, 2)
    if (file.tell() > free_space):
        flash('No free space for it')
        return redirect('account?e=1')
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
    if file:
        filename = file.filename
        filename.replace('<', '')
        filename.replace('/', '')
        filename.replace('..', '')
        try:
            os.mkdir(app.config['UPLOAD_FOLDER'] + idd)
        except:
            lsfjsf='1'
        dirs = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'] + idd))
        if base64.b64encode(bytes(filename, 'utf-8')).decode() + '.' + filename.split('.')[-1] in dirs:
            return redirect(request.url + '?e=3')
        else:
            open(os.path.join(app.config['UPLOAD_FOLDER'] + idd + '/' + base64.b64encode(bytes(filename, 'utf-8')).decode() + '.' + filename.split('.')[-1]), 'wb').writelines(s)
        flash('File successfully uploaded')
        return redirect('/')
    else:
        flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
        return redirect(request.url)

from werkzeug.utils import secure_filename
@app.route('/', methods=["GET","POST"])
def index():

    if (request.cookies.get('key')):
        DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
        cursor = DB.cursor()
        cursor.execute("USE userinfo")
        cursor.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key") + "'")

        s = []
        files = cursor.fetchall()
        if (str(files).__len__() > 3):
            for i in range(0, 4 ):
                s += [item[i] for item in files]
            cursor.execute("SELECT * FROM users WHERE id='"+str(s[3])+"';")
            s = []
            files = cursor.fetchall()
            if (str(files).__len__() > 3):
                for i in range(0, 3):
                    s += [item[i] for item in files]
                return redirect('/account')
        else:
            return indexPost()
    else:
        return indexPost()
@app.route('/login', methods=["GET","POST"])
def login():
    if (request.cookies.get('key')):
        DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
        cursor = DB.cursor()
        cursor.execute("USE userinfo")
        cursor.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key")+ "'")

        s = []
        files = cursor.fetchall()
        if (files.__sizeof__()>20):
            for i in range(0, 4 ):
                s += [item[i] for item in files]
            cursor.execute("SELECT * FROM users WHERE id='"+str(s[3])+"';")
            s = []
            files = cursor.fetchall()
            if (files.__sizeof__() > 20):
                for i in range(0, 4):
                    s += [item[i] for item in files]
                return redirect('/account')
        else:
            return loginPost()
    else:
        return loginPost()
@app.route('/asgagawsf;a[;wfwgfw,fowf,w',methods=['GET','POST'])
def adminPanel():
    DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557", database='userinfo')
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM users")
    s = str(cursor.fetchall())
    r = make_response(render_template("administrations.html",s=s))
    cursor.close()
    DB.commit()
    DB.close()
    return r

@app.route('/account',methods=['GET','POST'])
def account():
    if (request.cookies.get('key')):
        DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
        cursor = DB.cursor()
        cursor.execute("USE userinfo")
        cursor.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key") +  "'")

        s = []
        files = cursor.fetchall()
        if (files.__sizeof__() > 20):
            for i in range(0, 4):
                s += [item[i] for item in files]
            cursor.execute("SELECT * FROM users WHERE id='"+str(s[3])+"';")
            s = []
            files = cursor.fetchall()
            if (files.__sizeof__() > 20):
                for i in range(0, 5):
                    s += [item[i] for item in files]
                space = s[4] - get_size("app/static/../../../../uploads/" + s[1]) // 1048576
                if request.method == 'POST':
                    return file_upload("",  s[1].replace('/', 'a') + "/", free_space=s[4] * 1048576 - get_size("app/static/../../../../uploads/" + s[1]))
                t = ''
                if not request.args.get('e') is None:
                    if (request.args.get('e') == '2'):
                        t = 'Данный тип файлов не доступен для просмотра онлайн. Скачайте его и смотрите как хотите.'
                    elif (request.args.get('e') == '3'):
                        t = 'Файл c таким названием уже существует. Перед отправлением такого файла, удалите существующий.'
                    elif (request.args.get('e') == '4'):
                        t = 'У вас нет файлов. Чего вы ожидали, открывая эту страницу?'
                    else:
                        t = 'Файл слишком большой. Недостаточно свободного места.'

                r = make_response(render_template("account.html", tittle="Account", login=str(s[3]), space=space, t=t))
                return r
            else:
                return redirect('/')
    else:
        return redirect('/')
@app.route("/exit")
def exit():
    r = redirect("/")
    r.set_cookie('key', str(""), max_age=0)
    return r
@app.route("/view", methods=['GET', 'POST'])
def view():
    image_types = ['jpg', 'png', 'jpeg', 'bmp', 'gif']
    txt_types = ['txt', 'python', 'php', 'cpp', 'py']
    if request.cookies.get("key") is None:
        return redirect('/login')
    if request.args.get("edit") is None:
        edit = False
    else:
        edit = True
    if not request.args.get("file") is None:
        DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")

        cursor = DB.cursor()
        cursor.execute("USE userinfo")
        cursor.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key") + "'")
        s = []
        files = cursor.fetchall()
        if (files.__sizeof__() > 20):
            for i in range(0, 4):
                s += [item[i] for item in files]
            cursor.execute("SELECT * FROM users WHERE id='" + str(s[3]) + "';")
            s = []
            files = cursor.fetchall()
            if (files.__sizeof__() > 20):
                for i in range(0, 4):
                    s += [item[i] for item in files]
                path = "../../../uploads/"
                path += str(s[1].replace('/', 'a') + "/")
                print(path)
                if 'text' in request.form:
                    f = open('app/' + path + base64.b64encode(bytes(str(request.args.get("file")), 'utf-8')).decode() + '.' + request.args.get("file").split('.')[-1], 'w')
                    for i in request.form['text'].split('\n'):
                        f.write(i)
                    f.close()
                t = request.args.get("file").split('.')[-1]
                if (t in image_types):
                    type = 'i'
                    file = path + base64.b64encode(bytes(str(request.args.get("file")), 'utf-8')).decode() + '.' + request.args.get("file").split('.')[-1]
                elif (t in txt_types):
                    type = 't'
                    file = [i for i in open('app/' + path + base64.b64encode(bytes(str(request.args.get("file")), 'utf-8')).decode() + '.' + request.args.get("file").split('.')[-1], 'r').readlines()]
                else:
                    return redirect("/account?e=2")
                return make_response(render_template("view.html", file=file, type=type, edit=edit, filename=request.args.get("file")))

            else:
                return redirect("/")
        else:
            return redirect("/")
    else:
        DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
        cursor = DB.cursor()
        cursor.execute("USE userinfo")
        cursor.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key") + "'")
        files = cursor.fetchall()
        if (files.__sizeof__() > 20):
            return redirect("/files")
        return redirect("/login")
@app.route("/files", methods=['GET', 'POST'])
def files():
    try:
        if not request.args.get("delete") is None:
            DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
            cursor = DB.cursor()
            cursor.execute("USE userinfo")
            cursor.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key") + "'")
            s = []
            files = cursor.fetchall()
            if (files.__sizeof__() > 20):
                for i in range(0, 4):
                    s += [item[i] for item in files]
                cursor.execute("SELECT * FROM users WHERE id='" + str(s[3]) + "';")
                s = []
                files = cursor.fetchall()
                if (files.__sizeof__() > 20):
                    for i in range(0, 4):
                        s += [item[i] for item in files]
                    path = "app/static/../../../../uploads/"
                    path += str(s[1].replace('/', 'a') + "/")
                    dele = request.args.get("delete")
                    os.remove(path + base64.b64encode(bytes(str(dele), 'utf-8')).decode() + '.' + dele.split('.')[-1])
        if not request.args.get("file") is None:
            DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
            cursor = DB.cursor()
            cursor.execute("USE userinfo")
            cursor.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key") + "'")
            s = []
            files = cursor.fetchall()
            if (files.__sizeof__() > 20):
                for i in range(0, 4):
                    s += [item[i] for item in files]
                cursor.execute("SELECT * FROM users WHERE id='" + str(s[3]) + "';")
                s = []
                files = cursor.fetchall()
                if (files.__sizeof__() > 20):
                    for i in range(0, 4):
                        s += [item[i] for item in files]
                    path = "static/../../../../uploads/"
                    path += str(s[1].replace('/', 'a') + "/")
                    return fileDownload(path,  base64.b64encode(bytes(str(request.args.get("file")), 'utf-8')).decode())

                else:
                    return filesPost()
            else:
                return redirect("/")
        else:
            DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
            cursor = DB.cursor()
            cursor.execute("USE userinfo")
            cursor.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key") + "'")
            files = cursor.fetchall()
            if (files.__sizeof__() > 20):
                return filesPost()
            return redirect("/login")
    except:
        return redirect("/account?e=4")