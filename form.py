from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from pymongo import MongoClient

class RegisterForm(FlaskForm):
    userid = StringField('userid',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    re_password = PasswordField('re_password',validators=[DataRequired(),EqualTo('password')])
    nickname = StringField('nickname', validators=[DataRequired()])

class LoginForm(FlaskForm):
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message
        def __call__(self,form,field):
            userid = form['userid'].data
            password = field.data
            client = MongoClient('mongodb://localhost:27017/')
            db = client.project
            userCollection = db.user
            user = userCollection.find({'id':userid},{"_id":0,"id":1,"pwd":1})
            if user.count()>0:
                for x in user:
                    if x["id"]!=userid:
                        raise ValueError('wrong Account')
                    if x["pwd"]!= password:
                        raise ValueError('wrong password')
                    session['userid']=userid
            else:
                raise ValueError('No Account')
    userid = StringField('userid',validators=[DataRequired(), UserPassword()])
    password = PasswordField('password',validators=[DataRequired(), UserPassword()])

