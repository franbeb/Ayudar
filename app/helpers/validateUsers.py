from flask_wtf import FlaskForm
from flask import flash
from wtforms import widgets, BooleanField, Form, SelectMultipleField, StringField, PasswordField, validators, IntegerField, FieldList
from wtforms.validators import ValidationError, InputRequired, Length, DataRequired, Email
from wtforms.fields.html5 import EmailField
from email_validator import validate_email, EmailNotValidError
import re
from app.models.user import User
from app.models.user_has_role import UserHasRole


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message='Ingrese un nombre de usuari@')])
    email = EmailField('Email',validators=[validators.Email()])
    perfil = StringField('Perfil', validators=[InputRequired(message='Ingrese un nombre de perfil')])
    last_name = StringField('Apellido', validators=[InputRequired(message='Ingrese un apellido, por favor')])
    first_name = StringField('Nombre', validators=[InputRequired(message='Ingrese un nombre de perfil')])
    password = PasswordField('Contraseña', validators=[InputRequired(message='Debe ingresar una contraseña')])
    roles = MultiCheckboxField('Roles', choices = [], coerce = int)

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            flash("El nombre de usuari@ ya está en uso", "warning")
            raise ValidationError('El nombre de usuari@: {} ya está en uso')
        return True

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            flash("El email ingresado ya está en uso, pruebe con otro", "warning")
            raise ValidationError('El email ingresado ya está en uso, pruebe con otro')
        return True




class EditUserForm(FlaskForm):
    id = IntegerField('id')
    username = StringField('Username', validators=[InputRequired(message='Ingrese un nombre de usuari@')])
    email = EmailField('Email',validators=[validators.Email()])
    perfil = StringField('Perfil', validators=[InputRequired(message='Ingrese un nombre de perfil')])
    last_name = StringField('Apellido', validators=[InputRequired(message='Ingrese un apellido, por favor')])
    first_name = StringField('Nombre', validators=[InputRequired(message='Ingrese un nombre de perfil')])
    roles= MultiCheckboxField('Roles', choices = [], coerce = int)
    
    def validate_username(self, username):
        user = User.query.filter_by(id = self.id.data).first()
        if username.data != user.username:
            if User.query.filter_by(username=username.data).first():
                flash("El nombre de usuari@ ya está en uso", "warning")
                raise ValidationError('El nombre de usuari@: {} ya está en uso')

        return True



    def validate_email(self, email):
        user = User.query.filter_by(id =self.id.data).first()
        if email.data != user.email:
            if User.query.filter_by(email=email.data).first():
                flash("El email ingresado ya está en uso, pruebe con otro uso", "warning")
                raise ValidationError('El email ingresado ya está en uso, pruebe con otro')
        return True


class EditPassword(FlaskForm):
    password_0 = PasswordField('Contraseña antigua ', validators=[InputRequired(message='Ingrese contraseña antigua')])    
    password_1 = PasswordField('Contraseña ', validators=[InputRequired(message='Ingrese una contraseña')])
    password_2 = PasswordField('Vuelva a ingresar Contraseña',validators=[InputRequired(message='Ingrese la misma contraseña')])

