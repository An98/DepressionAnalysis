from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    userid = StringField('userid',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    re_password = PasswordField('re_password',validators=[DataRequired(),EqualTo('password')])
    nickname = StringField('nickname', validators=[DataRequired()])
