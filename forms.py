from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired, Email,Length,EqualTo

# Define a form class
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    name =StringField('username',validators=[DataRequired(),Length(min=2,max=150)])
    email =StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=10)])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit =SubmitField('Register')
