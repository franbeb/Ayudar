from flask_wtf import FlaskForm
from flask import flash
from wtforms import Form, StringField,  validators, TimeField, IntegerField,FileField,DateField,BooleanField,FloatField
from wtforms.validators import ValidationError, InputRequired, Length, DataRequired, Email, Optional
from wtforms.fields.html5 import EmailField
from email_validator import validate_email, EmailNotValidError
import re

from app.models.center import Center


class CreateCenterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired(message='Ingrese un nombre de centro')])
    email = EmailField('Email',validators=[Optional(), Email()])    
    direccion = StringField('Direccion', validators=[InputRequired(message='Ingrese una direccion')])
    hora_apertura = TimeField('Hora de apertura', validators=[InputRequired(message='Ingrese una hora de apertura')])
    hora_cierre = TimeField('Hora de cierre', validators=[InputRequired(message='Ingrese una hora de cierre')])
    telefono = StringField('Telefono',validators=[InputRequired(message='Ingrese un telefono')])
    web = StringField('Web',validators=[Optional()])
    protocolo_vista = StringField('Protocolo vista',validators=[Optional()])
    longitud = FloatField('Coordenada x ',validators=[Optional()])
    latitud = FloatField('Coordenada y',validators=[Optional()])
    municipio = IntegerField('Municipio', validators=[DataRequired(message='Seleccione un municipio')])



class EditCenterForm(FlaskForm):
    id = IntegerField('id')
    nombre = StringField('Nombre', validators=[InputRequired(message='Ingrese un nombre de centro')])
    email = EmailField('Email',validators=[Optional(), Email()])    
    direccion = StringField('Direccion', validators=[InputRequired(message='Ingrese una direccion')])
    hora_apertura = StringField('Hora de apertura', validators=[DataRequired(message='Ingrese una hora de apertura')])
    hora_cierre = StringField('Hora de cierre', validators=[DataRequired(message='Ingrese una hora de cierre')])
    telefono = StringField('Telefono',validators=[InputRequired(message='Ingrese un telefono')])
    web = StringField('Web',validators=[Optional()])
    protocolo_vista = StringField('Protocolo vista',validators=[Optional()])
    longitud = FloatField('Coordenada x ',validators=[Optional()])
    latitud = FloatField('Coordenada y',validators=[Optional()])
    municipio = IntegerField('Municipio', validators=[DataRequired(message='Seleccione un municipio')])
    estado = BooleanField('Estado')




