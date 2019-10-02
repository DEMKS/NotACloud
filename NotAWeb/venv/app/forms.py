from flask_wtf import Form
import wtforms
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required
class LoginForm(Form):
    remember_me = wtforms.BooleanField('remember_me',default=False)