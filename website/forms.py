from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class Registration(FlaskForm):
    username = StringField("Ваш нікнейм", [validators.DataRequired()])
    first_name = StringField("Ім'я", [validators.DataRequired()])
    last_name = StringField("Прізвище", [validators.DataRequired()])
    email = StringField("Емайл", [validators.DataRequired()])
    password = PasswordField(
        "Придумайте пароль",
        [
            validators.Length(min=6, max=40),
            validators.EqualTo("confirm", message="password must be match"),
        ],
    )

    confirm = PasswordField("Confirm password *", [validators.DataRequired()])


class UserLogin(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")


class ServiceForm(FlaskForm):
    service_name = StringField("Головна назва", [validators.DataRequired()])
    description = StringField("Опис", [validators.DataRequired()])
    price = StringField("Ціна", [validators.DataRequired()])
    contact = StringField("Ваші контакти", [validators.DataRequired()])


class AdminForm(FlaskForm):
    username = StringField("Ім'я користувача", [validators.DataRequired()])
