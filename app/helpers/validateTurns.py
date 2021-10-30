from flask_wtf import FlaskForm
from flask import flash
from wtforms import IntegerField,SelectField, DateField, SelectField
from wtforms.validators import ValidationError, InputRequired, DataRequired, Email
from wtforms.fields.html5 import EmailField, DateField
from app.models.turn import Turn
from app.models.center import Center


class CreateTurnForm(FlaskForm):
  center_id = IntegerField('center_id')
  email = EmailField('Email', validators=[InputRequired(message='Ingrese el email del solicitante del turno'), Email()])
  starting_time = SelectField('Hora de comienzo', choices = Turn.all_hours())
  date = DateField('Fecha del turno', validators=[DataRequired()])

  def validate_starting_time(self, form):
    if self.starting_time.data not in Turn.all_hours():
      flash("El horario elegido está fuera del rango horario, elija otro", "warning")
      raise ValidationError("El horario elegido está por fuera del rango horario, elija otro")

    if self.starting_time.data in Turn.hours_date(self.center_id.data, self.date.data):
      flash("El horario elegido no puede ser reservado, ya que está en uso por otra persona", "warning")
      raise ValidationError("El horario elegido no puede ser reservado, ya que está en uso por otra persona")

    return True

class EditTurnForm(FlaskForm):
  center_id = IntegerField('center_id')
  email = EmailField('Email', validators=[InputRequired(message='Ingrese el email del solicitante del turno'), Email()])
  starting_time = SelectField('Hora de comienzo', choices = Turn.all_hours())
  date = DateField('Fecha del turno', validators=[DataRequired()])

  def validate_starting_time(self, form):
    if self.starting_time.data not in Turn.all_hours():
      flash("El horario elegido está fuera del rango horario, elija otro", "warning")
      raise ValidationError("El horario elegido está por fuera del rango horario, elija otro")

    if self.starting_time.data in Turn.hours_date(self.center_id.data, self.date.data):
      flash("El horario elegido no puede ser reservado, ya que está en uso por otra persona", "warning")
      raise ValidationError("El horario elegido no puede ser reservado, ya que está en uso por otra persona")

    return True

class CreateTurnFormForAPI(FlaskForm):
  center_id = IntegerField('center_id')
  # email = EmailField('Email', validators=[Email()])
  starting_time = SelectField('Hora de comienzo', choices = Turn.all_hours())
  date = DateField('Fecha del turno', validators=[DataRequired()])

  def validate_starting_time(self, starting_time):
    if self.starting_time.data not in Turn.all_hours():
      flash("El horario elegido esta fuera del rango horario, elija otro", "warning")
      raise ValidationError("El horario elegido esta por fuera del rango horario, elija otro")

    if self.starting_time.data not in Turn.free_hours_api(self.center_id.data, self.date.data):
      flash("El horario elegido no puede ser reservado, ya que esta en uso por otra persona", "warning")
      raise ValidationError("El horario elegido no puede ser reservado, ya que esta en uso por otra persona")
    return True
