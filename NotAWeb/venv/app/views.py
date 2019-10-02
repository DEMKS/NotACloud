from flask import render_template,flash,redirect,request,make_response
import flask
from app import app
from app.forms import LoginForm
import sqlite3
import hashlib
import os
import time

UPLOAD_FOLDER = 'downloads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
def SecureStr(str):
    if str.find(";") == str.find("'") == str.find('"') == str.find("#") == str.find("=") ==-1:
        return True
    return False
def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size
def filePost():
    if request.method == "POST":
        login = request.form["login"]
        password = hashlib.md5(request.form["password"].encode('utf-8')).hexdigest()
        conn = sqlite3.connect('../NotADevs.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE login='" + login + "'")
        s = []
        f = c.fetchall()
        if (str(f).__len__() < 20):
            for i in range(0, 3):
                s += [item[i] for item in f]
        else:
            
def indexPost():
    try:
        if request.method == 'POST' and SecureStr(request.form["login"]) :
            login = request.form["login"]
            password = hashlib.md5(request.form["password"].encode('utf-8')).hexdigest()
            conn = sqlite3.connect('../NotADevs.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE login='" + login + "'")
            s = []
            f = c.fetchall()
            if (str(f).__len__() < 20):
                for i in range(0, 3):
                    s += [item[i] for item in f]

                c.execute("INSERT INTO users(login,password) VALUES('" + login + "','" + password + "');")

                conn.commit()
                r = make_response(render_template("login.html", form=LoginForm()))
                c.close()
                conn.close()
                return r;
            else:
                return render_template('registration.html',
                                       title='Sign in',
                                       form=LoginForm(), message="User with this login already exist")

        elif(not SecureStr(request.form["login"])):
            return render_template('registration.html',
                                       title='Sign in',
                                       form=LoginForm(), message="You login includes incorrect letters")
        else:
            return render_template('registration.html',
                                   title='Sign in',
                                   form=LoginForm())
    except:
        return render_template('registration.html',
                                   title='Sign in',
                                   form=LoginForm())
def loginPost():
    #try:
        if request.method == 'POST' and SecureStr(request.form["login"]):
            form = LoginForm()
            login = request.form["login"]
            password = hashlib.md5(request.form["password"].encode('utf-8')).hexdigest()
            conn = sqlite3.connect('../NotADevs.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE login='" + login + "' AND password='" + password + "';")

            s = []
            f = c.fetchall()

            if (str(f).__len__() > 3):
                for i in range(0, 3):
                    s += [item[i] for item in f]
                timee = time.time()
                key = hashlib.md5(str(login + password + str(timee)).encode('utf-8')).hexdigest()
                # Cookie set
                r=make_response(redirect("/account"))
                r.set_cookie('key', str(key), max_age=1800)
                c.execute("INSERT INTO tokens(token,time,user_id) VALUES('" + str(key) + "','" + str(
                    int(timee) + 1800) + "','" + str(s[0]) + "');")

                conn.commit()

                return r
            else:
                return render_template('login.html',
                                       title='Sign in',
                                       form=LoginForm(), message="Login or password is incorrect")
            c.close()
            conn.close()
        else:
            return render_template('login.html',
                                   title='Sign in',
                                   form=LoginForm())
    #except:
       # return render_template('login.html',
                         #     title='Sign in',
                       #        form=LoginForm(), message="ValyaLoh")
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def file_upload(path1,idd):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
    if file :
        #and allowed_file(file.filename)
        filename = secure_filename(file.filename)
        try:
            os.mkdir(app.config['UPLOAD_FOLDER']+idd)
        except:
            lsfjsf='1'
        file.save(os.path.join(app.config['UPLOAD_FOLDER']+idd, filename))
        flash('File successfully uploaded')
        return redirect('/')
    else:
        flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
        return redirect(request.url)

from werkzeug.utils import secure_filename
@app.route('/', methods=["GET","POST"])
def index():

    if (request.cookies.get('key')):
        conn = sqlite3.connect('../NotADevs.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key")+ "'")

        s = []
        f = c.fetchall()
        if (str(f).__len__() > 3):
            for i in range(0, 4 ):
                s += [item[i] for item in f]
            c.execute("SELECT * FROM users WHERE id='"+s[3]+"';")
            s = []
            f = c.fetchall()
            if (str(f).__len__() > 3):
                for i in range(0, 3):
                    s += [item[i] for item in f]
                return redirect('/account')
        else:
            return indexPost()
    else:
        return indexPost()
@app.route('/login', methods=["GET","POST"])
def login():
    if (request.cookies.get('key')):
        conn = sqlite3.connect('../NotADevs.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key")+ "'")

        s = []
        f = c.fetchall()
        if (f.__sizeof__()>20):
            for i in range(0, 4 ):
                s += [item[i] for item in f]
            c.execute("SELECT * FROM users WHERE id='"+s[3]+"';")
            s = []
            f = c.fetchall()
            if (f.__sizeof__()>20):
                for i in range(0, 4):
                    s += [item[i] for item in f]

                return redirect('/account')
        else:
            return loginPost()
    else:
        return loginPost()
@app.route('/asgagawsf;a[;wfwgfw,fowf,w',methods=['GET','POST'])
def adminPanel():
    conn = sqlite3.connect('../NotADevs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    s=str(c.fetchall())
    r = make_response(render_template("administrations.html",s=s))
    return r

@app.route('/account',methods=['GET','POST'])
def account():
    if (request.cookies.get('key')):
        conn = sqlite3.connect('../NotADevs.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tokens WHERE token='" + request.cookies.get("key")+ "'")

        s = []
        f = c.fetchall()
        if (f.__sizeof__()>20):
            for i in range(0, 4 ):
                s += [item[i] for item in f]
            c.execute("SELECT * FROM users WHERE id='"+s[3]+"';")
            s = []
            f = c.fetchall()
            if (f.__sizeof__()>20):
                for i in range(0, 4):
                    s += [item[i] for item in f]
                #try:
                if request.method == 'POST':
                    file_upload("",s[1]+"/")
                #except:
                    #$s[1]=str(request.files[0]);
                r = make_response(render_template("account.html",tittle="Account", login=s[1],space=s[3]-get_size("downloads/"+s[1])//1048576))
                return r
            else:
                return redirect('/')
    else:
        return redirect('/')
@app.route("/exit")
def exit():
    r = redirect("/")

    r.set_cookie('key', str(""), max_age=1800)
    return r
@app.route("/files",methods=['GET','POST']
def files:
    return FilesPost()
#s = []
#f = c.fetchall()
#for i in range(0, 3):
#    s += [item[i] for item in f]