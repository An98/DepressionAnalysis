from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TextAreaField
from wtforms.validators import DataRequired, EqualTo
from pymongo import MongoClient

class RegisterForm(FlaskForm):
    userid = StringField('userid',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    re_password = PasswordField('re_password',validators=[DataRequired(),EqualTo('password')])
    nickname = StringField('nickname', validators=[DataRequired()])

class LoginForm(FlaskForm):
    class UserPassword(object):
        nickname=None
        def __init__(self, message=None):
            self.message = message
        def __call__(self,form,field):
            userid = form['userid'].data
            password = field.data
            client = MongoClient('mongodb://localhost:27017/')
            db = client.project
            userCollection = db.user
            user = userCollection.find({'id':userid},{"_id":0})
            if user.count()>0:
                for x in user:
                    if x["id"]!=userid:
                        raise ValueError('wrong Account')
                    if x["pwd"]!= password:
                        raise ValueError('wrong password')
                    session['nickname']=x["nickname"]
                    session['userid']=x["id"]
            else:
                raise ValueError('No Account')
    userid = StringField('userid',validators=[DataRequired(), UserPassword()])
    password = PasswordField('password',validators=[DataRequired(), UserPassword()])

class WriteForm(FlaskForm):
    title = StringField('title',validators=[DataRequired()])
    content = TextAreaField('content',validators=[DataRequired()])