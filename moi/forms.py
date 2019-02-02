from flask_wtf import FlaskForm
from moi.models import User, Post
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class LoggedForm(FlaskForm):
    current_password=StringField('Current Password', validators=[DataRequired(),Length(min=3, max=20)])
    new_password=StringField('New Password', validators=[DataRequired(),Length(min=3, max=20)])
    submit = SubmitField ('Change')
