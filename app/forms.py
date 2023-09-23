from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, length, Optional
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember_me")
    submit = SubmitField("Sign_in")


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ProjectForm(FlaskForm):
    title = StringField('Название проекта', validators=[
        DataRequired(message='Поле не может быть пустым'),
        length(max=255, min=3, message='Введите название длиной от 3 до 255 символов')])
    text = TextAreaField(
        'Описание проекта', validators=[DataRequired(message='Поле не может быть пустым')])
    submit = SubmitField('Добавить проект')
