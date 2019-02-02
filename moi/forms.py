from flask_wtf import FlaskForm
from moi.models import User, Post
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp

def check_characters(form, field):
    for char in (field.data):
        if char == '<' or char == '(' or char == '[':
            raiseValidationError('Forbidden character used.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20), check_characters])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=30), check_characters])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20), check_characters])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=30), check_characters])
    submit = SubmitField('Sign In')

class LoggedForm(FlaskForm):
    current_password=StringField('Current Password', validators=[DataRequired(),Length(min=5, max=30), check_characters])
    new_password=StringField('New Password', validators=[DataRequired(),Length(min=5, max=30), check_characters])
    submit = SubmitField ('Change')
