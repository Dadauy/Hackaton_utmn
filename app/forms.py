from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, length
from app.models import User


class LoginForm(FlaskForm):
    email = EmailField("Электронная почта",
                       validators=[DataRequired(), Email(message="Неверный адрес электронной почты")])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class RegistrationForm(FlaskForm):
    username = StringField('ФИО', validators=[DataRequired()])
    email = EmailField('Электронная почта',
                       validators=[DataRequired(), Email(message="Неверный адрес электронной почты")])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = None if len(username.data.split()) == 3 else True
        if user is not None:
            raise ValidationError('Пожалуйста, напишите ФИО правильно.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой адрес электронной почты.')


class ProjectForm(FlaskForm):
    title = StringField('Название проекта', validators=[
        DataRequired(message='Поле не может быть пустым'),
        length(max=255, min=3, message='Введите название длиной от 3 до 255 символов')])
    city = StringField('Город', validators=[DataRequired(message='Поле не может быть пустым')])
    street = StringField('Улица', validators=[DataRequired(message='Поле не может быть пустым')])
    home = StringField('Дом', validators=[DataRequired(message='Поле не может быть пустым')])
    text = TextAreaField(
        'Описание проекта', validators=[DataRequired(message='Поле не может быть пустым')])
    submit = SubmitField('Добавить проект')


class EditProfileForm(FlaskForm):
    username = StringField('ФИО', validators=[DataRequired()])
    email = EmailField('Электронная почта',
                       validators=[DataRequired(), Email(message="Неверный адрес электронной почты")])
    info = TextAreaField('Дополнительная информация', validators=[length(min=0, max=256)])
    submit = SubmitField('Сохранить')

    def validate_username(self, username):
        user = None if len(username.data.split()) == 3 else True
        if user is not None:
            raise ValidationError('Пожалуйста, напишите ФИО правильно.')


class DeleteProfile(FlaskForm):
    submit = SubmitField("Удалить профиль")
