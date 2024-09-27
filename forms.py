from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

# Define a form class
class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username =StringField('username',validators=[DataRequired()])
    email =StringField('Email',validators=[DataRequired(),Email()])
    submit =SubmitField('Submit')
